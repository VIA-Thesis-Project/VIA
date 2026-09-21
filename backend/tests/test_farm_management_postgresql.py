"""PostgreSQL/PostGIS integration tests for Farm Management persistence."""

from __future__ import annotations

import os
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from pathlib import Path
from threading import Barrier
from uuid import UUID, uuid4

import pytest
from alembic import command
from alembic.config import Config
from geoalchemy2.elements import WKTElement
from sqlalchemy import Engine, func, select, text
from sqlalchemy.exc import IntegrityError

from database_test_support import require_test_database_url
from via_backend.contexts.farm_management.domain import (
    Parcel,
    ParcelGeometry,
    ParcelVersion,
    ParcelVersionConflictError,
    Project,
)
from via_backend.contexts.farm_management.infrastructure import create_database
from via_backend.contexts.farm_management.infrastructure.database import SessionFactory
from via_backend.contexts.farm_management.infrastructure.orm import ParcelVersionRecord
from via_backend.contexts.farm_management.infrastructure.postgresql_repositories import (
    PostgreSQLParcelRepository,
    PostgreSQLProjectRepository,
)

pytestmark = pytest.mark.integration
BACKEND_ROOT = Path(__file__).parents[1]


def _database_url() -> str:
    return require_test_database_url()


@pytest.fixture(scope="session")
def database() -> Iterator[tuple[Engine, SessionFactory]]:
    database_url = _database_url()
    previous = os.environ.get("VIA_DATABASE_URL")
    os.environ["VIA_DATABASE_URL"] = database_url
    try:
        config = Config(str(BACKEND_ROOT / "alembic.ini"))
        command.upgrade(config, "head")
    finally:
        if previous is None:
            os.environ.pop("VIA_DATABASE_URL", None)
        else:
            os.environ["VIA_DATABASE_URL"] = previous

    engine, sessions = create_database(database_url)
    yield engine, sessions
    engine.dispose()


@pytest.fixture(autouse=True)
def clean_farm_management(database: tuple[Engine, SessionFactory]) -> None:
    engine, _ = database
    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE farm_management.parcel_versions, "
                "farm_management.parcels, farm_management.projects CASCADE"
            )
        )


def _polygon(longitude: float = -77.6) -> ParcelGeometry:
    return ParcelGeometry.from_geojson(
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [longitude, -11.1],
                    [longitude + 0.01, -11.1],
                    [longitude + 0.01, -11.0],
                    [longitude, -11.1],
                ]
            ],
        }
    )


def _multi_polygon() -> ParcelGeometry:
    first = _polygon(-77.6).to_geojson()["coordinates"]
    second = _polygon(-77.4).to_geojson()["coordinates"]
    return ParcelGeometry.from_geojson(
        {"type": "MultiPolygon", "coordinates": [first, second]}
    )


def _project(now: datetime) -> Project:
    return Project(id=uuid4(), name="Huaura trial", created_at=now)


def _parcel(project_id: UUID, geometry: ParcelGeometry, now: datetime) -> Parcel:
    return Parcel(
        id=uuid4(),
        project_id=project_id,
        name="North field",
        versions=(ParcelVersion(number=1, geometry=geometry, created_at=now),),
        created_at=now,
    )


