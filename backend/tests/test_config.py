"""Tests for environment-driven application composition settings."""

from collections.abc import Callable
from pathlib import Path

import pytest

import via_backend.app as app_module
from via_backend.config import Settings, WorkerSettings


def test_database_url_selects_postgresql_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("VIA_FARM_MANAGEMENT_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_AGROCLIMATIC_EVALUATION_REPOSITORY", raising=False)
    monkeypatch.setenv("VIA_DATABASE_URL", "postgresql+psycopg://example.invalid/via")

    settings = Settings.from_env()

    assert settings.farm_management_repository == "postgresql"
    assert settings.environmental_information_repository == "postgresql"
    assert settings.agroclimatic_evaluation_repository == "postgresql"


def test_development_settings_can_fall_back_to_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("VIA_DATABASE_URL", raising=False)
    monkeypatch.delenv("VIA_FARM_MANAGEMENT_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_AGROCLIMATIC_EVALUATION_REPOSITORY", raising=False)

    settings = Settings.from_env()

    assert settings.farm_management_repository == "memory"
    assert settings.environmental_information_repository == "memory"
    assert settings.agroclimatic_evaluation_repository == "memory"


def test_production_settings_accept_postgresql_repositories_and_database_url() -> None:
    settings = Settings(
        farm_management_repository="postgresql",
        environmental_information_repository="postgresql",
        agroclimatic_evaluation_repository="postgresql",
        database_url="postgresql+psycopg://example.invalid/via",
    )

    assert settings.require_production() is settings


@pytest.mark.parametrize(
    ("settings", "environment_name"),
    [
        (
            Settings(
                farm_management_repository="memory",
                environmental_information_repository="postgresql",
                agroclimatic_evaluation_repository="postgresql",
                database_url="postgresql+psycopg://example.invalid/via",
            ),
            "VIA_FARM_MANAGEMENT_REPOSITORY",
        ),
        (
            Settings(
                farm_management_repository="postgresql",
                environmental_information_repository="memory",
                agroclimatic_evaluation_repository="postgresql",
                database_url="postgresql+psycopg://example.invalid/via",
            ),
            "VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY",
        ),
        (
            Settings(
                farm_management_repository="postgresql",
                environmental_information_repository="postgresql",
                agroclimatic_evaluation_repository="memory",
                database_url="postgresql+psycopg://example.invalid/via",
            ),
            "VIA_AGROCLIMATIC_EVALUATION_REPOSITORY",
        ),
    ],
)
def test_production_settings_reject_memory_repository(
    settings: Settings,
    environment_name: str,
) -> None:
    with pytest.raises(ValueError, match=environment_name):
        settings.require_production()


def test_create_production_app_validates_before_composition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = Settings()
    validation_calls: list[Settings] = []
    original_require_production = Settings.require_production

    monkeypatch.setattr(Settings, "from_env", lambda: settings)

    def record_validation(candidate: Settings) -> Settings:
        validation_calls.append(candidate)
        return original_require_production(candidate)

    monkeypatch.setattr(Settings, "require_production", record_validation)

    def fail_if_composed(_: Settings | None = None) -> None:
        raise AssertionError("create_app must not run for invalid production settings")

    monkeypatch.setattr(app_module, "create_app", fail_if_composed)

    with pytest.raises(ValueError, match="VIA_FARM_MANAGEMENT_REPOSITORY"):
        app_module.create_production_app()

    assert validation_calls == [settings]


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


def _scientific_worker_settings(
    tmp_path: Path,
    *,
    cropsuite_root: Path | None = None,
    workspace: Path | None = None,
    artifacts_root: Path | None = None,
) -> WorkerSettings:
    return WorkerSettings(
        database_url="postgresql+psycopg://example.invalid/via",
        cropsuite_root=cropsuite_root or tmp_path / "engine",
        cropsuite_python=tmp_path / "python",
        cropsuite_workspace=workspace or tmp_path / "workspace",
        artifacts_root=artifacts_root or tmp_path / "artifacts",
        cropsuite_input_bindings=tmp_path / "config" / "input-bindings.json",
    )


def test_worker_scientific_paths_accept_separate_runtime_roots(tmp_path: Path) -> None:
    settings = _scientific_worker_settings(tmp_path)

    assert settings.require_scientific_execution() == (
        tmp_path / "engine",
        tmp_path / "python",
        tmp_path / "workspace",
        tmp_path / "artifacts",
        tmp_path / "config" / "input-bindings.json",
    )
    assert settings.cropsuite_source_config is None
    assert settings.cropsuite_catalog is None


@pytest.mark.parametrize(
    ("workspace_relative", "artifacts_relative", "message"),
    [
        ("engine", "artifacts", "VIA_CROPSUITE_WORKSPACE"),
        ("engine/work", "artifacts", "VIA_CROPSUITE_WORKSPACE"),
        ("workspace", "engine", "VIA_ARTIFACTS_ROOT"),
        ("workspace", "engine/artifacts", "VIA_ARTIFACTS_ROOT"),
        ("workspace", "workspace", "distinct"),
        ("workspace", "workspace/artifacts", "inside VIA_CROPSUITE_WORKSPACE"),
    ],
)
def test_worker_scientific_paths_reject_unsafe_topology(
    tmp_path: Path,
    workspace_relative: str,
    artifacts_relative: str,
    message: str,
) -> None:
    settings = _scientific_worker_settings(
        tmp_path,
        workspace=tmp_path / workspace_relative,
        artifacts_root=tmp_path / artifacts_relative,
    )

    with pytest.raises(ValueError, match=message):
        settings.require_scientific_execution()
