"""FastAPI resources for Agroclimatic Evaluation requests."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from ..application.commands import ParcelSnapshotInput, RequestEvaluation
from ..application.queries import GetEvaluation, ListEvaluations
from ..application.service import (
    AgroclimaticEvaluationService,
    InvalidCommandError,
    ResourceConflictError,
    ResourceNotFoundError,
)
from ..domain.models import EvaluationStatus


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


class RequestEvaluationBody(_RequestModel):
    parcel_snapshot: ParcelSnapshotBody
    requested_crops: list[str] = Field(min_length=1)


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

    @router.get("/{evaluation_id}", response_model=EvaluationResponse)
    def get_evaluation(evaluation_id: UUID) -> EvaluationResponse:
        result = _execute(
            service.get_evaluation,
            GetEvaluation(evaluation_id),
        )
        return EvaluationResponse.model_validate(result)

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
