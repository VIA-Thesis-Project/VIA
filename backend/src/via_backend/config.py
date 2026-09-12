"""Environment-backed configuration for the VIA application host."""

from __future__ import annotations

import os
from dataclasses import dataclass
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
            "VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY": (
                self.environmental_information_repository
            ),
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
        evaluation_backend = (
            os.getenv("VIA_AGROCLIMATIC_EVALUATION_REPOSITORY") or default_backend
        )
        return cls(
            farm_management_repository=cast(
                RepositoryBackend, farm_backend.casefold()
            ),
            environmental_information_repository=cast(
                RepositoryBackend, environmental_backend.casefold()
            ),
            agroclimatic_evaluation_repository=cast(
                RepositoryBackend, evaluation_backend.casefold()
            ),
            database_url=database_url,
        )
