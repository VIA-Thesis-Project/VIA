"""In-memory Environmental Information repository adapters."""

from __future__ import annotations

from threading import RLock
from uuid import UUID

from ..domain.errors import DatasetVersionConflictError
from ..domain.models import Dataset, DatasetVersion


class InMemoryDatasetRepository:
    def __init__(self) -> None:
        self._datasets: dict[UUID, Dataset] = {}
        self._lock = RLock()

    def add(self, dataset: Dataset) -> None:
        with self._lock:
            if dataset.id in self._datasets:
                raise ValueError(f"Dataset {dataset.id} already exists.")
            self._datasets[dataset.id] = dataset

    def get(self, dataset_id: UUID) -> Dataset | None:
        with self._lock:
            return self._datasets.get(dataset_id)

    def list_all(self) -> tuple[Dataset, ...]:
        with self._lock:
            return tuple(
                sorted(self._datasets.values(), key=lambda item: (item.created_at, item.id))
            )


class InMemoryDatasetVersionRepository:
    def __init__(self) -> None:
        self._versions: dict[UUID, DatasetVersion] = {}
        self._lock = RLock()

    def add(self, version: DatasetVersion) -> None:
        with self._lock:
            duplicate = any(
                item.dataset_id == version.dataset_id
                and item.version_identifier == version.version_identifier
                for item in self._versions.values()
            )
            if version.id in self._versions or duplicate:
                raise DatasetVersionConflictError(
                    f"Version {version.version_identifier!r} already exists for "
                    f"dataset {version.dataset_id}."
                )
            self._versions[version.id] = version

    def get(self, version_id: UUID) -> DatasetVersion | None:
        with self._lock:
            return self._versions.get(version_id)

    def list_for_dataset(self, dataset_id: UUID) -> tuple[DatasetVersion, ...]:
        with self._lock:
            return tuple(
                sorted(
                    (
                        version
                        for version in self._versions.values()
                        if version.dataset_id == dataset_id
                    ),
                    key=lambda item: (item.registered_at, item.id),
                )
            )
