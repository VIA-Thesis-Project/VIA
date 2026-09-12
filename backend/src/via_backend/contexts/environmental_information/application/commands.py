"""Commands expressing Environmental Information use-case intent."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateDataset:
    name: str
    source: str
    variable: str
    unit: str


@dataclass(frozen=True, slots=True)
class CreateDatasetVersion:
    dataset_id: UUID
    version_identifier: str
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
    checksum: str
    storage_reference: str
