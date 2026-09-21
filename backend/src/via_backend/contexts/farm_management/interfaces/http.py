"""FastAPI resources for the Farm Management vertical slice."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from via_backend.contexts.identity_access.application.public import AuthenticatedPrincipal

from ..application import (
    CreateParcel,
    CreateProject,
    FarmManagementService,
    GetParcel,
    GetProject,
    InvalidCommandError,
    ListParcels,
    ListProjects,
    ParcelResult,
    ResourceConflictError,
    ResourceNotFoundError,
    ReviseParcelGeometry,
)


class _RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class GeometryBody(_RequestModel):
    type: Literal["Polygon", "MultiPolygon"]
    coordinates: list[Any]


class CreateProjectBody(_RequestModel):
    name: str = Field(min_length=1, max_length=120)


class CreateParcelBody(_RequestModel):
    name: str = Field(min_length=1, max_length=120)
    geometry: GeometryBody


class ReviseParcelGeometryBody(_RequestModel):
    geometry: GeometryBody


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    created_at: datetime


class ParcelVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    geometry: GeometryBody
    created_at: datetime


class ParcelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    name: str
    current_version: int
    versions: list[ParcelVersionResponse]
    created_at: datetime


def create_router(
    service: FarmManagementService,
    principal_resolver: Callable[..., AuthenticatedPrincipal],
) -> APIRouter:
    """Create a router bound to the supplied application service."""
    router = APIRouter(prefix="/projects", tags=["farm-management"])
    principal_dependency = Depends(principal_resolver)

    @router.post(
        "",
        response_model=ProjectResponse,
        status_code=status.HTTP_201_CREATED,
        operation_id="create_project",
        description="Create a project that owns parcels and their geometry history.",
    )
    def create_project(
        body: CreateProjectBody,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> ProjectResponse:
        return _project_response(
            _execute(
                service.create_project,
                CreateProject(name=body.name, owner_user_id=principal.user_id),
            )
        )

    @router.get(
        "",
        response_model=list[ProjectResponse],
        operation_id="list_projects",
        description="List projects visible to the current API process.",
    )
    def list_projects(
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> list[ProjectResponse]:
        return [
            _project_response(project)
            for project in _execute(
                service.list_projects,
                ListProjects(owner_user_id=principal.user_id),
            )
        ]

    @router.get(
        "/{project_id}",
        response_model=ProjectResponse,
        operation_id="get_project",
        description="Read one project by its public identifier.",
    )
    def get_project(
        project_id: UUID,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> ProjectResponse:
        return _project_response(
            _execute(
                service.get_project,
                GetProject(project_id, owner_user_id=principal.user_id),
            )
        )

    @router.post(
        "/{project_id}/parcels",
        response_model=ParcelResponse,
        status_code=status.HTTP_201_CREATED,
        operation_id="create_parcel",
        description="Create a parcel with geometry version 1 inside a project.",
    )
    def create_parcel(
        project_id: UUID,
        body: CreateParcelBody,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> ParcelResponse:
        parcel = _execute(
            service.create_parcel,
            CreateParcel(
                project_id=project_id,
                owner_user_id=principal.user_id,
                name=body.name,
                geometry=body.geometry.model_dump(),
            ),
        )
        return _parcel_response(parcel)

    @router.get(
        "/{project_id}/parcels",
        response_model=list[ParcelResponse],
        operation_id="list_parcels",
        description="List parcels and their immutable geometry versions for a project.",
    )
    def list_parcels(
        project_id: UUID,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> list[ParcelResponse]:
        return [
            _parcel_response(parcel)
            for parcel in _execute(
                service.list_parcels,
                ListParcels(project_id, owner_user_id=principal.user_id),
            )
        ]

    @router.get(
        "/{project_id}/parcels/{parcel_id}",
        response_model=ParcelResponse,
        operation_id="get_parcel",
        description="Read one parcel and its complete geometry-version history.",
    )
    def get_parcel(
        project_id: UUID,
        parcel_id: UUID,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> ParcelResponse:
        parcel = _execute(
            service.get_parcel,
            GetParcel(project_id, principal.user_id, parcel_id),
        )
        return _parcel_response(parcel)

    @router.post(
        "/{project_id}/parcels/{parcel_id}/versions",
        response_model=ParcelResponse,
        status_code=status.HTTP_201_CREATED,
        operation_id="create_parcel_version",
        description="Append an immutable geometry version to an existing parcel.",
    )
    def revise_parcel_geometry(
        project_id: UUID,
        parcel_id: UUID,
        body: ReviseParcelGeometryBody,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> ParcelResponse:
        parcel = _execute(
            service.revise_parcel_geometry,
            ReviseParcelGeometry(
                project_id=project_id,
                owner_user_id=principal.user_id,
                parcel_id=parcel_id,
                geometry=body.geometry.model_dump(),
            ),
        )
        return _parcel_response(parcel)

    return router


def _execute(operation: Any, message: Any) -> Any:
    try:
        return operation(message)
    except ResourceNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except InvalidCommandError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(error)
        ) from error
    except ResourceConflictError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


def _project_response(project: Any) -> ProjectResponse:
    return ProjectResponse.model_validate(project)


def _parcel_response(parcel: ParcelResult) -> ParcelResponse:
    return ParcelResponse.model_validate(parcel)
