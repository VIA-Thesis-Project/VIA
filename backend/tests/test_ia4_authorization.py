"""IA-4 HTTP authorization, burst protection, and safe dataset DTOs."""

from __future__ import annotations

from typing import cast
from uuid import UUID, uuid4

from fastapi import HTTPException, Request
from fastapi.testclient import TestClient

from test_agronomic_knowledge_http import _Builder, _Service
from via_backend.app import create_app
from via_backend.config import Settings
from via_backend.contexts.agroclimatic_evaluation.application.public import (
    OwnedEvaluationNotFoundError,
)
from via_backend.contexts.decision_support.application.knowledge_services import (
    RecommendationApplicationService,
    RecommendationContextBuilder,
)
from via_backend.contexts.decision_support.interfaces.http import create_router
from via_backend.contexts.identity_access.application.public import AuthenticatedPrincipal
from via_backend.contexts.identity_access.domain.models import UserRole
from via_backend.cost_protection import FixedWindowLimiter, RateLimitExceededError

PASSWORD = "CorrectHorseBatteryStaple1!"


def _token(client: TestClient, email: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD})
    assert response.status_code == 200
    return response.json()["access_token"]


def _body() -> dict[str, str]:
    return {"name": "Climate", "source": "Test", "variable": "rain", "unit": "mm"}


def _version() -> dict[str, object]:
    return {
        "version_identifier": "v1",
        "crs": "EPSG:4326",
        "resolution": {"x": 1, "y": 1, "unit": "degree"},
        "extent": {"west": -78, "south": -12, "east": -77, "north": -11},
        "checksum": "sha256:abc",
        "storage_reference": "/srv/private/climate.tif",
    }


def test_datasets_require_bearer_and_admin_for_writes_and_hide_paths() -> None:
    app = create_app(Settings())
    admin_service = app.state.identity_administration
    admin_service.create_user(email="user@example.com", role=UserRole.USER, password=PASSWORD)
    admin_service.create_user(email="admin@example.com", role=UserRole.ADMIN, password=PASSWORD)
    client = TestClient(app)
    for response in (client.get("/datasets"), client.post("/datasets", json=_body())):
        assert response.status_code == 401
        assert response.headers["www-authenticate"] == "Bearer"
    user = {"Authorization": f"Bearer {_token(client, 'user@example.com')}"}
    admin = {"Authorization": f"Bearer {_token(client, 'admin@example.com')}"}
    assert client.get("/datasets", headers=user).status_code == 200
    assert client.post("/datasets", json=_body(), headers=user).status_code == 403
    created = client.post("/datasets", json=_body(), headers=admin)
    assert created.status_code == 201
    dataset_id = created.json()["id"]
    path = f"/datasets/{dataset_id}/versions"
    assert client.post(path, json=_version(), headers=user).status_code == 403
    version = client.post(path, json=_version(), headers=admin)
    assert version.status_code == 201
    version_id = version.json()["id"]
    for endpoint in (path, f"{path}/{version_id}"):
        payload = client.get(endpoint, headers=user)
        assert payload.status_code == 200
        assert "storage_reference" not in payload.text
        assert "/srv/private" not in payload.text
    coverage = f"{path}/{version_id}/coverage"
    assert client.post(coverage, json={}, headers={}).status_code == 401


def test_login_refresh_and_coverage_rate_limits() -> None:
    app = create_app(
        Settings(
            rate_login_per_minute=2, rate_refresh_per_minute=2, rate_dataset_coverage_per_minute=1
        )
    )
    app.state.identity_administration.create_user(
        email="user@example.com", role=UserRole.USER, password=PASSWORD
    )
    client = TestClient(app)
    token = _token(client, "user@example.com")
    assert (
        client.post(
            "/api/v1/auth/login",
            json={
                "email": "x@example.com",
                "password": "wrong",
            },
        ).status_code
        == 401
    )
    limited = client.post(
        "/api/v1/auth/login",
        json={
            "email": "x@example.com",
            "password": "wrong",
        },
    )
    assert limited.status_code == 429 and int(limited.headers["retry-after"]) > 0
    for _ in range(2):
        assert client.post("/api/v1/auth/refresh").status_code == 401
    assert client.post("/api/v1/auth/refresh").status_code == 429
    path = f"/datasets/{uuid4()}/versions/{uuid4()}/coverage"
    body = {
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
        },
        "crs": "EPSG:4326",
    }
    headers = {"Authorization": f"Bearer {token}"}
    assert client.post(path, json=body, headers=headers).status_code == 404
    response = client.post(path, json=body, headers=headers)
    assert response.status_code == 429
    assert int(response.headers["retry-after"]) > 0


