"""Stable contracts deliberately published to other bounded contexts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Protocol, runtime_checkable
from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetPublishedDatasetVersion:
    dataset_id: UUID
    dataset_version_id: UUID


@dataclass(frozen=True, slots=True)
class PublishedDatasetVersion:
    dataset_id: UUID
    dataset_name: str
    source: str
    variable: str
    unit: str
    dataset_version_id: UUID
    version_identifier: str
    checksum: str
    storage_reference: str
    crs: str
    resolution_x: float
    resolution_y: float
    resolution_unit: str
    extent_west: float
    extent_south: float
    extent_east: float
    extent_north: float
    valid_from: date | None
    valid_to: date | None
    scenario: str | None
    registered_at: datetime


@runtime_checkable
class PublishedDatasetVersionReader(Protocol):
    """Public cross-context reader for exact immutable dataset versions."""

    def get_published_dataset_version(
        self,
        query: GetPublishedDatasetVersion,
    ) -> PublishedDatasetVersion | None: ...