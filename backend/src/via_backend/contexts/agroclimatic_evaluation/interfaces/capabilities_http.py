"""HTTP discovery contract for configured evaluation capabilities."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from ..application.capabilities import (
    CapabilityStatus,
    EvaluationCapabilitiesService,
    EvaluationCapabilitiesUnavailableError,
)
from ..domain.water_regime import WaterRegime


class CropEvaluationCapabilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    crop_id: str = Field(description="Identifier accepted in requested_crops.")
    display_name: str | None = Field(
        description="Canonical engine name when the selected catalog provides one."
    )
    water_regimes: list[WaterRegime] = Field(
        description="Scientific scenarios supported for this crop."
    )


class ScientificallyBoundDatasetVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    dataset_id: UUID = Field(
        description="Registered dataset identity associated with the scientific binding."
    )
    dataset_version_id: UUID = Field(
        description=(
            "Exact dataset version configured with a scientific binding "
            "for this deployment."
        )
    )


class EnvironmentalInputCapabilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    minimum_count: int = Field(
        description="Minimum environmental_inputs entries required."
    )
    maximum_input_key_length: int
    input_keys: list[str] = Field(
        description=(
            "Reserved canonical input keys. Empty because input_key values are "
            "caller-defined logical identifiers."
        )
    )
    input_key_discovery: str = Field(
        description=(
            "'arbitrary_unique' means callers create their own unique logical "
            "input_key values; the key does not select the scientific binding."
        )
    )
    requires_registered_dataset_version: bool
    requires_scientific_binding: bool
    scientifically_bound_dataset_versions: list[
        ScientificallyBoundDatasetVersionResponse
    ] = Field(
        description=(
            "Dataset versions configured with scientific bindings in this deployment. "
            "This does not guarantee that later runtime integrity checks will succeed."
        )
    )


class EvaluationCapabilitiesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: CapabilityStatus
    crops: list[CropEvaluationCapabilityResponse]
    environmental_inputs: EnvironmentalInputCapabilityResponse
    limitations: list[str]


def create_capabilities_router(
    service: EvaluationCapabilitiesService,
) -> APIRouter:
    router = APIRouter(tags=["agroclimatic-evaluation"])

    @router.get(
        "/evaluation-capabilities",
        response_model=EvaluationCapabilitiesResponse,
        operation_id="get_evaluation_capabilities",
        description=(
            "Discover the deployment-selected crop catalog, valid rainfed/irrigated "
            "scenarios, and dataset versions configured with scientific input bindings. "
            "Environmental input_key values are caller-defined unique logical identifiers. "
            "Irrigated is a scientific scenario and does not confirm water or "
            "infrastructure availability."
        ),
    )
    def get_evaluation_capabilities() -> EvaluationCapabilitiesResponse:
        try:
            result = service.get_capabilities()
        except EvaluationCapabilitiesUnavailableError as error:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(error),
            ) from error

        return EvaluationCapabilitiesResponse.model_validate(result)

    return router
