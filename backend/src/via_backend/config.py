"""Environment-backed configuration for the VIA application host."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal, cast

FarmRepositoryBackend = Literal["memory", "postgresql"]


@dataclass(frozen=True, slots=True)
class Settings:
    """Settings needed by the current backend composition root."""

    farm_management_repository: FarmRepositoryBackend = "memory"
    database_url: str | None = None

    def __post_init__(self) -> None:
        if self.farm_management_repository not in {"memory", "postgresql"}:
            raise ValueError(
                "VIA_FARM_MANAGEMENT_REPOSITORY must be 'memory' or 'postgresql'."
            )
        if self.farm_management_repository == "postgresql" and not self.database_url:
            raise ValueError(
                "VIA_DATABASE_URL is required when PostgreSQL persistence is selected."
            )

    @classmethod
    def from_env(cls) -> Settings:
        database_url = os.getenv("VIA_DATABASE_URL") or None
        configured_backend = os.getenv("VIA_FARM_MANAGEMENT_REPOSITORY")
        backend = configured_backend or ("postgresql" if database_url else "memory")
        return cls(
            farm_management_repository=cast(FarmRepositoryBackend, backend.casefold()),
            database_url=database_url,
        )
