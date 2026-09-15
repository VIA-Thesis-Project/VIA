"""Deterministic viability classification owned by Decision Support."""

from __future__ import annotations

from dataclasses import dataclass, field

from .errors import DomainValidationError
from .models import (
    CropViabilityAssessment,
    DecisionEvidence,
    PolicyReference,
    Viability,
    ViabilityPolicyConfiguration,
    ViabilityPolicyEvaluation,
    ViabilityPolicySnapshot,
)


@dataclass(frozen=True, slots=True)
class DeterministicViabilityPolicy:
    """Classify each comparable mean independently using injected thresholds."""

    reference: PolicyReference
    configuration: ViabilityPolicyConfiguration
    snapshot: ViabilityPolicySnapshot = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "snapshot",
            ViabilityPolicySnapshot(
                reference=self.reference,
                configuration=self.configuration,
            ),
        )

    def evaluate(self, evidence: DecisionEvidence) -> ViabilityPolicyEvaluation:
        """Return assessments in provider order without changing means or ranks."""

        if evidence.policy != self.reference:
            raise DomainValidationError(
                "Evidence policy identity must match the viability policy."
            )
        if not evidence.can_apply_policy:
            raise DomainValidationError(
                "Viability policy requires available comparable evidence."
            )

        assessments = tuple(
            CropViabilityAssessment(
                crop_id=crop.crop_id,
                comparable_mean=crop.mean,
                scientific_rank=crop.rank,
                viability=self._classify(crop.mean),
                policy=self.snapshot,
            )
            for crop in evidence.comparable_crops
        )
        return ViabilityPolicyEvaluation(
            evaluation_id=evidence.evaluation_id,
            policy=self.snapshot,
            assessments=assessments,
        )

    def _classify(self, mean: float) -> Viability:
        if mean < self.configuration.conditional_from:
            return Viability.NON_VIABLE
        if mean < self.configuration.viable_from:
            return Viability.CONDITIONAL
        return Viability.VIABLE
