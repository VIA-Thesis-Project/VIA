"""Authentication and administrative use cases for Identity Access."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from ..domain import (
    AuthSession,
    IAuthSessionRepository,
    IUserRepository,
    RefreshRotationStatus,
    User,
    UserRole,
    UserStatus,
    normalize_email,
)
from .errors import AuthenticationError, IdentityUserNotFoundError
from .password_policy import validate_password
from .ports import Clock, OpaqueTokenGenerator, PasswordHasher, TokenHasher
from .public import AuthenticatedPrincipal


@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    id: UUID
    email: str
    status: UserStatus
    role: UserRole


@dataclass(frozen=True, slots=True)
class AuthenticationResult:
    access_token: str
    refresh_token: str
    access_expires_in: int
    refresh_expires_in: int
    refresh_expires_at: datetime
    user: AuthenticatedUser


class AuthenticationService:
    def __init__(
        self,
        *,
        users: IUserRepository,
        sessions: IAuthSessionRepository,
        password_hasher: PasswordHasher,
        token_generator: OpaqueTokenGenerator,
        token_hasher: TokenHasher,
        clock: Clock,
        access_token_ttl_seconds: int,
        refresh_token_ttl_seconds: int,
    ) -> None:
        self._users = users
        self._sessions = sessions
        self._password_hasher = password_hasher
        self._token_generator = token_generator
        self._token_hasher = token_hasher
        self._clock = clock
        self._access_token_ttl_seconds = access_token_ttl_seconds
        self._refresh_token_ttl_seconds = refresh_token_ttl_seconds

    def login(self, *, email: str, password: str) -> AuthenticationResult:
        normalized_email = normalize_email(email)
        user = self._users.get_by_normalized_email(normalized_email)
        if user is None:
            raise AuthenticationError("Invalid credentials.")
        if not self._password_hasher.verify(password, user.password_hash):
            raise AuthenticationError("Invalid credentials.")
        if user.status is not UserStatus.ACTIVE:
            raise AuthenticationError("Invalid credentials.")

        now = self._clock.now()
        access_token = self._token_generator.generate()
        refresh_token = self._token_generator.generate()
        refresh_expires_at = now + timedelta(seconds=self._refresh_token_ttl_seconds)
        session = AuthSession(
            id=uuid4(),
            family_id=uuid4(),
            user_id=user.id,
            access_token_hash=self._token_hasher.hash(access_token),
            access_expires_at=now + timedelta(seconds=self._access_token_ttl_seconds),
            refresh_token_hash=self._token_hasher.hash(refresh_token),
            refresh_expires_at=refresh_expires_at,
            created_at=now,
        )
        self._sessions.add(session)
        return self._result(user, access_token, refresh_token, refresh_expires_at, now=now)

    def authenticate_access_token(self, access_token: str) -> AuthenticatedPrincipal:
        if not access_token:
            raise AuthenticationError("Invalid access token.")
        session = self._sessions.get_by_access_token_hash(self._token_hasher.hash(access_token))
        now = self._clock.now()
        if session is None or session.is_revoked or session.is_access_expired(now):
            raise AuthenticationError("Invalid access token.")
        user = self._users.get_by_id(session.user_id)
        if user is None or user.status is not UserStatus.ACTIVE:
            raise AuthenticationError("Invalid access token.")
        return AuthenticatedPrincipal(user_id=user.id, role=user.role)

    def refresh_session(self, refresh_token: str) -> AuthenticationResult:
        if not refresh_token:
            raise AuthenticationError("Invalid refresh token.")
        refresh_hash = self._token_hasher.hash(refresh_token)
        previous = self._sessions.get_by_refresh_token_hash(refresh_hash)
        now = self._clock.now()
        if previous is None:
            raise AuthenticationError("Invalid refresh token.")

        if previous.is_revoked:
            if previous.replaced_by_session_id is not None:
                self._sessions.revoke_family(
                    previous.family_id,
                    revoked_at=now,
                    reason="refresh_reuse",
                )
            raise AuthenticationError("Invalid refresh token.")
        if previous.is_refresh_expired(now):
            raise AuthenticationError("Invalid refresh token.")

        user = self._users.get_by_id(previous.user_id)
        if user is None or user.status is not UserStatus.ACTIVE:
            raise AuthenticationError("Invalid refresh token.")

        access_token = self._token_generator.generate()
        new_refresh_token = self._token_generator.generate()
        replacement = AuthSession(
            id=uuid4(),
            family_id=previous.family_id,
            user_id=previous.user_id,
            access_token_hash=self._token_hasher.hash(access_token),
            access_expires_at=now + timedelta(seconds=self._access_token_ttl_seconds),
            refresh_token_hash=self._token_hasher.hash(new_refresh_token),
            refresh_expires_at=previous.refresh_expires_at,
            created_at=now,
        )
        outcome = self._sessions.rotate_refresh(
            refresh_token_hash=refresh_hash,
            replacement=replacement,
            rotated_at=now,
        )
        if outcome is not RefreshRotationStatus.ROTATED:
            raise AuthenticationError("Invalid refresh token.")
        return self._result(
            user,
            access_token,
            new_refresh_token,
            replacement.refresh_expires_at,
            now=now,
        )

    def logout(self, refresh_token: str | None) -> None:
        if not refresh_token:
            return
        session = self._sessions.get_by_refresh_token_hash(self._token_hasher.hash(refresh_token))
        if session is None:
            return
        self._sessions.revoke_family(
            session.family_id,
            revoked_at=self._clock.now(),
            reason="logout",
        )

    def get_current_user(self, principal: AuthenticatedPrincipal) -> AuthenticatedUser:
        user = self._users.get_by_id(principal.user_id)
        if user is None or user.status is not UserStatus.ACTIVE:
            raise AuthenticationError("Invalid access token.")
        return _user_view(user)

    def _result(
        self,
        user: User,
        access_token: str,
        refresh_token: str,
        refresh_expires_at: datetime,
        *,
        now: datetime,
    ) -> AuthenticationResult:
        return AuthenticationResult(
            access_token=access_token,
            refresh_token=refresh_token,
            access_expires_in=self._access_token_ttl_seconds,
            refresh_expires_in=max(
                0,
                int((refresh_expires_at - now).total_seconds()),
            ),
            refresh_expires_at=refresh_expires_at,
            user=_user_view(user),
        )


class IdentityAdministrationService:
    def __init__(
        self,
        *,
        users: IUserRepository,
        sessions: IAuthSessionRepository,
        password_hasher: PasswordHasher,
        clock: Clock,
    ) -> None:
        self._users = users
        self._sessions = sessions
        self._password_hasher = password_hasher
        self._clock = clock

    def create_user(self, *, email: str, role: UserRole, password: str) -> User:
        validate_password(password)
        now = self._clock.now()
        user = User(
            id=uuid4(),
            email=normalize_email(email),
            password_hash=self._password_hasher.hash(password),
            status=UserStatus.ACTIVE,
            role=UserRole(role),
            created_at=now,
            updated_at=now,
        )
        self._users.add(user)
        return user

    def set_status(self, reference: str | UUID, status: UserStatus) -> User:
        user = self._resolve_user(reference)
        now = self._clock.now()
        updated = replace(user, status=UserStatus(status), updated_at=now)
        self._users.save(updated)
        if updated.status is UserStatus.DISABLED:
            self._sessions.revoke_user_sessions(
                updated.id,
                revoked_at=now,
                reason="user_disabled",
            )
        return updated

    def reset_password(self, reference: str | UUID, password: str) -> User:
        validate_password(password)
        user = self._resolve_user(reference)
        now = self._clock.now()
        password_hash = self._password_hasher.hash(password)
        self._sessions.revoke_user_sessions(
            user.id,
            revoked_at=now,
            reason="password_reset",
        )
        updated = replace(user, password_hash=password_hash, updated_at=now)
        self._users.save(updated)
        return updated

    def _resolve_user(self, reference: str | UUID) -> User:
        if isinstance(reference, UUID):
            user = self._users.get_by_id(reference)
        else:
            try:
                user_id = UUID(reference)
            except ValueError:
                user = self._users.get_by_normalized_email(normalize_email(reference))
            else:
                user = self._users.get_by_id(user_id)
        if user is None:
            raise IdentityUserNotFoundError("User was not found.")
        return user


def _user_view(user: User) -> AuthenticatedUser:
    return AuthenticatedUser(
        id=user.id,
        email=user.email,
        status=user.status,
        role=user.role,
    )
