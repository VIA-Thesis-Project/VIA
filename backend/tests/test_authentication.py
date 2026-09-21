from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import cast

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from via_backend.app import create_app
from via_backend.config import Settings
from via_backend.contexts.identity_access.application import (
    AuthenticationError,
    AuthenticationService,
    IdentityAdministrationService,
    PasswordPolicyError,
)
from via_backend.contexts.identity_access.domain import UserRole, UserStatus
from via_backend.contexts.identity_access.infrastructure import (
    InMemoryAuthSessionRepository,
    InMemoryUserRepository,
    Sha256TokenHasher,
)
from via_backend.contexts.identity_access.interfaces import AuthHttpSettings, create_router

NOW = datetime(2026, 9, 21, 6, tzinfo=UTC)
ACCESS_TTL = 900
REFRESH_TTL = 1_209_600
PASSWORD = "correct horse battery staple"
ORIGIN = "https://frontend.example"


class _Clock:
    def __init__(self, now: datetime = NOW) -> None:
        self.value = now

    def now(self) -> datetime:
        return self.value

    def advance(self, **delta: float) -> None:
        self.value += timedelta(**delta)


class _PasswordHasher:
    def hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify(self, password: str, password_hash: str) -> bool:
        return password_hash == self.hash(password)


class _TokenGenerator:
    def __init__(self) -> None:
        self._counter = 0

    def generate(self) -> str:
        self._counter += 1
        return f"opaque-test-token-{self._counter}"


@dataclass(slots=True)
class _Harness:
    auth: AuthenticationService
    admin: IdentityAdministrationService
    users: InMemoryUserRepository
    sessions: InMemoryAuthSessionRepository
    clock: _Clock
    token_hasher: Sha256TokenHasher


def _harness() -> _Harness:
    users = InMemoryUserRepository()
    sessions = InMemoryAuthSessionRepository()
    clock = _Clock()
    password_hasher = _PasswordHasher()
    token_hasher = Sha256TokenHasher()
    auth = AuthenticationService(
        users=users,
        sessions=sessions,
        password_hasher=password_hasher,
        token_generator=_TokenGenerator(),
        token_hasher=token_hasher,
        clock=clock,
        access_token_ttl_seconds=ACCESS_TTL,
        refresh_token_ttl_seconds=REFRESH_TTL,
    )
    admin = IdentityAdministrationService(
        users=users,
        sessions=sessions,
        password_hasher=password_hasher,
        clock=clock,
    )
    admin.create_user(email="User@Example.COM", role=UserRole.USER, password=PASSWORD)
    return _Harness(auth, admin, users, sessions, clock, token_hasher)


def _http_client() -> tuple[TestClient, _Harness]:
    harness = _harness()
    app = FastAPI()
    app.include_router(
        create_router(
            harness.auth,
            AuthHttpSettings(
                refresh_cookie_name="__Secure-via_refresh",
                refresh_cookie_secure=True,
                refresh_cookie_samesite="lax",
                trusted_origins=(ORIGIN,),
            ),
        ),
        prefix="/api/v1",
    )
    return TestClient(app, base_url="https://testserver"), harness


def test_password_policy_is_length_only_and_does_not_strip() -> None:
    harness = _harness()

    with pytest.raises(PasswordPolicyError):
        harness.admin.create_user(
            email="short@example.com",
            role=UserRole.USER,
            password="short",
        )
    with pytest.raises(PasswordPolicyError):
        harness.admin.create_user(
            email="long@example.com",
            role=UserRole.USER,
            password="x" * 129,
        )

    user = harness.admin.create_user(
        email="spaces@example.com",
        role=UserRole.USER,
        password=" 1234567890 ",
    )
    assert harness.users.get_by_id(user.id) is not None


def test_login_persists_hashes_and_resolves_minimal_principal() -> None:
    harness = _harness()

    result = harness.auth.login(email=" USER@example.com ", password=PASSWORD)
    session = harness.sessions.get_by_access_token_hash(
        harness.token_hasher.hash(result.access_token)
    )

    assert result.access_expires_in == ACCESS_TTL
    assert result.refresh_expires_in == REFRESH_TTL
    assert session is not None
    assert session.access_token_hash != result.access_token
    assert session.refresh_token_hash != result.refresh_token
    assert session.access_expires_at == NOW + timedelta(seconds=ACCESS_TTL)
    assert session.refresh_expires_at == NOW + timedelta(seconds=REFRESH_TTL)
    principal = harness.auth.authenticate_access_token(result.access_token)
    assert principal.user_id == result.user.id
    assert principal.role is UserRole.USER
    assert not hasattr(principal, "email")


def test_login_rejects_wrong_password_missing_user_and_disabled_user() -> None:
    harness = _harness()

    with pytest.raises(AuthenticationError):
        harness.auth.login(email="user@example.com", password="wrong password value")
    with pytest.raises(AuthenticationError):
        harness.auth.login(email="missing@example.com", password=PASSWORD)

    harness.admin.set_status("user@example.com", UserStatus.DISABLED)
    with pytest.raises(AuthenticationError):
        harness.auth.login(email="user@example.com", password=PASSWORD)


