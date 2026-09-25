"""One-shot production schema migration host for VIA releases."""

from __future__ import annotations

import argparse
import os
from collections.abc import Sequence
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

ALEMBIC_CONFIG_ENV = "VIA_ALEMBIC_CONFIG"


def _source_alembic_config() -> Path:
    """Return the repository-local Alembic config when running from source."""
    return Path(__file__).resolve().parents[2] / "alembic.ini"


def resolve_alembic_config() -> Path:
    """Resolve the Alembic config without depending on the process cwd."""
    configured = os.getenv(ALEMBIC_CONFIG_ENV)
    if configured is not None:
        if not configured.strip():
            raise ValueError(f"{ALEMBIC_CONFIG_ENV} must not be empty when set.")
        config_path = Path(configured).expanduser().resolve()
    else:
        config_path = _source_alembic_config().resolve()

    if not config_path.is_file():
        raise ValueError(
            f"Alembic configuration file does not exist: {config_path}. "
            f"Set {ALEMBIC_CONFIG_ENV} to the absolute alembic.ini path."
        )
    return config_path


def _require_production_postgresql() -> str:
    database_url = os.getenv("VIA_MIGRATION_DATABASE_URL") or os.getenv("VIA_DATABASE_URL")
    if not database_url:
        raise ValueError(
            "Production migration requires VIA_MIGRATION_DATABASE_URL or VIA_DATABASE_URL."
        )
    for setting_name in (
        "VIA_FARM_MANAGEMENT_REPOSITORY",
        "VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY",
        "VIA_AGROCLIMATIC_EVALUATION_REPOSITORY",
    ):
        selection = os.getenv(setting_name, "postgresql").casefold()
        if selection != "postgresql":
            raise ValueError(
                "Production migration requires PostgreSQL persistence: "
                f"{setting_name}=postgresql (got {selection!r})."
            )
    try:
        backend_name = make_url(database_url).get_backend_name()
    except ArgumentError as error:
        raise ValueError("Migration database URL must be a valid PostgreSQL URL.") from error
    if backend_name != "postgresql":
        raise ValueError("Production migration requires PostgreSQL persistence.")
    return database_url


def upgrade() -> None:
    """Validate production persistence and migrate the schema to Alembic head."""
    _require_production_postgresql()
    config_path = resolve_alembic_config()
    command.upgrade(Config(str(config_path)), "head")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="via-migrate")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("upgrade", help="Upgrade the production schema to Alembic head.")
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Run the explicit release migration CLI."""
    arguments = _build_parser().parse_args(argv)
    if arguments.command == "upgrade":
        upgrade()


if __name__ == "__main__":
    main()
