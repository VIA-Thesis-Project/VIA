"""Contract-focused tests for Farm Management repository adapters."""

from datetime import datetime, timezone
from uuid import uuid4

import pytest

from via_backend.contexts.farm_management.domain import (
    Parcel,
    ParcelGeometry,
    ParcelVersion,
    ParcelVersionConflictError,
)
from via_backend.contexts.farm_management.infrastructure import InMemoryParcelRepository


def _geometry(longitude: float) -> ParcelGeometry:
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


def test_stale_save_cannot_overwrite_persisted_geometry_history() -> None:
    now = datetime(2026, 9, 12, tzinfo=timezone.utc)
    original = Parcel(
        id=uuid4(),
        project_id=uuid4(),
        name="North field",
        versions=(ParcelVersion(1, _geometry(-77.6), now),),
        created_at=now,
    )
    first_revision = original.revise_geometry(_geometry(-77.5), now)
    stale_revision = original.revise_geometry(_geometry(-77.4), now)
    repository = InMemoryParcelRepository()
    repository.add(original)
    repository.save(first_revision, expected_version=1)

    with pytest.raises(ParcelVersionConflictError):
        repository.save(stale_revision, expected_version=1)

    assert repository.get(original.id) == first_revision