def test_access_token_rejects_expired_and_revoked_sessions() -> None:
    harness = _harness()
    expired = harness.auth.login(email="user@example.com", password=PASSWORD)
    harness.clock.advance(seconds=ACCESS_TTL)
    with pytest.raises(AuthenticationError):
        harness.auth.authenticate_access_token(expired.access_token)

    harness = _harness()
    revoked = harness.auth.login(email="user@example.com", password=PASSWORD)
    session = harness.sessions.get_by_access_token_hash(
        harness.token_hasher.hash(revoked.access_token)
    )
    assert session is not None
    harness.sessions.revoke_family(
        session.family_id,
        revoked_at=harness.clock.now(),
        reason="test_revocation",
    )
    with pytest.raises(AuthenticationError):
        harness.auth.authenticate_access_token(revoked.access_token)


def test_refresh_rotates_tokens_without_extending_absolute_expiry() -> None:
    harness = _harness()
    login = harness.auth.login(email="user@example.com", password=PASSWORD)
    previous = harness.sessions.get_by_refresh_token_hash(
        harness.token_hasher.hash(login.refresh_token)
    )
    assert previous is not None

    harness.clock.advance(seconds=60)
    refreshed = harness.auth.refresh_session(login.refresh_token)
    replacement = harness.sessions.get_by_refresh_token_hash(
        harness.token_hasher.hash(refreshed.refresh_token)
    )
    consumed = harness.sessions.get_by_id(previous.id)

    assert replacement is not None
    assert consumed is not None
    assert replacement.family_id == previous.family_id
    assert replacement.refresh_expires_at == previous.refresh_expires_at
    assert refreshed.refresh_expires_in == REFRESH_TTL - 60
    assert consumed.revoked_at == harness.clock.now()
    assert consumed.replaced_by_session_id == replacement.id
    assert consumed.revocation_reason == "refresh_rotated"
    assert harness.auth.authenticate_access_token(refreshed.access_token).user_id == login.user.id


def test_refresh_rejects_expired_and_unknown_tokens() -> None:
    harness = _harness()
    login = harness.auth.login(email="user@example.com", password=PASSWORD)

    with pytest.raises(AuthenticationError):
        harness.auth.refresh_session("unknown-refresh-token")

    harness.clock.advance(seconds=REFRESH_TTL)
    with pytest.raises(AuthenticationError):
        harness.auth.refresh_session(login.refresh_token)


def test_refresh_reuse_revokes_the_entire_family_and_double_use_has_one_rotation() -> None:
    harness = _harness()
    login = harness.auth.login(email="user@example.com", password=PASSWORD)
    first_rotation = harness.auth.refresh_session(login.refresh_token)

    with pytest.raises(AuthenticationError):
        harness.auth.refresh_session(login.refresh_token)

    replacement = harness.sessions.get_by_refresh_token_hash(
        harness.token_hasher.hash(first_rotation.refresh_token)
    )
    assert replacement is not None
    assert replacement.revoked_at == harness.clock.now()
    assert replacement.revocation_reason == "refresh_reuse"
    with pytest.raises(AuthenticationError):
        harness.auth.authenticate_access_token(first_rotation.access_token)
    with pytest.raises(AuthenticationError):
        harness.auth.refresh_session(first_rotation.refresh_token)


def test_logout_revokes_family_is_idempotent_and_does_not_require_access_token() -> None:
    harness = _harness()
    login = harness.auth.login(email="user@example.com", password=PASSWORD)

    harness.auth.logout(login.refresh_token)
    harness.auth.logout(login.refresh_token)
    harness.auth.logout(None)

    with pytest.raises(AuthenticationError):
        harness.auth.authenticate_access_token(login.access_token)
    with pytest.raises(AuthenticationError):
        harness.auth.refresh_session(login.refresh_token)


def test_disable_and_password_reset_revoke_existing_sessions() -> None:
    harness = _harness()
    first = harness.auth.login(email="user@example.com", password=PASSWORD)

    harness.admin.set_status("user@example.com", UserStatus.DISABLED)
    with pytest.raises(AuthenticationError):
        harness.auth.authenticate_access_token(first.access_token)

    harness.admin.set_status("user@example.com", UserStatus.ACTIVE)
    with pytest.raises(AuthenticationError):
        harness.auth.authenticate_access_token(first.access_token)

    second = harness.auth.login(email="user@example.com", password=PASSWORD)
    new_password = "a different valid password"
    harness.admin.reset_password("user@example.com", new_password)
    with pytest.raises(AuthenticationError):
        harness.auth.authenticate_access_token(second.access_token)
    with pytest.raises(AuthenticationError):
        harness.auth.login(email="user@example.com", password=PASSWORD)
    assert harness.auth.login(email="user@example.com", password=new_password).user.email == (
        "user@example.com"
    )


