"""Repository ports owned by Identity Access Domain."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Protocol
from uuid import UUID

from .models import AuthSession, User


class RefreshRotationStatus(StrEnum):
    """Outcome of one atomic refresh-token rotation attempt."""

    ROTATED = "rotated"
    NOT_FOUND = "not_found"
    EXPIRED = "expired"
    REVOKED = "revoked"
    REUSED = "reused"


class IUserRepository(Protocol):
    def add(self, user: User) -> None: ...

    def save(self, user: User) -> None: ...

    def get_by_id(self, user_id: UUID) -> User | None: ...

    def get_by_normalized_email(self, normalized_email: str) -> User | None: ...


class IAuthSessionRepository(Protocol):
    def add(self, auth_session: AuthSession) -> None: ...

    def save(self, auth_session: AuthSession) -> None: ...

    def get_by_id(self, session_id: UUID) -> AuthSession | None: ...

    def get_by_access_token_hash(self, token_hash: str) -> AuthSession | None: ...

    def get_by_refresh_token_hash(self, token_hash: str) -> AuthSession | None: ...

    def rotate_refresh(
        self,
        *,
        refresh_token_hash: str,
        replacement: AuthSession,
        rotated_at: datetime,
    ) -> RefreshRotationStatus: ...

    def revoke_family(self, family_id: UUID, *, revoked_at: datetime, reason: str) -> None: ...

    def revoke_user_sessions(
        self,
        user_id: UUID,
        *,
        revoked_at: datetime,
        reason: str,
    ) -> None: ...
