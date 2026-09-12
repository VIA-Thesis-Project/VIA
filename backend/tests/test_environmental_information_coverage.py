"""Fast tests for Environmental Information coverage orchestration."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from via_backend.contexts.environmental_information.application import (
    CheckDatasetVersionCoverage,
    EnvironmentalInformationService,
    InvalidCommandError,
    ResourceNotFoundError,
)
from via_backend.contexts.environmental_information.domain import (
    CoverageClassification,
    CoverageCompatibilityFailure,
    CoverageMeasurement,
    Dataset,
    DatasetVersion,
    SpatialExtent,
    SpatialResolution,
)
from via_backend.contexts.environmental_information.infrastructure import (
    InMemoryDatasetRepository,
    InMemoryDatasetVersionRepository,
)
from via_backend.contexts.environmental_information.interfaces import create_router


class StubCoveragePort:
    def __init__(self, outcome: CoverageMeasurement | CoverageCompatibilityFailure):
        self.outcome = outcome
        self.calls = 0

    def measure(self, version: DatasetVersion, geometry: Any):
        self.calls += 1
        return self.outcome


def _polygon(west: float = 1, south: float = 1, east: float = 2, north: float = 2):
    return {
        "type": "Polygon",
        "coordinates": [
            [[west, south], [east, south], [east, north], [west, north], [west, south]]
        ],
    }


def _multi_polygon():
    polygon = _polygon()["coordinates"]
    return {"type": "MultiPolygon", "coordinates": [polygon]}


def _service(outcome: CoverageMeasurement | CoverageCompatibilityFailure):
    datasets = InMemoryDatasetRepository()
    versions = InMemoryDatasetVersionRepository()
    dataset = Dataset(
        id=uuid4(),
        name="Test precipitation",
        source="Test provider",
        variable="precipitation",
        unit="mm/day",
        created_at=datetime(2026, 9, 12, tzinfo=UTC),
    )
    version = DatasetVersion(
        id=uuid4(),
        dataset_id=dataset.id,
        version_identifier="v1",
        crs="EPSG:4326",
        resolution=SpatialResolution(0.05, 0.05, "degree"),
        extent=SpatialExtent(0, 0, 10, 10),
        valid_from=None,
        valid_to=None,
        scenario=None,
        checksum="sha256:test",
        storage_reference="environmental/test/v1",
        registered_at=datetime(2026, 9, 12, tzinfo=UTC),
    )
    datasets.add(dataset)
    versions.add(version)
    port = StubCoveragePort(outcome)
    service = EnvironmentalInformationService(
        datasets=datasets, versions=versions, coverage=port
    )
    return service, datasets, versions, dataset, version, port


@pytest.mark.parametrize(
    "covered, fully, expected",
    [
        (100.0, True, CoverageClassification.FULL),
        (25.0, False, CoverageClassification.PARTIAL),
        (0.0, False, CoverageClassification.NONE),
    ],
)
def test_application_distinguishes_coverage_classes(
    covered: float, fully: bool, expected: CoverageClassification
) -> None:
    measurement = CoverageMeasurement(
        parcel_area_m2=100.0,
        covered_area_m2=covered,
        fully_covered=fully,
        comparison_crs="EPSG:4326",
        area_method="test-only measurement",
    )
    service, _, _, dataset, version, _ = _service(measurement)

    result = service.check_dataset_version_coverage(
        CheckDatasetVersionCoverage(
            dataset.id, version.id, _polygon(), "EPSG:4326"
        )
    )

    assert result.compatible is True
    assert result.coverage is expected
    assert result.coverage_percentage == covered
    assert result.coverage_percentage is not None
    assert 0 <= result.coverage_percentage <= 100
    assert result.warnings and "rectangular extent" in result.warnings[0]


def test_multi_polygon_boundary_contract_is_accepted() -> None:
    measurement = CoverageMeasurement(
        100.0, 100.0, True, "EPSG:4326", "test-only measurement"
    )
    service, _, _, dataset, version, port = _service(measurement)

    result = service.check_dataset_version_coverage(
        CheckDatasetVersionCoverage(
            dataset.id, version.id, _multi_polygon(), "EPSG:4326"
        )
    )

    assert result.coverage is CoverageClassification.FULL
    assert port.calls == 1


def test_incompatible_metadata_is_not_reported_as_no_coverage() -> None:
    service, _, _, dataset, version, _ = _service(
        CoverageCompatibilityFailure(("Dataset CRS cannot be transformed.",))
    )

    result = service.check_dataset_version_coverage(
        CheckDatasetVersionCoverage(
            dataset.id, version.id, _polygon(), "EPSG:4326"
        )
    )

    assert result.compatible is False
    assert result.coverage is CoverageClassification.NOT_ASSESSED
    assert result.coverage_percentage is None
    assert result.reasons == ("Dataset CRS cannot be transformed.",)


def test_coverage_check_does_not_mutate_dataset_version() -> None:
    measurement = CoverageMeasurement(
        100.0, 25.0, False, "EPSG:4326", "test-only measurement"
    )
    service, _, versions, dataset, version, _ = _service(measurement)
    before = versions.get(version.id)

    service.check_dataset_version_coverage(
        CheckDatasetVersionCoverage(
            dataset.id, version.id, _polygon(), "EPSG:4326"
        )
    )

    assert versions.get(version.id) == before == version


def test_invalid_geometry_is_rejected_before_spatial_adapter() -> None:
    measurement = CoverageMeasurement(
        100.0, 100.0, True, "EPSG:4326", "test-only measurement"
    )
    service, _, _, dataset, version, port = _service(measurement)

    with pytest.raises(InvalidCommandError, match="closed"):
        service.check_dataset_version_coverage(
            CheckDatasetVersionCoverage(
                dataset.id,
                version.id,
                {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1]]],
                },
                "EPSG:4326",
            )
        )
    assert port.calls == 0


def test_missing_dataset_or_version_is_not_found() -> None:
    measurement = CoverageMeasurement(
        100.0, 100.0, True, "EPSG:4326", "test-only measurement"
    )
    service, _, _, dataset, version, _ = _service(measurement)

    with pytest.raises(ResourceNotFoundError):
        service.check_dataset_version_coverage(
            CheckDatasetVersionCoverage(uuid4(), version.id, _polygon(), "EPSG:4326")
        )
    with pytest.raises(ResourceNotFoundError):
        service.check_dataset_version_coverage(
            CheckDatasetVersionCoverage(dataset.id, uuid4(), _polygon(), "EPSG:4326")
        )


def test_coverage_http_contract_and_missing_version_mapping() -> None:
    measurement = CoverageMeasurement(
        100.0, 25.0, False, "EPSG:4326", "test-only measurement"
    )
    service, _, _, dataset, version, _ = _service(measurement)
    app = FastAPI()
    app.include_router(create_router(service))

    async def scenario() -> tuple[dict[str, Any], int]:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                f"/datasets/{dataset.id}/versions/{version.id}/coverage",
                json={"geometry": _polygon(), "crs": "EPSG:4326"},
            )
            missing = await client.post(
                f"/datasets/{dataset.id}/versions/{uuid4()}/coverage",
                json={"geometry": _polygon(), "crs": "EPSG:4326"},
            )
            assert response.status_code == 200
            return response.json(), missing.status_code

    payload, missing_status = asyncio.run(scenario())
    assert payload["coverage"] == "partial"
    assert payload["coverage_percentage"] == 25.0
    assert missing_status == 404
