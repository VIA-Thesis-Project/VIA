"""In-memory Identity Access repository adapters."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from threading import RLock
from uuid import UUID

from ..domain.errors import IdentityConflictError
from ..domain.models import AuthSession, User, normalize_email
from ..domain.repositories import RefreshRotationStatus


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[UUID, User] = {}
        self._ids_by_email: dict[str, UUID] = {}
        self._lock = RLock()

    def add(self, user: User) -> None:
        with self._lock:
            if user.id in self._users or user.email in self._ids_by_email:
                raise IdentityConflictError("User already exists.")
            self._users[user.id] = user
            self._ids_by_email[user.email] = user.id

    def save(self, user: User) -> None:
        with self._lock:
            current = self._users.get(user.id)
            if current is None:
                raise IdentityConflictError("User does not exist.")
            conflicting_id = self._ids_by_email.get(user.email)
            if conflicting_id is not None and conflicting_id != user.id:
                raise IdentityConflictError("User already exists.")
            if current.email != user.email:
                del self._ids_by_email[current.email]
            self._users[user.id] = user
            self._ids_by_email[user.email] = user.id

    def get_by_id(self, user_id: UUID) -> User | None:
        with self._lock:
            return self._users.get(user_id)

    def get_by_normalized_email(self, normalized_email: str) -> User | None:
        email = normalize_email(normalized_email)
        with self._lock:
            user_id = self._ids_by_email.get(email)
            return self._users.get(user_id) if user_id is not None else None


class InMemoryAuthSessionRepository:
    def __init__(self) -> None:
        self._sessions: dict[UUID, AuthSession] = {}
        self._ids_by_access_hash: dict[str, UUID] = {}
        self._ids_by_refresh_hash: dict[str, UUID] = {}
        self._lock = RLock()

    def add(self, auth_session: AuthSession) -> None:
        with self._lock:
            if (
                auth_session.id in self._sessions
                or auth_session.access_token_hash in self._ids_by_access_hash
                or auth_session.refresh_token_hash in self._ids_by_refresh_hash
            ):
                raise IdentityConflictError("Auth session already exists.")
            self._store(auth_session)

    def save(self, auth_session: AuthSession) -> None:
        with self._lock:
            current = self._sessions.get(auth_session.id)
            if current is None:
                raise IdentityConflictError("Auth session does not exist.")
            access_owner = self._ids_by_access_hash.get(auth_session.access_token_hash)
            refresh_owner = self._ids_by_refresh_hash.get(auth_session.refresh_token_hash)
            if (access_owner is not None and access_owner != auth_session.id) or (
                refresh_owner is not None and refresh_owner != auth_session.id
            ):
                raise IdentityConflictError("Auth session already exists.")
            del self._ids_by_access_hash[current.access_token_hash]
            del self._ids_by_refresh_hash[current.refresh_token_hash]
            self._store(auth_session)

    def get_by_id(self, session_id: UUID) -> AuthSession | None:
        with self._lock:
            return self._sessions.get(session_id)

    def get_by_access_token_hash(self, token_hash: str) -> AuthSession | None:
        with self._lock:
            session_id = self._ids_by_access_hash.get(token_hash)
            return self._sessions.get(session_id) if session_id is not None else None

    def get_by_refresh_token_hash(self, token_hash: str) -> AuthSession | None:
        with self._lock:
            session_id = self._ids_by_refresh_hash.get(token_hash)
            return self._sessions.get(session_id) if session_id is not None else None

    def rotate_refresh(
        self,
        *,
        refresh_token_hash: str,
        replacement: AuthSession,
        rotated_at: datetime,
    ) -> RefreshRotationStatus:
        with self._lock:
            session_id = self._ids_by_refresh_hash.get(refresh_token_hash)
            if session_id is None:
                return RefreshRotationStatus.NOT_FOUND
            current = self._sessions[session_id]
            if current.revoked_at is not None:
                if current.replaced_by_session_id is not None:
                    self._revoke_family_locked(
                        current.family_id,
                        revoked_at=rotated_at,
                        reason="refresh_reuse",
                    )
                    return RefreshRotationStatus.REUSED
                return RefreshRotationStatus.REVOKED
            if current.is_refresh_expired(rotated_at):
                return RefreshRotationStatus.EXPIRED
            self._validate_replacement(current, replacement)
            self._ensure_unique(replacement)

            self._store(replacement)
            self._sessions[current.id] = replace(
                current,
                last_used_at=rotated_at,
                revoked_at=rotated_at,
                replaced_by_session_id=replacement.id,
                revocation_reason="refresh_rotated",
            )
            return RefreshRotationStatus.ROTATED

    def revoke_family(self, family_id: UUID, *, revoked_at: datetime, reason: str) -> None:
        with self._lock:
            self._revoke_family_locked(family_id, revoked_at=revoked_at, reason=reason)

    def revoke_user_sessions(
        self,
        user_id: UUID,
        *,
        revoked_at: datetime,
        reason: str,
    ) -> None:
        with self._lock:
            for session_id, auth_session in tuple(self._sessions.items()):
                if auth_session.user_id == user_id and auth_session.revoked_at is None:
                    self._sessions[session_id] = replace(
                        auth_session,
                        revoked_at=revoked_at,
                        revocation_reason=reason,
                    )

    def _revoke_family_locked(
        self,
        family_id: UUID,
        *,
        revoked_at: datetime,
        reason: str,
    ) -> None:
        for session_id, auth_session in tuple(self._sessions.items()):
            if auth_session.family_id == family_id and auth_session.revoked_at is None:
                self._sessions[session_id] = replace(
                    auth_session,
                    revoked_at=revoked_at,
                    revocation_reason=reason,
                )

    @staticmethod
    def _validate_replacement(current: AuthSession, replacement: AuthSession) -> None:
        if (
            replacement.family_id != current.family_id
            or replacement.user_id != current.user_id
            or replacement.refresh_expires_at != current.refresh_expires_at
        ):
            raise IdentityConflictError("Refresh replacement does not preserve session family.")

    def _ensure_unique(self, session: AuthSession) -> None:
        if (
            session.id in self._sessions
            or session.access_token_hash in self._ids_by_access_hash
            or session.refresh_token_hash in self._ids_by_refresh_hash
        ):
            raise IdentityConflictError("Auth session already exists.")

    def _store(self, session: AuthSession) -> None:
        self._sessions[session.id] = session
        self._ids_by_access_hash[session.access_token_hash] = session.id
        self._ids_by_refresh_hash[session.refresh_token_hash] = session.id
