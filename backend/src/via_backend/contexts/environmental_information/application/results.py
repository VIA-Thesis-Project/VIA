"""Transport-neutral results returned by Environmental Information use cases."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from ..domain.coverage import CoverageClassification
from ..domain.models import Dataset, DatasetVersion


@dataclass(frozen=True, slots=True)
class DatasetResult:
    id: UUID
    name: str
    source: str
    variable: str
    unit: str
    created_at: datetime

    @classmethod
    def from_domain(cls, dataset: Dataset) -> DatasetResult:
        return cls(
            id=dataset.id,
            name=dataset.name,
            source=dataset.source,
            variable=dataset.variable,
            unit=dataset.unit,
            created_at=dataset.created_at,
        )


@dataclass(frozen=True, slots=True)
class SpatialResolutionResult:
    x: float
    y: float
    unit: str


@dataclass(frozen=True, slots=True)
class SpatialExtentResult:
    west: float
    south: float
    east: float
    north: float


@dataclass(frozen=True, slots=True)
class DatasetVersionResult:
    id: UUID
    dataset_id: UUID
    version_identifier: str
    crs: str
    resolution: SpatialResolutionResult
    extent: SpatialExtentResult
    valid_from: date | None
    valid_to: date | None
    scenario: str | None
    checksum: str
    storage_reference: str
    registered_at: datetime

    @classmethod
    def from_domain(cls, version: DatasetVersion) -> DatasetVersionResult:
        return cls(
            id=version.id,
            dataset_id=version.dataset_id,
            version_identifier=version.version_identifier,
            crs=version.crs,
            resolution=SpatialResolutionResult(
                x=version.resolution.x,
                y=version.resolution.y,
                unit=version.resolution.unit,
            ),
            extent=SpatialExtentResult(
                west=version.extent.west,
                south=version.extent.south,
                east=version.extent.east,
                north=version.extent.north,
            ),
            valid_from=version.valid_from,
            valid_to=version.valid_to,
            scenario=version.scenario,
            checksum=version.checksum,
            storage_reference=version.storage_reference,
            registered_at=version.registered_at,
        )


@dataclass(frozen=True, slots=True)
class DatasetVersionCoverageResult:
    """Extent-based coverage and structural compatibility result."""

    dataset_id: UUID
    dataset_version_id: UUID
    compatible: bool
    coverage: CoverageClassification
    parcel_area_m2: float | None
    covered_area_m2: float | None
    coverage_percentage: float | None
    dataset_crs: str
    parcel_crs: str
    comparison_crs: str | None
    area_method: str | None
    transformations: tuple[str, ...]
    warnings: tuple[str, ...]
    reasons: tuple[str, ...]
