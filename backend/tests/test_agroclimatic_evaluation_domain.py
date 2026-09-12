"""Focused domain tests for immutable evaluation requests."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.application import (
    AgroclimaticEvaluationService,
    ParcelSnapshotInput,
    RequestEvaluation,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    DomainValidationError,
    Evaluation,
    EvaluationStatus,
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    InMemoryEvaluationRepository,
)

NOW = datetime(2026, 9, 12, 15, 0, tzinfo=UTC)


def _polygon() -> dict:
    return {
        "type": "Polygon",
        "coordinates": [[[-77.6, -11.1], [-77.5, -11.1], [-77.5, -11.0], [-77.6, -11.1]]],
    }


def _snapshot(geometry: dict | None = None) -> ParcelSnapshot:
    return ParcelSnapshot(
        project_id=uuid4(),
        parcel_id=uuid4(),
        parcel_version=3,
        geometry=SnapshotGeometry.from_geojson(geometry or _polygon()),
        crs="EPSG:4326",
        captured_at=NOW,
    )


def _evaluation(crops=("maize", "potato")) -> Evaluation:
    return Evaluation(
        id=uuid4(),
        parcel_snapshot=_snapshot(),
        requested_crops=crops,
        status=EvaluationStatus.QUEUED,
        created_at=NOW,
    )


def test_parcel_snapshot_is_deeply_immutable_and_detached_from_input() -> None:
    source = _polygon()
    snapshot = _snapshot(source)
    source["coordinates"][0][0][0] = 0

    assert snapshot.geometry.to_geojson()["coordinates"][0][0][0] == -77.6
    with pytest.raises(FrozenInstanceError):
        snapshot.parcel_version = 4  # type: ignore[misc]


def test_polygon_and_multipolygon_snapshot_geometry_are_supported() -> None:
    polygon = SnapshotGeometry.from_geojson(_polygon())
    multipolygon = SnapshotGeometry.from_geojson(
        {"type": "MultiPolygon", "coordinates": [_polygon()["coordinates"]]}
    )

    assert polygon.type == "Polygon"
    assert multipolygon.type == "MultiPolygon"


def test_requested_crops_preserve_order_and_are_immutable() -> None:
    crops = ["rice", "maize", "potato"]
    evaluation = _evaluation(crops)  # type: ignore[arg-type]
    crops.reverse()

    assert evaluation.requested_crops == ("rice", "maize", "potato")


@pytest.mark.parametrize("crops", [(), ("maize", "maize")])
def test_empty_or_duplicate_requested_crops_are_rejected(crops: tuple[str, ...]) -> None:
    with pytest.raises(DomainValidationError):
        _evaluation(crops)


def test_request_evaluation_starts_queued() -> None:
    evaluation_id = uuid4()
    snapshot = _snapshot()
    service = AgroclimaticEvaluationService(
        InMemoryEvaluationRepository(),
        new_id=lambda: evaluation_id,
        clock=lambda: NOW,
    )

    result = service.request_evaluation(
        RequestEvaluation(
            parcel_snapshot=ParcelSnapshotInput(
                project_id=snapshot.project_id,
                parcel_id=snapshot.parcel_id,
                parcel_version=snapshot.parcel_version,
                geometry=snapshot.geometry.to_geojson(),
                crs=snapshot.crs,
                captured_at=snapshot.captured_at,
            ),
            requested_crops=("maize", "potato"),
        )
    )

    assert result.id == evaluation_id
    assert result.status is EvaluationStatus.QUEUED
