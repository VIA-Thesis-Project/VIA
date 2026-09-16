"""Focused domain tests for immutable evaluation requests."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.application import (
    AgroclimaticEvaluationService,
    EnvironmentalInputReferenceInput,
    InvalidCommandError,
    ParcelSnapshotInput,
    RequestEvaluation,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    DomainValidationError,
    EnvironmentalInputManifest,
    EnvironmentalInputReference,
    EnvironmentalInputSnapshot,
    Evaluation,
    EvaluationStatus,
    InvalidEvaluationTransitionError,
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    InMemoryEvaluationRepository,
)

NOW = datetime(2026, 9, 12, 15, 0, tzinfo=UTC)
DATASET_ID = uuid4()
DATASET_VERSION_ID = uuid4()


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


def _reference(input_key: str = "soil.ph") -> EnvironmentalInputReference:
    return EnvironmentalInputReference(
        input_key=input_key,
        dataset_id=DATASET_ID,
        dataset_version_id=DATASET_VERSION_ID,
    )


def _manifest(input_key: str = "soil.ph") -> EnvironmentalInputManifest:
    return EnvironmentalInputManifest(
        resolved_at=NOW,
        inputs=(
            EnvironmentalInputSnapshot(
                input_key=input_key,
                dataset_id=DATASET_ID,
                dataset_name="Soil pH",
                source="Open catalog",
                variable="phh2o",
                unit="pH",
                dataset_version_id=DATASET_VERSION_ID,
                version_identifier="2026-09",
                checksum="sha256:abc",
                storage_reference="catalog://soil/ph/2026-09",
                crs="EPSG:4326",
                resolution_x=0.01,
                resolution_y=0.01,
                resolution_unit="degree",
                extent_west=-77.8,
                extent_south=-12.7,
                extent_east=-76.2,
                extent_north=-10.4,
                valid_from=None,
                valid_to=None,
                scenario=None,
                registered_at=NOW,
            ),
        ),
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
            environmental_inputs=(
                EnvironmentalInputReferenceInput(
                    input_key="soil.ph",
                    dataset_id=DATASET_ID,
                    dataset_version_id=DATASET_VERSION_ID,
                ),
            ),
        )
    )

    assert result.id == evaluation_id
    assert result.status is EvaluationStatus.QUEUED


def test_request_evaluation_rejects_empty_environmental_inputs() -> None:
    snapshot = _snapshot()
    service = AgroclimaticEvaluationService(InMemoryEvaluationRepository())

    with pytest.raises(InvalidCommandError, match="At least one environmental input"):
        service.request_evaluation(
            RequestEvaluation(
                parcel_snapshot=ParcelSnapshotInput(
                    project_id=snapshot.project_id,
                    parcel_id=snapshot.parcel_id,
                    parcel_version=snapshot.parcel_version,
                    geometry=snapshot.geometry.to_geojson(),
                    crs=snapshot.crs,
                    captured_at=snapshot.captured_at,
                ),
                requested_crops=("maize",),
                environmental_inputs=(),
            )
        )


def test_preparing_requires_exact_manifest_before_running() -> None:
    evaluation = Evaluation(
        id=uuid4(),
        parcel_snapshot=_snapshot(),
        requested_crops=("maize",),
        status=EvaluationStatus.QUEUED,
        created_at=NOW,
        environmental_input_references=(_reference(),),
    )
    preparing = evaluation.prepare()

    with pytest.raises(InvalidEvaluationTransitionError, match="without an environmental"):
        preparing.start_running()

    running = preparing.attach_environmental_input_manifest(_manifest()).start_running()
    assert running.status is EvaluationStatus.RUNNING
    assert running.environmental_input_manifest == _manifest()


def test_manifest_must_match_references_in_order_and_identity() -> None:
    with pytest.raises(DomainValidationError, match="exactly match requested references"):
        Evaluation(
            id=uuid4(),
            parcel_snapshot=_snapshot(),
            requested_crops=("maize",),
            status=EvaluationStatus.PREPARING,
            created_at=NOW,
            environmental_input_references=(_reference("soil.moisture"),),
            environmental_input_manifest=_manifest("soil.ph"),
        )


def test_historical_running_evaluation_without_environmental_inputs_can_hydrate() -> None:
    historical = Evaluation(
        id=uuid4(),
        parcel_snapshot=_snapshot(),
        requested_crops=("maize",),
        status=EvaluationStatus.RUNNING,
        created_at=NOW,
    )

    assert historical.environmental_input_references == ()
    assert historical.environmental_input_manifest is None
