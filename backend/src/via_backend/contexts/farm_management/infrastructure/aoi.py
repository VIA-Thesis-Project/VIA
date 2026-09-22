"""Authoritative Huaura area-of-interest validation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from shapely.geometry import MultiPolygon, Polygon, shape
from shapely.geometry.base import BaseGeometry
from shapely.validation import explain_validity

from ..domain.errors import DomainValidationError
from ..domain.geometry import ParcelGeometry


@dataclass(frozen=True, slots=True)
class AreaOfInterestProvenance:
    """Provenance declared next to the authoritative AOI asset."""

    name: str
    source: str
    crs: str
    geometry_type: str


class HuauraAreaOfInterestValidator:
    """Validate parcels against the versioned Huaura provincial boundary."""

    def __init__(self, boundary_path: Path, metadata_path: Path) -> None:
        self._provenance = _load_provenance(metadata_path)
        if self._provenance.crs != "EPSG:4326":
            raise ValueError("The Huaura AOI asset must declare CRS EPSG:4326.")

        self._boundary = _load_boundary(boundary_path)
        if self._boundary.geom_type != self._provenance.geometry_type:
            raise ValueError("The Huaura AOI geometry type does not match its metadata.")
        if self._boundary.is_empty or self._boundary.area <= 0 or not self._boundary.is_valid:
            raise ValueError(
                "The configured Huaura AOI boundary is not a valid positive-area geometry."
            )

    @property
    def provenance(self) -> AreaOfInterestProvenance:
        return self._provenance

    def validate(self, geometry: ParcelGeometry) -> None:
        """Require a valid positive-area parcel completely covered by the AOI."""
        parcel = shape(geometry.to_geojson())
        if parcel.is_empty or parcel.area <= 0:
            raise DomainValidationError("Parcel geometry must have positive area.")
        if not parcel.is_valid:
            detail = explain_validity(parcel)
            raise DomainValidationError(f"Parcel geometry is topologically invalid: {detail}.")
        if not self._boundary.covers(parcel):
            raise DomainValidationError(
                "Parcel geometry must be completely inside the configured Huaura area of interest."
            )


def _load_boundary(path: Path) -> BaseGeometry:
    if not path.is_file():
        raise ValueError(f"Huaura AOI boundary asset was not found: {path}")
    payload = _load_json(path)
    payload_type = payload.get("type")
    if payload_type == "FeatureCollection":
        features = payload.get("features")
        if (
            not isinstance(features, list)
            or len(features) != 1
            or not isinstance(features[0], dict)
            or features[0].get("type") != "Feature"
        ):
            raise ValueError(
                "Huaura AOI FeatureCollection must contain exactly one GeoJSON Feature."
            )
        raw_geometry = features[0].get("geometry")
    elif payload_type == "Feature":
        raw_geometry = payload.get("geometry")
    elif payload_type in {"Polygon", "MultiPolygon"}:
        raw_geometry = payload
    else:
        raise ValueError(
            "Huaura AOI boundary must be a GeoJSON FeatureCollection, Feature, "
            "Polygon, or MultiPolygon."
        )
    if not isinstance(raw_geometry, dict):
        raise ValueError("Huaura AOI boundary does not contain a GeoJSON geometry.")

    boundary = shape(raw_geometry)
    if not isinstance(boundary, (Polygon, MultiPolygon)):
        raise ValueError("Huaura AOI boundary must be a Polygon or MultiPolygon.")
    return boundary


def _load_provenance(path: Path) -> AreaOfInterestProvenance:
    if not path.is_file():
        raise ValueError(f"Huaura AOI metadata asset was not found: {path}")
    payload = _load_json(path)
    required = ("name", "source", "crs", "geometry_type")
    if any(
        not isinstance(payload.get(field), str) or not payload[field].strip()
        for field in required
    ):
        raise ValueError("Huaura AOI metadata is incomplete.")
    return AreaOfInterestProvenance(
        name=payload["name"],
        source=payload["source"],
        crs=payload["crs"],
        geometry_type=payload["geometry_type"],
    )


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Unable to read Huaura AOI asset: {path}") from error
    if not isinstance(payload, dict):
        raise ValueError(f"Huaura AOI asset must contain a JSON object: {path}")
    return payload
