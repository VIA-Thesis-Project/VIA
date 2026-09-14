"""Real PostGIS tests for Environmental Information coverage calculations."""

from __future__ import annotations

import math
import os
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, text

from database_test_support import require_test_database_url
from via_backend.contexts.environmental_information.application import (
    CheckDatasetVersionCoverage,
    EnvironmentalInformationService,
)
from via_backend.contexts.environmental_information.domain import (
    CoverageClassification,
    Dataset,
    DatasetVersion,
    SpatialExtent,
    SpatialResolution,
)
from via_backend.contexts.environmental_information.infrastructure import (
    PostGISCoverageCalculator,
    PostgreSQLDatasetRepository,
    PostgreSQLDatasetVersionRepository,
)
from via_backend.infrastructure import SessionFactory, create_database

pytestmark = pytest.mark.integration
BACKEND_ROOT = Path(__file__).parents[1]


def _database_url() -> str:
    return require_test_database_url()


@pytest.fixture(scope="module")
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
def clean_tables(database: tuple[Engine, SessionFactory]) -> None:
    engine, _ = database
    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE environmental_information.dataset_versions, "
                "environmental_information.datasets CASCADE"
            )
        )


def _polygon(west: float, south: float, east: float, north: float):
    return {
        "type": "Polygon",
        "coordinates": [
            [[west, south], [east, south], [east, north], [west, north], [west, south]]
        ],
    }


def _multi_polygon():
    return {
        "type": "MultiPolygon",
        "coordinates": [
            _polygon(1, 1, 2, 2)["coordinates"],
            _polygon(3, 3, 4, 4)["coordinates"],
        ],
    }


def _service(
    sessions: SessionFactory,
    *,
    crs: str = "EPSG:4326",
    extent: SpatialExtent | None = None,
):
    extent = extent or SpatialExtent(0, 0, 10, 10)
    datasets = PostgreSQLDatasetRepository(sessions)
    versions = PostgreSQLDatasetVersionRepository(sessions)
    dataset = Dataset(
        uuid4(),
        "Coverage dataset",
        "Test provider",
        "precipitation",
        "mm/day",
        datetime(2026, 9, 12, tzinfo=UTC),
    )
    version = DatasetVersion(
        uuid4(),
        dataset.id,
        "v1",
        crs,
        SpatialResolution(1, 1, "native-unit"),
        extent,
        None,
        None,
        None,
        "sha256:test",
        "environmental/test/v1",
        datetime(2026, 9, 12, tzinfo=UTC),
    )
    datasets.add(dataset)
    versions.add(version)
    service = EnvironmentalInformationService(
        datasets, versions, coverage=PostGISCoverageCalculator(sessions)
    )
    return service, versions, dataset, version


@pytest.mark.parametrize(
    "geometry, expected",
    [
        (_polygon(1, 1, 2, 2), CoverageClassification.FULL),
        (_polygon(9, 9, 11, 11), CoverageClassification.PARTIAL),
        (_polygon(20, 20, 21, 21), CoverageClassification.NONE),
        (_multi_polygon(), CoverageClassification.FULL),
    ],
)
def test_postgis_classifies_polygon_and_multipolygon_coverage(
    database: tuple[Engine, SessionFactory], geometry: dict, expected: CoverageClassification
) -> None:
    _, sessions = database
    service, versions, dataset, version = _service(sessions)
    before = versions.get(version.id)

    result = service.check_dataset_version_coverage(
        CheckDatasetVersionCoverage(dataset.id, version.id, geometry, "EPSG:4326")
    )

    assert result.compatible is True
    assert result.coverage is expected
    assert result.coverage_percentage is not None
    assert 0 <= result.coverage_percentage <= 100
    assert result.parcel_area_m2 is not None and result.parcel_area_m2 > 0
    assert versions.get(version.id) == before == version


def test_postgis_transforms_native_dataset_extent(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    radius = 6378137.0

    def mercator(longitude: float, latitude: float) -> tuple[float, float]:
        return (
            radius * math.radians(longitude),
            radius
            * math.log(math.tan(math.pi / 4 + math.radians(latitude) / 2)),
        )

    west, south = mercator(0, 0)
    east, north = mercator(10, 10)
    service, _, dataset, version = _service(
        sessions,
        crs="EPSG:3857",
        extent=SpatialExtent(west, south, east, north),
    )

    result = service.check_dataset_version_coverage(
        CheckDatasetVersionCoverage(
            dataset.id, version.id, _polygon(1, 1, 2, 2), "EPSG:4326"
        )
    )

    assert result.compatible is True
    assert result.coverage is CoverageClassification.FULL
    assert result.comparison_crs == "EPSG:3857"
    assert "EPSG:4326 -> EPSG:3857" in result.transformations[0]


def test_untransformable_registered_dataset_crs_is_incompatible(
    database: tuple[Engine, SessionFactory],
) -> None:
    _, sessions = database
    service, _, dataset, version = _service(
        sessions,
        crs="EPSG:999999",
        extent=SpatialExtent(0, 0, 10, 10),
    )

    result = service.check_dataset_version_coverage(
        CheckDatasetVersionCoverage(
            dataset.id, version.id, _polygon(1, 1, 2, 2), "EPSG:4326"
        )
    )

    assert result.compatible is False
    assert result.coverage is CoverageClassification.NOT_ASSESSED
    assert result.coverage_percentage is None
    assert "not transformable" in result.reasons[0]
