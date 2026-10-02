"""Global policy HTTP security and immutable binding behavior."""

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
from via_backend.contexts.agroclimatic_evaluation.domain import (
    Evaluation,
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    InMemoryEvaluationRepository,
)
from via_backend.contexts.decision_support.application.default_policy import (
    BASELINE_CONFIGURATION,
    DefaultViabilityPolicyService,
)
from via_backend.contexts.decision_support.application.errors import (
    EvaluationPolicyBindingConflictError,
)
from via_backend.contexts.decision_support.application.policy_lifecycle import (
    ViabilityPolicyLifecycleService,
)
from via_backend.contexts.decision_support.domain.models import (
    PolicyReference,
    ViabilityPolicyConfiguration,
    ViabilityPolicySnapshot,
)
from via_backend.contexts.decision_support.infrastructure.memory_policy import (
    InMemoryDefaultViabilityPolicyStore,
    InMemoryEvaluationPolicyBindingStore,
    InMemoryViabilityPolicyRepository,
)
from via_backend.contexts.identity_access.domain import UserRole

PASSWORD = "CorrectHorseBatteryStaple1!"
PATH = "/api/v1/decision-support/viability-policy"


def _headers(client: TestClient, email: str) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login", json={"email": email, "password": PASSWORD}
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_global_policy_http_auth_validation_idempotency_and_stale_writes() -> None:
    application = create_app(Settings())
    users = application.state.identity_administration
    users.create_user(email="user@example.com", role=UserRole.USER, password=PASSWORD)
    users.create_user(email="admin@example.com", role=UserRole.ADMIN, password=PASSWORD)
    client = TestClient(application)
    user = _headers(client, "user@example.com")
    admin = _headers(client, "admin@example.com")

    assert client.get(PATH).status_code == 401
    assert client.put(PATH, json={}).status_code == 401
    initial = client.get(PATH, headers=user)
    assert initial.status_code == 200
    first = initial.json()
    assert (first["identifier"], first["version"]) == ("via-policy", "1")
    assert first["default_configuration"] == {
        "conditional_from": 40.0,
        "viable_from": 70.0,
    }
    assert client.get(PATH, headers=admin).json() == first

    body = {
        "expected_identifier": first["identifier"],
        "expected_version": first["version"],
        "conditional_from": 45.0,
        "viable_from": 75.0,
    }
    assert client.put(PATH, headers=user, json=body).status_code == 403
    for invalid in ((75.0, 75.0), (-1.0, 75.0), (45.0, 101.0)):
        response = client.put(
            PATH,
            headers=admin,
            json={**body, "conditional_from": invalid[0], "viable_from": invalid[1]},
        )
        assert response.status_code == 422

    changed = client.put(PATH, headers=admin, json=body)
    assert changed.status_code == 200
    second = changed.json()
    assert second["version"] != first["version"]
    assert second["identifier"] == first["identifier"]
    assert (second["conditional_from"], second["viable_from"]) == (45.0, 75.0)
    assert client.put(PATH, headers=admin, json=body).status_code == 409
    repeated = client.put(
        PATH,
        headers=admin,
        json={**body, "expected_version": second["version"]},
    )
    assert repeated.status_code == 200
    assert repeated.json() == second


def test_binding_captures_default_once_and_preserves_versions() -> None:
    policies = InMemoryViabilityPolicyRepository()
    defaults = InMemoryDefaultViabilityPolicyStore(policies)
    bindings = InMemoryEvaluationPolicyBindingStore(policies)
    first = ViabilityPolicySnapshot(PolicyReference("via-policy", "1"), BASELINE_CONFIGURATION)
    policies.add(first)
    defaults.set_default_viability_policy(first.reference, expected_current=None)
    service = DefaultViabilityPolicyService(
        defaults, ViabilityPolicyLifecycleService(policies), bindings
    )
    evaluation_a, evaluation_b, legacy = uuid4(), uuid4(), uuid4()
    assert service.policy_for_evaluation(legacy) is None
    assert service.bind_default_policy_to_evaluation(evaluation_a) == first
    assert service.bind_default_policy_to_evaluation(evaluation_a) == first
    second = service.revise(
        first.reference, ViabilityPolicyConfiguration(45.0, 75.0)
    )
    with pytest.raises(EvaluationPolicyBindingConflictError):
        service.bind_default_policy_to_evaluation(evaluation_a)
    assert service.bind_default_policy_to_evaluation(evaluation_b) == second
    assert service.policy_for_evaluation(evaluation_a) == first
    assert service.policy_for_evaluation(evaluation_b) == second
    assert policies.get(first.reference) == first
    assert policies.get(second.reference) == second


