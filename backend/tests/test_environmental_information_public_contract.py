"""Public cross-context contract tests for Environmental Information."""

from dataclasses import FrozenInstanceError
from datetime import UTC, date, datetime
from uuid import UUID, uuid4

import pytest

from via_backend.contexts.environmental_information.application import (
    EnvironmentalInformationService,
    GetPublishedDatasetVersion,
    PublishedDatasetVersion,
    PublishedDatasetVersionReader,
)
from via_backend.contexts.environmental_information.domain import (
    Dataset,
    DatasetVersion,
    SpatialExtent,
    SpatialResolution,
)
from via_backend.contexts.environmental_information.infrastructure import (
    InMemoryDatasetRepository,
    InMemoryDatasetVersionRepository,
)

REGISTERED_AT = datetime(2026, 9, 16, 14, 30, tzinfo=UTC)


def _dataset(*, dataset_id: UUID | None = None, name: str = "CHIRPS") -> Dataset:
    return Dataset(
        id=dataset_id or uuid4(),
        name=name,
        source="Climate Hazards Center",
        variable="precipitation",
        unit="mm/day",
        created_at=datetime(2026, 9, 10, tzinfo=UTC),
    )


def _version(
    dataset_id: UUID,
    *,
    version_id: UUID | None = None,
    identifier: str = "v2.0",
    registered_at: datetime = REGISTERED_AT,
) -> DatasetVersion:
    return DatasetVersion(
        id=version_id or uuid4(),
        dataset_id=dataset_id,
        version_identifier=identifier,
        crs="EPSG:4326",
        resolution=SpatialResolution(0.05, 0.05, "degree"),
        extent=SpatialExtent(-77.8, -11.4, -77.0, -10.5),
        valid_from=date(2020, 1, 1),
        valid_to=date(2025, 12, 31),
        scenario="historical",
        checksum=f"sha256:{identifier}",
        storage_reference=f"environmental/chirps/{identifier}",
        registered_at=registered_at,
    )


def _service(
    datasets_to_add: tuple[Dataset, ...] = (),
    versions_to_add: tuple[DatasetVersion, ...] = (),
) -> EnvironmentalInformationService:
    datasets = InMemoryDatasetRepository()
    versions = InMemoryDatasetVersionRepository()
    for dataset in datasets_to_add:
        datasets.add(dataset)
    for version in versions_to_add:
        versions.add(version)
    return EnvironmentalInformationService(datasets=datasets, versions=versions)


def test_service_structurally_satisfies_public_reader_contract() -> None:
    service = _service()

    assert isinstance(service, PublishedDatasetVersionReader)


def test_exact_dataset_and_version_returns_all_published_metadata() -> None:
    dataset = _dataset()
    version = _version(dataset.id)
    service = _service((dataset,), (version,))

    result = service.get_published_dataset_version(
        GetPublishedDatasetVersion(dataset.id, version.id)
    )

    assert isinstance(result, PublishedDatasetVersion)
    assert result.dataset_id == dataset.id
    assert result.dataset_name == dataset.name
    assert result.source == dataset.source
    assert result.variable == dataset.variable
    assert result.unit == dataset.unit
    assert result.dataset_version_id == version.id
    assert result.version_identifier == version.version_identifier
    assert result.checksum == version.checksum
    assert result.storage_reference == version.storage_reference
    assert result.crs == version.crs
    assert result.resolution_x == version.resolution.x
    assert result.resolution_y == version.resolution.y
    assert result.resolution_unit == version.resolution.unit
    assert result.extent_west == version.extent.west
    assert result.extent_south == version.extent.south
    assert result.extent_east == version.extent.east
    assert result.extent_north == version.extent.north
    assert result.valid_from == version.valid_from
    assert result.valid_to == version.valid_to
    assert result.scenario == version.scenario
    assert result.registered_at == version.registered_at


def test_missing_dataset_returns_none() -> None:
    dataset = _dataset()
    version = _version(dataset.id)
    service = _service(versions_to_add=(version,))

    assert (
        service.get_published_dataset_version(
            GetPublishedDatasetVersion(dataset.id, version.id)
        )
        is None
    )


def test_missing_version_returns_none() -> None:
    dataset = _dataset()
    service = _service(datasets_to_add=(dataset,))

    assert (
        service.get_published_dataset_version(
            GetPublishedDatasetVersion(dataset.id, uuid4())
        )
        is None
    )


def test_version_belonging_to_different_dataset_returns_none() -> None:
    dataset_a = _dataset(name="Dataset A")
    dataset_b = _dataset(name="Dataset B")
    version_b = _version(dataset_b.id)
    service = _service((dataset_a, dataset_b), (version_b,))

    assert (
        service.get_published_dataset_version(
            GetPublishedDatasetVersion(dataset_a.id, version_b.id)
        )
        is None
    )


def test_multiple_versions_are_resolved_only_by_exact_version_id() -> None:
    dataset = _dataset()
    version_1 = _version(
        dataset.id,
        identifier="v1",
        registered_at=datetime(2026, 9, 14, tzinfo=UTC),
    )
    version_2 = _version(
        dataset.id,
        identifier="v2",
        registered_at=datetime(2026, 9, 15, tzinfo=UTC),
    )
    service = _service((dataset,), (version_1, version_2))

    result_1 = service.get_published_dataset_version(
        GetPublishedDatasetVersion(dataset.id, version_1.id)
    )
    result_2 = service.get_published_dataset_version(
        GetPublishedDatasetVersion(dataset.id, version_2.id)
    )

    assert result_1 is not None
    assert result_2 is not None
    assert result_1.dataset_version_id == version_1.id
    assert result_1.version_identifier == "v1"
    assert result_2.dataset_version_id == version_2.id
    assert result_2.version_identifier == "v2"


def test_published_dataset_version_is_immutable() -> None:
    dataset = _dataset()
    version = _version(dataset.id)
    result = _service((dataset,), (version,)).get_published_dataset_version(
        GetPublishedDatasetVersion(dataset.id, version.id)
    )

    assert result is not None
    field_name = "dataset_name"
    with pytest.raises(FrozenInstanceError):
        setattr(result, field_name, "mutated")