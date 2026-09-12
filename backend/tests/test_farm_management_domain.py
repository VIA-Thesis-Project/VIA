"""Unit tests for Farm Management invariants."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from via_backend.contexts.farm_management.domain import (
    DomainValidationError,
    Parcel,
    ParcelGeometry,
    ParcelVersion,
)


def _polygon(longitude_offset: float = 0) -> dict[str, object]:
    return {
        "type": "Polygon",
        "coordinates": [
            [
                [-77.6 + longitude_offset, -11.1],
                [-77.5 + longitude_offset, -11.1],
                [-77.5 + longitude_offset, -11.0],
                [-77.6 + longitude_offset, -11.1],
            ]
        ],
    }


def test_revising_geometry_appends_an_immutable_version() -> None:
    created_at = datetime(2026, 9, 12, tzinfo=UTC)
    parcel = Parcel(
        id=uuid4(),
        project_id=uuid4(),
        name="North field",
        versions=(
            ParcelVersion(
                number=1,
                geometry=ParcelGeometry.from_geojson(_polygon()),
                created_at=created_at,
            ),
        ),
        created_at=created_at,
    )

    revised = parcel.revise_geometry(
        ParcelGeometry.from_geojson(_polygon(0.01)),
        created_at + timedelta(hours=1),
    )

    assert parcel.current_version.number == 1
    assert len(parcel.versions) == 1
    assert revised.current_version.number == 2
    assert revised.versions[0] == parcel.versions[0]


@pytest.mark.parametrize(
    "geometry, expected_message",
    [
        ({"type": "Point", "coordinates": [-77.6, -11.1]}, "Polygon or MultiPolygon"),
        (
            {
                "type": "Polygon",
                "coordinates": [[[-77.6, -11.1], [-77.5, -11.1], [-77.5, -11.0]]],
            },
            "at least four",
        ),
        (
            {
                "type": "Polygon",
                "coordinates": [
                    [[-77.6, -11.1], [-77.5, -11.1], [-77.5, -11.0], [-77.6, -11.0]]
                ],
            },
            "closed",
        ),
    ],
)
def test_invalid_geometry_is_rejected(
    geometry: dict[str, object], expected_message: str
) -> None:
    with pytest.raises(DomainValidationError, match=expected_message):
        ParcelGeometry.from_geojson(geometry)

