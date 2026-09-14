"""Read-only Application views for Agroclimatic Evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from ..domain.models import Evaluation, EvaluationStatus
from ..domain.outcomes import CropOutcomeStatus


class EvaluationResultAvailability(StrEnum):
    """Whether persisted outcomes are pending, partial, or final."""

    PENDING = "pending"
    PARTIAL = "partial"
    FINAL = "final"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class EvaluationStatusResult:
    evaluation_id: UUID
    status: EvaluationStatus
    requested_crops: tuple[str, ...]
    requested_crop_count: int
    completed_crop_count: int
    created_at: datetime
    project_id: UUID
    parcel_id: UUID
    parcel_version: int
    parcel_captured_at: datetime
    failed: bool

    @classmethod
    def from_domain(cls, evaluation: Evaluation) -> EvaluationStatusResult:
        snapshot = evaluation.parcel_snapshot
        return cls(
            evaluation_id=evaluation.id,
            status=evaluation.status,
            requested_crops=evaluation.requested_crops,
            requested_crop_count=len(evaluation.requested_crops),
            completed_crop_count=len(evaluation.outcomes),
            created_at=evaluation.created_at,
            project_id=snapshot.project_id,
            parcel_id=snapshot.parcel_id,
            parcel_version=snapshot.parcel_version,
            parcel_captured_at=snapshot.captured_at,
            failed=evaluation.status is EvaluationStatus.FAILED,
        )


@dataclass(frozen=True, slots=True)
class SuitabilitySummaryResult:
    mean: float | None
    minimum: float | None
    maximum: float | None
    valid_cells: int
    valid_area_m2: float
    coverage_fraction: float
    zero_suitability_area_m2: float


@dataclass(frozen=True, slots=True)
class PersistedCropOutcomeResult:
    crop_id: str
    status: CropOutcomeStatus
    suitability: SuitabilitySummaryResult | None


@dataclass(frozen=True, slots=True)
class EvaluationReadResult:
    evaluation_id: UUID
    evaluation_status: EvaluationStatus
    availability: EvaluationResultAvailability
    requested_crops: tuple[str, ...]
    requested_crop_count: int
    completed_crop_count: int
    outcomes: tuple[PersistedCropOutcomeResult, ...]

    @classmethod
    def from_domain(cls, evaluation: Evaluation) -> EvaluationReadResult:
        return cls(
            evaluation_id=evaluation.id,
            evaluation_status=evaluation.status,
            availability=_availability(evaluation),
            requested_crops=evaluation.requested_crops,
            requested_crop_count=len(evaluation.requested_crops),
            completed_crop_count=len(evaluation.outcomes),
            outcomes=tuple(
                PersistedCropOutcomeResult(
                    crop_id=outcome.crop_id,
                    status=outcome.status,
                    suitability=(
                        SuitabilitySummaryResult(
                            mean=outcome.suitability.mean,
                            minimum=outcome.suitability.minimum,
                            maximum=outcome.suitability.maximum,
                            valid_cells=outcome.suitability.valid_cells,
                            valid_area_m2=outcome.suitability.valid_area_m2,
                            coverage_fraction=outcome.suitability.coverage_fraction,
                            zero_suitability_area_m2=(outcome.suitability.zero_suitability_area_m2),
                        )
                        if outcome.suitability is not None
                        else None
                    ),
                )
                for outcome in evaluation.outcomes
            ),
        )


@dataclass(frozen=True, slots=True)
class ScientificTraceResult:
    engine_identifier: str
    started_at: datetime
    finished_at: datetime
    elapsed_seconds: float
    execution_mode: str
    parcel_sha256: str
    parameter_sha256: str | None
    configuration_sha256: str | None
    source_files_unchanged: bool


@dataclass(frozen=True, slots=True)
class CropEvidenceResult:
    crop_id: str
    status: CropOutcomeStatus
    trace: ScientificTraceResult


@dataclass(frozen=True, slots=True)
class EvaluationEvidenceResult:
    evaluation_id: UUID
    evaluation_status: EvaluationStatus
    availability: EvaluationResultAvailability
    evidence: tuple[CropEvidenceResult, ...]

    @classmethod
    def from_domain(cls, evaluation: Evaluation) -> EvaluationEvidenceResult:
        return cls(
            evaluation_id=evaluation.id,
            evaluation_status=evaluation.status,
            availability=_availability(evaluation),
            evidence=tuple(
                CropEvidenceResult(
                    crop_id=outcome.crop_id,
                    status=outcome.status,
                    trace=ScientificTraceResult(
                        engine_identifier=outcome.trace.engine_identifier,
                        started_at=outcome.trace.started_at,
                        finished_at=outcome.trace.finished_at,
                        elapsed_seconds=outcome.trace.elapsed_seconds,
                        execution_mode=outcome.trace.execution_mode,
                        parcel_sha256=outcome.trace.parcel_sha256,
                        parameter_sha256=outcome.trace.parameter_sha256,
                        configuration_sha256=outcome.trace.configuration_sha256,
                        source_files_unchanged=outcome.trace.source_files_unchanged,
                    ),
                )
                for outcome in evaluation.outcomes
            ),
        )


def _availability(evaluation: Evaluation) -> EvaluationResultAvailability:
    if evaluation.status is EvaluationStatus.SUCCEEDED:
        return EvaluationResultAvailability.FINAL
    if evaluation.status is EvaluationStatus.FAILED:
        return EvaluationResultAvailability.FAILED
    if evaluation.status is EvaluationStatus.CANCELLED:
        return EvaluationResultAvailability.CANCELLED
    if evaluation.outcomes:
        return EvaluationResultAvailability.PARTIAL
    return EvaluationResultAvailability.PENDING
