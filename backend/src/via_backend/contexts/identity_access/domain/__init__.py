"""Identity Access domain."""

from .errors import IdentityConflictError, IdentityValidationError
from .models import AuthSession, User, UserRole, UserStatus, normalize_email
from .repositories import IAuthSessionRepository, IUserRepository, RefreshRotationStatus

__all__ = [
    "AuthSession",
    "IAuthSessionRepository",
    "IUserRepository",
    "IdentityConflictError",
    "IdentityValidationError",
    "RefreshRotationStatus",
    "User",
    "UserRole",
    "UserStatus",
    "normalize_email",
]
