"""End-to-end API tests for the Farm Management vertical slice."""

import asyncio
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI, Header, HTTPException, status
from httpx import ASGITransport, AsyncClient, Response

from via_backend.contexts.agroclimatic_evaluation.domain import (
    Evaluation,
    EvaluationStatus,
    ParcelSnapshot,
    SnapshotGeometry,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    InMemoryEvaluationRepository,
)
from via_backend.contexts.farm_management.application import (
    AuthorizedParcelSnapshotNotFoundError,
    FarmManagementService,
)
from via_backend.contexts.farm_management.infrastructure import (
    InMemoryParcelRepository,
    InMemoryProjectRepository,
)
from via_backend.contexts.farm_management.interfaces import create_router
from via_backend.contexts.identity_access.application.public import AuthenticatedPrincipal
from via_backend.contexts.identity_access.domain import UserRole

USER_A_ID = UUID("11111111-1111-4111-8111-111111111111")
USER_B_ID = UUID("22222222-2222-4222-8222-222222222222")
USER_A_HEADERS = {"Authorization": "Bearer user-a"}
USER_B_HEADERS = {"Authorization": "Bearer user-b"}


class _AllowAllAreaOfInterest:
    def validate(self, geometry: Any) -> None:
        pass


def _test_app():
    app = FastAPI()
    service = FarmManagementService(
        projects=InMemoryProjectRepository(),
        parcels=InMemoryParcelRepository(),
        area_of_interest=_AllowAllAreaOfInterest(),
    )
    app.state.farm_management = service

    def resolve_principal(
        authorization: str | None = Header(default=None),
    ) -> AuthenticatedPrincipal:
        if authorization == USER_A_HEADERS["Authorization"]:
            return AuthenticatedPrincipal(USER_A_ID, UserRole.USER)
        if authorization == USER_B_HEADERS["Authorization"]:
            return AuthenticatedPrincipal(USER_B_ID, UserRole.USER)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )

    app.include_router(create_router(service, resolve_principal))
    return app


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


def test_parcel_metadata_patch_and_soft_delete_preserve_versions() -> None:
    async def scenario() -> None:
        app = _test_app()
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            project = (
                await client.post("/projects", json={"name": "Owned"}, headers=USER_A_HEADERS)
            ).json()
            path = f"/projects/{project['id']}/parcels"
            created = (
                await client.post(
                    path,
                    json={"name": "Original", "description": "First", "geometry": _polygon()},
                    headers=USER_A_HEADERS,
                )
            ).json()
            item = f"{path}/{created['id']}"
            for body, expected_name, expected_description in (
                ({"name": "Renamed"}, "Renamed", "First"),
                ({"description": "Second"}, "Renamed", "Second"),
                ({"name": "Both", "description": "Third"}, "Both", "Third"),
            ):
                response = await client.patch(item, json=body, headers=USER_A_HEADERS)
                assert response.status_code == 200
                assert response.json()["name"] == expected_name
                assert response.json()["description"] == expected_description
                assert response.json()["current_version"] == 1
                assert response.json()["versions"] == created["versions"]
            assert (
                await client.patch(item, json={"name": "Foreign"}, headers=USER_B_HEADERS)
            ).status_code == 404
            assert (await client.delete(item, headers=USER_B_HEADERS)).status_code == 404
            assert (
                await client.patch(item, json={"name": " "}, headers=USER_A_HEADERS)
            ).status_code == 422
            assert (
                await client.patch(item, json={"description": "x" * 2001}, headers=USER_A_HEADERS)
            ).status_code == 422
            assert (
                await client.patch(item, json={"geometry": _polygon()}, headers=USER_A_HEADERS)
            ).status_code == 422
            snapshot = app.state.farm_management.resolve_authorized_parcel_snapshot(
                owner_user_id=USER_A_ID,
                project_id=UUID(project["id"]),
                parcel_id=UUID(created["id"]),
                parcel_version=1,
            )
            historical_evaluations = InMemoryEvaluationRepository()
            historical = Evaluation(
                id=uuid4(),
                parcel_snapshot=ParcelSnapshot(
                    project_id=snapshot.project_id,
                    parcel_id=snapshot.parcel_id,
                    parcel_version=snapshot.parcel_version,
                    geometry=SnapshotGeometry.from_geojson({
                        "type": snapshot.geometry.type,
                        "coordinates": snapshot.geometry.coordinates,
                    }),
                    crs=snapshot.crs,
                    captured_at=snapshot.captured_at,
                ),
                requested_crops=("maize",),
                status=EvaluationStatus.QUEUED,
                created_at=datetime.now(UTC),
                owner_user_id=USER_A_ID,
            )
            historical_evaluations.add(historical)
            assert (await client.delete(item, headers=USER_A_HEADERS)).status_code == 204
            assert (await client.get(item, headers=USER_A_HEADERS)).status_code == 404
            assert (await client.get(path, headers=USER_A_HEADERS)).json() == []
            assert (
                await client.patch(item, json={"name": "Again"}, headers=USER_A_HEADERS)
            ).status_code == 404
            assert (await client.delete(item, headers=USER_A_HEADERS)).status_code == 404
            assert (
                await client.post(
                    f"{item}/versions", json={"geometry": _polygon(0.01)}, headers=USER_A_HEADERS
                )
            ).status_code == 404
            assert snapshot.parcel_version == 1
            assert historical_evaluations.get(historical.id) == historical
            with pytest.raises(AuthorizedParcelSnapshotNotFoundError):
                app.state.farm_management.resolve_authorized_parcel_snapshot(
                    owner_user_id=USER_A_ID,
                    project_id=UUID(project["id"]),
                    parcel_id=UUID(created["id"]),
                    parcel_version=1,
                )

    asyncio.run(scenario())


