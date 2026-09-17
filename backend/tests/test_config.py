"""Tests for environment-driven application composition settings."""

from collections.abc import Callable
from pathlib import Path

import pytest

from via_backend.config import Settings, WorkerSettings


def test_database_url_selects_postgresql_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("VIA_FARM_MANAGEMENT_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_AGROCLIMATIC_EVALUATION_REPOSITORY", raising=False)
    monkeypatch.setenv("VIA_DATABASE_URL", "postgresql+psycopg://example.invalid/via")

    settings = Settings.from_env()

    assert settings.farm_management_repository == "postgresql"
    assert settings.environmental_information_repository == "postgresql"
    assert settings.agroclimatic_evaluation_repository == "postgresql"


def test_postgresql_selection_requires_database_url() -> None:
    with pytest.raises(ValueError, match="VIA_DATABASE_URL"):
        Settings(farm_management_repository="postgresql")


def test_environmental_postgresql_selection_requires_database_url() -> None:
    with pytest.raises(ValueError, match="VIA_DATABASE_URL"):
        Settings(environmental_information_repository="postgresql")


def test_evaluation_postgresql_selection_requires_database_url() -> None:
    with pytest.raises(ValueError, match="VIA_DATABASE_URL"):
        Settings(agroclimatic_evaluation_repository="postgresql")


@pytest.mark.parametrize(
    "settings_factory",
    [
        lambda: WorkerSettings(
            database_url="postgresql+psycopg://example.invalid/via",
            poll_interval_seconds=0.0,
        ),
        lambda: WorkerSettings(
            database_url="postgresql+psycopg://example.invalid/via",
            poll_interval_seconds=True,
        ),
        lambda: WorkerSettings(
            database_url="postgresql+psycopg://example.invalid/via",
            poll_interval_seconds=float("nan"),
        ),
        lambda: WorkerSettings(
            database_url="postgresql+psycopg://example.invalid/via",
            poll_interval_seconds=float("inf"),
        ),
        lambda: WorkerSettings(
            database_url="postgresql+psycopg://example.invalid/via",
            batch_size=0,
        ),
        lambda: WorkerSettings(
            database_url="postgresql+psycopg://example.invalid/via",
            batch_size=True,
        ),
        lambda: WorkerSettings(
            database_url="postgresql+psycopg://example.invalid/via",
            cropsuite_max_workers=0,
        ),
    ],
)
def test_worker_settings_require_positive_polling_values(
    settings_factory: Callable[[], WorkerSettings],
) -> None:
    with pytest.raises(ValueError):
        settings_factory()


def test_worker_settings_reuse_scientific_smoke_environment_names(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VIA_DATABASE_URL", "postgresql+psycopg://example.invalid/via")
    monkeypatch.setenv("VIA_CROPSUITE_ROOT", "C:/science/CropSuiteLite")
    monkeypatch.setenv("VIA_CROPSUITE_PYTHON", "C:/science/python.exe")
    monkeypatch.setenv("VIA_CROPSUITE_WORKSPACE", "C:/via/work")
    monkeypatch.setenv("VIA_CROPSUITE_INPUT_BINDINGS", "C:/via/cropsuite-input-bindings.json")
    monkeypatch.setenv("VIA_WORKER_POLL_INTERVAL_SECONDS", "2.5")
    monkeypatch.setenv("VIA_WORKER_BATCH_SIZE", "3")
    monkeypatch.setenv("VIA_ARTIFACTS_ROOT", "C:/via/artifacts")

    settings = WorkerSettings.from_env()

    assert settings.poll_interval_seconds == 2.5
    assert settings.batch_size == 3
    assert settings.require_scientific_execution() == (
        Path("C:/science/CropSuiteLite"),
        Path("C:/science/python.exe"),
        Path("C:/via/work"),
        Path("C:/via/artifacts"),
        Path("C:/via/cropsuite-input-bindings.json"),
    )


def test_worker_run_requires_scientific_paths() -> None:
    settings = WorkerSettings(database_url="postgresql+psycopg://example.invalid/via")

    with pytest.raises(ValueError, match="VIA_CROPSUITE_ROOT"):
        settings.require_scientific_execution()

def test_worker_run_requires_durable_artifact_root() -> None:
    settings = WorkerSettings(
        database_url="postgresql+psycopg://example.invalid/via",
        cropsuite_root=Path("C:/science/CropSuiteLite"),
        cropsuite_python=Path("C:/science/python.exe"),
        cropsuite_workspace=Path("C:/via/work"),
    )

    with pytest.raises(ValueError, match="VIA_ARTIFACTS_ROOT"):
        settings.require_scientific_execution()


def test_worker_run_requires_scientific_input_bindings() -> None:
    settings = WorkerSettings(
        database_url="postgresql+psycopg://example.invalid/via",
        cropsuite_root=Path("C:/science/CropSuiteLite"),
        cropsuite_python=Path("C:/science/python.exe"),
        cropsuite_workspace=Path("C:/via/work"),
        artifacts_root=Path("C:/via/artifacts"),
    )

    with pytest.raises(ValueError, match="VIA_CROPSUITE_INPUT_BINDINGS"):
        settings.require_scientific_execution()
