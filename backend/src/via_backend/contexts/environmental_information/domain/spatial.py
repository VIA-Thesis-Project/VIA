"""Framework-neutral spatial metadata value objects."""

from __future__ import annotations

import re
from dataclasses import dataclass
from math import isfinite

from .errors import DomainValidationError

_EPSG_PATTERN = re.compile(r"EPSG:([1-9][0-9]*)")


@dataclass(frozen=True, slots=True)
class SpatialResolution:
    """Positive horizontal and vertical source-cell resolution."""

    x: float
    y: float
    unit: str

    def __post_init__(self) -> None:
        if not isfinite(self.x) or not isfinite(self.y) or self.x <= 0 or self.y <= 0:
            raise DomainValidationError(
                "Spatial resolution values must be finite and positive."
            )
        _validate_text(self.unit, "Spatial resolution unit", 32)


@dataclass(frozen=True, slots=True)
class SpatialExtent:
    """A rectangular extent expressed in the dataset version's CRS."""

    west: float
    south: float
    east: float
    north: float

    def __post_init__(self) -> None:
        coordinates = (self.west, self.south, self.east, self.north)
        if any(not isfinite(value) for value in coordinates):
            raise DomainValidationError("Spatial extent coordinates must be finite.")
        if self.west >= self.east or self.south >= self.north:
            raise DomainValidationError(
                "Spatial extent must have west < east and south < north."
            )

    def validate_for(self, crs: str) -> None:
        if crs == "EPSG:4326" and (
            self.west < -180
            or self.east > 180
            or self.south < -90
            or self.north > 90
        ):
            raise DomainValidationError(
                "EPSG:4326 extent coordinates must be valid longitude/latitude values."
            )


def validate_crs(value: str) -> int:
    """Validate the first-slice CRS contract and return its EPSG code."""
    _validate_text(value, "CRS", 32)
    match = _EPSG_PATTERN.fullmatch(value)
    if match is None:
        raise DomainValidationError("CRS must use the form EPSG:<positive integer>.")
    return int(match.group(1))


def _validate_text(value: str, label: str, maximum: int) -> None:
    if not value or value != value.strip():
        raise DomainValidationError(f"{label} must be non-empty and trimmed.")
    if len(value) > maximum:
        raise DomainValidationError(f"{label} must be at most {maximum} characters.")
