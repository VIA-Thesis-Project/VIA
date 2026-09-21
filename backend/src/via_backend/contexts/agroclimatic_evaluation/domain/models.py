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
from .environmental_inputs import EnvironmentalInputManifest, EnvironmentalInputReference
from .errors import DomainValidationError, InvalidEvaluationTransitionError
from .outcomes import CropOutcome, CropOutcomeStatus
from .snapshot import ParcelSnapshot
from .water_regime import WaterRegime


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
class EvaluationScenarioResult:
    """Per-water-regime scientific comparison kept separate from other scenarios."""

    water_regime: WaterRegime
    common_support: CommonSupport
    comparable_crops: tuple[ComparableCrop, ...] = ()

    def __post_init__(self) -> None:
        try:
            regime = WaterRegime(self.water_regime)
        except ValueError as error:
            raise DomainValidationError("Evaluation water regime is not supported.") from error
        crops = tuple(self.comparable_crops)
        if crops or self.common_support.status is not CommonSupportStatus.COMPARABLE:
            validate_comparable_crops(self.common_support, crops)
        object.__setattr__(self, "water_regime", regime)
        object.__setattr__(self, "comparable_crops", crops)


@dataclass(frozen=True, slots=True)
class Evaluation:
    """An immutable multicrop evaluation and its scientific outcomes."""

    id: UUID
    parcel_snapshot: ParcelSnapshot
    requested_crops: tuple[str, ...]
    status: EvaluationStatus
    created_at: datetime
    owner_user_id: UUID | None = None
    environmental_input_references: tuple[EnvironmentalInputReference, ...] = ()
    environmental_input_manifest: EnvironmentalInputManifest | None = None
    requested_water_regimes: tuple[WaterRegime, ...] = (WaterRegime.RAINFED,)
    outcomes: tuple[CropOutcome, ...] = ()
    scenarios: tuple[EvaluationScenarioResult, ...] = ()
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
        if isinstance(self.requested_water_regimes, (str, bytes)):
            raise DomainValidationError("Requested water regimes must be a collection.")
        try:
            water_regimes = tuple(
                WaterRegime(regime) for regime in self.requested_water_regimes
            )
        except ValueError as error:
            raise DomainValidationError("Requested water regime is not supported.") from error
        if not water_regimes:
            raise DomainValidationError("At least one water regime must be requested.")
        if len(set(water_regimes)) != len(water_regimes):
            raise DomainValidationError("Requested water regimes must be unique.")
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise DomainValidationError("Evaluation creation time must be timezone-aware.")

        environmental_input_references = tuple(self.environmental_input_references)
        reference_keys = tuple(reference.input_key for reference in environmental_input_references)
        if len(set(reference_keys)) != len(reference_keys):
            raise DomainValidationError(
                "Environmental input keys must be unique within an evaluation request."
            )
        object.__setattr__(
            self,
            "environmental_input_references",
            environmental_input_references,
        )

        if self.environmental_input_manifest is not None:
            if not environmental_input_references:
                raise DomainValidationError(
                    "Environmental input manifest requires requested environmental inputs."
                )
            snapshots = self.environmental_input_manifest.inputs
            if len(snapshots) != len(environmental_input_references) or any(
                reference.input_key != snapshot.input_key
                or reference.dataset_id != snapshot.dataset_id
                or reference.dataset_version_id != snapshot.dataset_version_id
                for reference, snapshot in zip(
                    environmental_input_references,
                    snapshots,
                    strict=True,
                )
            ):
                raise DomainValidationError(
                    "Environmental input manifest must exactly match requested references in order."
                )
        outcomes = tuple(self.outcomes)
        execution_matrix = tuple(
            (crop_id, water_regime)
            for crop_id in crops
            for water_regime in water_regimes
        )
        outcome_identities = tuple(
            (outcome.crop_id, outcome.water_regime) for outcome in outcomes
        )
        if outcome_identities != execution_matrix[: len(outcome_identities)]:
            raise DomainValidationError(
                "Crop outcomes must be a unique ordered prefix of the execution matrix."
            )
        if self.status in {EvaluationStatus.QUEUED, EvaluationStatus.PREPARING} and outcomes:
            raise DomainValidationError("An evaluation cannot have outcomes before running.")
        if self.status in {EvaluationStatus.SUMMARIZING, EvaluationStatus.SUCCEEDED} and (
            outcome_identities != execution_matrix
        ):
            raise DomainValidationError(
                "Summarizing and succeeded evaluations require one outcome per "
                "requested scenario execution."
            )
        if self.status is EvaluationStatus.FAILED:
            if not self.failure_reason:
                raise DomainValidationError("A failed evaluation requires a failure reason.")
        elif self.failure_reason is not None:
            raise DomainValidationError(
                "Only a failed evaluation may retain an orchestration failure reason."
            )

        scenarios = tuple(self.scenarios)
        scenario_regimes = tuple(scenario.water_regime for scenario in scenarios)
        if scenario_regimes != water_regimes[: len(scenario_regimes)]:
            raise DomainValidationError(
                "Scenario comparisons must follow requested water-regime order."
            )
        if (
            self.status is EvaluationStatus.SUCCEEDED
            and scenarios
            and scenario_regimes != water_regimes
        ):
            raise DomainValidationError(
                "A succeeded evaluation requires one comparison per requested water regime."
            )
        object.__setattr__(self, "requested_crops", crops)
        object.__setattr__(self, "requested_water_regimes", water_regimes)
        object.__setattr__(self, "outcomes", outcomes)
        object.__setattr__(self, "scenarios", scenarios)
        if self.status in {
            EvaluationStatus.QUEUED,
            EvaluationStatus.PREPARING,
            EvaluationStatus.RUNNING,
            EvaluationStatus.CANCELLED,
        } and scenarios:
            raise DomainValidationError(
                "Scenario comparisons cannot exist before summarizing."
            )

    @property
    def execution_matrix(self) -> tuple[tuple[str, WaterRegime], ...]:
        return tuple(
            (crop_id, water_regime)
            for crop_id in self.requested_crops
            for water_regime in self.requested_water_regimes
        )

    def scenario_for(self, water_regime: WaterRegime) -> EvaluationScenarioResult | None:
        regime = WaterRegime(water_regime)
        return next(
            (scenario for scenario in self.scenarios if scenario.water_regime is regime),
            None,
        )

    @property
    def common_support(self) -> CommonSupport | None:
        scenario = self.scenario_for(WaterRegime.RAINFED)
        return scenario.common_support if scenario is not None else None

    @property
    def comparable_crops(self) -> tuple[ComparableCrop, ...]:
        scenario = self.scenario_for(WaterRegime.RAINFED)
        return scenario.comparable_crops if scenario is not None else ()

    def prepare(self) -> Evaluation:
        return self._transition(EvaluationStatus.QUEUED, EvaluationStatus.PREPARING)

    def attach_environmental_input_manifest(
        self,
        manifest: EnvironmentalInputManifest,
    ) -> Evaluation:
        if self.status is not EvaluationStatus.PREPARING:
            raise InvalidEvaluationTransitionError(
                "Environmental input manifest can only be attached while preparing."
            )
        if not self.environmental_input_references:
            raise InvalidEvaluationTransitionError(
                "Environmental input manifest requires requested environmental inputs."
            )
        if self.environmental_input_manifest is not None:
            raise InvalidEvaluationTransitionError(
                "Environmental input manifest has already been attached."
            )
        return replace(self, environmental_input_manifest=manifest)

    def start_running(self) -> Evaluation:
        if self.status is EvaluationStatus.PREPARING and self.environmental_input_manifest is None:
            raise InvalidEvaluationTransitionError(
                "Evaluation cannot start running without an environmental input manifest."
            )
        return self._transition(EvaluationStatus.PREPARING, EvaluationStatus.RUNNING)

    def record_outcome(self, outcome: CropOutcome) -> Evaluation:
        if self.status is not EvaluationStatus.RUNNING:
            raise InvalidEvaluationTransitionError(
                "Crop outcomes can only be recorded while an evaluation is running."
            )
        expected_index = len(self.outcomes)
        execution_matrix = self.execution_matrix
        if expected_index >= len(execution_matrix):
            raise InvalidEvaluationTransitionError(
                "Every requested scenario execution already has an outcome."
            )
        if (outcome.crop_id, outcome.water_regime) != execution_matrix[expected_index]:
            raise InvalidEvaluationTransitionError(
                "Crop outcomes must follow deterministic crop-major water-regime order."
            )
        return replace(self, outcomes=(*self.outcomes, outcome))

    def start_summarizing(self) -> Evaluation:
        return self._transition(EvaluationStatus.RUNNING, EvaluationStatus.SUMMARIZING)

    def record_common_support(
        self,
        common_support: CommonSupport,
        *,
        water_regime: WaterRegime = WaterRegime.RAINFED,
    ) -> Evaluation:
        if self.status is not EvaluationStatus.SUMMARIZING:
            raise InvalidEvaluationTransitionError(
                "Common support can only be recorded while summarizing."
            )

        regime = WaterRegime(water_regime)
        if regime not in self.requested_water_regimes:
            raise DomainValidationError("Water regime was not requested for this evaluation.")
        if self.scenario_for(regime) is not None:
            raise InvalidEvaluationTransitionError(
                "Common support has already been recorded for this water regime."
            )

        comparable_crops = tuple(
            outcome.crop_id
            for outcome in self.outcomes
            if outcome.water_regime is regime
            and outcome.status is not CropOutcomeStatus.FAILED
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
            scenarios=(
                *self.scenarios,
                EvaluationScenarioResult(
                    water_regime=regime,
                    common_support=common_support,
                ),
            ),
        )

    def record_comparison(
        self,
        common_support: CommonSupport,
        comparable_crops: tuple[ComparableCrop, ...],
        *,
        water_regime: WaterRegime = WaterRegime.RAINFED,
    ) -> Evaluation:
        if self.status is not EvaluationStatus.SUMMARIZING:
            raise InvalidEvaluationTransitionError(
                "Scientific comparison can only be recorded while summarizing."
            )

        regime = WaterRegime(water_regime)
        if regime not in self.requested_water_regimes:
            raise DomainValidationError("Water regime was not requested for this evaluation.")
        if self.scenario_for(regime) is not None:
            raise InvalidEvaluationTransitionError(
                "Scientific comparison has already been recorded for this water regime."
            )

        crops = tuple(comparable_crops)

        validate_comparable_crops(
            common_support,
            crops,
        )

        comparable_outcomes = tuple(
            outcome.crop_id
            for outcome in self.outcomes
            if outcome.water_regime is regime
            and outcome.status is not CropOutcomeStatus.FAILED
        )
        reported = (
            *common_support.eligible_crops,
            *common_support.excluded_without_coverage,
        )
        if set(reported) != set(comparable_outcomes):
            raise DomainValidationError(
                "Common support must partition every non-failed crop outcome."
            )
        if (
            common_support.status is CommonSupportStatus.NO_SUCCESSFUL_CROPS
            and comparable_outcomes
        ):
            raise DomainValidationError(
                "No-successful-crops requires every crop outcome to have failed."
            )
        if (
            common_support.status is not CommonSupportStatus.NO_SUCCESSFUL_CROPS
            and not comparable_outcomes
        ):
            raise DomainValidationError(
                "A spatial comparison requires at least one non-failed crop."
            )

        return replace(
            self,
            scenarios=(
                *self.scenarios,
                EvaluationScenarioResult(
                    water_regime=regime,
                    common_support=common_support,
                    comparable_crops=crops,
                ),
            ),
        )

    def succeed(self) -> Evaluation:
        scenario_regimes = tuple(scenario.water_regime for scenario in self.scenarios)
        if scenario_regimes != self.requested_water_regimes:
            raise InvalidEvaluationTransitionError(
                "Evaluation cannot succeed before every requested scenario is summarized."
            )
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
