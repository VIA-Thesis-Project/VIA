"""Safety guard shared by destructive PostgreSQL/PostGIS integration tests."""

from __future__ import annotations

import os
from collections.abc import Mapping

import pytest
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

EXTERNAL_TEST_DATABASE_OPT_IN = "VIA_ALLOW_EXTERNAL_TEST_DATABASE"


class UnsafeTestDatabaseError(ValueError):
    """Raised before destructive tests target a database that is not explicitly safe."""


def validate_test_database_url(
    database_url: str,
    *,
    allow_external: str | None,
) -> str:
    """Return a safe integration-test URL without ever including it in errors."""
    try:
        database_name = make_url(database_url).database or ""
    except ArgumentError as error:
        raise UnsafeTestDatabaseError(
            "VIA_TEST_DATABASE_URL must be a valid SQLAlchemy database URL."
        ) from error

    if not database_name:
        raise UnsafeTestDatabaseError(
            "VIA_TEST_DATABASE_URL must identify a database by name."
        )
    if database_name.casefold().endswith("_test"):
        return database_url
    if allow_external == "1":
        return database_url

    raise UnsafeTestDatabaseError(
        "Refusing destructive PostgreSQL/PostGIS tests: VIA_TEST_DATABASE_URL "
        "must name a database ending in '_test', or "
        f"{EXTERNAL_TEST_DATABASE_OPT_IN}=1 must explicitly confirm a dedicated, "
        "disposable externally managed test database."
    )


def require_test_database_url(
    environ: Mapping[str, str] | None = None,
) -> str:
    """Read and validate the test-only database settings before any DB operation."""
    environment = os.environ if environ is None else environ
    database_url = environment.get("VIA_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("Set VIA_TEST_DATABASE_URL to run PostgreSQL/PostGIS tests.")
    try:
        return validate_test_database_url(
            database_url,
            allow_external=environment.get(EXTERNAL_TEST_DATABASE_OPT_IN),
        )
    except UnsafeTestDatabaseError as error:
        pytest.fail(str(error), pytrace=False)
