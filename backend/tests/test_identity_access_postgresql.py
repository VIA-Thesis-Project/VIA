from __future__ import annotations

import os
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from pathlib import Path
from threading import Barrier
from uuid import UUID, uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, text

from database_test_support import require_test_database_url
from via_backend.contexts.identity_access.application import IdentityAdministrationService
from via_backend.contexts.identity_access.domain import (
    AuthSession,
    IdentityConflictError,
    RefreshRotationStatus,
    User,
    UserRole,
    UserStatus,
)
from via_backend.contexts.identity_access.infrastructure import create_database
from via_backend.contexts.identity_access.infrastructure.database import SessionFactory
from via_backend.contexts.identity_access.infrastructure.postgresql_repositories import (
    PostgreSQLAuthSessionRepository,
    PostgreSQLUserRepository,
)
from via_backend.contexts.identity_access.infrastructure.security import Sha256TokenHasher

pytestmark = pytest.mark.integration
BACKEND_ROOT = Path(__file__).parents[1]
NOW = datetime(2026, 9, 20, 12, tzinfo=UTC)


@pytest.fixture(scope="session")
def database() -> Iterator[tuple[Engine, SessionFactory]]:
    database_url = require_test_database_url()
    previous = os.environ.get("VIA_DATABASE_URL")
    os.environ["VIA_DATABASE_URL"] = database_url
    try:
        command.upgrade(Config(str(BACKEND_ROOT / "alembic.ini")), "head")
    finally:
        if previous is None:
            os.environ.pop("VIA_DATABASE_URL", None)
        else:
            os.environ["VIA_DATABASE_URL"] = previous

    engine, sessions = create_database(database_url)
    yield engine, sessions
    engine.dispose()


@pytest.fixture(autouse=True)
def clean_identity_access(database: tuple[Engine, SessionFactory]) -> None:
    engine, _ = database
    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE identity_access.auth_sessions, identity_access.users CASCADE")
        )


def _user(*, email: str = "user@example.com") -> User:
    return User(
        id=uuid4(),
        email=email,
        password_hash="opaque-password-hash",
        status=UserStatus.ACTIVE,
        role=UserRole.USER,
        created_at=NOW,
        updated_at=NOW,
    )


def _session(
    user_id: UUID,
    *,
    access_seed: str = "access",
    refresh_seed: str = "refresh",
    family_id: UUID | None = None,
    refresh_expires_at: datetime | None = None,
    created_at: datetime = NOW,
) -> AuthSession:
    hasher = Sha256TokenHasher()
    return AuthSession(
        id=uuid4(),
        family_id=family_id or uuid4(),
        user_id=user_id,
        access_token_hash=hasher.hash(access_seed),
        access_expires_at=created_at + timedelta(minutes=15),
        refresh_token_hash=hasher.hash(refresh_seed),
        refresh_expires_at=refresh_expires_at or created_at + timedelta(days=7),
        created_at=created_at,
    )


