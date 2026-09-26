"""IA-5 release security, rate limits, and production-surface gates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from shapely.geometry import box, mapping, shape

from test_agronomic_knowledge_http import _Builder, _Service
from via_backend.app import create_app
from via_backend.config import DEFAULT_HUAURA_AOI_BOUNDARY_PATH, Settings
from via_backend.contexts.decision_support.application.knowledge_services import (
    RecommendationApplicationService,
    RecommendationContextBuilder,
)
from via_backend.contexts.decision_support.interfaces.http import create_router
from via_backend.contexts.identity_access.application.public import AuthenticatedPrincipal
from via_backend.contexts.identity_access.domain import UserRole, UserStatus
from via_backend.cost_protection import FixedWindowLimiter

PASSWORD = "CorrectHorseBatteryStaple1!"


def _login(client: TestClient, email: str) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": PASSWORD},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.mark.parametrize(
    ("method", "path", "body"),
    (
        ("GET", "/api/v1/auth/me", None),
        ("GET", "/projects", None),
        ("POST", "/projects", {"name": "Release gate"}),
        ("GET", "/datasets", None),
        (
            "POST",
            "/datasets",
            {"name": "Climate", "source": "Test", "variable": "rain", "unit": "mm"},
        ),
        ("GET", "/api/v1/evaluations", None),
        ("GET", "/api/v1/evaluation-capabilities", None),
    ),
)
@pytest.mark.parametrize("authorization", (None, "Bearer invalid-token"))
def test_sensitive_routes_reject_missing_or_invalid_bearer(
    method: str,
    path: str,
    body: dict[str, Any] | None,
    authorization: str | None,
) -> None:
    client = TestClient(create_app(Settings()))
    headers = {"Authorization": authorization} if authorization else {}

    response = client.request(method, path, json=body, headers=headers)

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_disabled_user_access_token_is_rejected_by_http() -> None:
    application = create_app(Settings())
    admin = application.state.identity_administration
    user = admin.create_user(email="user@example.com", role=UserRole.USER, password=PASSWORD)
    client = TestClient(application)
    headers = _login(client, user.email)

    admin.set_status(user.email, UserStatus.DISABLED)

    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_production_surface_keeps_health_public_and_disables_schema_routes() -> None:
    client = TestClient(create_app(Settings(), include_api_docs=False))

    assert client.get("/health").status_code == 200
    for path in ("/docs", "/redoc", "/openapi.json"):
        assert client.get(path).status_code == 404
    assert client.get("/projects").status_code == 401


def _inside_geometry() -> dict[str, Any]:
    feature_collection = json.loads(
        Path(DEFAULT_HUAURA_AOI_BOUNDARY_PATH).read_text(encoding="utf-8")
    )
    boundary = shape(feature_collection["features"][0]["geometry"])
    center = boundary.representative_point()
    radius = min(center.distance(boundary.boundary) / 10, 0.001)
    parcel = box(center.x - radius, center.y - radius, center.x + radius, center.y + radius)
    assert boundary.covers(parcel)
    return json.loads(json.dumps(mapping(parcel)))


def test_multiple_evaluation_requests_are_queued_for_same_owner() -> None:
    application = create_app(Settings())
    application.state.identity_administration.create_user(
        email="user@example.com",
        role=UserRole.USER,
        password=PASSWORD,
    )
    client = TestClient(application)
    headers = _login(client, "user@example.com")
    project = client.post("/projects", json={"name": "Quota"}, headers=headers).json()
    parcel = client.post(
        f"/projects/{project['id']}/parcels",
        json={"name": "Quota parcel", "geometry": _inside_geometry()},
        headers=headers,
    ).json()
    body = {
        "parcel_reference": {
            "project_id": project["id"],
            "parcel_id": parcel["id"],
            "parcel_version": 1,
        },
        "requested_crops": ["maize"],
        "water_regimes": ["rainfed"],
        "environmental_inputs": [
            {
                "input_key": "release-gate",
                "dataset_id": str(uuid4()),
                "dataset_version_id": str(uuid4()),
            }
        ],
    }

    responses = [client.post("/api/v1/evaluations", json=body, headers=headers) for _ in range(4)]
    assert all(response.status_code == 201 for response in responses)
    assert all(response.json()["status"] == "queued" for response in responses)
    assert len({response.json()["id"] for response in responses}) == 4


class _Owned:
    def __init__(self, evaluation_id: UUID, owner_user_id: UUID) -> None:
        self.evaluation_id = evaluation_id
        self.owner_user_id = owner_user_id

    def resolve_owned_evaluation(self, owner_user_id: UUID, evaluation_id: UUID) -> None:
        assert owner_user_id == self.owner_user_id
        assert evaluation_id == self.evaluation_id


def _decision_support_client(
    service: _Service,
    *,
    knowledge_limit: int = 30,
    recommendation_limit: int = 5,
) -> tuple[TestClient, UUID]:
    owner_user_id = uuid4()
    evaluation_id = uuid4()
    application = FastAPI()
    application.include_router(
        create_router(
            cast(RecommendationContextBuilder, _Builder()),
            cast(RecommendationApplicationService, service),
            _Owned(evaluation_id, owner_user_id),
            lambda: AuthenticatedPrincipal(owner_user_id, UserRole.ADMIN),
            FixedWindowLimiter(),
            knowledge_limit,
            recommendation_limit,
        ),
        prefix="/api/v1",
    )
    return TestClient(application), evaluation_id


def test_knowledge_and_recommendation_rate_limits_return_429() -> None:
    client, evaluation_id = _decision_support_client(
        _Service(), knowledge_limit=1, recommendation_limit=1
    )
    root = f"/api/v1/decision-support/evaluations/{evaluation_id}"
    params = {"crop_id": "maize", "water_regime": "rainfed"}
    body = {"crop_id": "maize", "water_regime": "rainfed"}

    assert client.get(f"{root}/knowledge", params=params).status_code == 200
    knowledge_limited = client.get(f"{root}/knowledge", params=params)
    assert knowledge_limited.status_code == 429
    assert int(knowledge_limited.headers["retry-after"]) > 0
    assert client.post(f"{root}/recommendations", json=body).status_code == 200
    recommendation_limited = client.post(f"{root}/recommendations", json=body)
    assert recommendation_limited.status_code == 429
    assert int(recommendation_limited.headers["retry-after"]) > 0


def test_multiple_recommendation_generations_are_admitted() -> None:
    service = _Service()
    client, evaluation_id = _decision_support_client(service)
    path = f"/api/v1/decision-support/evaluations/{evaluation_id}/recommendations"
    body = {"crop_id": "maize", "water_regime": "rainfed"}

    assert client.post(path, json=body).status_code == 200
    for _ in range(3):
        assert client.post(path, json={**body, "force_regenerate": True}).status_code == 200
    assert service.generate_calls == 4
