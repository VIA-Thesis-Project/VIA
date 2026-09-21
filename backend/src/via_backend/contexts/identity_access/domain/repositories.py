"""Repository ports owned by Identity Access Domain."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from .models import AuthSession, User


class IUserRepository(Protocol):
    def add(self, user: User) -> None: ...

    def save(self, user: User) -> None: ...

    def get_by_id(self, user_id: UUID) -> User | None: ...

    def get_by_normalized_email(self, normalized_email: str) -> User | None: ...


class IAuthSessionRepository(Protocol):
    def add(self, session: AuthSession) -> None: ...

    def save(self, session: AuthSession) -> None: ...

    def get_by_id(self, session_id: UUID) -> AuthSession | None: ...

    def get_by_access_token_hash(self, token_hash: str) -> AuthSession | None: ...

    def get_by_refresh_token_hash(self, token_hash: str) -> AuthSession | None: ...
