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
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError

from via_backend.contexts.agroclimatic_evaluation.domain import (
    Evaluation,
    EvaluationStatus,
    ParcelSnapshot,
    SnapshotGeometry,
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
    value = os.getenv("VIA_TEST_DATABASE_URL")
    if not value:
        pytest.skip("Set VIA_TEST_DATABASE_URL to run PostgreSQL/PostGIS tests.")
    database_name = make_url(value).database or ""
    if not database_name.casefold().endswith("_test"):
        pytest.fail("VIA_TEST_DATABASE_URL must name a database ending in '_test'.")
    return value


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