async def _request(method: str, path: str, **kwargs: Any) -> Response:
    transport = ASGITransport(app=_test_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.request(method, path, **kwargs)


def test_project_and_versioned_parcel_lifecycle() -> None:
    async def scenario() -> None:
        transport = ASGITransport(app=_test_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            project_response = await client.post(
                "/projects",
                json={"name": "Huaura trial"},
                headers=USER_A_HEADERS,
            )
            assert project_response.status_code == 201
            project = project_response.json()

            parcel_response = await client.post(
                f"/projects/{project['id']}/parcels",
                json={"name": "North field", "geometry": _polygon()},
                headers=USER_A_HEADERS,
            )
            assert parcel_response.status_code == 201
            parcel = parcel_response.json()
            assert parcel["current_version"] == 1
            assert parcel["versions"][0]["geometry"] == _polygon()

            revision_response = await client.post(
                f"/projects/{project['id']}/parcels/{parcel['id']}/versions",
                json={"geometry": _polygon(0.01)},
                headers=USER_A_HEADERS,
            )
            assert revision_response.status_code == 201
            revised = revision_response.json()
            assert revised["current_version"] == 2
            assert [version["number"] for version in revised["versions"]] == [1, 2]
            assert revised["versions"][0]["geometry"] == _polygon()
            assert revised["versions"][1]["geometry"] == _polygon(0.01)

            projects_response = await client.get("/projects", headers=USER_A_HEADERS)
            parcels_response = await client.get(
                f"/projects/{project['id']}/parcels",
                headers=USER_A_HEADERS,
            )
            parcel_detail_response = await client.get(
                f"/projects/{project['id']}/parcels/{parcel['id']}",
                headers=USER_A_HEADERS,
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
            headers=USER_A_HEADERS,
        )
    )

    assert response.status_code == 404


def test_invalid_parcel_geometry_returns_validation_error() -> None:
    async def scenario() -> Response:
        transport = ASGITransport(app=_test_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            project = (
                await client.post(
                    "/projects",
                    json={"name": "Trial"},
                    headers=USER_A_HEADERS,
                )
            ).json()
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
                headers=USER_A_HEADERS,
            )

    response = asyncio.run(scenario())

    assert response.status_code == 422
    assert response.json()["detail"] == "A linear ring must be closed."


def test_project_ownership_isolated_between_users() -> None:
    async def scenario() -> None:
        transport = ASGITransport(app=_test_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            project = (
                await client.post(
                    "/projects",
                    json={"name": "Owner A project"},
                    headers=USER_A_HEADERS,
                )
            ).json()

            assert (await client.get("/projects", headers=USER_B_HEADERS)).json() == []

            detail = await client.get(f"/projects/{project['id']}", headers=USER_B_HEADERS)
            assert detail.status_code == 404

            parcel = await client.post(
                f"/projects/{project['id']}/parcels",
                json={"name": "Foreign parcel", "geometry": _polygon()},
                headers=USER_B_HEADERS,
            )
            assert parcel.status_code == 404

            owner_detail = await client.get(f"/projects/{project['id']}", headers=USER_A_HEADERS)
            assert owner_detail.status_code == 200

    asyncio.run(scenario())


def test_projects_require_authentication() -> None:
    response = asyncio.run(_request("GET", "/projects"))

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_nested_parcel_routes_enforce_project_owner_and_parent_identity() -> None:
    async def scenario() -> None:
        transport = ASGITransport(app=_test_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            project_a = (
                await client.post(
                    "/projects",
                    json={"name": "A project"},
                    headers=USER_A_HEADERS,
                )
            ).json()
            project_b = (
                await client.post(
                    "/projects",
                    json={"name": "B project"},
                    headers=USER_B_HEADERS,
                )
            ).json()
            parcel_a = (
                await client.post(
                    f"/projects/{project_a['id']}/parcels",
                    json={"name": "A parcel", "geometry": _polygon()},
                    headers=USER_A_HEADERS,
                )
            ).json()

            assert [
                item["id"]
                for item in (await client.get("/projects", headers=USER_A_HEADERS)).json()
            ] == [project_a["id"]]
            assert [
                item["id"]
                for item in (await client.get("/projects", headers=USER_B_HEADERS)).json()
            ] == [project_b["id"]]

            foreign_paths = (
                f"/projects/{project_a['id']}/parcels",
                f"/projects/{project_a['id']}/parcels/{parcel_a['id']}",
                f"/projects/{project_b['id']}/parcels/{parcel_a['id']}",
            )
            for path in foreign_paths:
                response = await client.get(path, headers=USER_B_HEADERS)
                assert response.status_code == 404

            foreign_revision = await client.post(
                f"/projects/{project_a['id']}/parcels/{parcel_a['id']}/versions",
                json={"geometry": _polygon(0.02)},
                headers=USER_B_HEADERS,
            )
            mismatched_parent_revision = await client.post(
                f"/projects/{project_b['id']}/parcels/{parcel_a['id']}/versions",
                json={"geometry": _polygon(0.02)},
                headers=USER_B_HEADERS,
            )
            assert foreign_revision.status_code == 404
            assert mismatched_parent_revision.status_code == 404

    asyncio.run(scenario())


def test_project_owner_is_not_client_editable() -> None:
    response = asyncio.run(
        _request(
            "POST",
            "/projects",
            json={"name": "Spoofed", "owner_user_id": str(USER_B_ID)},
            headers=USER_A_HEADERS,
        )
    )

    assert response.status_code == 422
