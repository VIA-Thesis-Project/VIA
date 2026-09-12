"""End-to-end API tests for the Farm Management vertical slice."""

import asyncio
from typing import Any
from uuid import uuid4

from httpx import ASGITransport, AsyncClient, Response

from via_backend.config import Settings
from via_backend.main import create_app


def _test_app():
    return create_app(Settings(farm_management_repository="memory"))


def _polygon(longitude_offset: float = 0) -> dict[str, Any]:
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


async def _request(method: str, path: str, **kwargs: Any) -> Response:
    transport = ASGITransport(app=_test_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.request(method, path, **kwargs)


def test_project_and_versioned_parcel_lifecycle() -> None:
    async def scenario() -> None:
        transport = ASGITransport(app=_test_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            project_response = await client.post("/projects", json={"name": "Huaura trial"})
            assert project_response.status_code == 201
            project = project_response.json()

            parcel_response = await client.post(
                f"/projects/{project['id']}/parcels",
                json={"name": "North field", "geometry": _polygon()},
            )
            assert parcel_response.status_code == 201
            parcel = parcel_response.json()
            assert parcel["current_version"] == 1
            assert parcel["versions"][0]["geometry"] == _polygon()

            revision_response = await client.post(
                f"/projects/{project['id']}/parcels/{parcel['id']}/versions",
                json={"geometry": _polygon(0.01)},
            )
            assert revision_response.status_code == 201
            revised = revision_response.json()
            assert revised["current_version"] == 2
            assert [version["number"] for version in revised["versions"]] == [1, 2]
            assert revised["versions"][0]["geometry"] == _polygon()
            assert revised["versions"][1]["geometry"] == _polygon(0.01)

            projects_response = await client.get("/projects")
            parcels_response = await client.get(f"/projects/{project['id']}/parcels")
            parcel_detail_response = await client.get(
                f"/projects/{project['id']}/parcels/{parcel['id']}"
            )

            assert projects_response.json() == [project]
            assert [item["id"] for item in parcels_response.json()] == [parcel["id"]]
            assert parcel_detail_response.json() == revised

    asyncio.run(scenario())


def test_parcel_requires_an_existing_project() -> None:
    response = asyncio.run(
        _request(
            "POST",
            f"/projects/{uuid4()}/parcels",
            json={"name": "Orphan", "geometry": _polygon()},
        )
    )

    assert response.status_code == 404


def test_invalid_parcel_geometry_returns_validation_error() -> None:
    async def scenario() -> Response:
        transport = ASGITransport(app=_test_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            project = (await client.post("/projects", json={"name": "Trial"})).json()
            return await client.post(
                f"/projects/{project['id']}/parcels",
                json={
                    "name": "Open ring",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [-77.6, -11.1],
                                [-77.5, -11.1],
                                [-77.5, -11.0],
                                [-77.6, -11.0],
                            ]
                        ],
                    },
                },
            )

    response = asyncio.run(scenario())

    assert response.status_code == 422
    assert response.json()["detail"] == "A linear ring must be closed."
