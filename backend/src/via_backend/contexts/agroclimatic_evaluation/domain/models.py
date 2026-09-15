"""Agroclimatic Evaluation aggregate."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from .comparison import (
    CommonSupport,
    CommonSupportStatus,
    ComparableCrop,
    validate_comparable_crops,
)
from .errors import DomainValidationError, InvalidEvaluationTransitionError
from .outcomes import CropOutcome, CropOutcomeStatus
from .snapshot import ParcelSnapshot


class EvaluationStatus(StrEnum):
    """Architecture-approved lifecycle vocabulary."""

    QUEUED = "queued"
    PREPARING = "preparing"
    RUNNING = "running"
    SUMMARIZING = "summarizing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class Evaluation:
    """An immutable multicrop evaluation and its scientific outcomes."""

    id: UUID
    parcel_snapshot: ParcelSnapshot
    requested_crops: tuple[str, ...]
    status: EvaluationStatus
    created_at: datetime
    outcomes: tuple[CropOutcome, ...] = ()
    common_support: CommonSupport | None = None
    comparable_crops: tuple[ComparableCrop, ...] = ()
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if isinstance(self.requested_crops, (str, bytes)):
            raise DomainValidationError("Requested crops must be a collection.")
        crops = tuple(self.requested_crops)
        if not crops:
            raise DomainValidationError("At least one crop must be requested.")
        for crop_id in crops:
            if not crop_id or crop_id != crop_id.strip():
                raise DomainValidationError(
                    "Crop identifiers must be non-empty and trimmed."
                )
            if len(crop_id) > 120:
                raise DomainValidationError(
                    "Crop identifiers must be at most 120 characters."
                )
        if len(set(crops)) != len(crops):
            raise DomainValidationError("Requested crop identifiers must be unique.")
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise DomainValidationError("Evaluation creation time must be timezone-aware.")
        outcomes = tuple(self.outcomes)
        outcome_crops = tuple(outcome.crop_id for outcome in outcomes)
        if outcome_crops != crops[: len(outcome_crops)]:
            raise DomainValidationError(
                "Crop outcomes must be a unique ordered prefix of requested crops."
            )
        if self.status in {EvaluationStatus.QUEUED, EvaluationStatus.PREPARING} and outcomes:
            raise DomainValidationError("An evaluation cannot have outcomes before running.")
        if self.status in {EvaluationStatus.SUMMARIZING, EvaluationStatus.SUCCEEDED} and (
            outcome_crops != crops
        ):
            raise DomainValidationError(
                "Summarizing and succeeded evaluations require one outcome per requested crop."
            )
        if self.status is EvaluationStatus.FAILED:
            if not self.failure_reason:
                raise DomainValidationError("A failed evaluation requires a failure reason.")
        elif self.failure_reason is not None:
            raise DomainValidationError(
                "Only a failed evaluation may retain an orchestration failure reason."
            )

        comparable_crops = tuple(self.comparable_crops)

        if comparable_crops:
            if self.common_support is None:
                raise DomainValidationError(
                    "Comparable crop results require common support."
                )

            validate_comparable_crops(
                self.common_support,
                comparable_crops,
            )
        object.__setattr__(
            self,
            "comparable_crops",
            comparable_crops,
        )
        object.__setattr__(self, "requested_crops", crops)
        object.__setattr__(self, "outcomes", outcomes)
        if self.status in {
            EvaluationStatus.QUEUED,
            EvaluationStatus.PREPARING,
            EvaluationStatus.RUNNING,
            EvaluationStatus.CANCELLED,
        } and self.common_support is not None:
            raise DomainValidationError(
            "Common support cannot exist before summarizing."
        )

    def prepare(self) -> Evaluation:
        return self._transition(EvaluationStatus.QUEUED, EvaluationStatus.PREPARING)

    def start_running(self) -> Evaluation:
        return self._transition(EvaluationStatus.PREPARING, EvaluationStatus.RUNNING)

    def record_outcome(self, outcome: CropOutcome) -> Evaluation:
        if self.status is not EvaluationStatus.RUNNING:
            raise InvalidEvaluationTransitionError(
                "Crop outcomes can only be recorded while an evaluation is running."
            )
        expected_index = len(self.outcomes)
        if expected_index >= len(self.requested_crops):
            raise InvalidEvaluationTransitionError(
                "Every requested crop already has an outcome."
            )
        if outcome.crop_id != self.requested_crops[expected_index]:
            raise InvalidEvaluationTransitionError(
                "Crop outcomes must follow the deterministic requested-crop order."
            )
        return replace(self, outcomes=(*self.outcomes, outcome))

    def start_summarizing(self) -> Evaluation:
        return self._transition(EvaluationStatus.RUNNING, EvaluationStatus.SUMMARIZING)

    def record_common_support(
        self,
        common_support: CommonSupport,
    ) -> Evaluation:
        if self.status is not EvaluationStatus.SUMMARIZING:
            raise InvalidEvaluationTransitionError(
                "Common support can only be recorded while summarizing."
            )

        if self.common_support is not None:
            raise InvalidEvaluationTransitionError(
                "Common support has already been recorded."
            )

        comparable_crops = tuple(
            outcome.crop_id
            for outcome in self.outcomes
            if outcome.status is not CropOutcomeStatus.FAILED
        )

        reported = (
            *common_support.eligible_crops,
            *common_support.excluded_without_coverage,
        )

        if set(reported) != set(comparable_crops):
            raise DomainValidationError(
                "Common support must partition every non-failed crop outcome."
            )

        if (
            common_support.status
            is CommonSupportStatus.NO_SUCCESSFUL_CROPS
            and comparable_crops
        ):
            raise DomainValidationError(
                "No-successful-crops requires every crop outcome to have failed."
            )

        if (
            common_support.status
            is not CommonSupportStatus.NO_SUCCESSFUL_CROPS
            and not comparable_crops
        ):
            raise DomainValidationError(
                "A spatial comparison requires at least one non-failed crop."
            )

        return replace(
            self,
            common_support=common_support,
        )

    def record_comparison(
        self,
        common_support: CommonSupport,
        comparable_crops: tuple[ComparableCrop, ...],
    ) -> Evaluation:
        if self.status is not EvaluationStatus.SUMMARIZING:
            raise InvalidEvaluationTransitionError(
                "Scientific comparison can only be recorded while summarizing."
            )

        if self.common_support is not None:
            raise InvalidEvaluationTransitionError(
                "Scientific comparison has already been recorded."
            )

        crops = tuple(comparable_crops)

        validate_comparable_crops(
            common_support,
            crops,
        )

        with_support = self.record_common_support(
            common_support
        )

        return replace(
            with_support,
            comparable_crops=crops,
        )
    
    def succeed(self) -> Evaluation:
        return self._transition(EvaluationStatus.SUMMARIZING, EvaluationStatus.SUCCEEDED)

    def fail(self, reason: str) -> Evaluation:
        if self.status not in {
            EvaluationStatus.PREPARING,
            EvaluationStatus.RUNNING,
            EvaluationStatus.SUMMARIZING,
        }:
            raise InvalidEvaluationTransitionError(
                f"Evaluation cannot fail from {self.status.value}."
            )
        reason = reason.strip()
        if not reason:
            raise DomainValidationError("An orchestration failure reason must be non-empty.")
        return replace(self, status=EvaluationStatus.FAILED, failure_reason=reason)

    def _transition(
        self, expected: EvaluationStatus, target: EvaluationStatus
    ) -> Evaluation:
        if self.status is not expected:
            raise InvalidEvaluationTransitionError(
                f"Evaluation cannot transition from {self.status.value} to {target.value}."
            )
        return replace(self, status=target)
