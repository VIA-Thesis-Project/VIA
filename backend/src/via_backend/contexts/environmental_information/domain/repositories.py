"""Repository abstractions for Environmental Information aggregates."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from .models import Dataset, DatasetVersion


class DatasetRepository(Protocol):
    def add(self, dataset: Dataset) -> None: ...

    def get(self, dataset_id: UUID) -> Dataset | None: ...

    def list_all(self) -> tuple[Dataset, ...]: ...


class DatasetVersionRepository(Protocol):
    def add(self, version: DatasetVersion) -> None: ...

    def get(self, version_id: UUID) -> DatasetVersion | None: ...

    def list_for_dataset(self, dataset_id: UUID) -> tuple[DatasetVersion, ...]: ...
