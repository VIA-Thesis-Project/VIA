"""Immutable parcel snapshot values owned by Agroclimatic Evaluation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from math import isfinite
from typing import Any, Literal, TypeAlias, cast
from uuid import UUID

from .errors import DomainValidationError

Position: TypeAlias = tuple[float, float]
LinearRing: TypeAlias = tuple[Position, ...]
PolygonCoordinates: TypeAlias = tuple[LinearRing, ...]
MultiPolygonCoordinates: TypeAlias = tuple[PolygonCoordinates, ...]
GeometryCoordinates: TypeAlias = PolygonCoordinates | MultiPolygonCoordinates
GeometryType: TypeAlias = Literal["Polygon", "MultiPolygon"]


@dataclass(frozen=True, slots=True)
class SnapshotGeometry:
    """A deeply immutable GeoJSON Polygon or MultiPolygon."""

    type: GeometryType
    coordinates: GeometryCoordinates

    def __post_init__(self) -> None:
        if self.type == "Polygon":
            coordinates: GeometryCoordinates = _parse_polygon(self.coordinates)
        elif self.type == "MultiPolygon":
            coordinates = _parse_multi_polygon(self.coordinates)
        else:
            raise DomainValidationError(
                "Snapshot geometry must be a GeoJSON Polygon or MultiPolygon."
            )
        object.__setattr__(self, "coordinates", coordinates)

    @classmethod
    def from_geojson(cls, value: Mapping[str, Any]) -> SnapshotGeometry:
        geometry_type = value.get("type")
        if geometry_type not in {"Polygon", "MultiPolygon"}:
            raise DomainValidationError(
                "Snapshot geometry must be a GeoJSON Polygon or MultiPolygon."
            )

        raw_coordinates = value.get("coordinates")
        if geometry_type == "Polygon":
            coordinates: GeometryCoordinates = _parse_polygon(raw_coordinates)
        else:
            coordinates = _parse_multi_polygon(raw_coordinates)
        return cls(type=cast(GeometryType, geometry_type), coordinates=coordinates)

    def to_geojson(self) -> dict[str, Any]:
        """Return a detached JSON-compatible geometry representation."""
        return {"type": self.type, "coordinates": _to_lists(self.coordinates)}


@dataclass(frozen=True, slots=True)
class ParcelSnapshot:
    """The exact Farm Management parcel state accepted for an evaluation."""

    project_id: UUID
    parcel_id: UUID
    parcel_version: int
    geometry: SnapshotGeometry
    crs: str
    captured_at: datetime

    def __post_init__(self) -> None:
        if isinstance(self.parcel_version, bool) or self.parcel_version < 1:
            raise DomainValidationError("Parcel snapshot version must be positive.")
        if self.crs != "EPSG:4326":
            raise DomainValidationError(
                "Parcel snapshot CRS must be EPSG:4326 in the current Farm Management slice."
            )
        if self.captured_at.tzinfo is None or self.captured_at.utcoffset() is None:
            raise DomainValidationError("Parcel snapshot capture time must be timezone-aware.")


def _parse_multi_polygon(value: Any) -> MultiPolygonCoordinates:
    polygons = _require_sequence(value, "MultiPolygon coordinates")
    if not polygons:
        raise DomainValidationError("A MultiPolygon must contain at least one polygon.")
    return tuple(_parse_polygon(polygon) for polygon in polygons)


def _parse_polygon(value: Any) -> PolygonCoordinates:
    rings = _require_sequence(value, "Polygon coordinates")
    if not rings:
        raise DomainValidationError("A Polygon must contain at least one linear ring.")
    return tuple(_parse_ring(ring) for ring in rings)


def _parse_ring(value: Any) -> LinearRing:
    raw_positions = _require_sequence(value, "Linear ring")
    positions = tuple(_parse_position(position) for position in raw_positions)
    if len(positions) < 4:
        raise DomainValidationError("A linear ring must contain at least four positions.")
    if positions[0] != positions[-1]:
        raise DomainValidationError("A linear ring must be closed.")
    return positions


def _parse_position(value: Any) -> Position:
    numbers = _require_sequence(value, "Position")
    if len(numbers) != 2:
        raise DomainValidationError("A position must contain longitude and latitude.")
    if any(
        isinstance(number, bool) or not isinstance(number, (int, float))
        for number in numbers
    ):
        raise DomainValidationError("Position coordinates must be finite numbers.")

    longitude, latitude = (float(number) for number in numbers)
    if not isfinite(longitude) or not isfinite(latitude):
        raise DomainValidationError("Position coordinates must be finite numbers.")
    if not -180 <= longitude <= 180 or not -90 <= latitude <= 90:
        raise DomainValidationError(
            "Position coordinates must use valid longitude and latitude ranges."
        )
    return longitude, latitude


def _require_sequence(value: Any, label: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise DomainValidationError(f"{label} must be an array.")
    return value


def _to_lists(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_to_lists(item) for item in value]
    return value
