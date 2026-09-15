"""Focused tests for the Decision Support bounded-context foundation."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.application.public import (
    FinalizedCommonSupport,
    FinalizedCommonSupportStatus,
    FinalizedComparableCrop,
    FinalizedEvaluationResult,
    GetFinalizedEvaluationResult,
)
from via_backend.contexts.decision_support.application import (
    DecisionSupportService,
    EvaluateDecisionSupport,
    IDecisionPolicy,
)
from via_backend.contexts.decision_support.domain import (
    CommonSupportEvidence,
    CommonSupportStatus,
    ComparableCropEvidence,
    CropViabilityAssessment,
    DecisionEvidence,
    DeterministicViabilityPolicy,
    DomainValidationError,
    EvidenceAvailability,
    PolicyReference,
    Viability,
    ViabilityPolicyConfiguration,
    ViabilityPolicyEvaluation,
)

NOW = datetime(2026, 9, 14, 12, tzinfo=UTC)
POLICY = PolicyReference(identifier="via-deterministic-policy", version="0.1")
TEST_CONFIGURATION = ViabilityPolicyConfiguration(
    conditional_from=40.0,
    viable_from=70.0,
)


class _FinalizedResultReader:
    def __init__(self, result: FinalizedEvaluationResult) -> None:
        self.result = result
        self.queries: list[GetFinalizedEvaluationResult] = []

    def get_finalized_evaluation_result(
        self, query: GetFinalizedEvaluationResult
    ) -> FinalizedEvaluationResult:
        self.queries.append(query)
        return self.result


class _RecordingPolicy:
    reference = POLICY

    def __init__(self) -> None:
        self.evidence: list[Any] = []

    def evaluate(self, evidence: Any) -> str:
        self.evidence.append(evidence)
        return "policy-output-placeholder"



def _common_support(
    status: FinalizedCommonSupportStatus,
) -> FinalizedCommonSupport:
    comparable = status is FinalizedCommonSupportStatus.COMPARABLE
    return FinalizedCommonSupport(
        status=status,
        method="common-valid-cell arithmetic mean" if comparable else None,
        area_crs="EPSG:32718" if comparable else None,
        parcel_area_m2=100.0,
        common_valid_area_m2=75.0 if comparable else 0.0,
        common_coverage_fraction=0.75 if comparable else 0.0,
        eligible_crops=("maize", "potato", "rice") if comparable else (),
        excluded_without_coverage=(),
    )


def _finalized_result(
    *,
    common_support: FinalizedCommonSupport | None,
    comparable_crops: tuple[FinalizedComparableCrop, ...] = (),
) -> FinalizedEvaluationResult:
    return FinalizedEvaluationResult(
        evaluation_id=uuid4(),
        requested_crops=("maize", "potato", "rice"),
        project_id=uuid4(),
        parcel_id=uuid4(),
        parcel_version=3,
        parcel_captured_at=NOW,
        created_at=NOW,
        outcomes=(),
        common_support=common_support,
        comparable_crops=comparable_crops,
    )


def _domain_common_support(
    *,
    eligible_crops: tuple[str, ...] = ("maize", "potato", "rice"),
    excluded_without_coverage: tuple[str, ...] = (),
) -> CommonSupportEvidence:
    return CommonSupportEvidence(
        status=CommonSupportStatus.COMPARABLE,
        method="common-valid-cell arithmetic mean",
        area_crs="EPSG:32718",
        parcel_area_m2=100.0,
        common_valid_area_m2=75.0,
        common_coverage_fraction=0.75,
        eligible_crops=eligible_crops,
        excluded_without_coverage=excluded_without_coverage,
    )


def _evaluate(
    finalized: FinalizedEvaluationResult,
    policy: IDecisionPolicy[Any],
) -> tuple[_FinalizedResultReader, Any]:
    reader = _FinalizedResultReader(finalized)
    service = DecisionSupportService(reader)
    result = service.evaluate(
        EvaluateDecisionSupport(finalized.evaluation_id, POLICY),
        policy,
    )
    return reader, result


def _viability_policy() -> DeterministicViabilityPolicy:
    return DeterministicViabilityPolicy(
        reference=POLICY,
        configuration=TEST_CONFIGURATION,
    )


def _decision_evidence(
    comparable_crops: tuple[ComparableCropEvidence, ...],
) -> DecisionEvidence:
    crop_ids = tuple(crop.crop_id for crop in comparable_crops)
    return DecisionEvidence(
        evaluation_id=uuid4(),
        policy=POLICY,
        availability=EvidenceAvailability.COMPARABLE_EVIDENCE_AVAILABLE,
        common_support=_domain_common_support(eligible_crops=crop_ids),
        comparable_crops=comparable_crops,
    )


def test_translation_preserves_crop_order_means_ranks_and_ties() -> None:
    finalized = _finalized_result(
        common_support=_common_support(FinalizedCommonSupportStatus.COMPARABLE),
        comparable_crops=(
            FinalizedComparableCrop("potato", 61.25, 1),
            FinalizedComparableCrop("maize", 61.25, 1),
            FinalizedComparableCrop("rice", 48.5, 3),
        ),
    )
    policy = _RecordingPolicy()

    reader, result = _evaluate(finalized, policy)

    assert reader.queries == [GetFinalizedEvaluationResult(finalized.evaluation_id)]
    assert result.evidence.evaluation_id == finalized.evaluation_id
    assert result.evidence.policy == POLICY
    assert result.evidence.availability is EvidenceAvailability.COMPARABLE_EVIDENCE_AVAILABLE
    assert result.evidence.common_support is not None
    assert result.evidence.common_support.status is CommonSupportStatus.COMPARABLE
    assert [
        (crop.crop_id, crop.mean, crop.rank)
        for crop in result.evidence.comparable_crops
    ] == [
        ("potato", 61.25, 1),
        ("maize", 61.25, 1),
        ("rice", 48.5, 3),
    ]
    assert result.policy_applied is True
    assert result.policy_evaluation == "policy-output-placeholder"
    assert policy.evidence == [result.evidence]


@pytest.mark.parametrize(
    ("support_status", "availability"),
    [
        (
            FinalizedCommonSupportStatus.NO_COMMON_COVERAGE,
            EvidenceAvailability.NO_COMMON_COVERAGE,
        ),
        (
            FinalizedCommonSupportStatus.NO_SUCCESSFUL_CROPS,
            EvidenceAvailability.NO_SUCCESSFUL_CROPS,
        ),
    ],
)
def test_unavailable_common_support_does_not_apply_policy(
    support_status: FinalizedCommonSupportStatus,
    availability: EvidenceAvailability,
) -> None:
    finalized = _finalized_result(common_support=_common_support(support_status))

    _, result = _evaluate(finalized, _viability_policy())

    assert result.evidence.availability is availability
    assert result.evidence.comparable_crops == ()
    assert result.policy_applied is False
    assert result.policy_evaluation is None


def test_legacy_common_support_without_comparable_crops_is_representable() -> None:
    finalized = _finalized_result(
        common_support=_common_support(FinalizedCommonSupportStatus.COMPARABLE)
    )

    _, result = _evaluate(finalized, _viability_policy())

    assert result.evidence.availability is EvidenceAvailability.LEGACY_COMPARISON_MISSING
    assert result.evidence.common_support is not None
    assert result.evidence.common_support.status is CommonSupportStatus.COMPARABLE
    assert result.evidence.comparable_crops == ()
    assert result.policy_applied is False
    assert result.policy_evaluation is None


def test_unrecorded_common_support_remains_distinct_from_low_suitability() -> None:
    finalized = _finalized_result(common_support=None)

    _, result = _evaluate(finalized, _viability_policy())

    assert result.evidence.availability is EvidenceAvailability.COMMON_SUPPORT_NOT_RECORDED
    assert result.evidence.common_support is None
    assert result.policy_applied is False
    assert result.policy_evaluation is None


def test_decision_support_does_not_publish_automatic_recommendations() -> None:
    finalized = _finalized_result(
        common_support=_common_support(FinalizedCommonSupportStatus.COMPARABLE),
        comparable_crops=(
            FinalizedComparableCrop("maize", 12.0, 1),
            FinalizedComparableCrop("potato", 11.0, 2),
            FinalizedComparableCrop("rice", 10.0, 3),
        ),
    )

    _, result = _evaluate(finalized, _RecordingPolicy())

    forbidden_fields = {"best_crop", "recommended_crop", "recommendation_rank"}
    assert forbidden_fields.isdisjoint(vars(type(result.evidence)))
    assert forbidden_fields.isdisjoint(vars(type(result)))
    assert forbidden_fields.isdisjoint(vars(CropViabilityAssessment))
    assert forbidden_fields.isdisjoint(vars(ViabilityPolicyEvaluation))


@pytest.mark.parametrize(
    ("conditional_from", "viable_from"),
    [
        (-0.001, 70.0),
        (40.0, 100.001),
        (40.0, 40.0),
        (70.0, 40.0),
        (float("nan"), 70.0),
        (40.0, float("nan")),
        (float("inf"), 70.0),
        (40.0, float("-inf")),
        (True, 70.0),
        (40.0, False),
        ("40", 70.0),
        (40.0, "70"),
    ],
)
def test_viability_configuration_rejects_invalid_thresholds(
    conditional_from: object,
    viable_from: object,
) -> None:
    with pytest.raises(DomainValidationError, match="threshold"):
        ViabilityPolicyConfiguration(
            conditional_from=conditional_from,  # type: ignore[arg-type]
            viable_from=viable_from,  # type: ignore[arg-type]
        )


def test_viability_configuration_preserves_exact_numeric_values() -> None:
    configuration = ViabilityPolicyConfiguration(
        conditional_from=40.125,
        viable_from=70.875,
    )

    assert configuration.conditional_from == 40.125
    assert configuration.viable_from == 70.875


@pytest.mark.parametrize(
    ("mean", "expected"),
    [
        (39.999, Viability.NON_VIABLE),
        (40.0, Viability.CONDITIONAL),
        (55.0, Viability.CONDITIONAL),
        (69.999, Viability.CONDITIONAL),
        (70.0, Viability.VIABLE),
        (85.0, Viability.VIABLE),
    ],
)
def test_viability_policy_classifies_boundaries_exactly(
    mean: float,
    expected: Viability,
) -> None:
    evidence = _decision_evidence((ComparableCropEvidence("maize", mean, 1),))

    evaluation = _viability_policy().evaluate(evidence)

    assert evaluation.assessments[0].viability is expected


def test_rank_one_low_score_can_be_non_viable() -> None:
    evidence = _decision_evidence((ComparableCropEvidence("maize", 12.0, 1),))

    assessment = _viability_policy().evaluate(evidence).assessments[0]

    assert assessment.scientific_rank == 1
    assert assessment.viability is Viability.NON_VIABLE


def test_policy_preserves_order_ties_scientific_values_and_snapshot() -> None:
    crops = (
        ComparableCropEvidence("maize", 80.0, 1),
        ComparableCropEvidence("potato", 80.0, 1),
        ComparableCropEvidence("rice", 70.0, 3),
    )
    policy = _viability_policy()

    evaluation = policy.evaluate(_decision_evidence(crops))

    assert [
        (
            assessment.crop_id,
            assessment.comparable_mean,
            assessment.scientific_rank,
        )
        for assessment in evaluation.assessments
    ] == [
        ("maize", 80.0, 1),
        ("potato", 80.0, 1),
        ("rice", 70.0, 3),
    ]
    assert evaluation.policy.reference == POLICY
    assert evaluation.policy.configuration == TEST_CONFIGURATION
    assert all(
        assessment.policy == evaluation.policy
        for assessment in evaluation.assessments
    )


def test_service_integrates_configured_deterministic_policy() -> None:
    finalized = _finalized_result(
        common_support=_common_support(FinalizedCommonSupportStatus.COMPARABLE),
        comparable_crops=(
            FinalizedComparableCrop("maize", 35.0, 1),
            FinalizedComparableCrop("potato", 55.0, 2),
            FinalizedComparableCrop("rice", 75.0, 3),
        ),
    )

    _, result = _evaluate(finalized, _viability_policy())

    assert result.policy_applied is True
    assert isinstance(result.policy_evaluation, ViabilityPolicyEvaluation)
    assert [
        assessment.viability
        for assessment in result.policy_evaluation.assessments
    ] == [
        Viability.NON_VIABLE,
        Viability.CONDITIONAL,
        Viability.VIABLE,
    ]


@pytest.mark.parametrize("rank", [True, 1.5])
def test_comparable_crop_requires_an_actual_integer_rank(rank: object) -> None:
    with pytest.raises(DomainValidationError, match="positive integer"):
        ComparableCropEvidence(
            crop_id="maize",
            mean=50.0,
            rank=rank,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "mean",
    [-0.01, 100.01, float("nan"), float("inf"), float("-inf"), True, "50"],
)
def test_comparable_crop_rejects_invalid_mean(mean: object) -> None:
    with pytest.raises(DomainValidationError, match="mean"):
        ComparableCropEvidence(
            crop_id="maize",
            mean=mean,  # type: ignore[arg-type]
            rank=1,
        )


@pytest.mark.parametrize("crop_id", ["", " maize", "maize ", None])
def test_comparable_crop_rejects_malformed_identifier(crop_id: object) -> None:
    with pytest.raises(DomainValidationError, match="already-trimmed"):
        ComparableCropEvidence(
            crop_id=crop_id,  # type: ignore[arg-type]
            mean=50.0,
            rank=1,
        )


@pytest.mark.parametrize(
    ("identifier", "version"),
    [
        (" policy", "1.0"),
        ("policy", "1.0 "),
        ("", "1.0"),
        ("policy", ""),
        (None, "1.0"),
        ("policy", None),
    ],
)
def test_policy_reference_rejects_malformed_identity(
    identifier: object,
    version: object,
) -> None:
    with pytest.raises(DomainValidationError, match="already-trimmed"):
        PolicyReference(
            identifier=identifier,  # type: ignore[arg-type]
            version=version,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("eligible_crops", "excluded_without_coverage"),
    [
        (("maize", "maize"), ()),
        (("maize",), ("rice", "rice")),
    ],
)
def test_common_support_rejects_duplicate_crop_membership(
    eligible_crops: tuple[str, ...],
    excluded_without_coverage: tuple[str, ...],
) -> None:
    with pytest.raises(DomainValidationError, match="unique"):
        _domain_common_support(
            eligible_crops=eligible_crops,
            excluded_without_coverage=excluded_without_coverage,
        )


@pytest.mark.parametrize(
    ("eligible_crops", "excluded_without_coverage"),
    [
        ((" maize",), ()),
        (("maize",), ("rice ",)),
    ],
)
def test_common_support_rejects_malformed_crop_membership(
    eligible_crops: tuple[str, ...],
    excluded_without_coverage: tuple[str, ...],
) -> None:
    with pytest.raises(DomainValidationError, match="already-trimmed"):
        _domain_common_support(
            eligible_crops=eligible_crops,
            excluded_without_coverage=excluded_without_coverage,
        )


def test_common_support_rejects_overlap_between_eligible_and_excluded() -> None:
    with pytest.raises(DomainValidationError, match="disjoint"):
        _domain_common_support(
            eligible_crops=("maize", "potato"),
            excluded_without_coverage=("potato",),
        )


@pytest.mark.parametrize(
    "comparable_crops",
    [
        (
            ComparableCropEvidence("maize", 70.0, 1),
            ComparableCropEvidence("potato", 60.0, 2),
        ),
        (
            ComparableCropEvidence("maize", 70.0, 1),
            ComparableCropEvidence("potato", 60.0, 2),
            ComparableCropEvidence("rice", 50.0, 3),
            ComparableCropEvidence("unknown", 40.0, 4),
        ),
    ],
)
def test_comparable_evidence_must_exactly_match_eligible_crop_membership(
    comparable_crops: tuple[ComparableCropEvidence, ...],
) -> None:
    with pytest.raises(DomainValidationError, match="exactly match"):
        DecisionEvidence(
            evaluation_id=uuid4(),
            policy=POLICY,
            availability=EvidenceAvailability.COMPARABLE_EVIDENCE_AVAILABLE,
            common_support=_domain_common_support(),
            comparable_crops=comparable_crops,
        )


def test_valid_tied_ranking_is_accepted_without_reordering() -> None:
    comparable_crops = (
        ComparableCropEvidence("potato", 61.25, 1),
        ComparableCropEvidence("maize", 61.25, 1),
        ComparableCropEvidence("rice", 48.5, 3),
    )

    evidence = DecisionEvidence(
        evaluation_id=uuid4(),
        policy=POLICY,
        availability=EvidenceAvailability.COMPARABLE_EVIDENCE_AVAILABLE,
        common_support=_domain_common_support(),
        comparable_crops=comparable_crops,
    )

    assert evidence.comparable_crops == comparable_crops
    assert [crop.rank for crop in evidence.comparable_crops] == [1, 1, 3]