def test_project_survives_a_new_repository_instance(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    now = datetime(2026, 9, 12, tzinfo=UTC)
    project = _project(now)

    PostgreSQLProjectRepository(sessions).add(project)

    assert PostgreSQLProjectRepository(sessions).get(project.id) == project


def test_project_owner_user_id_round_trips_without_identity_foreign_key(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    project = Project(
        id=uuid4(),
        name="Owned Huaura trial",
        created_at=datetime(2026, 9, 12, tzinfo=UTC),
        owner_user_id=uuid4(),
    )

    PostgreSQLProjectRepository(sessions).add(project)

    assert PostgreSQLProjectRepository(sessions).get(project.id) == project


@pytest.mark.parametrize("geometry", [_polygon(), _multi_polygon()])
def test_parcel_geometry_round_trips_through_postgis(
    database: tuple[Engine, SessionFactory], geometry: ParcelGeometry
) -> None:
    engine, sessions = database
    now = datetime(2026, 9, 12, tzinfo=UTC)
    project = _project(now)
    parcel = _parcel(project.id, geometry, now)
    PostgreSQLProjectRepository(sessions).add(project)

    PostgreSQLParcelRepository(sessions).add(parcel)
    loaded = PostgreSQLParcelRepository(sessions).get(parcel.id)

    assert loaded == parcel
    with engine.connect() as connection:
        geometry_type, srid = connection.execute(
            select(
                func.ST_GeometryType(ParcelVersionRecord.geometry),
                func.ST_SRID(ParcelVersionRecord.geometry),
            ).where(ParcelVersionRecord.parcel_id == parcel.id)
        ).one()
    assert geometry_type == "ST_MultiPolygon"
    assert srid == 4326


def test_revision_is_immutable_and_stale_save_conflicts(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    now = datetime(2026, 9, 12, tzinfo=UTC)
    project = _project(now)
    parcel = _parcel(project.id, _polygon(), now)
    projects = PostgreSQLProjectRepository(sessions)
    parcels = PostgreSQLParcelRepository(sessions)
    projects.add(project)
    parcels.add(parcel)
    first_reader = parcels.get(parcel.id)
    stale_reader = parcels.get(parcel.id)
    assert first_reader is not None and stale_reader is not None

    first_revision = first_reader.revise_geometry(
        _polygon(-77.5), now + timedelta(hours=1)
    )
    stale_revision = stale_reader.revise_geometry(
        _polygon(-77.4), now + timedelta(hours=2)
    )
    parcels.save(first_revision, expected_version=1)

    with pytest.raises(ParcelVersionConflictError):
        parcels.save(stale_revision, expected_version=1)

    loaded = PostgreSQLParcelRepository(sessions).get(parcel.id)

    assert loaded is not None
    assert loaded == first_revision
    assert loaded.versions[0] == parcel.versions[0]


def test_concurrent_revisions_allow_exactly_one_writer(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    now = datetime(2026, 9, 12, tzinfo=UTC)
    project = _project(now)
    parcel = _parcel(project.id, _polygon(), now)
    PostgreSQLProjectRepository(sessions).add(project)
    PostgreSQLParcelRepository(sessions).add(parcel)

    revisions = (
        parcel.revise_geometry(_polygon(-77.5), now + timedelta(hours=1)),
        parcel.revise_geometry(_polygon(-77.4), now + timedelta(hours=2)),
    )
    start = Barrier(2)

    def save(revision: Parcel) -> str:
        repository = PostgreSQLParcelRepository(sessions)
        start.wait()
        try:
            repository.save(revision, expected_version=1)
        except ParcelVersionConflictError:
            return "conflict"
        return "saved"

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = tuple(executor.map(save, revisions))

    assert sorted(outcomes) == ["conflict", "saved"]
    loaded = PostgreSQLParcelRepository(sessions).get(parcel.id)
    assert loaded is not None
    assert loaded.current_version.number == 2
    assert len(loaded.versions) == 2
    assert loaded.versions[0] == parcel.versions[0]


def test_duplicate_parcel_version_number_is_rejected(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    now = datetime(2026, 9, 12, tzinfo=UTC)
    project = _project(now)
    parcel = _parcel(project.id, _polygon(), now)
    PostgreSQLProjectRepository(sessions).add(project)
    PostgreSQLParcelRepository(sessions).add(parcel)

    with pytest.raises(IntegrityError):
        with sessions.begin() as session:
            session.add(
                ParcelVersionRecord(
                    parcel_id=parcel.id,
                    number=1,
                    geometry_type="Polygon",
                    geometry=WKTElement(
                        "MULTIPOLYGON (((-77.6 -11.1, -77.5 -11.1, "
                        "-77.5 -11.0, -77.6 -11.1)))",
                        srid=4326,
                    ),
                    created_at=now,
                )
            )
