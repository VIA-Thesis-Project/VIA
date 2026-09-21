"""PostgreSQL repository adapters for Identity Access."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..domain.errors import IdentityConflictError
from ..domain.models import AuthSession, User, UserRole, UserStatus, normalize_email
from .database import SessionFactory
from .orm import AuthSessionRecord, UserRecord


class PostgreSQLUserRepository:
    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def add(self, user: User) -> None:
        try:
            with self._sessions.begin() as session:
                session.add(_user_record(user))
        except IntegrityError as error:
            raise IdentityConflictError("User already exists.") from error

    def save(self, user: User) -> None:
        try:
            with self._sessions.begin() as session:
                record = session.get(UserRecord, user.id)
                if record is None:
                    raise IdentityConflictError("User does not exist.")
                record.email = user.email
                record.password_hash = user.password_hash
                record.status = user.status.value
                record.role = user.role.value
                record.created_at = user.created_at
                record.updated_at = user.updated_at
        except IntegrityError as error:
            raise IdentityConflictError("User already exists.") from error

    def get_by_id(self, user_id: UUID) -> User | None:
        with self._sessions() as session:
            record = session.get(UserRecord, user_id)
            return _user_from_record(record) if record is not None else None

    def get_by_normalized_email(self, normalized_email: str) -> User | None:
        email = normalize_email(normalized_email)
        with self._sessions() as session:
            record = session.scalar(select(UserRecord).where(UserRecord.email == email))
            return _user_from_record(record) if record is not None else None


class PostgreSQLAuthSessionRepository:
    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def add(self, auth_session: AuthSession) -> None:
        try:
            with self._sessions.begin() as session:
                session.add(_auth_session_record(auth_session))
        except IntegrityError as error:
            raise IdentityConflictError("Auth session conflicts with persisted data.") from error

    def save(self, auth_session: AuthSession) -> None:
        try:
            with self._sessions.begin() as session:
                record = session.get(AuthSessionRecord, auth_session.id)
                if record is None:
                    raise IdentityConflictError("Auth session does not exist.")
                record.family_id = auth_session.family_id
                record.user_id = auth_session.user_id
                record.access_token_hash = auth_session.access_token_hash
                record.access_expires_at = auth_session.access_expires_at
                record.refresh_token_hash = auth_session.refresh_token_hash
                record.refresh_expires_at = auth_session.refresh_expires_at
                record.created_at = auth_session.created_at
                record.last_used_at = auth_session.last_used_at
                record.revoked_at = auth_session.revoked_at
                record.replaced_by_session_id = auth_session.replaced_by_session_id
                record.revocation_reason = auth_session.revocation_reason
        except IntegrityError as error:
            raise IdentityConflictError("Auth session conflicts with persisted data.") from error

    def get_by_id(self, session_id: UUID) -> AuthSession | None:
        with self._sessions() as session:
            record = session.get(AuthSessionRecord, session_id)
            return _auth_session_from_record(record) if record is not None else None

    def get_by_access_token_hash(self, token_hash: str) -> AuthSession | None:
        with self._sessions() as session:
            record = session.scalar(
                select(AuthSessionRecord).where(AuthSessionRecord.access_token_hash == token_hash)
            )
            return _auth_session_from_record(record) if record is not None else None

    def get_by_refresh_token_hash(self, token_hash: str) -> AuthSession | None:
        with self._sessions() as session:
            record = session.scalar(
                select(AuthSessionRecord).where(AuthSessionRecord.refresh_token_hash == token_hash)
            )
            return _auth_session_from_record(record) if record is not None else None


def _user_record(user: User) -> UserRecord:
    return UserRecord(
        id=user.id,
        email=user.email,
        password_hash=user.password_hash,
        status=user.status.value,
        role=user.role.value,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def _user_from_record(record: UserRecord) -> User:
    return User(
        id=record.id,
        email=record.email,
        password_hash=record.password_hash,
        status=UserStatus(record.status),
        role=UserRole(record.role),
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


def _auth_session_record(auth_session: AuthSession) -> AuthSessionRecord:
    return AuthSessionRecord(
        id=auth_session.id,
        family_id=auth_session.family_id,
        user_id=auth_session.user_id,
        access_token_hash=auth_session.access_token_hash,
        access_expires_at=auth_session.access_expires_at,
        refresh_token_hash=auth_session.refresh_token_hash,
        refresh_expires_at=auth_session.refresh_expires_at,
        created_at=auth_session.created_at,
        last_used_at=auth_session.last_used_at,
        revoked_at=auth_session.revoked_at,
        replaced_by_session_id=auth_session.replaced_by_session_id,
        revocation_reason=auth_session.revocation_reason,
    )


def _auth_session_from_record(record: AuthSessionRecord) -> AuthSession:
    return AuthSession(
        id=record.id,
        family_id=record.family_id,
        user_id=record.user_id,
        access_token_hash=record.access_token_hash,
        access_expires_at=record.access_expires_at,
        refresh_token_hash=record.refresh_token_hash,
        refresh_expires_at=record.refresh_expires_at,
        created_at=record.created_at,
        last_used_at=record.last_used_at,
        revoked_at=record.revoked_at,
        replaced_by_session_id=record.replaced_by_session_id,
        revocation_reason=record.revocation_reason,
    )
