"""Environmental Information domain model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from .errors import DomainValidationError
from .spatial import SpatialExtent, SpatialResolution, validate_crs


@dataclass(frozen=True, slots=True)
class Dataset:
    """Stable logical identity for a geoenvironmental dataset."""

    id: UUID
    name: str
    source: str
    variable: str
    unit: str
    created_at: datetime

    def __post_init__(self) -> None:
        _validate_text(self.name, "Dataset name", 120)
        _validate_text(self.source, "Dataset source", 255)
        _validate_text(self.variable, "Environmental variable", 120)
        _validate_text(self.unit, "Environmental variable unit", 64)


@dataclass(frozen=True, slots=True)
class DatasetVersion:
    """Immutable reproducibility metadata for one dataset release."""

    id: UUID
    dataset_id: UUID
    version_identifier: str
    crs: str
    resolution: SpatialResolution
    extent: SpatialExtent
    valid_from: date | None
    valid_to: date | None
    scenario: str | None
    checksum: str
    storage_reference: str
    registered_at: datetime

    def __post_init__(self) -> None:
        validate_crs(self.crs)
        self.extent.validate_for(self.crs)
        _validate_text(self.version_identifier, "Dataset version identifier", 120)
        _validate_text(self.checksum, "Dataset version checksum", 256)
        _validate_text(self.storage_reference, "Storage reference", 1024)
        if self.scenario is not None:
            _validate_text(self.scenario, "Scenario", 120)
        if self.valid_from is not None and self.valid_to is not None:
            if self.valid_from > self.valid_to:
                raise DomainValidationError(
                    "Dataset validity start must not be after its end."
                )


def _validate_text(value: str, label: str, maximum: int) -> None:
    if not value or value != value.strip():
        raise DomainValidationError(f"{label} must be non-empty and trimmed.")
    if len(value) > maximum:
        raise DomainValidationError(f"{label} must be at most {maximum} characters.")
