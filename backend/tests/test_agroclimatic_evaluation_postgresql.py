"""PostgreSQL/PostGIS integration tests for Agroclimatic Evaluation."""

from __future__ import annotations

import os
from collections.abc import Iterator
from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, func, select, text
from sqlalchemy.exc import IntegrityError

from database_test_support import require_test_database_url
from via_backend.contexts.agroclimatic_evaluation.application import (
    AgroclimaticEvaluationRecoveryService,
    RecoverEvaluation,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    CommonSupport,
    CommonSupportStatus,
    ComparableCrop,
    CropOutcome,
    CropOutcomeStatus,
    EnvironmentalInputManifest,
    EnvironmentalInputReference,
    EnvironmentalInputSnapshot,
    Evaluation,
    EvaluationConflictError,
    EvaluationStatus,
    ParcelSnapshot,
    ScientificArtifact,
    ScientificArtifactGrid,
    ScientificArtifactRole,
    ScientificTrace,
    SnapshotGeometry,
    SuitabilitySummary,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.orm import (
    EvaluationCommonSupportRecord,
    EvaluationComparableCropRecord,
    EvaluationCropRecord,
    EvaluationRecord,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.postgresql_repositories import (
    PostgreSQLEvaluationRepository,
)
from via_backend.infrastructure import SessionFactory, create_database

pytestmark = pytest.mark.integration
BACKEND_ROOT = Path(__file__).parents[1]
NOW = datetime(2026, 9, 12, 15, 0, tzinfo=UTC)
RESOLVED_AT = NOW + timedelta(minutes=30)


def _database_url() -> str:
    return require_test_database_url()


@pytest.fixture(scope="session")
def database() -> Iterator[tuple[Engine, SessionFactory]]:
    database_url = _database_url()
    previous = os.environ.get("VIA_DATABASE_URL")
    os.environ["VIA_DATABASE_URL"] = database_url
    try:
        command.upgrade(Config(str(BACKEND_ROOT / "alembic.ini")), "head")
    finally:
        if previous is None:
            os.environ.pop("VIA_DATABASE_URL", None)
        else:
            os.environ["VIA_DATABASE_URL"] = previous
    engine, sessions = create_database(database_url)
    yield engine, sessions
    engine.dispose()


@pytest.fixture(autouse=True)
def clean_evaluations(database: tuple[Engine, SessionFactory]) -> None:
    engine, _ = database
    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE agroclimatic_evaluation.evaluation_crops, "
                "agroclimatic_evaluation.evaluations CASCADE"
            )
        )


def _polygon() -> dict:
    return {
        "type": "Polygon",
        "coordinates": [[[-77.6, -11.1], [-77.5, -11.1], [-77.5, -11.0], [-77.6, -11.1]]],
    }


def _multipolygon() -> dict:
    return {"type": "MultiPolygon", "coordinates": [_polygon()["coordinates"]]}


def _references() -> tuple[EnvironmentalInputReference, ...]:
    return (
        EnvironmentalInputReference(
            input_key="soil.ph",
            dataset_id=uuid4(),
            dataset_version_id=uuid4(),
        ),
        EnvironmentalInputReference(
            input_key="climate.precipitation",
            dataset_id=uuid4(),
            dataset_version_id=uuid4(),
        ),
    )