def test_queued_evaluation_keeps_creation_policy_while_default_changes() -> None:
    policies = InMemoryViabilityPolicyRepository()
    defaults = InMemoryDefaultViabilityPolicyStore(policies)
    bindings = InMemoryEvaluationPolicyBindingStore(policies)
    first = ViabilityPolicySnapshot(PolicyReference("via-policy", "1"), BASELINE_CONFIGURATION)
    policies.add(first)
    defaults.set_default_viability_policy(first.reference, expected_current=None)
    policy_service = DefaultViabilityPolicyService(
        defaults, ViabilityPolicyLifecycleService(policies), bindings
    )
    evaluation_repository = InMemoryEvaluationRepository()
    owner_id, project_id, parcel_id = uuid4(), uuid4(), uuid4()

    class ParcelProvider:
        def resolve(self, **_: object) -> ParcelSnapshot:
            return ParcelSnapshot(
                project_id=project_id,
                parcel_id=parcel_id,
                parcel_version=1,
                geometry=SnapshotGeometry.from_geojson({
                    "type": "Polygon",
                    "coordinates": [[
                        [-77.6, -11.1], [-77.5, -11.1], [-77.5, -11.0], [-77.6, -11.1]
                    ]],
                }),
                crs="EPSG:4326",
                captured_at=datetime(2026, 9, 27, tzinfo=UTC),
            )

    service = AgroclimaticEvaluationService(
        evaluation_repository,
        ParcelProvider(),
        bind_viability_policy=lambda evaluation_id, _owner: (
            policy_service.bind_default_policy_to_evaluation(evaluation_id)
        ),
    )
    command = RequestEvaluation(
        owner_user_id=owner_id,
        parcel_reference=ParcelReferenceInput(project_id, parcel_id, 1),
        requested_crops=("maize",),
        environmental_inputs=(
            EnvironmentalInputReferenceInput("climate", uuid4(), uuid4()),
        ),
    )
    evaluation_a = service.request_evaluation(command)
    assert policy_service.policy_for_evaluation(evaluation_a.id) == first
    second = policy_service.revise(
        first.reference, ViabilityPolicyConfiguration(45.0, 75.0)
    )
    evaluation_b = service.request_evaluation(command)
    assert policy_service.policy_for_evaluation(evaluation_a.id) == first
    assert policy_service.policy_for_evaluation(evaluation_b.id) == second
    assert policy_service.policy_for_evaluation(uuid4()) is None

    class FailingRepository(InMemoryEvaluationRepository):
        def add(self, evaluation: Evaluation) -> None:
            raise RuntimeError("Simulated persistence failure")

    failing_repository = FailingRepository()
    failed_id = uuid4()

    def recover(evaluation_id: UUID) -> None:
        if failing_repository.get(evaluation_id) is None:
            bindings.release_orphan(evaluation_id)

    failing_service = AgroclimaticEvaluationService(
        failing_repository,
        ParcelProvider(),
        new_id=lambda: failed_id,
        bind_viability_policy=lambda evaluation_id, _owner: (
            policy_service.bind_default_policy_to_evaluation(evaluation_id)
        ),
        recover_unpersisted_policy=recover,
    )
    with pytest.raises(RuntimeError, match="Simulated persistence failure"):
        failing_service.request_evaluation(command)
    assert policy_service.policy_for_evaluation(failed_id) is None
