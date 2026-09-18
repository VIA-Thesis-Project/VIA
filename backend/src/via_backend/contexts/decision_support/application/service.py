"""Decision Support evidence translation and policy coordination."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from via_backend.contexts.agroclimatic_evaluation.application.public import (
    FinalizedCommonSupport,
    FinalizedCommonSupportStatus,
    FinalizedEvaluationResult,
    FinalizedEvaluationResultReader,
    GetFinalizedEvaluationResult,
)

from ..domain.models import (
    CommonSupportEvidence,
    CommonSupportStatus,
    ComparableCropEvidence,
    DecisionEvidence,
    EvidenceAvailability,
)
from .ports import IDecisionPolicy
from .queries import EvaluateDecisionSupport

PolicyEvaluationT = TypeVar("PolicyEvaluationT")


class PolicyReferenceMismatchError(ValueError):
    """Raised when the supplied policy differs from the requested policy identity."""


@dataclass(frozen=True, slots=True)
class DecisionSupportResult(Generic[PolicyEvaluationT]):
    """Prepared evidence plus an optional externally supplied policy evaluation."""

    evidence: DecisionEvidence
    policy_applied: bool
    policy_evaluation: PolicyEvaluationT | None


class DecisionSupportService:
    """Translate finalized scientific results and coordinate deterministic policy use."""

    def __init__(self, finalized_results: FinalizedEvaluationResultReader) -> None:
        self._finalized_results = finalized_results

    def prepare_evidence(self, query: EvaluateDecisionSupport) -> DecisionEvidence:
        finalized = self._finalized_results.get_finalized_evaluation_result(
            GetFinalizedEvaluationResult(
                evaluation_id=query.evaluation_id,
                water_regime=query.water_regime,
            )
        )
        return _translate_evidence(finalized, query)

    def evaluate(
        self,
        query: EvaluateDecisionSupport,
        policy: IDecisionPolicy[PolicyEvaluationT],
    ) -> DecisionSupportResult[PolicyEvaluationT]:
        if policy.reference != query.policy:
            raise PolicyReferenceMismatchError(
                "Supplied policy identity does not match the requested policy."
            )

        evidence = self.prepare_evidence(query)
        if not evidence.can_apply_policy:
            return DecisionSupportResult(
                evidence=evidence,
                policy_applied=False,
                policy_evaluation=None,
            )

        return DecisionSupportResult(
            evidence=evidence,
            policy_applied=True,
            policy_evaluation=policy.evaluate(evidence),
        )


def _translate_evidence(
    finalized: FinalizedEvaluationResult,
    query: EvaluateDecisionSupport,
) -> DecisionEvidence:
    common_support = _translate_common_support(finalized.common_support)
    comparable_crops = tuple(
        ComparableCropEvidence(
            crop_id=crop.crop_id,
            mean=crop.mean,
            rank=crop.rank,
        )
        for crop in finalized.comparable_crops
    )

    if common_support is None:
        availability = EvidenceAvailability.COMMON_SUPPORT_NOT_RECORDED
    elif common_support.status is CommonSupportStatus.NO_COMMON_COVERAGE:
        availability = EvidenceAvailability.NO_COMMON_COVERAGE
    elif common_support.status is CommonSupportStatus.NO_SUCCESSFUL_CROPS:
        availability = EvidenceAvailability.NO_SUCCESSFUL_CROPS
    elif comparable_crops:
        availability = EvidenceAvailability.COMPARABLE_EVIDENCE_AVAILABLE
    else:
        availability = EvidenceAvailability.LEGACY_COMPARISON_MISSING

    return DecisionEvidence(
        evaluation_id=finalized.evaluation_id,
        policy=query.policy,
        availability=availability,
        common_support=common_support,
        comparable_crops=comparable_crops,
    )


def _translate_common_support(
    source: FinalizedCommonSupport | None,
) -> CommonSupportEvidence | None:
    if source is None:
        return None

    statuses = {
        FinalizedCommonSupportStatus.COMPARABLE: CommonSupportStatus.COMPARABLE,
        FinalizedCommonSupportStatus.NO_COMMON_COVERAGE: (
            CommonSupportStatus.NO_COMMON_COVERAGE
        ),
        FinalizedCommonSupportStatus.NO_SUCCESSFUL_CROPS: (
            CommonSupportStatus.NO_SUCCESSFUL_CROPS
        ),
    }
    return CommonSupportEvidence(
        status=statuses[source.status],
        method=source.method,
        area_crs=source.area_crs,
        parcel_area_m2=source.parcel_area_m2,
        common_valid_area_m2=source.common_valid_area_m2,
        common_coverage_fraction=source.common_coverage_fraction,
        eligible_crops=source.eligible_crops,
        excluded_without_coverage=source.excluded_without_coverage,
    )
