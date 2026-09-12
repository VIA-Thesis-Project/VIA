"""Unit tests for Environmental Information invariants."""

from dataclasses import FrozenInstanceError
from datetime import date, datetime, timezone
from uuid import uuid4

import pytest

from via_backend.contexts.environmental_information.domain import (
    DatasetVersion,
    DomainValidationError,
    SpatialExtent,
    SpatialResolution,
)


def _version(**overrides: object) -> DatasetVersion:
    values: dict[str, object] = {
        "id": uuid4(),
        "dataset_id": uuid4(),
        "version_identifier": "chirps-2026-09",
        "crs": "EPSG:4326",
        "resolution": SpatialResolution(0.05, 0.05, "degree"),
        "extent": SpatialExtent(-77.8, -11.4, -77.0, -10.5),
        "valid_from": date(2026, 1, 1),
        "valid_to": date(2026, 9, 1),
        "scenario": None,
        "checksum": "sha256:abc123",
        "storage_reference": "environmental/chirps/2026-09",
        "registered_at": datetime(2026, 9, 12, tzinfo=timezone.utc),
    }
    values.update(overrides)
    return DatasetVersion(**values)  # type: ignore[arg-type]


def test_dataset_version_is_immutable() -> None:
    version = _version()

    with pytest.raises(FrozenInstanceError):
        version.checksum = "sha256:changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    "overrides, message",
    [
        ({"crs": "WGS84"}, "EPSG"),
        ({"resolution": SpatialResolution(0.05, 0.05, "degree"), "extent": SpatialExtent(-181, -11, -77, -10)}, "longitude/latitude"),
        ({"valid_from": date(2026, 9, 1), "valid_to": date(2026, 1, 1)}, "must not be after"),
    ],
)
def test_invalid_dataset_version_metadata_is_rejected(
    overrides: dict[str, object], message: str
) -> None:
    with pytest.raises(DomainValidationError, match=message):
        _version(**overrides)


@pytest.mark.parametrize(
    "resolution",
    [
        (0.0, 1.0),
        (1.0, -1.0),
        (float("inf"), 1.0),
    ],
)
def test_resolution_must_be_finite_and_positive(
    resolution: tuple[float, float]
) -> None:
    with pytest.raises(DomainValidationError, match="finite and positive"):
        SpatialResolution(*resolution, unit="metre")


def test_extent_must_be_ordered() -> None:
    with pytest.raises(DomainValidationError, match="west < east"):
        SpatialExtent(-77.0, -11.0, -78.0, -10.0)
