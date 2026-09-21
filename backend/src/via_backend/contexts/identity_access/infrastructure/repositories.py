"""In-memory Identity Access repository adapters."""

from __future__ import annotations

from threading import RLock
from uuid import UUID

from ..domain.errors import IdentityConflictError
from ..domain.models import AuthSession, User, normalize_email


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

    def add(self, session: AuthSession) -> None:
        with self._lock:
            if (
                session.id in self._sessions
                or session.access_token_hash in self._ids_by_access_hash
                or session.refresh_token_hash in self._ids_by_refresh_hash
            ):
                raise IdentityConflictError("Auth session already exists.")
            self._store(session)

    def save(self, session: AuthSession) -> None:
        with self._lock:
            current = self._sessions.get(session.id)
            if current is None:
                raise IdentityConflictError("Auth session does not exist.")
            access_owner = self._ids_by_access_hash.get(session.access_token_hash)
            refresh_owner = self._ids_by_refresh_hash.get(session.refresh_token_hash)
            if (access_owner is not None and access_owner != session.id) or (
                refresh_owner is not None and refresh_owner != session.id
            ):
                raise IdentityConflictError("Auth session already exists.")
            del self._ids_by_access_hash[current.access_token_hash]
            del self._ids_by_refresh_hash[current.refresh_token_hash]
            self._store(session)

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

    def _store(self, session: AuthSession) -> None:
        self._sessions[session.id] = session
        self._ids_by_access_hash[session.access_token_hash] = session.id
        self._ids_by_refresh_hash[session.refresh_token_hash] = session.id
