from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import uuid4

import pytest
from sqlalchemy import Table

from via_backend.contexts.agroclimatic_evaluation.infrastructure.orm import EvaluationRecord
from via_backend.contexts.farm_management.infrastructure.orm import ProjectRecord
from via_backend.contexts.identity_access.domain import (
    AuthSession,
    IdentityConflictError,
    IdentityValidationError,
    User,
    UserRole,
    UserStatus,
)
from via_backend.contexts.identity_access.infrastructure.orm import AuthSessionRecord, UserRecord
from via_backend.contexts.identity_access.infrastructure.repositories import (
    InMemoryAuthSessionRepository,
    InMemoryUserRepository,
)
from via_backend.contexts.identity_access.infrastructure.security import (
    Argon2PasswordHasher,
    SecretsOpaqueTokenGenerator,
    Sha256TokenHasher,
)

NOW = datetime(2026, 9, 20, 12, tzinfo=UTC)


def _user(*, email: str = "User@Example.COM") -> User:
    return User(
        id=uuid4(),
        email=email,
        password_hash="opaque-password-hash",
        status=UserStatus.ACTIVE,
        role=UserRole.USER,
        created_at=NOW,
        updated_at=NOW,
    )


def _session(user_id=None) -> AuthSession:
    token_hasher = Sha256TokenHasher()
    return AuthSession(
        id=uuid4(),
        family_id=uuid4(),
        user_id=user_id or uuid4(),
        access_token_hash=token_hasher.hash("access-token"),
        access_expires_at=NOW + timedelta(minutes=15),
        refresh_token_hash=token_hasher.hash("refresh-token"),
        refresh_expires_at=NOW + timedelta(days=7),
        created_at=NOW,
    )


def test_user_normalizes_email_and_exposes_canonical_value() -> None:
    user = _user(email="  USER@Example.COM  ")

    assert user.email == "user@example.com"
    assert user.normalized_email == "user@example.com"


def test_user_preserves_supported_status_and_role() -> None:
    user = replace(_user(), status=UserStatus.DISABLED, role=UserRole.ADMIN)

    assert user.status is UserStatus.DISABLED
    assert user.role is UserRole.ADMIN


@pytest.mark.parametrize("email", ["", "   ", "a" * 321])
def test_user_rejects_invalid_canonical_email(email: str) -> None:
    with pytest.raises(IdentityValidationError):
        _user(email=email)


def test_identity_timestamps_must_be_timezone_aware() -> None:
    with pytest.raises(IdentityValidationError, match="timezone-aware"):
        replace(_user(), created_at=NOW.replace(tzinfo=None))


def test_auth_session_reports_expiry_and_revocation_state() -> None:
    session = _session()

    assert not session.is_access_expired(NOW)
    assert session.is_access_expired(session.access_expires_at)
    assert not session.is_revoked

    revoked = replace(session, revoked_at=NOW)
    assert revoked.is_revoked


def test_auth_session_accepts_valid_sha256_token_hashes() -> None:
    session = _session()

    assert len(session.access_token_hash) == 64
    assert len(session.refresh_token_hash) == 64


@pytest.mark.parametrize("field_name", ["access_token_hash", "refresh_token_hash"])
def test_auth_session_rejects_sha256_hash_with_incorrect_length(field_name: str) -> None:
    with pytest.raises(IdentityValidationError, match="exactly 64 lowercase hexadecimal"):
        replace(_session(), **{field_name: "a" * 63})


@pytest.mark.parametrize("field_name", ["access_token_hash", "refresh_token_hash"])
def test_auth_session_rejects_non_hex_sha256_hash(field_name: str) -> None:
    with pytest.raises(IdentityValidationError, match="exactly 64 lowercase hexadecimal"):
        replace(_session(), **{field_name: "g" + "a" * 63})


@pytest.mark.parametrize("field_name", ["access_token_hash", "refresh_token_hash"])
def test_auth_session_rejects_uppercase_sha256_hash(field_name: str) -> None:
    with pytest.raises(IdentityValidationError, match="exactly 64 lowercase hexadecimal"):
        replace(_session(), **{field_name: "A" + "a" * 63})


def test_argon2id_hashing_is_salted_and_verifiable() -> None:
    hasher = Argon2PasswordHasher()
    password = "correct horse battery staple"

    first = hasher.hash(password)
    second = hasher.hash(password)

    assert first != password
    assert first != second
    assert first.startswith("$argon2id$")
    assert hasher.verify(password, first)
    assert not hasher.verify("wrong password", first)


def test_opaque_tokens_are_distinct_url_safe_and_hashed_deterministically() -> None:
    generator = SecretsOpaqueTokenGenerator()
    hasher = Sha256TokenHasher()

    first = generator.generate()
    second = generator.generate()
    first_hash = hasher.hash(first)

    assert first != second
    assert len(first) >= 43
    assert all(character.isalnum() or character in "-_" for character in first)
    assert len(first_hash) == 64
    assert first_hash != first
    assert first_hash == hasher.hash(first)
    assert first_hash != hasher.hash(second)


def test_in_memory_user_repository_uses_normalized_email_and_rejects_duplicates() -> None:
    repository = InMemoryUserRepository()
    user = _user()
    repository.add(user)

    assert repository.get_by_id(user.id) == user
    assert repository.get_by_normalized_email(" USER@example.com ") == user

    with pytest.raises(IdentityConflictError, match="already exists"):
        repository.add(_user(email="user@example.com"))


def test_in_memory_session_repository_indexes_only_hashes() -> None:
    repository = InMemoryAuthSessionRepository()
    session = _session()
    repository.add(session)

    assert repository.get_by_id(session.id) == session
    assert repository.get_by_access_token_hash(session.access_token_hash) == session
    assert repository.get_by_refresh_token_hash(session.refresh_token_hash) == session
    assert repository.get_by_access_token_hash("access-token") is None


def test_identity_metadata_contains_expected_constraints_and_indexes() -> None:
    user_table = cast(Table, UserRecord.__table__)
    auth_session_table = cast(Table, AuthSessionRecord.__table__)

    assert user_table.schema == "identity_access"
    assert auth_session_table.schema == "identity_access"
    assert user_table.c.email.unique is not True
    assert any(
        constraint.name == "uq_users_email"
        for constraint in user_table.constraints
    )
    assert any(
        constraint.name == "uq_auth_sessions_access_token_hash"
        for constraint in auth_session_table.constraints
    )
    assert {
        index.name for index in auth_session_table.indexes
    } >= {"ix_auth_sessions_user_refresh_expires_at", "ix_auth_sessions_family_id"}


def test_ownership_columns_are_nullable_and_have_no_cross_context_foreign_keys() -> None:
    project_table = cast(Table, ProjectRecord.__table__)
    evaluation_table = cast(Table, EvaluationRecord.__table__)
    project_owner = project_table.c.owner_user_id
    evaluation_owner = evaluation_table.c.owner_user_id

    assert project_owner.nullable
    assert evaluation_owner.nullable
    assert not project_owner.foreign_keys
    assert not evaluation_owner.foreign_keys
    assert "ix_projects_owner_user_id" in {index.name for index in project_table.indexes}
    assert "ix_evaluations_owner_user_id" in {
        index.name for index in evaluation_table.indexes
    }
