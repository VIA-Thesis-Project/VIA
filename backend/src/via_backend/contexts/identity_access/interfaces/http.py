"""FastAPI resources for Identity Access authentication."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict

from via_backend.cost_protection import FixedWindowLimiter, RateLimitExceededError

from ..application import (
    AuthenticatedPrincipal,
    AuthenticatedUser,
    AuthenticationError,
    AuthenticationResult,
    AuthenticationService,
)
from ..application.public import PrincipalResolver
from ..domain import IdentityValidationError, UserRole, UserStatus

AUTH_COOKIE_PATH = "/api/v1/auth"
NO_STORE_HEADERS = {"Cache-Control": "no-store"}


@dataclass(frozen=True, slots=True)
class AuthHttpSettings:
    refresh_cookie_name: str
    refresh_cookie_secure: bool
    refresh_cookie_samesite: Literal["lax", "strict", "none"]
    trusted_origins: tuple[str, ...]


class _RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LoginBody(_RequestModel):
    email: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    status: UserStatus
    role: UserRole


class AuthenticationResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int
    user: UserResponse


def create_principal_resolver(service: AuthenticationService) -> PrincipalResolver:
    """Build the reusable bearer-token dependency exposed by Identity Access."""
    bearer = HTTPBearer(auto_error=False, scheme_name="BearerAuth")
    bearer_security = Security(bearer)

    def resolve_principal(
        credentials: HTTPAuthorizationCredentials | None = bearer_security,
    ) -> AuthenticatedPrincipal:
        if credentials is None or credentials.scheme.casefold() != "bearer":
            raise _bearer_unauthorized()
        try:
            return service.authenticate_access_token(credentials.credentials)
        except AuthenticationError as error:
            raise _bearer_unauthorized() from error

    return resolve_principal


def create_router(
    service: AuthenticationService,
    settings: AuthHttpSettings,
    principal_resolver: PrincipalResolver | None = None,
    limiter: FixedWindowLimiter | None = None,
    login_limit: int = 5,
    refresh_limit: int = 10,
) -> APIRouter:
    """Create Identity Access authentication routes."""
    router = APIRouter(prefix="/auth", tags=["identity-access"])
    resolve_principal = principal_resolver or create_principal_resolver(service)

    principal_dependency = Depends(resolve_principal)

    @router.post(
        "/login",
        response_model=AuthenticationResponse,
        operation_id="auth_login",
        responses={
            401: {"description": "Invalid credentials."},
            429: {"description": "Login rate limit exceeded."},
        },
    )
    def login(body: LoginBody, response: Response, request: Request) -> AuthenticationResponse:
        if limiter is not None:
            host = request.client.host if request.client else "unknown"
            email_hash = sha256(body.email.strip().casefold().encode()).hexdigest()
            try:
                limiter.check("login_host", host, login_limit)
                limiter.check("login_email", email_hash, login_limit)
            except RateLimitExceededError as error:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests.",
                    headers={"Retry-After": str(error.retry_after), **NO_STORE_HEADERS},
                ) from error
        try:
            result = service.login(email=body.email, password=body.password)
        except IdentityValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(error),
                headers=NO_STORE_HEADERS,
            ) from error
        except AuthenticationError as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers=NO_STORE_HEADERS,
            ) from error
        _set_refresh_cookie(response, result, settings)
        response.headers["Cache-Control"] = "no-store"
        return _authentication_response(result)

    @router.post(
        "/refresh",
        response_model=AuthenticationResponse,
        operation_id="auth_refresh",
        responses={
            401: {"description": "Invalid or missing refresh cookie."},
            403: {"description": "Origin is not trusted."},
            429: {"description": "Refresh rate limit exceeded."},
        },
    )
    def refresh(
        request: Request,
        response: Response,
        refresh_token: str | None = Cookie(
            default=None,
            alias=settings.refresh_cookie_name,
        ),
    ) -> AuthenticationResponse:
        _validate_origin(request, settings)
        if limiter is not None:
            host = request.client.host if request.client else "unknown"
            try:
                limiter.check("refresh_host", host, refresh_limit)
            except RateLimitExceededError as error:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests.",
                    headers={"Retry-After": str(error.retry_after), **NO_STORE_HEADERS},
                ) from error
        if refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
                headers=NO_STORE_HEADERS,
            )
        try:
            result = service.refresh_session(refresh_token)
        except AuthenticationError as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
                headers=NO_STORE_HEADERS,
            ) from error
        _set_refresh_cookie(response, result, settings)
        response.headers["Cache-Control"] = "no-store"
        return _authentication_response(result)

    @router.post(
        "/logout",
        status_code=status.HTTP_204_NO_CONTENT,
        operation_id="auth_logout",
        responses={403: {"description": "Origin is not trusted."}},
    )
    def logout(
        request: Request,
        refresh_token: str | None = Cookie(
            default=None,
            alias=settings.refresh_cookie_name,
        ),
    ) -> Response:
        _validate_origin(request, settings)
        service.logout(refresh_token)
        response = Response(status_code=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(
            key=settings.refresh_cookie_name,
            path=AUTH_COOKIE_PATH,
            secure=settings.refresh_cookie_secure,
            httponly=True,
            samesite=settings.refresh_cookie_samesite,
        )
        response.headers["Cache-Control"] = "no-store"
        return response

    @router.get(
        "/me",
        response_model=UserResponse,
        operation_id="auth_me",
        responses={401: {"description": "Invalid or missing bearer token."}},
    )
    def me(
        response: Response,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> UserResponse:
        try:
            user = service.get_current_user(principal)
        except AuthenticationError as error:
            raise _bearer_unauthorized() from error
        response.headers["Cache-Control"] = "no-store"
        return _user_response(user)

    return router


def _authentication_response(result: AuthenticationResult) -> AuthenticationResponse:
    return AuthenticationResponse(
        access_token=result.access_token,
        expires_in=result.access_expires_in,
        user=_user_response(result.user),
    )


def _user_response(user: AuthenticatedUser) -> UserResponse:
    return UserResponse.model_validate(user)


def _set_refresh_cookie(
    response: Response,
    result: AuthenticationResult,
    settings: AuthHttpSettings,
) -> None:
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=result.refresh_token,
        max_age=result.refresh_expires_in,
        expires=result.refresh_expires_at,
        path=AUTH_COOKIE_PATH,
        secure=settings.refresh_cookie_secure,
        httponly=True,
        samesite=settings.refresh_cookie_samesite,
    )


def _validate_origin(request: Request, settings: AuthHttpSettings) -> None:
    origin = request.headers.get("origin")
    if origin is not None and origin not in settings.trusted_origins:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Origin is not allowed.",
            headers=NO_STORE_HEADERS,
        )


def _bearer_unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing bearer token.",
        headers={"WWW-Authenticate": "Bearer", **NO_STORE_HEADERS},
    )
