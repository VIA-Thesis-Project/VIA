"""Identity Access domain models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from .errors import IdentityValidationError


class UserStatus(StrEnum):
    ACTIVE = "active"
    DISABLED = "disabled"


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


def normalize_email(value: str) -> str:
    """Return the canonical email representation used for identity lookup."""
    normalized = value.strip().lower()
    if not normalized:
        raise IdentityValidationError("Email must be non-empty.")
    if len(normalized) > 320:
        raise IdentityValidationError("Email must be at most 320 characters.")
    return normalized


def _require_aware(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise IdentityValidationError(f"{field_name} must be timezone-aware.")


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or value != value.strip():
        raise IdentityValidationError(f"{field_name} must be non-empty and trimmed.")


def _require_sha256_hex(value: str, field_name: str) -> None:
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise IdentityValidationError(
            f"{field_name} must be exactly 64 lowercase hexadecimal characters."
        )


@dataclass(frozen=True, slots=True)
class User:
    id: UUID
    email: str
    password_hash: str
    status: UserStatus
    role: UserRole
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "email", normalize_email(self.email))
        _require_non_empty(self.password_hash, "Password hash")
        try:
            object.__setattr__(self, "status", UserStatus(self.status))
            object.__setattr__(self, "role", UserRole(self.role))
        except ValueError as error:
            raise IdentityValidationError("User status or role is not supported.") from error
        _require_aware(self.created_at, "User creation time")
        _require_aware(self.updated_at, "User update time")
        if self.updated_at < self.created_at:
            raise IdentityValidationError("User update time cannot precede creation time.")

    @property
    def normalized_email(self) -> str:
        return self.email


@dataclass(frozen=True, slots=True)
class AuthSession:
    id: UUID
    family_id: UUID
    user_id: UUID
    access_token_hash: str
    access_expires_at: datetime
    refresh_token_hash: str
    refresh_expires_at: datetime
    created_at: datetime
    last_used_at: datetime | None = None
    revoked_at: datetime | None = None
    replaced_by_session_id: UUID | None = None
    revocation_reason: str | None = None

    def __post_init__(self) -> None:
        _require_sha256_hex(self.access_token_hash, "Access token hash")
        _require_sha256_hex(self.refresh_token_hash, "Refresh token hash")
        for value, field_name in (
            (self.access_expires_at, "Access token expiry"),
            (self.refresh_expires_at, "Refresh token expiry"),
            (self.created_at, "Session creation time"),
        ):
            _require_aware(value, field_name)
        for value, field_name in (
            (self.last_used_at, "Session last-used time"),
            (self.revoked_at, "Session revocation time"),
        ):
            if value is not None:
                _require_aware(value, field_name)
        if self.access_expires_at <= self.created_at:
            raise IdentityValidationError("Access token expiry must follow session creation time.")
        if self.refresh_expires_at <= self.created_at:
            raise IdentityValidationError("Refresh token expiry must follow session creation time.")
        if self.revocation_reason is not None:
            _require_non_empty(self.revocation_reason, "Revocation reason")
            if self.revoked_at is None:
                raise IdentityValidationError("A revocation reason requires a revocation time.")

    def is_access_expired(self, now: datetime) -> bool:
        _require_aware(now, "Current time")
        return now >= self.access_expires_at

    def is_refresh_expired(self, now: datetime) -> bool:
        _require_aware(now, "Current time")
        return now >= self.refresh_expires_at

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None
