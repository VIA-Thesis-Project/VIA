"""Focused domain tests for immutable environmental input manifests."""

from dataclasses import replace
from datetime import UTC, date, datetime
from uuid import UUID

import pytest

from via_backend.contexts.agroclimatic_evaluation.domain import (
    DomainValidationError,
    EnvironmentalInputManifest,
    EnvironmentalInputReference,
    EnvironmentalInputSnapshot,
)

DATASET_ID = UUID("10000000-0000-0000-0000-000000000001")
DATASET_VERSION_ID = UUID("20000000-0000-0000-0000-000000000001")
REGISTERED_AT = datetime(2026, 9, 16, 12, 0, tzinfo=UTC)
RESOLVED_AT = datetime(2026, 9, 16, 12, 30, tzinfo=UTC)


def _snapshot() -> EnvironmentalInputSnapshot:
    return EnvironmentalInputSnapshot(
        input_key="soil.ph",
        dataset_id=DATASET_ID,
        dataset_name="Soil pH",
        source="Open environmental catalog",
        variable="phh2o",
        unit="pH",
        dataset_version_id=DATASET_VERSION_ID,
        version_identifier="2026-09",
        checksum="sha256:0123456789abcdef",
        storage_reference="catalog://soil/ph/2026-09",
        crs="EPSG:4326",
        resolution_x=0.0008333333,
        resolution_y=0.0008333333,
        resolution_unit="degree",
        extent_west=-77.8,
        extent_south=-12.7,
        extent_east=-76.2,
        extent_north=-10.4,
        valid_from=date(2026, 1, 1),
        valid_to=date(2026, 12, 31),
        scenario=None,
        registered_at=REGISTERED_AT,
    )


def test_environmental_input_snapshot_accepts_valid_reproducibility_metadata() -> None:
    snapshot = _snapshot()
    assert snapshot.dataset_id == DATASET_ID
    assert snapshot.dataset_version_id == DATASET_VERSION_ID


def test_environmental_input_reference_accepts_exact_version_identity() -> None:
    reference = EnvironmentalInputReference(
        input_key="soil.ph",
        dataset_id=DATASET_ID,
        dataset_version_id=DATASET_VERSION_ID,
    )

    assert reference.input_key == "soil.ph"
    assert reference.dataset_id == DATASET_ID
    assert reference.dataset_version_id == DATASET_VERSION_ID


@pytest.mark.parametrize("input_key", ["", " soil.ph", "soil.ph "])
def test_environmental_input_reference_rejects_empty_or_untrimmed_key(
    input_key: str,
) -> None:
    with pytest.raises(DomainValidationError):
        EnvironmentalInputReference(
            input_key=input_key,
            dataset_id=DATASET_ID,
            dataset_version_id=DATASET_VERSION_ID,
        )


def test_environmental_input_manifest_accepts_valid_inputs() -> None:
    snapshot = _snapshot()
    manifest = EnvironmentalInputManifest(resolved_at=RESOLVED_AT, inputs=(snapshot,))
    assert manifest.inputs == (snapshot,)


def test_environmental_input_manifest_rejects_empty_inputs() -> None:
    with pytest.raises(DomainValidationError):
        EnvironmentalInputManifest(resolved_at=RESOLVED_AT, inputs=())


def test_environmental_input_manifest_rejects_duplicate_input_key() -> None:
    first = _snapshot()
    second = replace(first, dataset_id=UUID("10000000-0000-0000-0000-000000000002"))
    with pytest.raises(DomainValidationError):
        EnvironmentalInputManifest(resolved_at=RESOLVED_AT, inputs=(first, second))


def test_environmental_input_manifest_allows_same_version_for_distinct_input_keys() -> None:
    first = _snapshot()
    second = replace(first, input_key="soil.ph.secondary")
    manifest = EnvironmentalInputManifest(resolved_at=RESOLVED_AT, inputs=(first, second))
    assert manifest.inputs[0].dataset_version_id == manifest.inputs[1].dataset_version_id


