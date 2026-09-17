"""FastAPI resources for Agroclimatic Evaluation requests and reads."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from ..application.commands import (
    EnvironmentalInputReferenceInput,
    ParcelSnapshotInput,
    RequestEvaluation,
)
from ..application.queries import (
    GetEvaluation,
    GetEvaluationEvidence,
    GetEvaluationResult,
    ListEvaluations,
)
from ..application.read_models import EvaluationResultAvailability
from ..application.service import (
    AgroclimaticEvaluationService,
    InvalidCommandError,
    ResourceConflictError,
    ResourceNotFoundError,
)
from ..domain.comparison import CommonSupportStatus
from ..domain.models import EvaluationStatus
from ..domain.outcomes import CropOutcomeStatus


class _RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SnapshotGeometryBody(_RequestModel):
    type: Literal["Polygon", "MultiPolygon"]
    coordinates: list[Any]


class ParcelSnapshotBody(_RequestModel):
    project_id: UUID
    parcel_id: UUID
    parcel_version: int = Field(gt=0)
    geometry: SnapshotGeometryBody
    crs: str = Field(min_length=1, max_length=32)
    captured_at: datetime


class EnvironmentalInputReferenceBody(_RequestModel):
    input_key: str
    dataset_id: UUID
    dataset_version_id: UUID


class RequestEvaluationBody(_RequestModel):
    parcel_snapshot: ParcelSnapshotBody
    requested_crops: list[str] = Field(min_length=1)
    environmental_inputs: list[EnvironmentalInputReferenceBody] = Field(min_length=1)


class SnapshotGeometryResponse(BaseModel):
    type: Literal["Polygon", "MultiPolygon"]
    coordinates: list[Any]


class ParcelSnapshotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: UUID
    parcel_id: UUID
    parcel_version: int
    geometry: SnapshotGeometryResponse
    crs: str
    captured_at: datetime


class EvaluationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    parcel_snapshot: ParcelSnapshotResponse
    requested_crops: list[str]
    status: EvaluationStatus
    created_at: datetime


class EvaluationStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    evaluation_id: UUID
    status: EvaluationStatus
    requested_crops: list[str]
    requested_crop_count: int
    completed_crop_count: int
    created_at: datetime
    project_id: UUID
    parcel_id: UUID
    parcel_version: int
    parcel_captured_at: datetime
    failed: bool


class SuitabilitySummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mean: float | None
    minimum: float | None
    maximum: float | None
    valid_cells: int
    valid_area_m2: float
    coverage_fraction: float
    zero_suitability_area_m2: float


class CropOutcomeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    crop_id: str
    status: CropOutcomeStatus
    suitability: SuitabilitySummaryResponse | None

class CommonSupportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: CommonSupportStatus
    method: str | None
    area_crs: str | None
    parcel_area_m2: float
    common_valid_area_m2: float
    common_coverage_fraction: float
    eligible_crops: list[str]
    excluded_without_coverage: list[str]


class ComparableCropResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    crop_id: str
    mean: float
    rank: int

class EvaluationResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    evaluation_id: UUID
    evaluation_status: EvaluationStatus
    availability: EvaluationResultAvailability
    requested_crops: list[str]
    requested_crop_count: int
    completed_crop_count: int
    outcomes: list[CropOutcomeResponse]
    common_support: CommonSupportResponse | None
    comparable_crops: list[ComparableCropResponse]


class ScientificTraceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    engine_identifier: str
    started_at: datetime
    finished_at: datetime
    elapsed_seconds: float
    execution_mode: str
    parcel_sha256: str
    parameter_sha256: str | None
    configuration_sha256: str | None
    source_files_unchanged: bool
    source_sha256: list[str]


class CropEvidenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    crop_id: str
    status: CropOutcomeStatus
    trace: ScientificTraceResponse


class EvaluationEvidenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    evaluation_id: UUID
    evaluation_status: EvaluationStatus
    availability: EvaluationResultAvailability
    evidence: list[CropEvidenceResponse]


def create_router(service: AgroclimaticEvaluationService) -> APIRouter:
    """Create a router bound to the supplied evaluation application service."""
    router = APIRouter(prefix="/evaluations", tags=["agroclimatic-evaluation"])

    @router.post(
        "",
        response_model=EvaluationResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def request_evaluation(body: RequestEvaluationBody) -> EvaluationResponse:
        snapshot = body.parcel_snapshot
        result = _execute(
            service.request_evaluation,
            RequestEvaluation(
                parcel_snapshot=ParcelSnapshotInput(
                    project_id=snapshot.project_id,
                    parcel_id=snapshot.parcel_id,
                    parcel_version=snapshot.parcel_version,
                    geometry=snapshot.geometry.model_dump(),
                    crs=snapshot.crs,
                    captured_at=snapshot.captured_at,
                ),
                requested_crops=tuple(body.requested_crops),
                environmental_inputs=tuple(
                    EnvironmentalInputReferenceInput(
                        input_key=item.input_key,
                        dataset_id=item.dataset_id,
                        dataset_version_id=item.dataset_version_id,
                    )
                    for item in body.environmental_inputs
                ),
            ),
        )
        return EvaluationResponse.model_validate(result)

    @router.get("", response_model=list[EvaluationResponse])
    def list_evaluations() -> list[EvaluationResponse]:
        return [
            EvaluationResponse.model_validate(evaluation)
            for evaluation in _execute(
                service.list_evaluations,
                ListEvaluations(),
            )
        ]

    @router.get("/{evaluation_id}/result", response_model=EvaluationResultResponse)
    def get_evaluation_result(evaluation_id: UUID) -> EvaluationResultResponse:
        result = _execute(
            service.get_evaluation_result,
            GetEvaluationResult(evaluation_id),
        )
        return EvaluationResultResponse.model_validate(result)

    @router.get("/{evaluation_id}/evidence", response_model=EvaluationEvidenceResponse)
    def get_evaluation_evidence(evaluation_id: UUID) -> EvaluationEvidenceResponse:
        result = _execute(
            service.get_evaluation_evidence,
            GetEvaluationEvidence(evaluation_id),
        )
        return EvaluationEvidenceResponse.model_validate(result)

    @router.get("/{evaluation_id}", response_model=EvaluationStatusResponse)
    def get_evaluation(evaluation_id: UUID) -> EvaluationStatusResponse:
        result = _execute(
            service.get_evaluation,
            GetEvaluation(evaluation_id),
        )
        return EvaluationStatusResponse.model_validate(result)

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
