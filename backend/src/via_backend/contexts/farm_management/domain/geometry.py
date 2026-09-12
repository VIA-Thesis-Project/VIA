"""GeoJSON geometry value objects owned by Farm Management."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any, Literal, Mapping, Sequence, TypeAlias, cast

from .errors import DomainValidationError

Position: TypeAlias = tuple[float, float]
LinearRing: TypeAlias = tuple[Position, ...]
PolygonCoordinates: TypeAlias = tuple[LinearRing, ...]
MultiPolygonCoordinates: TypeAlias = tuple[PolygonCoordinates, ...]
GeometryCoordinates: TypeAlias = PolygonCoordinates | MultiPolygonCoordinates
GeometryType: TypeAlias = Literal["Polygon", "MultiPolygon"]


@dataclass(frozen=True, slots=True)
class ParcelGeometry:
    """An immutable, minimally validated Polygon or MultiPolygon geometry."""

    type: GeometryType
    coordinates: GeometryCoordinates

    @classmethod
    def from_geojson(cls, value: Mapping[str, Any]) -> ParcelGeometry:
        geometry_type = value.get("type")
        if geometry_type not in {"Polygon", "MultiPolygon"}:
            raise DomainValidationError(
                "Parcel geometry must be a GeoJSON Polygon or MultiPolygon."
            )

        raw_coordinates = value.get("coordinates")
        if geometry_type == "Polygon":
            coordinates: GeometryCoordinates = _parse_polygon(raw_coordinates)
        else:
            coordinates = _parse_multi_polygon(raw_coordinates)

        return cls(type=cast(GeometryType, geometry_type), coordinates=coordinates)

    def to_geojson(self) -> dict[str, Any]:
        """Return a JSON-compatible copy of this geometry."""
        return {"type": self.type, "coordinates": _to_lists(self.coordinates)}


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
