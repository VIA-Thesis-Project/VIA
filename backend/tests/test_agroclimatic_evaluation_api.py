"""End-to-end API tests for evaluation request persistence."""

import asyncio
from typing import Any
from uuid import uuid4

from httpx import ASGITransport, AsyncClient, Response

from via_backend.config import Settings
from via_backend.main import create_app


def _test_app():
    return create_app(
        Settings(
            farm_management_repository="memory",
            environmental_information_repository="memory",
            agroclimatic_evaluation_repository="memory",
        )
    )


def _body() -> dict[str, Any]:
    return {
        "parcel_snapshot": {
            "project_id": str(uuid4()),
            "parcel_id": str(uuid4()),
            "parcel_version": 2,
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-77.6, -11.1],
                    [-77.5, -11.1],
                    [-77.5, -11.0],
                    [-77.6, -11.1],
                ]],
            },
            "crs": "EPSG:4326",
            "captured_at": "2026-09-12T15:00:00Z",
        },
        "requested_crops": ["maize", "potato", "rice"],
    }


async def _request(method: str, path: str, **kwargs: Any) -> Response:
    transport = ASGITransport(app=_test_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.request(method, path, **kwargs)


def test_create_get_and_list_evaluation() -> None:
    async def scenario() -> None:
        transport = ASGITransport(app=_test_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            body = _body()
            created_response = await client.post("/evaluations", json=body)
            assert created_response.status_code == 201
            created = created_response.json()
            assert created["status"] == "queued"
            assert created["requested_crops"] == ["maize", "potato", "rice"]
            assert created["parcel_snapshot"] == body["parcel_snapshot"]

            assert (await client.get(f"/evaluations/{created['id']}")).json() == created
            assert (await client.get("/evaluations")).json() == [created]

    asyncio.run(scenario())


def test_duplicate_crops_return_validation_error() -> None:
    body = _body()
    body["requested_crops"] = ["maize", "maize"]

    response = asyncio.run(_request("POST", "/evaluations", json=body))

    assert response.status_code == 422
    assert "unique" in response.json()["detail"]


def test_missing_evaluation_returns_not_found() -> None:
    response = asyncio.run(_request("GET", f"/evaluations/{uuid4()}"))

    assert response.status_code == 404
