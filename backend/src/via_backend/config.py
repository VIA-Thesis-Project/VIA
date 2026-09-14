"""Environment-backed configuration for the VIA application host."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

RepositoryBackend = Literal["memory", "postgresql"]


@dataclass(frozen=True, slots=True)
class Settings:
    """Settings needed by the current backend composition root."""

    farm_management_repository: RepositoryBackend = "memory"
    environmental_information_repository: RepositoryBackend = "memory"
    agroclimatic_evaluation_repository: RepositoryBackend = "memory"
    database_url: str | None = None

    def __post_init__(self) -> None:
        selections = {
            "VIA_FARM_MANAGEMENT_REPOSITORY": self.farm_management_repository,
            "VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY": (self.environmental_information_repository),
            "VIA_AGROCLIMATIC_EVALUATION_REPOSITORY": self.agroclimatic_evaluation_repository,
        }
        for setting_name, selection in selections.items():
            if selection not in {"memory", "postgresql"}:
                raise ValueError(f"{setting_name} must be 'memory' or 'postgresql'.")
        if "postgresql" in selections.values() and not self.database_url:
            raise ValueError(
                "VIA_DATABASE_URL is required when PostgreSQL persistence is selected."
            )

    @classmethod
    def from_env(cls) -> Settings:
        database_url = os.getenv("VIA_DATABASE_URL") or None
        default_backend = "postgresql" if database_url else "memory"
        farm_backend = os.getenv("VIA_FARM_MANAGEMENT_REPOSITORY") or default_backend
        environmental_backend = (
            os.getenv("VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY") or default_backend
        )
        evaluation_backend = os.getenv("VIA_AGROCLIMATIC_EVALUATION_REPOSITORY") or default_backend
        return cls(
            farm_management_repository=cast(RepositoryBackend, farm_backend.casefold()),
            environmental_information_repository=cast(
                RepositoryBackend, environmental_backend.casefold()
            ),
            agroclimatic_evaluation_repository=cast(
                RepositoryBackend, evaluation_backend.casefold()
            ),
            database_url=database_url,
        )


@dataclass(frozen=True, slots=True)
class WorkerSettings:
    """Settings for the PostgreSQL polling worker process."""

    database_url: str
    cropsuite_root: Path | None = None
    cropsuite_python: Path | None = None
    cropsuite_workspace: Path | None = None
    cropsuite_source_config: Path | None = None
    cropsuite_catalog: Path | None = None
    poll_interval_seconds: float = 5.0
    batch_size: int = 1
    cropsuite_max_workers: int = 2

    def __post_init__(self) -> None:
        if not self.database_url:
            raise ValueError("VIA_DATABASE_URL is required for the worker.")
        if self.poll_interval_seconds <= 0:
            raise ValueError("VIA_WORKER_POLL_INTERVAL_SECONDS must be greater than zero.")
        if isinstance(self.batch_size, bool) or self.batch_size < 1:
            raise ValueError("VIA_WORKER_BATCH_SIZE must be a positive integer.")
        if isinstance(self.cropsuite_max_workers, bool) or self.cropsuite_max_workers < 1:
            raise ValueError("VIA_CROPSUITE_MAX_WORKERS must be a positive integer.")

    def require_scientific_execution(self) -> tuple[Path, Path, Path]:
        missing = [
            name
            for name, value in (
                ("VIA_CROPSUITE_ROOT", self.cropsuite_root),
                ("VIA_CROPSUITE_PYTHON", self.cropsuite_python),
                ("VIA_CROPSUITE_WORKSPACE", self.cropsuite_workspace),
            )
            if value is None
        ]
        if missing:
            raise ValueError("Worker scientific execution requires " + ", ".join(missing) + ".")
        assert self.cropsuite_root is not None
        assert self.cropsuite_python is not None
        assert self.cropsuite_workspace is not None
        return (
            self.cropsuite_root,
            self.cropsuite_python,
            self.cropsuite_workspace,
        )

    @classmethod
    def from_env(cls) -> WorkerSettings:
        return cls(
            database_url=os.getenv("VIA_DATABASE_URL") or "",
            cropsuite_root=_optional_path("VIA_CROPSUITE_ROOT"),
            cropsuite_python=_optional_path("VIA_CROPSUITE_PYTHON"),
            cropsuite_workspace=_optional_path("VIA_CROPSUITE_WORKSPACE"),
            cropsuite_source_config=_optional_path("VIA_CROPSUITE_SOURCE_CONFIG"),
            cropsuite_catalog=_optional_path("VIA_CROPSUITE_CATALOG"),
            poll_interval_seconds=_environment_float("VIA_WORKER_POLL_INTERVAL_SECONDS", 5.0),
            batch_size=_environment_integer("VIA_WORKER_BATCH_SIZE", 1),
            cropsuite_max_workers=_environment_integer("VIA_CROPSUITE_MAX_WORKERS", 2),
        )


def _optional_path(name: str) -> Path | None:
    value = os.getenv(name)
    return Path(value) if value else None


def _environment_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError as error:
        raise ValueError(f"{name} must be numeric.") from error


def _environment_integer(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError as error:
        raise ValueError(f"{name} must be an integer.") from error
