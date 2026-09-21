"""Stable contracts deliberately published to other bounded contexts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol, runtime_checkable
from uuid import UUID

from .factor_labels import factor_display_label


class OwnedEvaluationNotFoundError(LookupError):
    """The evaluation does not exist for this owner."""


@runtime_checkable
class OwnedEvaluationResolver(Protocol):
    def resolve_owned_evaluation(self, owner_user_id: UUID, evaluation_id: UUID) -> None: ...


class FinalizedEvaluationNotFoundError(LookupError):
    """Published failure for a missing evaluation requested by another context."""


class FinalizedEvaluationNotReadyError(RuntimeError):
    """Published failure for an evaluation without finalized scenario evidence."""


class WaterRegime(StrEnum):
    """Published water-regime values shared with consumer bounded contexts."""

    RAINFED = "rainfed"
    IRRIGATED = "irrigated"


class FinalizedCropOutcomeStatus(StrEnum):
    SUCCEEDED = "succeeded"
    NO_COVERAGE = "no_coverage"
    FAILED = "failed"


class FinalizedLimitationEvidenceAvailability(StrEnum):
    AVAILABLE = "available"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class GetFinalizedEvaluationResult:
    evaluation_id: UUID
    water_regime: WaterRegime = WaterRegime.RAINFED


@dataclass(frozen=True, slots=True)
class FinalizedSuitabilitySummary:
    mean: float | None
    minimum: float | None
    maximum: float | None
    valid_cells: int
    valid_area_m2: float
    coverage_fraction: float
    zero_suitability_area_m2: float


@dataclass(frozen=True, slots=True)
class FinalizedScientificTrace:
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
class FinalizedLimitingFactorEvidence:
    factor_code: str
    label: str
    raw_code: int
    affected_cells: int
    affected_area_m2: float
    affected_fraction: float
    dominant: bool
    source_storage_reference: str | None
    source_sha256: str

    @property
    def display_label(self) -> str:
        return factor_display_label(self.factor_code, raw_label=self.label)


@dataclass(frozen=True, slots=True)
class FinalizedCropLimitationEvidence:
    availability: FinalizedLimitationEvidenceAvailability
    reason: str | None
    warnings: tuple[str, ...] = ()
    factors: tuple[FinalizedLimitingFactorEvidence, ...] = ()


DEFAULT_FINALIZED_UNAVAILABLE_LIMITATION_EVIDENCE = FinalizedCropLimitationEvidence(
    availability=FinalizedLimitationEvidenceAvailability.UNAVAILABLE,
    reason="limitation_evidence_not_persisted",
)


@dataclass(frozen=True, slots=True)
class FinalizedCropOutcome:
    crop_id: str
    status: FinalizedCropOutcomeStatus
    suitability: FinalizedSuitabilitySummary | None
    trace: FinalizedScientificTrace
    water_regime: WaterRegime = WaterRegime.RAINFED
    limitation_evidence: FinalizedCropLimitationEvidence = (
        DEFAULT_FINALIZED_UNAVAILABLE_LIMITATION_EVIDENCE
    )


@dataclass(frozen=True, slots=True)
class FinalizedEvaluationResult:
    evaluation_id: UUID
    water_regime: WaterRegime
    requested_crops: tuple[str, ...]
    project_id: UUID
    parcel_id: UUID
    parcel_version: int
    parcel_captured_at: datetime
    created_at: datetime
    outcomes: tuple[FinalizedCropOutcome, ...]
    common_support: FinalizedCommonSupport | None
    comparable_crops: tuple[FinalizedComparableCrop, ...]


@runtime_checkable
class FinalizedEvaluationResultReader(Protocol):
    """Public local interface for a future Decision Support consumer."""

    def get_finalized_evaluation_result(
        self, query: GetFinalizedEvaluationResult
    ) -> FinalizedEvaluationResult: ...

class FinalizedCommonSupportStatus(StrEnum):
    COMPARABLE = "comparable"
    NO_COMMON_COVERAGE = "no_common_coverage"
    NO_SUCCESSFUL_CROPS = "no_successful_crops"


@dataclass(frozen=True, slots=True)
class FinalizedCommonSupport:
    status: FinalizedCommonSupportStatus
    method: str | None
    area_crs: str | None
    parcel_area_m2: float
    common_valid_area_m2: float
    common_coverage_fraction: float
    eligible_crops: tuple[str, ...]
    excluded_without_coverage: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FinalizedComparableCrop:
    crop_id: str
    mean: float
    rank: int