def _snapshot_for_reference(
    reference: EnvironmentalInputReference,
    *,
    position: int,
) -> EnvironmentalInputSnapshot:
    resolution_x = (0.01, 0.011)[position]
    resolution_y = (0.02, 0.021)[position]

    extent_west = (-77.8, -77.79)[position]
    extent_south = (-12.7, -12.69)[position]
    extent_east = (-76.2, -76.19)[position]
    extent_north = (-10.4, -10.39)[position]

    return EnvironmentalInputSnapshot(
        input_key=reference.input_key,
        dataset_id=reference.dataset_id,
        dataset_name=f"Dataset {position}",
        source=f"Source {position}",
        variable=f"variable_{position}",
        unit="unit",
        dataset_version_id=reference.dataset_version_id,
        version_identifier=f"2026-09-{position}",
        checksum=f"sha256:{reference.dataset_version_id.hex}",
        storage_reference=f"catalog://{reference.dataset_version_id}",
        crs="EPSG:4326",
        resolution_x=resolution_x,
        resolution_y=resolution_y,
        resolution_unit="degree",
        extent_west=extent_west,
        extent_south=extent_south,
        extent_east=extent_east,
        extent_north=extent_north,
        valid_from=date(2026, 1, 1) if position == 0 else None,
        valid_to=date(2026, 12, 31) if position == 0 else None,
        scenario="baseline" if position == 0 else None,
        registered_at=NOW - timedelta(days=position),
    )


def _manifest(
    references: tuple[EnvironmentalInputReference, ...],
) -> EnvironmentalInputManifest:
    return EnvironmentalInputManifest(
        resolved_at=RESOLVED_AT,
        inputs=tuple(
            _snapshot_for_reference(reference, position=position)
            for position, reference in enumerate(references)
        ),
    )


def _evaluation(
    geometry: dict | None = None,
    *,
    references: tuple[EnvironmentalInputReference, ...] | None = None,
) -> Evaluation:
    references = _references() if references is None else references
    return Evaluation(
        id=uuid4(),
        parcel_snapshot=ParcelSnapshot(
            project_id=uuid4(),
            parcel_id=uuid4(),
            parcel_version=4,
            geometry=SnapshotGeometry.from_geojson(geometry or _polygon()),
            crs="EPSG:4326",
            captured_at=NOW,
        ),
        requested_crops=("rice", "maize", "potato"),
        status=EvaluationStatus.QUEUED,
        created_at=NOW,
        environmental_input_references=references,
    )


def _start_running(
    repository: PostgreSQLEvaluationRepository,
    preparing: Evaluation,
) -> Evaluation:
    running = (
        preparing.attach_environmental_input_manifest(
            _manifest(preparing.environmental_input_references)
        ).start_running()
    )
    repository.save(running, expected_status=EvaluationStatus.PREPARING)
    return running


@pytest.mark.parametrize("geometry", [_polygon(), _multipolygon()])
def test_evaluation_snapshot_round_trips_as_postgis_multipolygon(
    database: tuple[Engine, SessionFactory], geometry: dict
) -> None:
    engine, sessions = database
    evaluation = _evaluation(geometry)

    PostgreSQLEvaluationRepository(sessions).add(evaluation)
    restored = PostgreSQLEvaluationRepository(sessions).get(evaluation.id)

    assert restored == evaluation
    with engine.connect() as connection:
        geometry_type, srid = connection.execute(
            select(
                func.ST_GeometryType(EvaluationRecord.snapshot_geometry),
                func.ST_SRID(EvaluationRecord.snapshot_geometry),
            ).where(EvaluationRecord.id == evaluation.id)
        ).one()
    assert geometry_type == "ST_MultiPolygon"
    assert srid == 4326