def test_postgresql_user_round_trip_and_normalized_uniqueness(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    repository = PostgreSQLUserRepository(sessions)
    user = _user(email=" User@Example.COM ")
    repository.add(user)

    assert PostgreSQLUserRepository(sessions).get_by_id(user.id) == user
    assert repository.get_by_normalized_email("USER@example.com") == user

    with pytest.raises(IdentityConflictError, match="already exists"):
        repository.add(_user(email="user@example.com"))


def test_postgresql_auth_session_round_trip_hash_lookup_and_constraints(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    user = _user()
    PostgreSQLUserRepository(sessions).add(user)
    repository = PostgreSQLAuthSessionRepository(sessions)
    auth_session = _session(user.id)
    repository.add(auth_session)

    assert PostgreSQLAuthSessionRepository(sessions).get_by_id(auth_session.id) == auth_session
    assert repository.get_by_access_token_hash(auth_session.access_token_hash) == auth_session
    assert repository.get_by_refresh_token_hash(auth_session.refresh_token_hash) == auth_session

    duplicate_hash = _session(
        user.id,
        access_seed="access",
        refresh_seed="another-refresh",
    )
    with pytest.raises(IdentityConflictError, match="conflicts"):
        repository.add(duplicate_hash)

    missing_user_session = _session(uuid4(), access_seed="other", refresh_seed="other-refresh")
    with pytest.raises(IdentityConflictError, match="conflicts"):
        repository.add(missing_user_session)


def test_postgresql_refresh_rotation_preserves_family_and_absolute_expiry(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    user = _user()
    PostgreSQLUserRepository(sessions).add(user)
    repository = PostgreSQLAuthSessionRepository(sessions)
    original = _session(user.id)
    repository.add(original)
    rotated_at = NOW + timedelta(minutes=1)
    replacement = _session(
        user.id,
        access_seed="replacement-access",
        refresh_seed="replacement-refresh",
        family_id=original.family_id,
        refresh_expires_at=original.refresh_expires_at,
        created_at=rotated_at,
    )

    outcome = repository.rotate_refresh(
        refresh_token_hash=original.refresh_token_hash,
        replacement=replacement,
        rotated_at=rotated_at,
    )

    assert outcome is RefreshRotationStatus.ROTATED
    consumed = repository.get_by_id(original.id)
    persisted_replacement = repository.get_by_id(replacement.id)
    assert consumed is not None
    assert persisted_replacement is not None
    assert consumed.last_used_at == rotated_at
    assert consumed.revoked_at == rotated_at
    assert consumed.replaced_by_session_id == replacement.id
    assert consumed.revocation_reason == "refresh_rotated"
    assert persisted_replacement.family_id == original.family_id
    assert persisted_replacement.refresh_expires_at == original.refresh_expires_at


def test_postgresql_refresh_reuse_revokes_the_whole_family(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    user = _user()
    PostgreSQLUserRepository(sessions).add(user)
    repository = PostgreSQLAuthSessionRepository(sessions)
    original = _session(user.id)
    repository.add(original)
    first_rotated_at = NOW + timedelta(minutes=1)
    replacement = _session(
        user.id,
        access_seed="replacement-access",
        refresh_seed="replacement-refresh",
        family_id=original.family_id,
        refresh_expires_at=original.refresh_expires_at,
        created_at=first_rotated_at,
    )
    assert repository.rotate_refresh(
        refresh_token_hash=original.refresh_token_hash,
        replacement=replacement,
        rotated_at=first_rotated_at,
    ) is RefreshRotationStatus.ROTATED

    unused_candidate = _session(
        user.id,
        access_seed="unused-access",
        refresh_seed="unused-refresh",
        family_id=original.family_id,
        refresh_expires_at=original.refresh_expires_at,
        created_at=NOW + timedelta(minutes=2),
    )
    outcome = repository.rotate_refresh(
        refresh_token_hash=original.refresh_token_hash,
        replacement=unused_candidate,
        rotated_at=NOW + timedelta(minutes=2),
    )

    assert outcome is RefreshRotationStatus.REUSED
    revoked_replacement = repository.get_by_id(replacement.id)
    assert revoked_replacement is not None
    assert revoked_replacement.revoked_at == NOW + timedelta(minutes=2)
    assert revoked_replacement.revocation_reason == "refresh_reuse"
    assert repository.get_by_id(unused_candidate.id) is None


def test_postgresql_family_and_user_revocation_scope(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    first_user = _user(email="first@example.com")
    second_user = _user(email="second@example.com")
    users = PostgreSQLUserRepository(sessions)
    users.add(first_user)
    users.add(second_user)
    repository = PostgreSQLAuthSessionRepository(sessions)
    first_family = _session(first_user.id, access_seed="a1", refresh_seed="r1")
    second_family = _session(first_user.id, access_seed="a2", refresh_seed="r2")
    other_user = _session(second_user.id, access_seed="a3", refresh_seed="r3")
    for auth_session in (first_family, second_family, other_user):
        repository.add(auth_session)

    family_revoked_at = NOW + timedelta(minutes=1)
    repository.revoke_family(
        first_family.family_id,
        revoked_at=family_revoked_at,
        reason="family_test",
    )
    assert repository.get_by_id(first_family.id).revocation_reason == "family_test"  # type: ignore[union-attr]
    assert repository.get_by_id(second_family.id).revoked_at is None  # type: ignore[union-attr]
    assert repository.get_by_id(other_user.id).revoked_at is None  # type: ignore[union-attr]

    user_revoked_at = NOW + timedelta(minutes=2)
    repository.revoke_user_sessions(
        first_user.id,
        revoked_at=user_revoked_at,
        reason="user_test",
    )
    already_revoked = repository.get_by_id(first_family.id)
    newly_revoked = repository.get_by_id(second_family.id)
    untouched = repository.get_by_id(other_user.id)
    assert already_revoked is not None and already_revoked.revocation_reason == "family_test"
    assert newly_revoked is not None and newly_revoked.revocation_reason == "user_test"
    assert untouched is not None and untouched.revoked_at is None


def test_postgresql_concurrent_double_use_has_one_rotation_and_detects_reuse(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    user = _user()
    PostgreSQLUserRepository(sessions).add(user)
    repository = PostgreSQLAuthSessionRepository(sessions)
    original = _session(user.id)
    repository.add(original)
    rotated_at = NOW + timedelta(minutes=1)
    replacements = [
        _session(
            user.id,
            access_seed=f"concurrent-access-{index}",
            refresh_seed=f"concurrent-refresh-{index}",
            family_id=original.family_id,
            refresh_expires_at=original.refresh_expires_at,
            created_at=rotated_at,
        )
        for index in range(2)
    ]
    barrier = Barrier(2)

    def rotate(replacement: AuthSession) -> RefreshRotationStatus:
        barrier.wait()
        return PostgreSQLAuthSessionRepository(sessions).rotate_refresh(
            refresh_token_hash=original.refresh_token_hash,
            replacement=replacement,
            rotated_at=rotated_at,
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = list(executor.map(rotate, replacements))

    assert set(outcomes) == {
        RefreshRotationStatus.ROTATED,
        RefreshRotationStatus.REUSED,
    }
    persisted = [repository.get_by_id(candidate.id) for candidate in replacements]
    winners = [candidate for candidate in persisted if candidate is not None]
    assert len(winners) == 1
    assert winners[0].revocation_reason == "refresh_reuse"
    consumed = repository.get_by_id(original.id)
    assert consumed is not None
    assert consumed.replaced_by_session_id == winners[0].id


def test_postgresql_admin_disable_and_reset_revoke_sessions(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    users = PostgreSQLUserRepository(sessions)
    auth_sessions = PostgreSQLAuthSessionRepository(sessions)
    user = _user()
    users.add(user)
    first = _session(user.id, access_seed="first-access", refresh_seed="first-refresh")
    auth_sessions.add(first)

    class _Clock:
        def now(self) -> datetime:
            return NOW + timedelta(hours=1)

    class _PasswordHasher:
        def hash(self, password: str) -> str:
            return f"hashed:{password}"

        def verify(self, password: str, password_hash: str) -> bool:
            return password_hash == self.hash(password)

    admin = IdentityAdministrationService(
        users=users,
        sessions=auth_sessions,
        password_hasher=_PasswordHasher(),
        clock=_Clock(),
    )

    disabled = admin.set_status(user.id, UserStatus.DISABLED)
    assert disabled.status is UserStatus.DISABLED
    revoked_by_disable = auth_sessions.get_by_id(first.id)
    assert revoked_by_disable is not None
    assert revoked_by_disable.revocation_reason == "user_disabled"

    admin.set_status(user.id, UserStatus.ACTIVE)
    second = _session(user.id, access_seed="second-access", refresh_seed="second-refresh")
    auth_sessions.add(second)
    admin.reset_password(user.id, "a sufficiently long password")
    revoked_by_reset = auth_sessions.get_by_id(second.id)
    assert revoked_by_reset is not None
    assert revoked_by_reset.revocation_reason == "password_reset"
