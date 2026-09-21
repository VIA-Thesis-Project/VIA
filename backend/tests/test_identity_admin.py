from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime

import pytest

import via_backend.identity_admin as identity_admin
from via_backend.contexts.identity_access.application import (
    AuthenticationError,
    AuthenticationService,
    IdentityAdministrationService,
)
from via_backend.contexts.identity_access.domain import UserRole, UserStatus
from via_backend.contexts.identity_access.infrastructure import (
    InMemoryAuthSessionRepository,
    InMemoryUserRepository,
    Sha256TokenHasher,
)

NOW = datetime(2026, 9, 21, 6, tzinfo=UTC)
PASSWORD = "correct horse battery staple"
NEW_PASSWORD = "another correct horse battery"


class _Clock:
    def now(self) -> datetime:
        return NOW


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
        return f"cli-token-{self._counter}"


class _Engine:
    def __init__(self) -> None:
        self.dispose_calls = 0

    def dispose(self) -> None:
        self.dispose_calls += 1


@dataclass(slots=True)
class _Harness:
    admin: IdentityAdministrationService
    auth: AuthenticationService
    users: InMemoryUserRepository
    engine: _Engine


def _harness(monkeypatch: pytest.MonkeyPatch) -> _Harness:
    users = InMemoryUserRepository()
    sessions = InMemoryAuthSessionRepository()
    password_hasher = _PasswordHasher()
    clock = _Clock()
    admin = IdentityAdministrationService(
        users=users,
        sessions=sessions,
        password_hasher=password_hasher,
        clock=clock,
    )
    auth = AuthenticationService(
        users=users,
        sessions=sessions,
        password_hasher=password_hasher,
        token_generator=_TokenGenerator(),
        token_hasher=Sha256TokenHasher(),
        clock=clock,
        access_token_ttl_seconds=900,
        refresh_token_ttl_seconds=1_209_600,
    )
    engine = _Engine()
    monkeypatch.setattr(identity_admin, "_service_from_env", lambda: (admin, engine))
    return _Harness(admin=admin, auth=auth, users=users, engine=engine)


def _password_prompts(monkeypatch: pytest.MonkeyPatch, *values: str) -> list[str]:
    prompts: list[str] = []
    answers = iter(values)

    def prompt(label: str) -> str:
        prompts.append(label)
        return next(answers)

    monkeypatch.setattr(identity_admin.getpass, "getpass", prompt)
    return prompts


def test_create_user_cli_prompts_hidden_password_and_accepts_uppercase_role(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    harness = _harness(monkeypatch)
    prompts = _password_prompts(monkeypatch, PASSWORD, PASSWORD)

    assert identity_admin.main(
        ["create-user", "--email", " Admin@Example.COM ", "--role", "ADMIN"]
    ) == 0

    user = harness.users.get_by_normalized_email("admin@example.com")
    assert user is not None
    assert user.role is UserRole.ADMIN
    assert user.status is UserStatus.ACTIVE
    assert prompts == ["Password: ", "Confirm password: "]
    assert PASSWORD not in capsys.readouterr().out
    assert harness.engine.dispose_calls == 1


def test_create_user_cli_rejects_duplicate_user(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _harness(monkeypatch)
    _password_prompts(monkeypatch, PASSWORD, PASSWORD, PASSWORD, PASSWORD)

    assert identity_admin.main(["create-user", "--email", "user@example.com"]) == 0
    with pytest.raises(SystemExit, match="already exists"):
        identity_admin.main(["create-user", "--email", "USER@example.com"])


def test_cli_does_not_accept_plaintext_password_argument() -> None:
    with pytest.raises(SystemExit):
        identity_admin._build_parser().parse_args(
            [
                "create-user",
                "--email",
                "user@example.com",
                "--password",
                PASSWORD,
            ]
        )


def test_set_status_and_reset_password_cli_revoke_existing_sessions(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    harness = _harness(monkeypatch)
    harness.admin.create_user(
        email="user@example.com",
        role=UserRole.USER,
        password=PASSWORD,
    )
    first = harness.auth.login(email="user@example.com", password=PASSWORD)

    assert identity_admin.main(
        ["set-status", "USER@example.com", "--status", "DISABLED"]
    ) == 0
    user = harness.users.get_by_normalized_email("user@example.com")
    assert user is not None and user.status is UserStatus.DISABLED
    with pytest.raises(AuthenticationError):
        harness.auth.authenticate_access_token(first.access_token)

    assert identity_admin.main(
        ["set-status", "user@example.com", "--status", "ACTIVE"]
    ) == 0
    with pytest.raises(AuthenticationError):
        harness.auth.authenticate_access_token(first.access_token)

    second = harness.auth.login(email="user@example.com", password=PASSWORD)
    _password_prompts(monkeypatch, NEW_PASSWORD, NEW_PASSWORD)
    assert identity_admin.main(["reset-password", "user@example.com"]) == 0

    with pytest.raises(AuthenticationError):
        harness.auth.authenticate_access_token(second.access_token)
    with pytest.raises(AuthenticationError):
        harness.auth.login(email="user@example.com", password=PASSWORD)
    assert harness.auth.login(email="user@example.com", password=NEW_PASSWORD).user.email == (
        "user@example.com"
    )
    assert NEW_PASSWORD not in capsys.readouterr().out


def test_reset_password_cli_rejects_confirmation_mismatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    harness = _harness(monkeypatch)
    harness.admin.create_user(
        email="user@example.com",
        role=UserRole.USER,
        password=PASSWORD,
    )
    original = harness.users.get_by_normalized_email("user@example.com")
    assert original is not None
    _password_prompts(monkeypatch, NEW_PASSWORD, "different confirmation")

    with pytest.raises(SystemExit, match="confirmation does not match"):
        identity_admin.main(["reset-password", "user@example.com"])

    assert harness.users.get_by_id(original.id) == original
