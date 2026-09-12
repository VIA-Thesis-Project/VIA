"""FastAPI resources for the Farm Management vertical slice."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

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


def create_router(service: FarmManagementService) -> APIRouter:
    """Create a router bound to the supplied application service."""
    router = APIRouter(prefix="/projects", tags=["farm-management"])

    @router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
    def create_project(body: CreateProjectBody) -> ProjectResponse:
        return _project_response(_execute(service.create_project, CreateProject(name=body.name)))

    @router.get("", response_model=list[ProjectResponse])
    def list_projects() -> list[ProjectResponse]:
        return [
            _project_response(project)
            for project in _execute(service.list_projects, ListProjects())
        ]

    @router.get("/{project_id}", response_model=ProjectResponse)
    def get_project(project_id: UUID) -> ProjectResponse:
        return _project_response(_execute(service.get_project, GetProject(project_id)))

    @router.post(
        "/{project_id}/parcels",
        response_model=ParcelResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_parcel(project_id: UUID, body: CreateParcelBody) -> ParcelResponse:
        parcel = _execute(
            service.create_parcel,
            CreateParcel(
                project_id=project_id,
                name=body.name,
                geometry=body.geometry.model_dump(),
            ),
        )
        return _parcel_response(parcel)

    @router.get("/{project_id}/parcels", response_model=list[ParcelResponse])
    def list_parcels(project_id: UUID) -> list[ParcelResponse]:
        return [
            _parcel_response(parcel)
            for parcel in _execute(service.list_parcels, ListParcels(project_id))
        ]

    @router.get("/{project_id}/parcels/{parcel_id}", response_model=ParcelResponse)
    def get_parcel(project_id: UUID, parcel_id: UUID) -> ParcelResponse:
        parcel = _execute(service.get_parcel, GetParcel(project_id, parcel_id))
        return _parcel_response(parcel)

    @router.post(
        "/{project_id}/parcels/{parcel_id}/versions",
        response_model=ParcelResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def revise_parcel_geometry(
        project_id: UUID,
        parcel_id: UUID,
        body: ReviseParcelGeometryBody,
    ) -> ParcelResponse:
        parcel = _execute(
            service.revise_parcel_geometry,
            ReviseParcelGeometry(
                project_id=project_id,
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