def test_environmental_input_manifest_rejects_naive_resolved_at() -> None:
    with pytest.raises(DomainValidationError):
        EnvironmentalInputManifest(
            resolved_at=datetime(2026, 9, 16, 12, 30),
            inputs=(_snapshot(),),
        )


def test_environmental_input_snapshot_rejects_naive_registered_at() -> None:
    with pytest.raises(DomainValidationError):
        replace(_snapshot(), registered_at=datetime(2026, 9, 16, 12, 0))


def test_environmental_input_manifest_rejects_input_registered_after_resolution() -> None:
    snapshot = replace(
        _snapshot(), registered_at=datetime(2026, 9, 16, 13, 0, tzinfo=UTC)
    )
    with pytest.raises(DomainValidationError):
        EnvironmentalInputManifest(resolved_at=RESOLVED_AT, inputs=(snapshot,))


@pytest.mark.parametrize("input_key", ["", " soil.ph", "soil.ph "])
def test_environmental_input_snapshot_rejects_empty_or_untrimmed_input_key(
    input_key: str,
) -> None:
    with pytest.raises(DomainValidationError):
        replace(_snapshot(), input_key=input_key)


@pytest.mark.parametrize("crs", ["4326", "epsg:4326", "EPSG:0", "EPSG:-1", "EPSG: 4326"])
def test_environmental_input_snapshot_rejects_invalid_crs(crs: str) -> None:
    with pytest.raises(DomainValidationError):
        replace(_snapshot(), crs=crs)


@pytest.mark.parametrize("field", ["resolution_x", "resolution_y"])
def test_environmental_input_snapshot_rejects_bool_resolution(field: str) -> None:
    with pytest.raises(DomainValidationError):
        replace(_snapshot(), **{field: True})


@pytest.mark.parametrize("value", [0.0, -0.1])
def test_environmental_input_snapshot_rejects_non_positive_resolution(value: float) -> None:
    with pytest.raises(DomainValidationError):
        replace(_snapshot(), resolution_x=value)


@pytest.mark.parametrize("value", [float("inf"), float("-inf"), float("nan")])
def test_environmental_input_snapshot_rejects_non_finite_resolution(value: float) -> None:
    with pytest.raises(DomainValidationError):
        replace(_snapshot(), resolution_y=value)


@pytest.mark.parametrize(
    ("west", "south", "east", "north"),
    [
        (-76.0, -12.0, -77.0, -11.0),
        (-77.0, -11.0, -76.0, -12.0),
        (float("nan"), -12.0, -76.0, -11.0),
        (-77.0, -12.0, float("inf"), -11.0),
    ],
)
def test_environmental_input_snapshot_rejects_invalid_extent(
    west: float, south: float, east: float, north: float
) -> None:
    with pytest.raises(DomainValidationError):
        replace(
            _snapshot(),
            extent_west=west,
            extent_south=south,
            extent_east=east,
            extent_north=north,
        )


@pytest.mark.parametrize(
    ("west", "south", "east", "north"),
    [
        (-180.1, -12.0, -76.0, -11.0),
        (-77.0, -90.1, -76.0, -11.0),
        (-77.0, -12.0, 180.1, -11.0),
        (-77.0, -12.0, -76.0, 90.1),
    ],
)
def test_environmental_input_snapshot_rejects_invalid_epsg_4326_extent(
    west: float, south: float, east: float, north: float
) -> None:
    with pytest.raises(DomainValidationError):
        replace(
            _snapshot(),
            extent_west=west,
            extent_south=south,
            extent_east=east,
            extent_north=north,
        )


def test_environmental_input_snapshot_rejects_reversed_validity_window() -> None:
    with pytest.raises(DomainValidationError):
        replace(
            _snapshot(),
            valid_from=date(2026, 12, 31),
            valid_to=date(2026, 1, 1),
        )


@pytest.mark.parametrize("scenario", ["", " SSP2-4.5", "SSP2-4.5 "])
def test_environmental_input_snapshot_rejects_invalid_scenario(scenario: str) -> None:
    with pytest.raises(DomainValidationError):
        replace(_snapshot(), scenario=scenario)