def test_exact_environmental_input_references_round_trip_in_order_without_manifest(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    references = _references()
    evaluation = _evaluation(references=references)
    repository = PostgreSQLEvaluationRepository(sessions)

    repository.add(evaluation)
    restored = repository.get(evaluation.id)

    assert restored is not None
    assert restored.environmental_input_references == references
    assert restored.environmental_input_manifest is None


def test_same_exact_dataset_version_can_serve_distinct_input_keys(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    dataset_id = uuid4()
    dataset_version_id = uuid4()
    references = (
        EnvironmentalInputReference("soil.ph", dataset_id, dataset_version_id),
        EnvironmentalInputReference("soil.texture", dataset_id, dataset_version_id),
    )
    evaluation = _evaluation(references=references)
    repository = PostgreSQLEvaluationRepository(sessions)

    repository.add(evaluation)
    restored = repository.get(evaluation.id)

    assert restored is not None
    assert restored.environmental_input_references == references


def test_historical_evaluation_without_environmental_rows_still_loads(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    evaluation = _evaluation(references=())
    repository = PostgreSQLEvaluationRepository(sessions)

    repository.add(evaluation)
    restored = repository.get(evaluation.id)

    assert restored == evaluation
    assert restored is not None
    assert restored.environmental_input_references == ()
    assert restored.environmental_input_manifest is None


def test_snapshot_is_independent_of_later_source_changes(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    source = _polygon()
    evaluation = _evaluation(source)
    repository = PostgreSQLEvaluationRepository(sessions)
    repository.add(evaluation)

    source["coordinates"][0][0][0] = 0

    restored = repository.get(evaluation.id)
    assert restored is not None
    assert restored.parcel_snapshot.geometry.to_geojson()["coordinates"][0][0][0] == -77.6


def test_duplicate_requested_crop_is_rejected_by_database(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    evaluation = _evaluation()
    PostgreSQLEvaluationRepository(sessions).add(evaluation)

    with pytest.raises(IntegrityError), sessions.begin() as session:
        session.add(
            EvaluationCropRecord(
                evaluation_id=evaluation.id,
                position=99,
                crop_id="rice",
            )
        )


def test_evaluation_schema_has_no_cross_context_foreign_keys(
    database: tuple[Engine, SessionFactory],
) -> None:
    engine, _ = database
    with engine.connect() as connection:
        referenced_schemas = set(
            connection.scalars(
                text(
                    "SELECT ccu.table_schema FROM information_schema.table_constraints tc "
                    "JOIN information_schema.constraint_column_usage ccu "
                    "ON tc.constraint_name = ccu.constraint_name "
                    "AND tc.constraint_schema = ccu.constraint_schema "
                    "WHERE tc.constraint_type = 'FOREIGN KEY' "
                    "AND tc.table_schema = 'agroclimatic_evaluation'"
                )
            )
        )

    assert referenced_schemas <= {"agroclimatic_evaluation"}


def _succeeded_outcome(crop_id: str = "rice") -> CropOutcome:
    return CropOutcome(
        crop_id=crop_id,
        status=CropOutcomeStatus.SUCCEEDED,
        suitability=SuitabilitySummary(
            mean=0.0,
            minimum=0.0,
            maximum=0.0,
            valid_cells=3,
            valid_area_m2=75.0,
            coverage_fraction=0.75,
            zero_suitability_area_m2=75.0,
        ),
        failure_message=None,
        trace=ScientificTrace(
            engine_identifier="CropSuiteLite",
            execution_reference="opaque-engine-reference",
            started_at=NOW,
            finished_at=NOW,
            elapsed_seconds=2.5,
            execution_mode="sequential_isolated_processes",
            parcel_sha256="parcel-sha256",
            parameter_sha256="parameter-sha256",
            configuration_sha256="configuration-sha256",
            source_files_unchanged=True,
        ),
        artifacts=(_scientific_artifact(),),
    )

def _scientific_artifact() -> ScientificArtifact:
    return ScientificArtifact(
        role=ScientificArtifactRole.CROP_SUITABILITY,
        storage_reference=(
            "evaluations/00000000-0000-0000-0000-000000000001/"
            "crops/maize/crop_suitability.tif"
        ),
        sha256="a" * 64,
        media_type="image/tiff",
        size_bytes=723,
        grid=ScientificArtifactGrid(
            crs="EPSG:4326",
            width=12,
            height=8,
            transform=(
                0.0041666667,
                0.0,
                -77.5,
                0.0,
                -0.0041666667,
                -11.0,
            ),
            nodata=-1.0,
        ),
    )

def test_crop_outcome_and_trace_fields_round_trip(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    evaluation = _evaluation()
    repository = PostgreSQLEvaluationRepository(sessions)
    repository.add(evaluation)
    preparing = evaluation.prepare()
    repository.save(preparing, expected_status=EvaluationStatus.QUEUED)
    _start_running(repository, preparing)
    outcome = _succeeded_outcome()
    repository.add_outcome(evaluation.id, outcome)

    restored = repository.get(evaluation.id)

    assert restored is not None
    assert restored.status is EvaluationStatus.RUNNING
    assert restored.outcomes == (outcome,)
    assert restored.outcomes[0].suitability is not None
    assert restored.outcomes[0].suitability.mean == 0.0


def test_duplicate_crop_outcome_is_rejected_by_database(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    evaluation = _evaluation()
    repository = PostgreSQLEvaluationRepository(sessions)
    repository.add(evaluation)
    preparing = evaluation.prepare()
    repository.save(preparing, expected_status=EvaluationStatus.QUEUED)
    _start_running(repository, preparing)
    outcome = _succeeded_outcome()
    repository.add_outcome(evaluation.id, outcome)

    with pytest.raises(EvaluationConflictError):
        repository.add_outcome(evaluation.id, outcome)


def test_queued_discovery_filters_orders_and_limits(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    repository = PostgreSQLEvaluationRepository(sessions)
    older = replace(
        _evaluation(),
        id=UUID(int=20),
        created_at=NOW - timedelta(minutes=1),
    )
    same_time_first = replace(_evaluation(), id=UUID(int=1))
    same_time_second = replace(_evaluation(), id=UUID(int=2))
    active = replace(_evaluation(), id=UUID(int=0)).prepare()
    for evaluation in (same_time_second, active, older, same_time_first):
        repository.add(evaluation)

    assert repository.list_queued_ids(limit=2) == (
        older.id,
        same_time_first.id,
    )


def test_preparing_to_running_persists_complete_manifest_atomically(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    references = _references()
    evaluation = _evaluation(references=references)
    repository = PostgreSQLEvaluationRepository(sessions)
    repository.add(evaluation)
    preparing = evaluation.prepare()
    repository.save(preparing, expected_status=EvaluationStatus.QUEUED)
    manifest = _manifest(references)
    running = preparing.attach_environmental_input_manifest(manifest).start_running()

    repository.save(running, expected_status=EvaluationStatus.PREPARING)
    restored = repository.get(evaluation.id)

    assert restored is not None
    assert restored.status is EvaluationStatus.RUNNING
    assert restored.environmental_input_references == references
    restored_manifest = restored.environmental_input_manifest
    assert restored_manifest is not None
    assert restored_manifest == manifest
    assert restored_manifest.inputs == manifest.inputs


def test_manifest_persistence_is_idempotent_and_cannot_be_overwritten(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    evaluation = _evaluation()
    repository = PostgreSQLEvaluationRepository(sessions)
    repository.add(evaluation)
    preparing = evaluation.prepare()
    repository.save(preparing, expected_status=EvaluationStatus.QUEUED)
    running = _start_running(repository, preparing)

    repository.save(running, expected_status=EvaluationStatus.RUNNING)

    original_manifest = running.environmental_input_manifest
    assert original_manifest is not None
    changed_first_input = replace(
        original_manifest.inputs[0],
        checksum="sha256:different-but-still-valid",
    )
    different_manifest = EnvironmentalInputManifest(
        resolved_at=original_manifest.resolved_at,
        inputs=(changed_first_input, *original_manifest.inputs[1:]),
    )
    conflicting = replace(
        running,
        environmental_input_manifest=different_manifest,
    )

    with pytest.raises(EvaluationConflictError, match="different environmental input manifest"):
        repository.save(conflicting, expected_status=EvaluationStatus.RUNNING)

    restored = repository.get(evaluation.id)
    assert restored is not None
    assert restored.status is EvaluationStatus.RUNNING
    assert restored.environmental_input_manifest == original_manifest


def test_failed_preparing_evaluation_can_persist_without_manifest(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    evaluation = _evaluation()
    repository = PostgreSQLEvaluationRepository(sessions)
    repository.add(evaluation)
    preparing = evaluation.prepare()
    repository.save(preparing, expected_status=EvaluationStatus.QUEUED)
    failed = preparing.fail("environmental input resolution failed")

    repository.save(failed, expected_status=EvaluationStatus.PREPARING)
    restored = repository.get(evaluation.id)

    assert restored == failed
    assert restored is not None
    assert restored.environmental_input_references == evaluation.environmental_input_references
    assert restored.environmental_input_manifest is None


def test_explicit_recovery_persists_failure_and_preserves_outcomes(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    repository = PostgreSQLEvaluationRepository(sessions)
    evaluation = _evaluation()
    repository.add(evaluation)
    preparing = evaluation.prepare()
    repository.save(preparing, expected_status=EvaluationStatus.QUEUED)
    _start_running(repository, preparing)
    outcome = _succeeded_outcome()
    repository.add_outcome(evaluation.id, outcome)

    result = AgroclimaticEvaluationRecoveryService(repository).recover_evaluation(
        RecoverEvaluation(evaluation.id, "worker process terminated")
    )

    restored = repository.get(evaluation.id)
    assert result.status is EvaluationStatus.FAILED
    assert restored is not None
    assert restored.status is EvaluationStatus.FAILED
    assert restored.failure_reason == "worker process terminated"
    assert restored.outcomes == (outcome,)

def _common_support() -> CommonSupport:
    return CommonSupport(
        status=CommonSupportStatus.COMPARABLE,
        method="area_weighted_mean_on_common_valid_cells",
        area_crs="EPSG:6933",
        parcel_area_m2=100.0,
        common_valid_area_m2=80.0,
        common_coverage_fraction=0.8,
        eligible_crops=("rice", "potato"),
        excluded_without_coverage=("maize",),
    )



def _comparable_crops() -> tuple[ComparableCrop, ...]:
    return (
        ComparableCrop(
            crop_id="rice",
            mean=82.0,
            rank=1,
        ),
        ComparableCrop(
            crop_id="potato",
            mean=74.0,
            rank=2,
        ),
    )

def test_comparison_round_trips_atomically_with_success(
    database: tuple[Engine, SessionFactory],
) -> None:
    engine, sessions = database
    repository = PostgreSQLEvaluationRepository(sessions)

    evaluation = _evaluation()
    repository.add(evaluation)

    preparing = evaluation.prepare()
    repository.save(
        preparing,
        expected_status=EvaluationStatus.QUEUED,
    )

    running = _start_running(repository, preparing)

    current = running

    for crop_id in evaluation.requested_crops:
        outcome = _succeeded_outcome(crop_id)
        repository.add_outcome(
            evaluation.id,
            outcome,
        )
        current = current.record_outcome(outcome)

    summarizing = current.start_summarizing()
    repository.save(
        summarizing,
        expected_status=EvaluationStatus.RUNNING,
    )

    summarized = summarizing.record_comparison(
        _common_support(),
        _comparable_crops(),
    )
    succeeded = summarized.succeed()

    repository.save(
        succeeded,
        expected_status=EvaluationStatus.SUMMARIZING,
    )

    restored = repository.get(evaluation.id)

    assert restored is not None
    assert restored == succeeded

    common_support = restored.common_support

    assert common_support is not None
    assert common_support == _common_support()
    assert common_support.eligible_crops == (
        "rice",
        "potato",
    )
    assert common_support.excluded_without_coverage == (
        "maize",
    )
    assert restored.comparable_crops == _comparable_crops()

    with engine.connect() as connection:
        record = connection.execute(
            select(
                EvaluationCommonSupportRecord.status,
                EvaluationCommonSupportRecord.eligible_crops,
                EvaluationCommonSupportRecord.excluded_without_coverage,
            ).where(
                EvaluationCommonSupportRecord.evaluation_id
                == evaluation.id
            )
        ).one()

        comparable_records = tuple(
            connection.execute(
                select(
                    EvaluationComparableCropRecord.crop_id,
                    EvaluationComparableCropRecord.position,
                    EvaluationComparableCropRecord.mean,
                    EvaluationComparableCropRecord.rank,
                )
                .where(
                    EvaluationComparableCropRecord.evaluation_id
                    == evaluation.id
                )
                .order_by(EvaluationComparableCropRecord.position)
            )
        )

    assert record.status == "comparable"
    assert record.eligible_crops == ["rice", "potato"]
    assert record.excluded_without_coverage == ["maize"]
    assert comparable_records == (
        ("rice", 0, 82.0, 1),
        ("potato", 1, 74.0, 2),
    )


def test_legacy_common_support_without_comparable_crops_still_round_trips(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    repository = PostgreSQLEvaluationRepository(sessions)

    evaluation = _evaluation()
    repository.add(evaluation)

    preparing = evaluation.prepare()
    repository.save(
        preparing,
        expected_status=EvaluationStatus.QUEUED,
    )

    running = _start_running(repository, preparing)

    current = running
    for crop_id in evaluation.requested_crops:
        outcome = _succeeded_outcome(crop_id)
        repository.add_outcome(evaluation.id, outcome)
        current = current.record_outcome(outcome)

    summarizing = current.start_summarizing()
    repository.save(
        summarizing,
        expected_status=EvaluationStatus.RUNNING,
    )

    legacy_succeeded = (
        summarizing
        .record_common_support(_common_support())
        .succeed()
    )

    repository.save(
        legacy_succeeded,
        expected_status=EvaluationStatus.SUMMARIZING,
    )

    restored = repository.get(evaluation.id)

    assert restored is not None
    assert restored == legacy_succeeded
    assert restored.common_support == _common_support()
    assert restored.comparable_crops == ()


def test_comparison_persistence_rolls_back_final_state_atomically_on_conflict(
    database: tuple[Engine, SessionFactory],
) -> None:
    engine, sessions = database
    repository = PostgreSQLEvaluationRepository(sessions)

    evaluation = _evaluation()
    repository.add(evaluation)

    preparing = evaluation.prepare()
    repository.save(
        preparing,
        expected_status=EvaluationStatus.QUEUED,
    )

    running = _start_running(repository, preparing)

    current = running
    for crop_id in evaluation.requested_crops:
        outcome = _succeeded_outcome(crop_id)
        repository.add_outcome(evaluation.id, outcome)
        current = current.record_outcome(outcome)

    summarizing = current.start_summarizing()
    repository.save(
        summarizing,
        expected_status=EvaluationStatus.RUNNING,
    )

    succeeded = summarizing.record_comparison(
        _common_support(),
        _comparable_crops(),
    ).succeed()

    with sessions.begin() as session:
        session.add(
            EvaluationComparableCropRecord(
                evaluation_id=evaluation.id,
                crop_id="rice",
                position=0,
                mean=1.0,
                rank=1,
            )
        )

    with pytest.raises(
        EvaluationConflictError,
        match="comparable-crop data",
    ):
        repository.save(
            succeeded,
            expected_status=EvaluationStatus.SUMMARIZING,
        )

    with engine.connect() as connection:
        status = connection.scalar(
            select(EvaluationRecord.status).where(
                EvaluationRecord.id == evaluation.id
            )
        )
        common_support_count = connection.scalar(
            select(func.count())
            .select_from(EvaluationCommonSupportRecord)
            .where(
                EvaluationCommonSupportRecord.evaluation_id
                == evaluation.id
            )
        )
        comparable_count = connection.scalar(
            select(func.count())
            .select_from(EvaluationComparableCropRecord)
            .where(
                EvaluationComparableCropRecord.evaluation_id
                == evaluation.id
            )
        )

    assert status == EvaluationStatus.SUMMARIZING.value
    assert common_support_count == 0
    assert comparable_count == 1
