"""IA-5 public-release Huaura AOI enforcement."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from shapely.geometry import box, mapping, shape

from via_backend.app import create_app
from via_backend.config import (
    DEFAULT_HUAURA_AOI_BOUNDARY_PATH,
    DEFAULT_HUAURA_AOI_METADATA_PATH,
    Settings,
)
from via_backend.contexts.farm_management.infrastructure import (
    HuauraAreaOfInterestValidator,
)
from via_backend.contexts.identity_access.domain.models import UserRole

PASSWORD = "CorrectHorseBatteryStaple1!"


def _authoritative_boundary() -> Any:
    payload = json.loads(DEFAULT_HUAURA_AOI_BOUNDARY_PATH.read_text(encoding="utf-8"))
    return shape(payload["features"][0]["geometry"])


def _geojson(geometry: Any) -> dict[str, Any]:
    return json.loads(json.dumps(mapping(geometry)))


def _inside_parcels() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    boundary = _authoritative_boundary()
    center = boundary.representative_point()
    clearance = center.distance(boundary.boundary)
    assert clearance > 0
    radius = min(clearance / 8, 0.002)
    first = box(
        center.x - radius,
        center.y - radius,
        center.x + radius,
        center.y + radius,
    )
    second_center_x = center.x + (3 * radius)
    second = box(
        second_center_x - radius,
        center.y - radius,
        second_center_x + radius,
        center.y + radius,
    )
    third_center_x = center.x - (3 * radius)
    third = box(
        third_center_x - radius,
        center.y - radius,
        third_center_x + radius,
        center.y + radius,
    )
    assert boundary.covers(first)
    assert boundary.covers(second)
    assert boundary.covers(third)
    assert not first.equals(second)
    assert not first.equals(third)
    assert not second.equals(third)
    return _geojson(first), _geojson(second), _geojson(third)


def _authenticated_client() -> tuple[TestClient, dict[str, str]]:
    app = create_app(Settings())
    app.state.identity_administration.create_user(
        email="user@example.com",
        role=UserRole.USER,
        password=PASSWORD,
    )
    client = TestClient(app)
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": PASSWORD},
    )
    assert login.status_code == 200
    return client, {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_authoritative_huaura_asset_provenance_is_loaded() -> None:
    validator = HuauraAreaOfInterestValidator(
        DEFAULT_HUAURA_AOI_BOUNDARY_PATH,
        DEFAULT_HUAURA_AOI_METADATA_PATH,
    )

    assert validator.provenance.name == "Provincia de Huaura"
    assert validator.provenance.source == "GADM 4.1"
    assert validator.provenance.crs == "EPSG:4326"
    assert validator.provenance.geometry_type == "MultiPolygon"


def test_public_parcel_flow_allows_multiple_distinct_inside_geometries_and_revision() -> None:
    client, headers = _authenticated_client()
    first_geometry, second_geometry, third_geometry = _inside_parcels()
    project = client.post("/projects", json={"name": "Huaura"}, headers=headers)
    assert project.status_code == 201
    project_id = project.json()["id"]

    first = client.post(
        f"/projects/{project_id}/parcels",
        json={"name": "Parcel A", "geometry": first_geometry},
        headers=headers,
    )
    second = client.post(
        f"/projects/{project_id}/parcels",
        json={"name": "Parcel B", "geometry": second_geometry},
        headers=headers,
    )
    third = client.post(
        f"/projects/{project_id}/parcels",
        json={"name": "Parcel C", "geometry": third_geometry},
        headers=headers,
    )
    assert first.status_code == 201
    assert second.status_code == 201
    assert third.status_code == 201
    assert len({first.json()["id"], second.json()["id"], third.json()["id"]}) == 3
    geometries = {
        json.dumps(item.json()["versions"][0]["geometry"], sort_keys=True)
        for item in (first, second, third)
    }
    assert len(geometries) == 3

    revised = client.post(
        f"/projects/{project_id}/parcels/{first.json()['id']}/versions",
        json={"geometry": third_geometry},
        headers=headers,
    )
    assert revised.status_code == 201
    assert revised.json()["current_version"] == 2
    assert revised.json()["versions"][0]["geometry"] == first_geometry
    assert revised.json()["versions"][1]["geometry"] == third_geometry


def test_public_parcel_flow_rejects_outside_crossing_zero_area_and_invalid_topology() -> None:
    client, headers = _authenticated_client()
    project = client.post("/projects", json={"name": "Huaura"}, headers=headers)
    assert project.status_code == 201
    project_id = project.json()["id"]
    boundary = _authoritative_boundary()
    center = boundary.representative_point()
    min_x, _, max_x, _ = boundary.bounds
    clearance = center.distance(boundary.boundary)
    radius = min(clearance / 10, 0.001)

    outside = box(max_x + radius, center.y - radius, max_x + (3 * radius), center.y + radius)
    crossing = box(center.x, center.y - radius, max_x + radius, center.y + radius)
    assert not boundary.covers(outside)
    assert boundary.intersects(crossing)
    assert not boundary.covers(crossing)

    zero_area = {
        "type": "Polygon",
        "coordinates": [[
            [center.x, center.y],
            [center.x + radius, center.y],
            [center.x + (2 * radius), center.y],
            [center.x, center.y],
        ]],
    }
    outer = box(
        center.x - (4 * radius),
        center.y - (4 * radius),
        center.x + (4 * radius),
        center.y + (4 * radius),
    )
    invalid_hole = box(
        center.x + (3 * radius),
        center.y - radius,
        center.x + (5 * radius),
        center.y + radius,
    )
    invalid_topology = {
        "type": "Polygon",
        "coordinates": [
            list(mapping(outer)["coordinates"][0]),
            list(mapping(invalid_hole)["coordinates"][0]),
        ],
    }
    invalid_shape = shape(invalid_topology)
    assert invalid_shape.area > 0
    assert not invalid_shape.is_valid

    cases = (
        (_geojson(outside), "completely inside"),
        (_geojson(crossing), "completely inside"),
        (zero_area, "positive area"),
        (invalid_topology, "topologically invalid"),
    )
    for index, (geometry, detail) in enumerate(cases):
        response = client.post(
            f"/projects/{project_id}/parcels",
            json={"name": f"Rejected {index}", "geometry": geometry},
            headers=headers,
        )
        assert response.status_code == 422
        assert detail in response.json()["detail"]

    listed = client.get(f"/projects/{project_id}/parcels", headers=headers)
    assert listed.status_code == 200
    assert listed.json() == []
    assert min_x < max_x


def test_missing_authoritative_aoi_asset_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="boundary asset was not found"):
        create_app(Settings(huaura_aoi_boundary_path=tmp_path / "missing.geojson"))
