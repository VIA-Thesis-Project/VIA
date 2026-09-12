"""Tests for environment-driven application composition settings."""

import pytest

from via_backend.config import Settings


def test_database_url_selects_postgresql_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("VIA_FARM_MANAGEMENT_REPOSITORY", raising=False)
    monkeypatch.setenv("VIA_DATABASE_URL", "postgresql+psycopg://example.invalid/via")

    settings = Settings.from_env()

    assert settings.farm_management_repository == "postgresql"


def test_postgresql_selection_requires_database_url() -> None:
    with pytest.raises(ValueError, match="VIA_DATABASE_URL"):
        Settings(farm_management_repository="postgresql")
