"""Contract-focused Environmental Information repository tests."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from via_backend.contexts.environmental_information.domain import (
    DatasetVersion,
    DatasetVersionConflictError,
    SpatialExtent,
    SpatialResolution,
)
from via_backend.contexts.environmental_information.infrastructure import (
    InMemoryDatasetVersionRepository,
)


def _version(identifier: str = "v1") -> DatasetVersion:
    return DatasetVersion(
        id=uuid4(),
        dataset_id=DATASET_ID,
        version_identifier=identifier,
        crs="EPSG:4326",
        resolution=SpatialResolution(0.05, 0.05, "degree"),
        extent=SpatialExtent(-77.8, -11.4, -77.0, -10.5),
        valid_from=None,
        valid_to=None,
        scenario=None,
        checksum="sha256:abc123",
        storage_reference="environmental/chirps/v1",
        registered_at=datetime(2026, 9, 12, tzinfo=UTC),
    )


DATASET_ID = uuid4()


def test_duplicate_version_identifier_is_rejected() -> None:
    repository = InMemoryDatasetVersionRepository()
    original = _version()
    repository.add(original)

    with pytest.raises(DatasetVersionConflictError):
        repository.add(_version())

    assert repository.list_for_dataset(DATASET_ID) == (original,)
