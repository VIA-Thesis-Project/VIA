"""Coverage semantics and parcel-shaped collaboration values."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Any, Literal, TypeAlias, cast

from .errors import DomainValidationError
from .spatial import validate_crs

Position: TypeAlias = tuple[float, float]
LinearRing: TypeAlias = tuple[Position, ...]
PolygonCoordinates: TypeAlias = tuple[LinearRing, ...]
MultiPolygonCoordinates: TypeAlias = tuple[PolygonCoordinates, ...]
GeometryCoordinates: TypeAlias = PolygonCoordinates | MultiPolygonCoordinates
GeometryType: TypeAlias = Literal["Polygon", "MultiPolygon"]


class CoverageClassification(StrEnum):
    """Extent-based relationship between a dataset version and a parcel."""

    FULL = "full"
    PARTIAL = "partial"
    NONE = "none"
    NOT_ASSESSED = "not_assessed"


@dataclass(frozen=True, slots=True)
class CoverageGeometry:
    """Transport-neutral geometry supplied at the collaboration boundary."""

    type: GeometryType
    coordinates: GeometryCoordinates
    crs: str

    @classmethod
    def from_geojson(
        cls, value: Mapping[str, Any], *, crs: str
    ) -> CoverageGeometry:
        validate_crs(crs)
        geometry_type = value.get("type")
        if geometry_type not in {"Polygon", "MultiPolygon"}:
            raise DomainValidationError(
                "Coverage geometry must be a GeoJSON Polygon or MultiPolygon."
            )

        raw_coordinates = value.get("coordinates")
        if geometry_type == "Polygon":
            coordinates: GeometryCoordinates = _parse_polygon(raw_coordinates, crs)
        else:
            coordinates = _parse_multi_polygon(raw_coordinates, crs)
        return cls(
            type=cast(GeometryType, geometry_type),
            coordinates=coordinates,
            crs=crs,
        )

    def to_geojson(self) -> dict[str, Any]:
        return {"type": self.type, "coordinates": _to_lists(self.coordinates)}


@dataclass(frozen=True, slots=True)
class CoverageMeasurement:
    """Successful, CRS-aware area measurement returned by a spatial port."""

    parcel_area_m2: float
    covered_area_m2: float
    fully_covered: bool
    comparison_crs: str
    area_method: str
    transformations: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        validate_crs(self.comparison_crs)
        if not isfinite(self.parcel_area_m2) or self.parcel_area_m2 <= 0:
            raise DomainValidationError("Parcel area must be finite and positive.")
        if not isfinite(self.covered_area_m2) or self.covered_area_m2 < 0:
            raise DomainValidationError(
                "Covered area must be finite and non-negative."
            )
        tolerance = max(1e-6, self.parcel_area_m2 * 1e-9)
        if self.covered_area_m2 > self.parcel_area_m2 + tolerance:
            raise DomainValidationError("Covered area cannot exceed parcel area.")
        if not self.area_method.strip():
            raise DomainValidationError("Area method must be explicit.")

    @property
    def classification(self) -> CoverageClassification:
        if self.fully_covered:
            return CoverageClassification.FULL
        if self.covered_area_m2 > 0:
            return CoverageClassification.PARTIAL
        return CoverageClassification.NONE

    @property
    def coverage_percentage(self) -> float:
        if self.fully_covered:
            return 100.0
        percentage = 100.0 * self.covered_area_m2 / self.parcel_area_m2
        return min(100.0, max(0.0, percentage))


@dataclass(frozen=True, slots=True)
class CoverageCompatibilityFailure:
    """Structural metadata prevented a meaningful spatial measurement."""

    reasons: tuple[str, ...]
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.reasons or any(not reason.strip() for reason in self.reasons):
            raise DomainValidationError(
                "An incompatible coverage result requires at least one reason."
            )


def _parse_multi_polygon(value: Any, crs: str) -> MultiPolygonCoordinates:
    polygons = _require_sequence(value, "MultiPolygon coordinates")
    if not polygons:
        raise DomainValidationError("A MultiPolygon must contain at least one polygon.")
    return tuple(_parse_polygon(polygon, crs) for polygon in polygons)


def _parse_polygon(value: Any, crs: str) -> PolygonCoordinates:
    rings = _require_sequence(value, "Polygon coordinates")
    if not rings:
        raise DomainValidationError("A Polygon must contain at least one linear ring.")
    return tuple(_parse_ring(ring, crs) for ring in rings)


def _parse_ring(value: Any, crs: str) -> LinearRing:
    raw_positions = _require_sequence(value, "Linear ring")
    positions = tuple(_parse_position(position, crs) for position in raw_positions)
    if len(positions) < 4:
        raise DomainValidationError("A linear ring must contain at least four positions.")
    if positions[0] != positions[-1]:
        raise DomainValidationError("A linear ring must be closed.")
    return positions


def _parse_position(value: Any, crs: str) -> Position:
    numbers = _require_sequence(value, "Position")
    if len(numbers) != 2:
        raise DomainValidationError("A position must contain exactly two coordinates.")
    if any(
        isinstance(number, bool) or not isinstance(number, (int, float))
        for number in numbers
    ):
        raise DomainValidationError("Position coordinates must be finite numbers.")
    x, y = (float(number) for number in numbers)
    if not isfinite(x) or not isfinite(y):
        raise DomainValidationError("Position coordinates must be finite numbers.")
    if crs == "EPSG:4326" and (not -180 <= x <= 180 or not -90 <= y <= 90):
        raise DomainValidationError(
            "EPSG:4326 positions must use valid longitude and latitude ranges."
        )
    return x, y


def _require_sequence(value: Any, label: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise DomainValidationError(f"{label} must be an array.")
    return value


def _to_lists(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_to_lists(item) for item in value]
    return value
