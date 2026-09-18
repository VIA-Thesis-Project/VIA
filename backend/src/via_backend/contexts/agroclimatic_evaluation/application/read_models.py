"""Read-only Application views for Agroclimatic Evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from ..domain.comparison import CommonSupportStatus
from ..domain.models import Evaluation, EvaluationStatus
from ..domain.outcomes import CropOutcomeStatus
from ..domain.water_regime import WaterRegime


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
    requested_water_regimes: tuple[WaterRegime, ...]
    requested_execution_count: int
    completed_execution_count: int
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
            requested_water_regimes=evaluation.requested_water_regimes,
            requested_execution_count=len(evaluation.execution_matrix),
            completed_execution_count=len(evaluation.outcomes),
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
    water_regime: WaterRegime = WaterRegime.RAINFED

@dataclass(frozen=True, slots=True)
class CommonSupportReadResult:
    status: CommonSupportStatus
    method: str | None
    area_crs: str | None
    parcel_area_m2: float
    common_valid_area_m2: float
    common_coverage_fraction: float
    eligible_crops: tuple[str, ...]
    excluded_without_coverage: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ComparableCropReadResult:
    crop_id: str
    mean: float
    rank: int


@dataclass(frozen=True, slots=True)
class ScenarioReadResult:
    """One independently summarized water-regime scenario.

    Irrigated means sufficient irrigation is assumed for scientific evaluation; it
    does not verify infrastructure or actual water availability.
    """

    water_regime: WaterRegime
    outcomes: tuple[PersistedCropOutcomeResult, ...]
    common_support: CommonSupportReadResult
    comparable_crops: tuple[ComparableCropReadResult, ...]

@dataclass(frozen=True, slots=True)
class EvaluationReadResult:
    evaluation_id: UUID
    evaluation_status: EvaluationStatus
    availability: EvaluationResultAvailability
    requested_crops: tuple[str, ...]
    requested_crop_count: int
    completed_crop_count: int
    requested_water_regimes: tuple[WaterRegime, ...]
    requested_execution_count: int
    completed_execution_count: int
    outcomes: tuple[PersistedCropOutcomeResult, ...]
    common_support: CommonSupportReadResult | None
    comparable_crops: tuple[ComparableCropReadResult, ...]
    scenarios: tuple[ScenarioReadResult, ...]

    @classmethod
    def from_domain(cls, evaluation: Evaluation) -> EvaluationReadResult:
        common_support = evaluation.common_support

        return cls(
            evaluation_id=evaluation.id,
            evaluation_status=evaluation.status,
            availability=_availability(evaluation),
            requested_crops=evaluation.requested_crops,
            requested_crop_count=len(evaluation.requested_crops),
            completed_crop_count=len(evaluation.outcomes),
            requested_water_regimes=evaluation.requested_water_regimes,
            requested_execution_count=len(evaluation.execution_matrix),
            completed_execution_count=len(evaluation.outcomes),
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
                            zero_suitability_area_m2=(
                                outcome.suitability.zero_suitability_area_m2
                            ),
                        )
                        if outcome.suitability is not None
                        else None
                    ),
                    water_regime=outcome.water_regime,
                )
                for outcome in evaluation.outcomes
            ),
            common_support=(
                CommonSupportReadResult(
                    status=common_support.status,
                    method=common_support.method,
                    area_crs=common_support.area_crs,
                    parcel_area_m2=common_support.parcel_area_m2,
                    common_valid_area_m2=common_support.common_valid_area_m2,
                    common_coverage_fraction=(
                        common_support.common_coverage_fraction
                    ),
                    eligible_crops=common_support.eligible_crops,
                    excluded_without_coverage=(
                        common_support.excluded_without_coverage
                    ),
                )
                if common_support is not None
                else None
            ),
            comparable_crops=tuple(
                ComparableCropReadResult(
                    crop_id=crop.crop_id,
                    mean=crop.mean,
                    rank=crop.rank,
                )
                for crop in evaluation.comparable_crops
            ),
            scenarios=tuple(
                ScenarioReadResult(
                    water_regime=scenario.water_regime,
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
                                    zero_suitability_area_m2=(
                                        outcome.suitability.zero_suitability_area_m2
                                    ),
                                )
                                if outcome.suitability is not None
                                else None
                            ),
                            water_regime=outcome.water_regime,
                        )
                        for outcome in evaluation.outcomes
                        if outcome.water_regime is scenario.water_regime
                    ),
                    common_support=CommonSupportReadResult(
                        status=scenario.common_support.status,
                        method=scenario.common_support.method,
                        area_crs=scenario.common_support.area_crs,
                        parcel_area_m2=scenario.common_support.parcel_area_m2,
                        common_valid_area_m2=scenario.common_support.common_valid_area_m2,
                        common_coverage_fraction=(
                            scenario.common_support.common_coverage_fraction
                        ),
                        eligible_crops=scenario.common_support.eligible_crops,
                        excluded_without_coverage=(
                            scenario.common_support.excluded_without_coverage
                        ),
                    ),
                    comparable_crops=tuple(
                        ComparableCropReadResult(
                            crop_id=crop.crop_id,
                            mean=crop.mean,
                            rank=crop.rank,
                        )
                        for crop in scenario.comparable_crops
                    ),
                )
                for scenario in evaluation.scenarios
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
    source_sha256: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CropEvidenceResult:
    crop_id: str
    status: CropOutcomeStatus
    trace: ScientificTraceResult
    water_regime: WaterRegime = WaterRegime.RAINFED


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
                    water_regime=outcome.water_regime,
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
                        source_sha256=tuple(
                            fingerprint.sha256
                            for fingerprint in outcome.trace.source_fingerprints
                        ),
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