def test_fixed_window_clock_and_separate_subjects() -> None:
    now = [0.0]
    limiter = FixedWindowLimiter(lambda: now[0])
    limiter.check("knowledge", "a", 1)
    limiter.check("knowledge", "b", 1)
    try:
        limiter.check("knowledge", "a", 1)
    except RateLimitExceededError as error:
        assert error.retry_after == 60
    else:
        raise AssertionError("Expected 429")
    now[0] = 60.0
    limiter.check("knowledge", "a", 1)


class _Owned:
    def __init__(self, owners: dict[UUID, UUID]) -> None:
        self.owners = owners

    def resolve_owned_evaluation(self, owner_user_id: UUID, evaluation_id: UUID) -> None:
        if self.owners.get(evaluation_id) != owner_user_id:
            raise OwnedEvaluationNotFoundError("Evaluation was not found.")


def test_decision_support_owner_role_and_rate_checks_precede_cost() -> None:
    from fastapi import FastAPI

    user_a, user_b, admin_id = uuid4(), uuid4(), uuid4()
    own_a, own_b, own_admin = uuid4(), uuid4(), uuid4()
    owners = _Owned({own_a: user_a, own_b: user_b, own_admin: admin_id})
    service = _Service()
    principals = {
        "a": AuthenticatedPrincipal(user_a, UserRole.USER),
        "b": AuthenticatedPrincipal(user_b, UserRole.USER),
        "admin": AuthenticatedPrincipal(admin_id, UserRole.ADMIN),
    }

    def principal(request: Request) -> AuthenticatedPrincipal:
        token = request.headers.get("authorization", "").removeprefix("Bearer ")
        if token not in principals:
            raise HTTPException(status_code=401, headers={"WWW-Authenticate": "Bearer"})
        return principals[token]

    app = FastAPI()
    app.include_router(
        create_router(
            cast(RecommendationContextBuilder, _Builder()),
            cast(RecommendationApplicationService, service),
            owners,
            principal,
            FixedWindowLimiter(),
            1,
            5,
        ),
        prefix="/api/v1",
    )
    client = TestClient(app)
    root = "/api/v1/decision-support/evaluations"
    params = {"crop_id": "maize", "water_regime": "rainfed"}
    assert client.get(f"{root}/{own_a}/knowledge", params=params).status_code == 401
    assert (
        client.get(
            f"{root}/{own_a}/knowledge", params=params, headers={"Authorization": "Bearer b"}
        ).status_code
        == 404
    )
    assert (
        client.get(
            f"{root}/{uuid4()}/knowledge", params=params, headers={"Authorization": "Bearer b"}
        ).status_code
        == 404
    )
    assert service.retrieve_calls == 0
    assert (
        client.get(
            f"{root}/{own_a}/knowledge", params=params, headers={"Authorization": "Bearer a"}
        ).status_code
        == 200
    )
    assert (
        client.get(
            f"{root}/{own_a}/knowledge", params=params, headers={"Authorization": "Bearer a"}
        ).status_code
        == 429
    )
    assert (
        client.get(
            f"{root}/{own_b}/knowledge", params=params, headers={"Authorization": "Bearer b"}
        ).status_code
        == 200
    )
    body = {"crop_id": "maize", "water_regime": "rainfed"}
    assert (
        client.post(
            f"{root}/{own_a}/recommendations", json=body, headers={"Authorization": "Bearer b"}
        ).status_code
        == 404
    )
    assert service.generate_calls == 0
    assert (
        client.post(
            f"{root}/{own_a}/recommendations", json=body, headers={"Authorization": "Bearer a"}
        ).status_code
        == 200
    )
    assert (
        client.post(
            f"{root}/{own_a}/recommendations",
            json={**body, "force_regenerate": True},
            headers={"Authorization": "Bearer a"},
        ).status_code
        == 403
    )
    assert (
        client.post(
            f"{root}/{own_admin}/recommendations",
            json={**body, "force_regenerate": True},
            headers={"Authorization": "Bearer admin"},
        ).status_code
        == 200
    )
    assert (
        client.post(
            f"{root}/{own_a}/recommendations",
            json={**body, "force_regenerate": True},
            headers={"Authorization": "Bearer admin"},
        ).status_code
        == 404
    )
    assert (
        client.get(
            f"{root}/{own_a}/recommendations", headers={"Authorization": "Bearer b"}
        ).status_code
        == 404
    )


def test_live_openapi_bearer_security() -> None:
    schema = create_app(Settings()).openapi()
    for path in ("/datasets", "/api/v1/evaluations"):
        for operation in schema["paths"][path].values():
            assert {"BearerAuth": []} in operation.get("security", [])
