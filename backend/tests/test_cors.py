"""Environment-configured development CORS behavior."""

from fastapi.testclient import TestClient

from via_backend.app import create_app
from via_backend.config import Settings

ALLOWED = "http://localhost:5173"


def _client(*origins: str) -> TestClient:
    return TestClient(create_app(Settings(cors_allowed_origins=origins)))


def test_allowed_origin_is_echoed() -> None:
    response = _client(ALLOWED).get("/health", headers={"Origin": ALLOWED})

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED
    assert response.headers["access-control-allow-credentials"] == "true"


def test_allowed_preflight_supports_frontend_method_and_headers() -> None:
    response = _client(ALLOWED).options(
        "/projects",
        headers={
            "Origin": ALLOWED,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,authorization",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED
    assert "POST" in response.headers["access-control-allow-methods"]
    allowed_headers = response.headers["access-control-allow-headers"].casefold()
    assert "content-type" in allowed_headers
    assert "authorization" in allowed_headers


def test_disallowed_origin_receives_no_cors_permission() -> None:
    response = _client(ALLOWED).get(
        "/health", headers={"Origin": "http://malicious.invalid"}
    )

    assert "access-control-allow-origin" not in response.headers


def test_empty_configuration_preserves_no_cors_behavior() -> None:
    response = _client().get("/health", headers={"Origin": ALLOWED})

    assert "access-control-allow-origin" not in response.headers