def test_http_login_me_refresh_and_logout_contract() -> None:
    client, _ = _http_client()
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": PASSWORD},
    )

    assert login.status_code == 200
    assert login.headers["cache-control"] == "no-store"
    body = login.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == ACCESS_TTL
    assert "refresh_token" not in body
    cookie = login.headers["set-cookie"]
    assert "__Secure-via_refresh=" in cookie
    assert "HttpOnly" in cookie
    assert "Secure" in cookie
    assert "SameSite=lax" in cookie
    assert "Path=/api/v1/auth" in cookie
    assert f"Max-Age={REFRESH_TTL}" in cookie
    assert "Domain=" not in cookie
    original_refresh = client.cookies.get("__Secure-via_refresh")
    assert original_refresh is not None

    unauthorized = client.get("/api/v1/auth/me")
    assert unauthorized.status_code == 401
    assert unauthorized.headers["www-authenticate"] == "Bearer"
    assert unauthorized.headers["cache-control"] == "no-store"

    me = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {body['access_token']}"},
    )
    assert me.status_code == 200
    assert me.headers["cache-control"] == "no-store"
    assert me.json() == {
        "id": body["user"]["id"],
        "email": "user@example.com",
        "status": "active",
        "role": "user",
    }

    refreshed = client.post("/api/v1/auth/refresh", headers={"Origin": ORIGIN})
    assert refreshed.status_code == 200
    assert refreshed.headers["cache-control"] == "no-store"
    refreshed_access = refreshed.json()["access_token"]
    assert refreshed_access != body["access_token"]
    assert client.cookies.get("__Secure-via_refresh") != original_refresh

    logout = client.post("/api/v1/auth/logout", headers={"Origin": ORIGIN})
    assert logout.status_code == 204
    assert logout.headers["cache-control"] == "no-store"
    assert "Max-Age=0" in logout.headers["set-cookie"]
    assert client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {refreshed_access}"},
    ).status_code == 401


def test_http_login_failures_do_not_reveal_account_existence() -> None:
    client, _ = _http_client()
    wrong = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "wrong password value"},
    )
    missing = client.post(
        "/api/v1/auth/login",
        json={"email": "missing@example.com", "password": PASSWORD},
    )

    assert wrong.status_code == missing.status_code == 401
    assert wrong.json() == missing.json() == {"detail": "Invalid email or password."}
    assert client.post("/api/v1/auth/login", json={}).status_code == 422


def test_refresh_and_logout_validate_browser_origin_and_refresh_is_cookie_only() -> None:
    client, _ = _http_client()
    client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": PASSWORD},
    )

    denied = client.post(
        "/api/v1/auth/refresh",
        headers={"Origin": "https://malicious.invalid"},
    )
    assert denied.status_code == 403

    allowed = client.post("/api/v1/auth/refresh", headers={"Origin": ORIGIN})
    assert allowed.status_code == 200

    no_cookie_client, _ = _http_client()
    without_cookie = no_cookie_client.post(
        "/api/v1/auth/refresh",
        headers={"Origin": ORIGIN},
        json={"refresh_token": "body-token-must-not-work"},
    )
    assert without_cookie.status_code == 401

    denied_logout = client.post(
        "/api/v1/auth/logout",
        headers={"Origin": "https://malicious.invalid"},
    )
    assert denied_logout.status_code == 403


def test_auth_openapi_exposes_bearer_only_for_me() -> None:
    client, _ = _http_client()
    schema = cast(FastAPI, client.app).openapi()

    bearer = schema["components"]["securitySchemes"]["BearerAuth"]
    assert bearer["type"] == "http"
    assert bearer["scheme"] == "bearer"
    assert schema["paths"]["/api/v1/auth/me"]["get"]["security"] == [
        {"BearerAuth": []}
    ]
    for path, method in [
        ("/api/v1/auth/login", "post"),
        ("/api/v1/auth/refresh", "post"),
        ("/api/v1/auth/logout", "post"),
    ]:
        assert "security" not in schema["paths"][path][method]
    assert {
        schema["paths"]["/api/v1/auth/login"]["post"]["operationId"],
        schema["paths"]["/api/v1/auth/refresh"]["post"]["operationId"],
        schema["paths"]["/api/v1/auth/logout"]["post"]["operationId"],
        schema["paths"]["/api/v1/auth/me"]["get"]["operationId"],
    } == {"auth_login", "auth_refresh", "auth_logout", "auth_me"}


def test_ia2_keeps_health_and_existing_functional_routes_public() -> None:
    client = TestClient(create_app(Settings()))

    assert client.get("/health").status_code == 200
    assert client.get("/projects").status_code == 200
    schema = cast(FastAPI, client.app).openapi()
    assert "/api/v1/auth/register" not in schema["paths"]
    assert "/register" not in schema["paths"]
