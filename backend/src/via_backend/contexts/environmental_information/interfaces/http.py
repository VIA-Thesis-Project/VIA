"""FastAPI resources for the Environmental Information vertical slice."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from ..application import (
    CheckDatasetVersionCoverage,
    CoverageUnavailableError,
    CreateDataset,
    CreateDatasetVersion,
    DatasetVersionCoverageResult,
    DatasetVersionResult,
    EnvironmentalInformationService,
    GetDataset,
    GetDatasetVersion,
    InvalidCommandError,
    ListDatasets,
    ListDatasetVersions,
    ResourceConflictError,
    ResourceNotFoundError,
)
from ..domain import CoverageClassification


class _RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CreateDatasetBody(_RequestModel):
    name: str = Field(min_length=1, max_length=120)
    source: str = Field(min_length=1, max_length=255)
    variable: str = Field(min_length=1, max_length=120)
    unit: str = Field(min_length=1, max_length=64)


class SpatialResolutionBody(_RequestModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    x: float = Field(gt=0)
    y: float = Field(gt=0)
    unit: str = Field(min_length=1, max_length=32)


class SpatialExtentBody(_RequestModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    west: float
    south: float
    east: float
    north: float


class CreateDatasetVersionBody(_RequestModel):
    version_identifier: str = Field(min_length=1, max_length=120)
    crs: str = Field(min_length=1, max_length=32)
    resolution: SpatialResolutionBody
    extent: SpatialExtentBody
    valid_from: date | None = None
    valid_to: date | None = None
    scenario: str | None = Field(default=None, min_length=1, max_length=120)
    checksum: str = Field(min_length=1, max_length=256)
    storage_reference: str = Field(min_length=1, max_length=1024)


class CoverageGeometryBody(_RequestModel):
    type: Literal["Polygon", "MultiPolygon"]
    coordinates: list[Any]


class CheckCoverageBody(_RequestModel):
    geometry: CoverageGeometryBody
    crs: str = Field(min_length=1, max_length=32)


class DatasetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    source: str
    variable: str
    unit: str
    created_at: datetime


class DatasetVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    dataset_id: UUID
    version_identifier: str
    crs: str
    resolution: SpatialResolutionBody
    extent: SpatialExtentBody
    valid_from: date | None
    valid_to: date | None
    scenario: str | None
    checksum: str
    storage_reference: str
    registered_at: datetime


class DatasetVersionCoverageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    dataset_id: UUID
    dataset_version_id: UUID
    compatible: bool
    coverage: CoverageClassification
    parcel_area_m2: float | None
    covered_area_m2: float | None
    coverage_percentage: float | None
    dataset_crs: str
    parcel_crs: str
    comparison_crs: str | None
    area_method: str | None
    transformations: list[str]
    warnings: list[str]
    reasons: list[str]


def create_router(service: EnvironmentalInformationService) -> APIRouter:
    """Create a router bound to the supplied application service."""
    router = APIRouter(prefix="/datasets", tags=["environmental-information"])

    @router.post(
        "",
        response_model=DatasetResponse,
        status_code=status.HTTP_201_CREATED,
        operation_id="create_dataset",
        description="Register environmental dataset identity and variable metadata.",
    )
    def create_dataset(body: CreateDatasetBody) -> DatasetResponse:
        result = _execute(
            service.create_dataset,
            CreateDataset(
                name=body.name,
                source=body.source,
                variable=body.variable,
                unit=body.unit,
            ),
        )
        return DatasetResponse.model_validate(result)

    @router.get(
        "",
        response_model=list[DatasetResponse],
        operation_id="list_datasets",
        description="List registered environmental datasets.",
    )
    def list_datasets() -> list[DatasetResponse]:
        return [
            DatasetResponse.model_validate(dataset)
            for dataset in _execute(service.list_datasets, ListDatasets())
        ]

    @router.get(
        "/{dataset_id}",
        response_model=DatasetResponse,
        operation_id="get_dataset",
        description="Read one environmental dataset.",
    )
    def get_dataset(dataset_id: UUID) -> DatasetResponse:
        result = _execute(service.get_dataset, GetDataset(dataset_id))
        return DatasetResponse.model_validate(result)

    @router.post(
        "/{dataset_id}/versions",
        response_model=DatasetVersionResponse,
        status_code=status.HTTP_201_CREATED,
        operation_id="create_dataset_version",
        description="Register an immutable environmental dataset version.",
    )
    def create_dataset_version(
        dataset_id: UUID, body: CreateDatasetVersionBody
    ) -> DatasetVersionResponse:
        result = _execute(
            service.create_dataset_version,
            CreateDatasetVersion(
                dataset_id=dataset_id,
                version_identifier=body.version_identifier,
                crs=body.crs,
                resolution_x=body.resolution.x,
                resolution_y=body.resolution.y,
                resolution_unit=body.resolution.unit,
                extent_west=body.extent.west,
                extent_south=body.extent.south,
                extent_east=body.extent.east,
                extent_north=body.extent.north,
                valid_from=body.valid_from,
                valid_to=body.valid_to,
                scenario=body.scenario,
                checksum=body.checksum,
                storage_reference=body.storage_reference,
            ),
        )
        return DatasetVersionResponse.model_validate(result)

    @router.get(
        "/{dataset_id}/versions",
        response_model=list[DatasetVersionResponse],
        operation_id="list_dataset_versions",
        description="List immutable versions registered for a dataset.",
    )
    def list_dataset_versions(dataset_id: UUID) -> list[DatasetVersionResponse]:
        return [
            DatasetVersionResponse.model_validate(version)
            for version in _execute(
                service.list_dataset_versions,
                ListDatasetVersions(dataset_id),
            )
        ]

    @router.get(
        "/{dataset_id}/versions/{version_id}",
        response_model=DatasetVersionResponse,
        operation_id="get_dataset_version",
        description="Read one exact environmental dataset version.",
    )
    def get_dataset_version(
        dataset_id: UUID, version_id: UUID
    ) -> DatasetVersionResponse:
        result: DatasetVersionResult = _execute(
            service.get_dataset_version,
            GetDatasetVersion(dataset_id, version_id),
        )
        return DatasetVersionResponse.model_validate(result)

    @router.post(
        "/{dataset_id}/versions/{version_id}/coverage",
        response_model=DatasetVersionCoverageResponse,
        operation_id="check_dataset_coverage",
        description=(
            "Check spatial compatibility and parcel coverage for one exact dataset version."
        ),
    )
    def check_dataset_version_coverage(
        dataset_id: UUID,
        version_id: UUID,
        body: CheckCoverageBody,
    ) -> DatasetVersionCoverageResponse:
        result: DatasetVersionCoverageResult = _execute(
            service.check_dataset_version_coverage,
            CheckDatasetVersionCoverage(
                dataset_id=dataset_id,
                version_id=version_id,
                geometry=body.geometry.model_dump(),
                geometry_crs=body.crs,
            ),
        )
        return DatasetVersionCoverageResponse.model_validate(result)

    return router


def _execute(operation: Any, message: Any) -> Any:
    try:
        return operation(message)
    except ResourceNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
        ) from error
    except InvalidCommandError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(error)
        ) from error
    except ResourceConflictError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(error)
        ) from error
    except CoverageUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)
        ) from error
