"""FastAPI resources for Agroclimatic Evaluation requests and reads."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from via_backend.contexts.identity_access.application.public import AuthenticatedPrincipal

from ..application.commands import (
    EnvironmentalInputReferenceInput,
    ParcelReferenceInput,
    RequestEvaluation,
)
from ..application.queries import (
    GetEvaluation,
    GetEvaluationEvidence,
    GetEvaluationLimitations,
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
from ..domain.outcomes import (
    CropOutcomeStatus,
    LimitationEvidenceAvailability,
)
from ..domain.water_regime import WaterRegime


class _RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ParcelReferenceBody(_RequestModel):
    project_id: UUID
    parcel_id: UUID
    parcel_version: int = Field(gt=0)


class EnvironmentalInputReferenceBody(_RequestModel):
    input_key: str
    dataset_id: UUID
    dataset_version_id: UUID


class RequestEvaluationBody(_RequestModel):
    parcel_reference: ParcelReferenceBody
    requested_crops: list[str] = Field(min_length=1)
    water_regimes: list[WaterRegime] = Field(
        default_factory=lambda: [WaterRegime.RAINFED],
        min_length=1,
    )
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
    requested_water_regimes: list[WaterRegime]
    status: EvaluationStatus
    created_at: datetime


class EvaluationStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    evaluation_id: UUID
    status: EvaluationStatus
    requested_crops: list[str]
    requested_crop_count: int
    completed_crop_count: int
    requested_water_regimes: list[WaterRegime]
    requested_execution_count: int
    completed_execution_count: int
    created_at: datetime
    project_id: UUID
    parcel_id: UUID
    parcel_version: int
    parcel_captured_at: datetime
    failed: bool


class SuitabilitySummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mean: float | None = Field(ge=0, le=100)
    minimum: float | None = Field(ge=0, le=100)
    maximum: float | None = Field(ge=0, le=100)
    valid_cells: int
    valid_area_m2: float
    coverage_fraction: float = Field(
        ge=0,
        le=1,
        description=(
            "Fraction of parcel area with valid scientific cells. No-data is excluded; "
            "a valid suitability score of 0 is not no-data."
        ),
    )
    zero_suitability_area_m2: float


class CropOutcomeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    crop_id: str
    water_regime: WaterRegime
    status: CropOutcomeStatus
    suitability: SuitabilitySummaryResponse | None

class CommonSupportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: CommonSupportStatus
    method: str | None
    area_crs: str | None
    parcel_area_m2: float
    common_valid_area_m2: float
    common_coverage_fraction: float = Field(ge=0, le=1)
    eligible_crops: list[str]
    excluded_without_coverage: list[str]


class ComparableCropResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    crop_id: str
    mean: float
    rank: int = Field(
        description="Comparable ranking on common valid support; use this list for rankings."
    )


class ScenarioResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    water_regime: WaterRegime
    outcomes: list[CropOutcomeResponse]
    common_support: CommonSupportResponse
    comparable_crops: list[ComparableCropResponse]

class EvaluationResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    evaluation_id: UUID
    evaluation_status: EvaluationStatus
    availability: EvaluationResultAvailability
    requested_crops: list[str]
    requested_crop_count: int
    completed_crop_count: int
    requested_water_regimes: list[WaterRegime]
    requested_execution_count: int
    completed_execution_count: int
    outcomes: list[CropOutcomeResponse]
    common_support: CommonSupportResponse | None
    comparable_crops: list[ComparableCropResponse]
    scenarios: list[ScenarioResultResponse]


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
    water_regime: WaterRegime
    status: CropOutcomeStatus
    trace: ScientificTraceResponse


class EvaluationEvidenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    evaluation_id: UUID
    evaluation_status: EvaluationStatus
    availability: EvaluationResultAvailability
    evidence: list[CropEvidenceResponse]


class LimitingFactorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    factor_code: str
    label: str
    display_label: str
    raw_code: int
    affected_cells: int
    affected_area_m2: float
    affected_fraction: float = Field(
        ge=0,
        le=1,
        description="Fraction of the valid analyzed area affected by this factor.",
    )
    dominant: bool
    source_storage_reference: str | None
    source_sha256: str


class LimitationEvidenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    availability: LimitationEvidenceAvailability
    reason: str | None
    warnings: list[str]
    factors: list[LimitingFactorResponse]


class CropLimitationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    crop_id: str
    water_regime: WaterRegime
    status: CropOutcomeStatus
    suitability: SuitabilitySummaryResponse | None
    limitation_evidence: LimitationEvidenceResponse


class EvaluationLimitationsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    evaluation_id: UUID
    evaluation_status: EvaluationStatus
    availability: EvaluationResultAvailability
    limitations: list[CropLimitationResponse]


def create_router(
    service: AgroclimaticEvaluationService,
    principal_resolver: Callable[..., AuthenticatedPrincipal],
) -> APIRouter:
    """Create a router bound to the supplied evaluation application service."""
    router = APIRouter(prefix="/evaluations", tags=["agroclimatic-evaluation"])
    principal_dependency = Depends(principal_resolver)

    @router.post(
        "",
        response_model=EvaluationResponse,
        status_code=status.HTTP_201_CREATED,
        operation_id="request_evaluation",
        description=(
            "Queue an asynchronous evaluation for exact parcel and dataset versions. "
            "Rainfed and irrigated are distinct scientific scenarios; irrigated does not "
            "confirm real water or irrigation-infrastructure availability."
        ),
    )
    def request_evaluation(
        body: RequestEvaluationBody,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> EvaluationResponse:
        reference = body.parcel_reference
        result = _execute(
            service.request_evaluation,
            RequestEvaluation(
                owner_user_id=principal.user_id,
                parcel_reference=ParcelReferenceInput(
                    project_id=reference.project_id,
                    parcel_id=reference.parcel_id,
                    parcel_version=reference.parcel_version,
                ),
                requested_crops=tuple(body.requested_crops),
                requested_water_regimes=tuple(body.water_regimes),
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

    @router.get(
        "",
        response_model=list[EvaluationResponse],
        operation_id="list_evaluations",
        description="List submitted evaluations without waiting for scientific execution.",
    )
    def list_evaluations(
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> list[EvaluationResponse]:
        return [
            EvaluationResponse.model_validate(evaluation)
            for evaluation in _execute(
                service.list_evaluations,
                ListEvaluations(principal.user_id),
            )
        ]

    @router.get(
        "/{evaluation_id}/result",
        response_model=EvaluationResultResponse,
        operation_id="get_evaluation_result",
        description=(
            "Read per-crop suitability in the 0..100 scale. coverage_fraction is 0..1; "
            "null/no_coverage is not suitability 0. Use comparable_crops, not raw means, "
            "for rankings across crops."
        ),
    )
    def get_evaluation_result(
        evaluation_id: UUID,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> EvaluationResultResponse:
        result = _execute(
            service.get_evaluation_result,
            GetEvaluationResult(evaluation_id, principal.user_id),
        )
        return EvaluationResultResponse.model_validate(result)

    @router.get(
        "/{evaluation_id}/evidence",
        response_model=EvaluationEvidenceResponse,
        operation_id="get_evaluation_evidence",
        description="Read safe scientific trace evidence without internal storage paths.",
    )
    def get_evaluation_evidence(
        evaluation_id: UUID,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> EvaluationEvidenceResponse:
        result = _execute(
            service.get_evaluation_evidence,
            GetEvaluationEvidence(evaluation_id, principal.user_id),
        )
        return EvaluationEvidenceResponse.model_validate(result)

    @router.get(
        "/{evaluation_id}/limitations",
        response_model=EvaluationLimitationsResponse,
        operation_id="get_evaluation_limitations",
        description=(
            "Read limiting factors. affected_fraction is in 0..1 and remains distinct "
            "from no-data or no coverage."
        ),
    )
    def get_evaluation_limitations(
        evaluation_id: UUID,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> EvaluationLimitationsResponse:
        result = _execute(
            service.get_evaluation_limitations,
            GetEvaluationLimitations(evaluation_id, principal.user_id),
        )
        return EvaluationLimitationsResponse.model_validate(result)

    @router.get(
        "/{evaluation_id}",
        response_model=EvaluationStatusResponse,
        operation_id="get_evaluation",
        description="Poll evaluation lifecycle and per-scenario completion counts.",
    )
    def get_evaluation(
        evaluation_id: UUID,
        principal: AuthenticatedPrincipal = principal_dependency,
    ) -> EvaluationStatusResponse:
        result = _execute(
            service.get_evaluation,
            GetEvaluation(evaluation_id, principal.user_id),
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
