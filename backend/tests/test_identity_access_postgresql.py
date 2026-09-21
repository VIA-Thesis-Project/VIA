from __future__ import annotations

import os
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, text

from database_test_support import require_test_database_url
from via_backend.contexts.identity_access.domain import (
    AuthSession,
    IdentityConflictError,
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


def _session(user_id, *, access_seed: str = "access", refresh_seed: str = "refresh") -> AuthSession:
    hasher = Sha256TokenHasher()
    return AuthSession(
        id=uuid4(),
        family_id=uuid4(),
        user_id=user_id,
        access_token_hash=hasher.hash(access_seed),
        access_expires_at=NOW + timedelta(minutes=15),
        refresh_token_hash=hasher.hash(refresh_seed),
        refresh_expires_at=NOW + timedelta(days=7),
        created_at=NOW,
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
