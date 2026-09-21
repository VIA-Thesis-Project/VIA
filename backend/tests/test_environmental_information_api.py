"""End-to-end API tests for Environmental Information."""

import asyncio
from typing import Any
from uuid import UUID, uuid4

from httpx import ASGITransport, AsyncClient, Response

from via_backend.config import Settings
from via_backend.contexts.identity_access.application.public import AuthenticatedPrincipal
from via_backend.contexts.identity_access.domain.models import UserRole
from via_backend.main import create_app


def _test_app():
    app = create_app(
        Settings(
            farm_management_repository="memory",
            environmental_information_repository="memory",
        )
    )
    # These lifecycle tests exercise dataset behavior under an authenticated admin.
    for route in app.routes:
        dependant = getattr(route, "dependant", None)
        for dependency in dependant.dependencies if dependant is not None else ():
            if getattr(dependency.call, "__name__", "") == "resolve_principal":
                app.dependency_overrides[dependency.call] = lambda: AuthenticatedPrincipal(
                    UUID("11111111-1111-4111-8111-111111111111"), UserRole.ADMIN
                )
    return app


def _dataset_body() -> dict[str, Any]:
    return {
        "name": "CHIRPS precipitation",
        "source": "Climate Hazards Center",
        "variable": "precipitation",
        "unit": "mm/day",
    }


def _version_body(identifier: str = "2026-09") -> dict[str, Any]:
    return {
        "version_identifier": identifier,
        "crs": "EPSG:4326",
        "resolution": {"x": 0.05, "y": 0.05, "unit": "degree"},
        "extent": {
            "west": -77.8,
            "south": -11.4,
            "east": -77.0,
            "north": -10.5,
        },
        "valid_from": "2026-01-01",
        "valid_to": "2026-09-01",
        "scenario": None,
        "checksum": "sha256:abc123",
        "storage_reference": "environmental/chirps/2026-09",
    }


async def _request(method: str, path: str, **kwargs: Any) -> Response:
    transport = ASGITransport(app=_test_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.request(method, path, **kwargs)


def test_dataset_and_version_lifecycle() -> None:
    async def scenario() -> None:
        transport = ASGITransport(app=_test_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            dataset_response = await client.post("/datasets", json=_dataset_body())
            assert dataset_response.status_code == 201
            dataset = dataset_response.json()

            version_response = await client.post(
                f"/datasets/{dataset['id']}/versions",
                json=_version_body(),
            )
            assert version_response.status_code == 201
            version = version_response.json()
            assert version["dataset_id"] == dataset["id"]
            assert version["extent"] == _version_body()["extent"]

            assert (await client.get("/datasets")).json() == [dataset]
            assert (await client.get(f"/datasets/{dataset['id']}")).json() == dataset
            assert (
                await client.get(f"/datasets/{dataset['id']}/versions")
            ).json() == [version]
            assert (
                await client.get(
                    f"/datasets/{dataset['id']}/versions/{version['id']}"
                )
            ).json() == version

    asyncio.run(scenario())


def test_duplicate_version_identifier_returns_conflict() -> None:
    async def scenario() -> Response:
        transport = ASGITransport(app=_test_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            dataset = (await client.post("/datasets", json=_dataset_body())).json()
            path = f"/datasets/{dataset['id']}/versions"
            assert (await client.post(path, json=_version_body())).status_code == 201
            return await client.post(path, json=_version_body())

    response = asyncio.run(scenario())

    assert response.status_code == 409


def test_missing_dataset_returns_not_found() -> None:
    response = asyncio.run(
        _request("POST", f"/datasets/{uuid4()}/versions", json=_version_body())
    )

    assert response.status_code == 404


def test_invalid_extent_returns_validation_error() -> None:
    async def scenario() -> Response:
        transport = ASGITransport(app=_test_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            dataset = (await client.post("/datasets", json=_dataset_body())).json()
            body = _version_body()
            body["extent"] = {
                "west": -77.0,
                "south": -11.4,
                "east": -77.8,
                "north": -10.5,
            }
            return await client.post(
                f"/datasets/{dataset['id']}/versions", json=body
            )

    response = asyncio.run(scenario())

    assert response.status_code == 422
    assert "west < east" in response.json()["detail"]
