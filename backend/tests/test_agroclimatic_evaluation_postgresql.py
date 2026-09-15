"""PostgreSQL/PostGIS integration tests for Agroclimatic Evaluation."""

from __future__ import annotations

import os
from collections.abc import Iterator
from dataclasses import replace
from datetime import UTC, datetime, timedelta
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


def _evaluation(geometry: dict | None = None) -> Evaluation:
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
    )


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
    running = preparing.start_running()
    repository.save(running, expected_status=EvaluationStatus.PREPARING)
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
    running = preparing.start_running()
    repository.save(running, expected_status=EvaluationStatus.PREPARING)
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


def test_explicit_recovery_persists_failure_and_preserves_outcomes(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    repository = PostgreSQLEvaluationRepository(sessions)
    evaluation = _evaluation()
    repository.add(evaluation)
    preparing = evaluation.prepare()
    repository.save(preparing, expected_status=EvaluationStatus.QUEUED)
    running = preparing.start_running()
    repository.save(running, expected_status=EvaluationStatus.PREPARING)
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

    running = preparing.start_running()
    repository.save(
        running,
        expected_status=EvaluationStatus.PREPARING,
    )

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

    running = preparing.start_running()
    repository.save(
        running,
        expected_status=EvaluationStatus.PREPARING,
    )

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

    running = preparing.start_running()
    repository.save(
        running,
        expected_status=EvaluationStatus.PREPARING,
    )

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
