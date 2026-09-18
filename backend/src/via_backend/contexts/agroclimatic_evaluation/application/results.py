"""Transport-neutral Agroclimatic Evaluation results."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from ..domain.models import Evaluation, EvaluationStatus
from ..domain.outcomes import CropOutcomeStatus
from ..domain.water_regime import WaterRegime


@dataclass(frozen=True, slots=True)
class ParcelSnapshotResult:
    project_id: UUID
    parcel_id: UUID
    parcel_version: int
    geometry: Mapping[str, Any]
    crs: str
    captured_at: datetime


@dataclass(frozen=True, slots=True)
class CropOutcomeResult:
    crop_id: str
    status: CropOutcomeStatus
    mean: float | None
    failure_message: str | None
    execution_reference: str
    water_regime: WaterRegime = WaterRegime.RAINFED


@dataclass(frozen=True, slots=True)
class ActiveEvaluationResult:
    evaluation_id: UUID
    status: EvaluationStatus
    created_at: datetime
    requested_crop_count: int
    completed_crop_count: int
    requested_water_regimes: tuple[WaterRegime, ...]
    requested_execution_count: int
    completed_execution_count: int

    @classmethod
    def from_domain(cls, evaluation: Evaluation) -> ActiveEvaluationResult:
        return cls(
            evaluation_id=evaluation.id,
            status=evaluation.status,
            created_at=evaluation.created_at,
            requested_crop_count=len(evaluation.requested_crops),
            completed_crop_count=len(evaluation.outcomes),
            requested_water_regimes=evaluation.requested_water_regimes,
            requested_execution_count=len(evaluation.execution_matrix),
            completed_execution_count=len(evaluation.outcomes),
        )


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    id: UUID
    parcel_snapshot: ParcelSnapshotResult
    requested_crops: tuple[str, ...]
    requested_water_regimes: tuple[WaterRegime, ...]
    status: EvaluationStatus
    created_at: datetime
    outcomes: tuple[CropOutcomeResult, ...]
    failure_reason: str | None

    @classmethod
    def from_domain(cls, evaluation: Evaluation) -> EvaluationResult:
        snapshot = evaluation.parcel_snapshot
        return cls(
            id=evaluation.id,
            parcel_snapshot=ParcelSnapshotResult(
                project_id=snapshot.project_id,
                parcel_id=snapshot.parcel_id,
                parcel_version=snapshot.parcel_version,
                geometry=snapshot.geometry.to_geojson(),
                crs=snapshot.crs,
                captured_at=snapshot.captured_at,
            ),
            requested_crops=evaluation.requested_crops,
            requested_water_regimes=evaluation.requested_water_regimes,
            status=evaluation.status,
            created_at=evaluation.created_at,
            outcomes=tuple(
                CropOutcomeResult(
                    crop_id=outcome.crop_id,
                    status=outcome.status,
                    mean=(
                        outcome.suitability.mean
                        if outcome.suitability is not None
                        else None
                    ),
                    failure_message=outcome.failure_message,
                    execution_reference=outcome.trace.execution_reference,
                    water_regime=outcome.water_regime,
                )
                for outcome in evaluation.outcomes
            ),
            failure_reason=evaluation.failure_reason,
        )
