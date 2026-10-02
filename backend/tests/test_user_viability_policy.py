"""Personal settings isolation, optimistic writes, and historical evaluation policies."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from via_backend.app import create_app
from via_backend.config import Settings
from via_backend.contexts.agroclimatic_evaluation.application.commands import (
    EnvironmentalInputReferenceInput,
    ParcelReferenceInput,
    RequestEvaluation,
)
from via_backend.contexts.agroclimatic_evaluation.application.service import (
    AgroclimaticEvaluationService,
)
from via_backend.contexts.agroclimatic_evaluation.domain import ParcelSnapshot, SnapshotGeometry
from via_backend.contexts.agroclimatic_evaluation.infrastructure import InMemoryEvaluationRepository
from via_backend.contexts.decision_support.application.default_policy import (
    BASELINE_CONFIGURATION,
    DefaultViabilityPolicyService,
)
from via_backend.contexts.decision_support.application.errors import (
    UserViabilityPolicyConflictError,
)
from via_backend.contexts.decision_support.application.policy_lifecycle import (
    ViabilityPolicyLifecycleService,
)
from via_backend.contexts.decision_support.application.user_policy import UserViabilityPolicyService
from via_backend.contexts.decision_support.domain.models import (
    PolicyReference,
    ViabilityPolicyConfiguration,
    ViabilityPolicySnapshot,
)
from via_backend.contexts.decision_support.infrastructure.memory_policy import (
    InMemoryDefaultViabilityPolicyStore,
    InMemoryEvaluationPolicyBindingStore,
    InMemoryUserViabilityPolicyStore,
    InMemoryViabilityPolicyRepository,
)
from via_backend.contexts.identity_access.domain import UserRole

PATH = "/api/v1/decision-support/my-viability-policy"


@pytest.fixture
def service() -> UserViabilityPolicyService:
    policies = InMemoryViabilityPolicyRepository()
    defaults = InMemoryDefaultViabilityPolicyStore(policies)
    first = ViabilityPolicySnapshot(PolicyReference("via-policy", "1"), BASELINE_CONFIGURATION)
    policies.add(first)
    defaults.set_default_viability_policy(first.reference, expected_current=None)
    return UserViabilityPolicyService(
        DefaultViabilityPolicyService(
            defaults,
            ViabilityPolicyLifecycleService(policies),
            InMemoryEvaluationPolicyBindingStore(policies),
        ),
        InMemoryUserViabilityPolicyStore(policies),
    )


def test_authenticated_user_can_change_only_personal_settings() -> None:
    app = create_app(Settings())
    client = TestClient(app)
    headers: list[dict[str, str]] = []
    password = "CorrectHorseBatteryStaple1!"
    for email in ("a@example.com", "b@example.com"):
        app.state.identity_administration.create_user(
            email=email, role=UserRole.USER, password=password
        )
        login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
        assert login.status_code == 200
        headers.append({"Authorization": f"Bearer {login.json()['access_token']}"})
    user_a, user_b = headers
    assert client.get(PATH).status_code == 401
    assert client.put(PATH, json={}).status_code == 401
    first = client.get(PATH, headers=user_a).json()
    assert client.get(PATH, headers=user_b).json() == first
    body = {
        "expected_identifier": first["identifier"],
        "expected_version": first["version"],
        "conditional_from": 45,
        "viable_from": 75,
    }
    changed = client.put(PATH, headers=user_a, json=body)
    assert changed.status_code == 200
    second = changed.json()
    assert second["conditional_from"] == 45
    assert second["viable_from"] == 75
    assert client.get(PATH, headers=user_b).json() == first
    assert client.get("/api/v1/decision-support/viability-policy", headers=user_a).json() == first
    assert client.put(PATH, headers=user_a, json=body).status_code == 409
    body.update(expected_version=second["version"])
    assert client.put(PATH, headers=user_a, json=body).json() == second
    for invalid in ((75, 75), (-1, 75), (45, 101)):
        response = client.put(
            PATH,
            headers=user_a,
            json={
                **body,
                "conditional_from": invalid[0],
                "viable_from": invalid[1],
            },
        )
        assert response.status_code == 422
    assert (
        client.put(PATH, headers=user_a, json={**body, "user_id": str(uuid4())}).status_code == 422
    )
    assert client.get(PATH, headers=user_a).json() == second


def test_new_evaluations_capture_the_owners_personal_policy(
    service: UserViabilityPolicyService,
) -> None:
    user_a, user_b, project, parcel = uuid4(), uuid4(), uuid4(), uuid4()
    first = service.current(user_a)
    personal = service.revise(user_a, first.reference, ViabilityPolicyConfiguration(45, 75))

    class ParcelProvider:
        def resolve(self, **_: object) -> ParcelSnapshot:
            return ParcelSnapshot(
                project_id=project,
                parcel_id=parcel,
                parcel_version=1,
                geometry=SnapshotGeometry.from_geojson(
                    {
                        "type": "Polygon",
                        "coordinates": [
                            [[-77.6, -11.1], [-77.5, -11.1], [-77.5, -11.0], [-77.6, -11.1]]
                        ],
                    }
                ),
                crs="EPSG:4326",
                captured_at=datetime(2026, 10, 1, tzinfo=UTC),
            )

    evaluations = AgroclimaticEvaluationService(
        InMemoryEvaluationRepository(),
        ParcelProvider(),
        bind_viability_policy=service.bind_policy_to_evaluation,
    )

    def request(owner: UUID) -> UUID:
        return evaluations.request_evaluation(
            RequestEvaluation(
                owner_user_id=owner,
                parcel_reference=ParcelReferenceInput(project, parcel, 1),
                requested_crops=("maize",),
                environmental_inputs=(
                    EnvironmentalInputReferenceInput("climate", uuid4(), uuid4()),
                ),
            )
        ).id

    old_a, old_b = request(user_a), request(user_b)
    second = service.revise(user_a, personal.reference, ViabilityPolicyConfiguration(50, 80))
    new_a = request(user_a)
    assert service.defaults.policy_for_evaluation(old_a) == personal
    assert service.defaults.policy_for_evaluation(old_b) == first
    assert service.defaults.policy_for_evaluation(new_a) == second
    assert service.current(user_b) == first


def test_saving_default_values_pins_them_to_the_account(
    service: UserViabilityPolicyService,
) -> None:
    user_a, user_b = uuid4(), uuid4()
    first = service.current(user_a)
    service.revise(user_a, first.reference, first.configuration)
    changed = service.defaults.revise(first.reference, ViabilityPolicyConfiguration(45, 75))
    assert service.current(user_a) == first
    assert service.current(user_b) == changed


def test_store_rejects_concurrent_first_and_stale_updates(
    service: UserViabilityPolicyService,
) -> None:
    user = uuid4()
    first = service.current(user)
    personal = service.revise(user, first.reference, ViabilityPolicyConfiguration(45, 75))
    with pytest.raises(UserViabilityPolicyConflictError):
        service.users.set_user_viability_policy(user, first.reference, expected_current=None)
    with pytest.raises(UserViabilityPolicyConflictError):
        service.users.set_user_viability_policy(
            user, first.reference, expected_current=first.reference
        )
    assert service.current(user) == personal
