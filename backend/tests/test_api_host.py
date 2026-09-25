"""Focused tests for the provider-neutral production API process host."""

from __future__ import annotations

import importlib
import sys
from collections.abc import Callable
from types import ModuleType

import fastapi
import pytest
from fastapi import FastAPI

import via_backend.api as api_module
from via_backend.api import ApiServerSettings


def _clear_api_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("VIA_API_HOST", raising=False)
    monkeypatch.delenv("VIA_API_PORT", raising=False)
    monkeypatch.delenv("PORT", raising=False)


def _configure_production_persistence(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "VIA_DATABASE_URL", "postgresql+psycopg://via:via@example.invalid/via"
    )
    monkeypatch.delenv("VIA_FARM_MANAGEMENT_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_AGROCLIMATIC_EVALUATION_REPOSITORY", raising=False)


def test_api_server_settings_default_to_container_safe_bind(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_api_environment(monkeypatch)

    settings = ApiServerSettings.from_env()

    assert settings.host == "0.0.0.0"
    assert settings.port == 8000


def test_api_server_settings_accept_environment_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VIA_API_HOST", "10.20.30.40")
    monkeypatch.setenv("VIA_API_PORT", "9123")

    settings = ApiServerSettings.from_env()

    assert settings.host == "10.20.30.40"
    assert settings.port == 9123


def test_api_server_settings_accept_cloud_run_port(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_api_environment(monkeypatch)
    monkeypatch.setenv("PORT", "8080")

    settings = ApiServerSettings.from_env()

    assert settings.port == 8080


def test_api_specific_port_overrides_cloud_run_port(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VIA_API_PORT", "9123")
    monkeypatch.setenv("PORT", "8080")

    assert ApiServerSettings.from_env().port == 9123


@pytest.mark.parametrize("value", ["not-a-port", "8000.5", "true"])
def test_api_server_settings_reject_malformed_environment_port(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
) -> None:
    monkeypatch.setenv("VIA_API_PORT", value)

    with pytest.raises(ValueError, match="VIA_API_PORT must be an integer"):
        ApiServerSettings.from_env()


@pytest.mark.parametrize("port", [0, 65536])
def test_api_server_settings_reject_out_of_range_port(port: int) -> None:
    with pytest.raises(ValueError, match="between 1 and 65535"):
        ApiServerSettings(port=port)


@pytest.mark.parametrize("port", [True, 8000.0])
def test_api_server_settings_reject_non_integer_direct_port(port: object) -> None:
    with pytest.raises(ValueError, match="VIA_API_PORT must be an integer"):
        ApiServerSettings(port=port)  # type: ignore[arg-type]


def test_production_api_command_uses_side_effect_free_uvicorn_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _configure_production_persistence(monkeypatch)
    monkeypatch.setenv("VIA_API_HOST", "0.0.0.0")
    monkeypatch.setenv("VIA_API_PORT", "9001")
    calls: list[tuple[str, dict[str, object]]] = []

    def record_run(target: str, **kwargs: object) -> None:
        calls.append((target, kwargs))

    monkeypatch.setattr(api_module.uvicorn, "run", record_run)

    api_module.main()

    assert calls == [
        (
            "via_backend.app:create_production_app",
            {"factory": True, "host": "0.0.0.0", "port": 9001},
        )
    ]
    assert "reload" not in calls[0][1]


def test_production_api_command_validates_persistence_before_uvicorn(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_api_environment(monkeypatch)
    monkeypatch.delenv("VIA_DATABASE_URL", raising=False)
    monkeypatch.delenv("VIA_FARM_MANAGEMENT_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY", raising=False)
    monkeypatch.delenv("VIA_AGROCLIMATIC_EVALUATION_REPOSITORY", raising=False)

    def fail_if_started(*_: object, **__: object) -> None:
        raise AssertionError("Uvicorn must not start with invalid production persistence")

    monkeypatch.setattr(api_module.uvicorn, "run", fail_if_started)

    with pytest.raises(ValueError, match="Production API requires PostgreSQL persistence"):
        api_module.main()


def test_importing_factory_module_does_not_instantiate_fastapi(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_module = sys.modules.pop("via_backend.app", None)

    def fail_if_instantiated(*_: object, **__: object) -> FastAPI:
        raise AssertionError("via_backend.app instantiated FastAPI during import")

    try:
        with monkeypatch.context() as context:
            context.setattr(fastapi, "FastAPI", fail_if_instantiated)
            imported = importlib.import_module("via_backend.app")
            assert isinstance(imported, ModuleType)
    finally:
        sys.modules.pop("via_backend.app", None)
        if original_module is not None:
            sys.modules["via_backend.app"] = original_module


def test_development_main_app_compatibility_remains_available() -> None:
    main_module = importlib.import_module("via_backend.main")

    assert isinstance(main_module.app, FastAPI)
    assert isinstance(main_module.create_app, Callable)
