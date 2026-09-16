"""Immutable environmental input snapshots owned by Agroclimatic Evaluation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from math import isfinite
from uuid import UUID

from .errors import DomainValidationError

_EPSG_PATTERN = re.compile(r"EPSG:([1-9][0-9]*)")


@dataclass(frozen=True, slots=True)
class EnvironmentalInputReference:
    """Caller-selected exact environmental dataset version."""

    input_key: str
    dataset_id: UUID
    dataset_version_id: UUID

    def __post_init__(self) -> None:
        _validate_text(self.input_key, "Environmental input key", 120)


@dataclass(frozen=True, slots=True)
class EnvironmentalInputSnapshot:
    """Historical environmental input metadata captured for one evaluation input."""

    input_key: str
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

    def __post_init__(self) -> None:
        _validate_text(self.input_key, "Environmental input key", 120)
        _validate_text(self.dataset_name, "Dataset name", 120)
        _validate_text(self.source, "Dataset source", 255)
        _validate_text(self.variable, "Environmental variable", 120)
        _validate_text(self.unit, "Environmental variable unit", 64)
        _validate_text(self.version_identifier, "Dataset version identifier", 120)
        _validate_text(self.checksum, "Dataset version checksum", 256)
        _validate_text(self.storage_reference, "Storage reference", 1024)
        _validate_crs(self.crs)
        _validate_positive_number(self.resolution_x, "Horizontal resolution")
        _validate_positive_number(self.resolution_y, "Vertical resolution")
        _validate_text(self.resolution_unit, "Spatial resolution unit", 32)

        extent = (
            self.extent_west,
            self.extent_south,
            self.extent_east,
            self.extent_north,
        )
        if any(not _is_finite_number(value) for value in extent):
            raise DomainValidationError("Spatial extent coordinates must be finite numbers.")
        if self.extent_west >= self.extent_east or self.extent_south >= self.extent_north:
            raise DomainValidationError(
                "Spatial extent must have west < east and south < north."
            )
        if self.crs == "EPSG:4326" and (
            self.extent_west < -180
            or self.extent_east > 180
            or self.extent_south < -90
            or self.extent_north > 90
        ):
            raise DomainValidationError(
                "EPSG:4326 extent coordinates must be valid longitude/latitude values."
            )

        if self.valid_from is not None and self.valid_to is not None:
            if self.valid_from > self.valid_to:
                raise DomainValidationError(
                    "Dataset validity start must not be after its end."
                )
        if self.scenario is not None:
            _validate_text(self.scenario, "Scenario", 120)
        _validate_aware_datetime(self.registered_at, "Dataset registration time")


@dataclass(frozen=True, slots=True)
class EnvironmentalInputManifest:
    """Immutable set of exact environmental inputs resolved for an evaluation."""

    resolved_at: datetime
    inputs: tuple[EnvironmentalInputSnapshot, ...]

    def __post_init__(self) -> None:
        _validate_aware_datetime(self.resolved_at, "Environmental input resolution time")
        inputs = tuple(self.inputs)
        if not inputs:
            raise DomainValidationError(
                "Environmental input manifest must contain at least one input."
            )

        input_keys = tuple(item.input_key for item in inputs)
        if len(set(input_keys)) != len(input_keys):
            raise DomainValidationError(
                "Environmental input keys must be unique within a manifest."
            )
        if any(item.registered_at > self.resolved_at for item in inputs):
            raise DomainValidationError(
                "Environmental inputs must be registered no later than manifest resolution."
            )

        object.__setattr__(self, "inputs", inputs)


def _validate_text(value: str, label: str, maximum: int) -> None:
    if not value or value != value.strip():
        raise DomainValidationError(f"{label} must be non-empty and trimmed.")
    if len(value) > maximum:
        raise DomainValidationError(f"{label} must be at most {maximum} characters.")


def _validate_crs(value: str) -> None:
    if _EPSG_PATTERN.fullmatch(value) is None:
        raise DomainValidationError("CRS must use the form EPSG:<positive integer>.")


def _validate_positive_number(value: float, label: str) -> None:
    if not _is_finite_number(value) or value <= 0:
        raise DomainValidationError(f"{label} must be a finite positive number.")


def _is_finite_number(value: object) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, (int, float))
        and isfinite(value)
    )


def _validate_aware_datetime(value: datetime, label: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise DomainValidationError(f"{label} must be timezone-aware.")
