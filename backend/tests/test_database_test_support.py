"""Focused tests for destructive integration-database safety."""

from __future__ import annotations

import pytest

from database_test_support import UnsafeTestDatabaseError, validate_test_database_url
from via_backend.config import Settings


def test_local_test_database_is_accepted_without_external_opt_in() -> None:
    database_url = "postgresql+psycopg://via:secret@example.invalid/via_test"

    assert validate_test_database_url(database_url, allow_external=None) == database_url


def test_external_database_is_rejected_without_opt_in() -> None:
    with pytest.raises(UnsafeTestDatabaseError, match="Refusing destructive"):
        validate_test_database_url(
            "postgresql+psycopg://via:secret@example.invalid/postgres",
            allow_external=None,
        )


def test_external_database_is_accepted_with_explicit_opt_in() -> None:
    database_url = "postgresql+psycopg://via:secret@example.invalid/postgres"

    assert validate_test_database_url(database_url, allow_external="1") == database_url


@pytest.mark.parametrize("allow_external", [None, "", "0", "false", "true", "yes", " 1"])
def test_false_or_invalid_opt_in_does_not_bypass_guard(
    allow_external: str | None,
) -> None:
    with pytest.raises(UnsafeTestDatabaseError):
        validate_test_database_url(
            "postgresql+psycopg://via:secret@example.invalid/postgres",
            allow_external=allow_external,
        )


def test_rejection_does_not_print_or_expose_database_secret(
    capsys: pytest.CaptureFixture[str],
) -> None:
    password = "never-print-this-password"
    database_url = f"postgresql+psycopg://via:{password}@example.invalid/postgres"

    with pytest.raises(UnsafeTestDatabaseError) as raised:
        validate_test_database_url(database_url, allow_external="0")

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert password not in str(raised.value)
    assert database_url not in str(raised.value)


def test_external_test_opt_in_does_not_change_application_database_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    application_url = "postgresql+psycopg://via:app-secret@example.invalid/via"
    monkeypatch.setenv("VIA_DATABASE_URL", application_url)
    monkeypatch.setenv("VIA_ALLOW_EXTERNAL_TEST_DATABASE", "1")

    settings = Settings.from_env()

    assert settings.database_url == application_url
