"""PostgreSQL/PostGIS integration tests for Agroclimatic Evaluation."""

from __future__ import annotations

import os
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, func, select, text
from sqlalchemy.exc import IntegrityError

from database_test_support import require_test_database_url
from via_backend.contexts.agroclimatic_evaluation.domain import (
    CropOutcome,
    CropOutcomeStatus,
    Evaluation,
    EvaluationConflictError,
    EvaluationStatus,
    ParcelSnapshot,
    ScientificTrace,
    SnapshotGeometry,
    SuitabilitySummary,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.orm import (
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
