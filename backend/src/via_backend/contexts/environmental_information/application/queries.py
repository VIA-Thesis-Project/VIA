"""Queries supported by the Environmental Information service."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
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


@dataclass(frozen=True, slots=True)
class CheckDatasetVersionCoverage:
    dataset_id: UUID
    version_id: UUID
    geometry: Mapping[str, Any]
    geometry_crs: str
