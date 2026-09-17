"""Focused tests for the explicit VIA release migration host."""

from __future__ import annotations

from pathlib import Path

import pytest

import via_backend.api as api_host
import via_backend.migrate as migration_host
import via_backend.worker as worker_host


def _configure_valid_production(monkeypatch: pytest.MonkeyPatch, config_path: Path) -> None:
    monkeypatch.setenv("VIA_DATABASE_URL", "postgresql+psycopg://via:secret@example.invalid/via")
    monkeypatch.delenv("VIA_FARM_MANAGEMENT_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_AGROCLIMATIC_EVALUATION_REPOSITORY", raising=False)
    monkeypatch.setenv("VIA_ALEMBIC_CONFIG", str(config_path))


def test_cli_exposes_only_explicit_upgrade(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as help_exit:
        migration_host.main(["--help"])

    assert help_exit.value.code == 0
    help_text = capsys.readouterr().out
    assert "upgrade" in help_text
    assert "downgrade" not in help_text


def test_missing_database_url_is_rejected_before_alembic(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("VIA_DATABASE_URL", raising=False)
    calls: list[str] = []
    monkeypatch.setattr(
        migration_host.command,
        "upgrade",
        lambda *_args: calls.append("alembic"),
    )

    with pytest.raises(ValueError, match="VIA_DATABASE_URL"):
        migration_host.main(["upgrade"])

    assert calls == []


def test_source_alembic_config_resolution_does_not_depend_on_cwd(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv("VIA_ALEMBIC_CONFIG", raising=False)
    monkeypatch.chdir(tmp_path)

    resolved = migration_host.resolve_alembic_config()

    assert resolved == (Path(migration_host.__file__).resolve().parents[2] / "alembic.ini")


def test_invalid_production_repository_configuration_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VIA_DATABASE_URL", "postgresql+psycopg://via:secret@example.invalid/via")
    monkeypatch.setenv("VIA_FARM_MANAGEMENT_REPOSITORY", "memory")
    calls: list[str] = []
    monkeypatch.setattr(
        migration_host.command,
        "upgrade",
        lambda *_args: calls.append("alembic"),
    )

    with pytest.raises(ValueError, match="VIA_FARM_MANAGEMENT_REPOSITORY"):
        migration_host.main(["upgrade"])

    assert calls == []


def test_non_postgresql_database_url_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VIA_DATABASE_URL", "sqlite:///via.db")
    monkeypatch.delenv("VIA_FARM_MANAGEMENT_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_AGROCLIMATIC_EVALUATION_REPOSITORY", raising=False)

    with pytest.raises(ValueError, match="requires PostgreSQL persistence"):
        migration_host.main(["upgrade"])


@pytest.mark.parametrize("configured_path", ["", "missing/alembic.ini"])
def test_missing_or_invalid_alembic_config_path_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    configured_path: str,
) -> None:
    path = configured_path
    if configured_path:
        path = str(tmp_path / configured_path)
    _configure_valid_production(monkeypatch, tmp_path / "unused.ini")
    monkeypatch.setenv("VIA_ALEMBIC_CONFIG", path)

    with pytest.raises(ValueError, match="VIA_ALEMBIC_CONFIG|does not exist"):
        migration_host.main(["upgrade"])


def test_alembic_is_invoked_with_absolute_config_and_head(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "alembic.ini"
    config_path.write_text("[alembic]\nscript_location = migrations\n", encoding="utf-8")
    _configure_valid_production(monkeypatch, config_path)
    calls: list[tuple[str | None, str]] = []

    def record_upgrade(config: object, revision: str) -> None:
        calls.append((getattr(config, "config_file_name", None), revision))

    monkeypatch.setattr(migration_host.command, "upgrade", record_upgrade)

    migration_host.main(["upgrade"])

    assert calls == [(str(config_path.resolve()), "head")]


def test_alembic_failure_propagates(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "alembic.ini"
    config_path.write_text("[alembic]\nscript_location = migrations\n", encoding="utf-8")
    _configure_valid_production(monkeypatch, config_path)

    def fail_upgrade(*_args: object) -> None:
        raise RuntimeError("migration failed")

    monkeypatch.setattr(migration_host.command, "upgrade", fail_upgrade)

    with pytest.raises(RuntimeError, match="migration failed"):
        migration_host.main(["upgrade"])


def test_arbitrary_revision_cannot_be_supplied() -> None:
    with pytest.raises(SystemExit) as exit_info:
        migration_host.main(["upgrade", "20260916_0010"])

    assert exit_info.value.code != 0


def test_downgrade_command_does_not_exist() -> None:
    with pytest.raises(SystemExit) as exit_info:
        migration_host.main(["downgrade"])

    assert exit_info.value.code != 0


def test_upgrade_does_not_start_api_or_worker(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "alembic.ini"
    config_path.write_text("[alembic]\nscript_location = migrations\n", encoding="utf-8")
    _configure_valid_production(monkeypatch, config_path)

    def unexpected_start(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("migration host must not start API or worker processes")

    monkeypatch.setattr(api_host, "main", unexpected_start)
    monkeypatch.setattr(worker_host, "main", unexpected_start)
    monkeypatch.setattr(migration_host.command, "upgrade", lambda *_args: None)

    migration_host.main(["upgrade"])
