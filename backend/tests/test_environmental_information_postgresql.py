"""PostgreSQL/PostGIS integration tests for Environmental Information."""

from __future__ import annotations

import os
from collections.abc import Iterator
from datetime import UTC, date, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, func, select, text

from database_test_support import require_test_database_url
from via_backend.contexts.environmental_information.domain import (
    Dataset,
    DatasetVersion,
    DatasetVersionConflictError,
    SpatialExtent,
    SpatialResolution,
)
from via_backend.contexts.environmental_information.infrastructure.orm import (
    DatasetVersionRecord,
)
from via_backend.contexts.environmental_information.infrastructure.postgresql_repositories import (
    PostgreSQLDatasetRepository,
    PostgreSQLDatasetVersionRepository,
)
from via_backend.infrastructure import SessionFactory, create_database

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
def clean_environmental_information(
    database: tuple[Engine, SessionFactory],
) -> None:
    engine, _ = database
    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE environmental_information.dataset_versions, "
                "environmental_information.datasets CASCADE"
            )
        )


def _dataset() -> Dataset:
    return Dataset(
        id=uuid4(),
        name="CHIRPS precipitation",
        source="Climate Hazards Center",
        variable="precipitation",
        unit="mm/day",
        created_at=datetime(2026, 9, 12, tzinfo=UTC),
    )


def _version(dataset_id, identifier: str = "2026-09") -> DatasetVersion:
    return DatasetVersion(
        id=uuid4(),
        dataset_id=dataset_id,
        version_identifier=identifier,
        crs="EPSG:4326",
        resolution=SpatialResolution(0.05, 0.05, "degree"),
        extent=SpatialExtent(-77.8, -11.4, -77.0, -10.5),
        valid_from=date(2026, 1, 1),
        valid_to=date(2026, 9, 1),
        scenario=None,
        checksum="sha256:abc123",
        storage_reference="environmental/chirps/2026-09",
        registered_at=datetime(2026, 9, 12, tzinfo=UTC),
    )


def test_dataset_and_version_survive_new_repository_instances(
    database: tuple[Engine, SessionFactory],
) -> None:
    engine, sessions = database
    dataset = _dataset()
    version = _version(dataset.id)

    PostgreSQLDatasetRepository(sessions).add(dataset)
    PostgreSQLDatasetVersionRepository(sessions).add(version)

    assert PostgreSQLDatasetRepository(sessions).get(dataset.id) == dataset
    assert PostgreSQLDatasetVersionRepository(sessions).get(version.id) == version
    with engine.connect() as connection:
        geometry_type, srid = connection.execute(
            select(
                func.ST_GeometryType(DatasetVersionRecord.extent),
                func.ST_SRID(DatasetVersionRecord.extent),
            ).where(DatasetVersionRecord.id == version.id)
        ).one()
    assert geometry_type == "ST_Polygon"
    assert srid == 4326


def test_duplicate_version_identifier_is_rejected_by_postgresql(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    dataset = _dataset()
    repository = PostgreSQLDatasetVersionRepository(sessions)
    PostgreSQLDatasetRepository(sessions).add(dataset)
    repository.add(_version(dataset.id))

    with pytest.raises(DatasetVersionConflictError):
        repository.add(_version(dataset.id))


def test_environmental_schema_owns_only_slice_tables(
    database: tuple[Engine, SessionFactory],
) -> None:
    engine, _ = database
    with engine.connect() as connection:
        tables = set(
            connection.scalars(
                text(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema = 'environmental_information'"
                )
            )
        )

    assert tables == {"datasets", "dataset_versions"}
