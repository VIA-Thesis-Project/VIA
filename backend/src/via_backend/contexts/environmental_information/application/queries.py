"""Queries supported by the Environmental Information service."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetDataset:
    dataset_id: UUID


@dataclass(frozen=True, slots=True)
class ListDatasets:
    pass


@dataclass(frozen=True, slots=True)
class GetDatasetVersion:
    dataset_id: UUID
    version_id: UUID


@dataclass(frozen=True, slots=True)
class ListDatasetVersions:
    dataset_id: UUID
