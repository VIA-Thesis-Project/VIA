"""Administrative CLI for VIA identity users."""

from __future__ import annotations

import argparse
import getpass
from collections.abc import Sequence

from sqlalchemy import Engine
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

from via_backend.config import Settings
from via_backend.contexts.identity_access.application import (
    IdentityAdministrationService,
    IdentityUserNotFoundError,
    PasswordPolicyError,
)
from via_backend.contexts.identity_access.domain import (
    IdentityConflictError,
    IdentityValidationError,
    UserRole,
    UserStatus,
)
from via_backend.contexts.identity_access.infrastructure import (
    Argon2PasswordHasher,
    PostgreSQLAuthSessionRepository,
    PostgreSQLUserRepository,
    SystemClock,
)
from via_backend.infrastructure import create_database


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="via-identity-admin")
    commands = parser.add_subparsers(dest="command", required=True)

    create = commands.add_parser("create-user", help="Create an active identity user.")
    create.add_argument("--email", required=True)
    create.add_argument(
        "--role",
        type=str.casefold,
        choices=[role.value for role in UserRole],
        default=UserRole.USER.value,
    )

    status = commands.add_parser("set-status", help="Set a user's account status.")
    status.add_argument("reference", help="User email or UUID.")
    status.add_argument(
        "--status",
        required=True,
        type=str.casefold,
        choices=[value.value for value in UserStatus],
    )

    reset = commands.add_parser("reset-password", help="Reset a user's password.")
    reset.add_argument("reference", help="User email or UUID.")
    return parser


def _prompt_password(*, confirmation_label: str = "Confirm password: ") -> str:
    password = getpass.getpass("Password: ")
    confirmation = getpass.getpass(confirmation_label)
    if password != confirmation:
        raise PasswordPolicyError("Password confirmation does not match.")
    return password


def _service_from_env() -> tuple[IdentityAdministrationService, Engine]:
    settings = Settings.from_env()
    if settings.database_url is None:
        raise SystemExit("VIA_DATABASE_URL is required for identity administration.")
    try:
        backend = make_url(settings.database_url).get_backend_name()
    except ArgumentError as error:
        raise SystemExit("VIA_DATABASE_URL must be a valid PostgreSQL URL.") from error
    if backend != "postgresql":
        raise SystemExit("Identity administration requires PostgreSQL persistence.")

    engine, sessions = create_database(settings.database_url)
    service = IdentityAdministrationService(
        users=PostgreSQLUserRepository(sessions),
        sessions=PostgreSQLAuthSessionRepository(sessions),
        password_hasher=Argon2PasswordHasher(),
        clock=SystemClock(),
    )
    return service, engine


def main(argv: Sequence[str] | None = None) -> int:
    """Run identity administration against the configured PostgreSQL database."""
    args = _build_parser().parse_args(argv)
    service, engine = _service_from_env()
    try:
        if args.command == "create-user":
            password = _prompt_password()
            user = service.create_user(
                email=args.email,
                role=UserRole(args.role),
                password=password,
            )
            print(f"created user_id={user.id} email={user.email} role={user.role.value}")
            return 0
        if args.command == "set-status":
            user = service.set_status(args.reference, UserStatus(args.status))
            print(f"updated user_id={user.id} status={user.status.value}")
            return 0
        if args.command == "reset-password":
            password = _prompt_password(confirmation_label="Confirm new password: ")
            user = service.reset_password(args.reference, password)
            print(f"password reset user_id={user.id}")
            return 0
        raise AssertionError(f"Unhandled command {args.command!r}")
    except (
        IdentityConflictError,
        IdentityUserNotFoundError,
        IdentityValidationError,
        PasswordPolicyError,
    ) as error:
        raise SystemExit(str(error)) from error
    finally:
        engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())
