"""Decision Support-owned evidence and policy identity models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from uuid import UUID

from .errors import DomainValidationError


class CommonSupportStatus(StrEnum):
    """Scientific common-support state translated into local domain language."""

    COMPARABLE = "comparable"
    NO_COMMON_COVERAGE = "no_common_coverage"
    NO_SUCCESSFUL_CROPS = "no_successful_crops"


class EvidenceAvailability(StrEnum):
    """Whether deterministic policy evaluation has sufficient scientific evidence."""

    COMPARABLE_EVIDENCE_AVAILABLE = "comparable_evidence_available"
    NO_COMMON_COVERAGE = "no_common_coverage"
    NO_SUCCESSFUL_CROPS = "no_successful_crops"
    LEGACY_COMPARISON_MISSING = "legacy_comparison_missing"
    COMMON_SUPPORT_NOT_RECORDED = "common_support_not_recorded"


@dataclass(frozen=True, slots=True)
class PolicyReference:
    """Stable identity of the deterministic policy selected for an evaluation."""

    identifier: str
    version: str

    def __post_init__(self) -> None:
        _require_trimmed_identifier(self.identifier, "Policy identifier")
        _require_trimmed_identifier(self.version, "Policy version")


@dataclass(frozen=True, slots=True)
class ComparableCropEvidence:
    """A provider-produced crop mean and rank over common valid support."""

    crop_id: str
    mean: float
    rank: int

    def __post_init__(self) -> None:
        _require_trimmed_identifier(self.crop_id, "Comparable crop identifier")
        if isinstance(self.mean, bool) or not isinstance(self.mean, (int, float)):
            raise DomainValidationError("Comparable crop mean must be numeric.")
        if not isfinite(self.mean) or not 0 <= self.mean <= 100:
            raise DomainValidationError(
                "Comparable crop mean must be finite and between zero and 100."
            )
        if (
            isinstance(self.rank, bool)
            or not isinstance(self.rank, int)
            or self.rank < 1
        ):
            raise DomainValidationError("Comparable crop rank must be a positive integer.")


@dataclass(frozen=True, slots=True)
class CommonSupportEvidence:
    """Coverage metadata supporting the provider's scientific comparison."""

    status: CommonSupportStatus
    method: str | None
    area_crs: str | None
    parcel_area_m2: float
    common_valid_area_m2: float
    common_coverage_fraction: float
    eligible_crops: tuple[str, ...]
    excluded_without_coverage: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isfinite(self.parcel_area_m2) or self.parcel_area_m2 < 0:
            raise DomainValidationError("Parcel area must be finite and non-negative.")
        if (
            not isfinite(self.common_valid_area_m2)
            or self.common_valid_area_m2 < 0
        ):
            raise DomainValidationError(
                "Common valid area must be finite and non-negative."
            )
        tolerance = max(1e-6, self.parcel_area_m2 * 1e-9)
        if self.common_valid_area_m2 > self.parcel_area_m2 + tolerance:
            raise DomainValidationError("Common valid area cannot exceed parcel area.")
        if (
            not isfinite(self.common_coverage_fraction)
            or not 0 <= self.common_coverage_fraction <= 1
        ):
            raise DomainValidationError(
                "Common coverage fraction must be between zero and one."
            )
        _require_unique_identifiers(self.eligible_crops, "Eligible crop identifiers")
        _require_unique_identifiers(
            self.excluded_without_coverage,
            "Excluded crop identifiers",
        )
        if set(self.eligible_crops) & set(self.excluded_without_coverage):
            raise DomainValidationError(
                "Eligible and excluded crop identifiers must be disjoint."
            )
        if self.status is CommonSupportStatus.COMPARABLE:
            if self.method is None or not self.method.strip():
                raise DomainValidationError(
                    "Comparable common support requires an explicit method."
                )
            if self.area_crs is None or not self.area_crs.strip():
                raise DomainValidationError(
                    "Comparable common support requires an explicit area CRS."
                )


@dataclass(frozen=True, slots=True)
class DecisionEvidence:
    """Scientific evidence prepared for one explicit deterministic policy."""

    evaluation_id: UUID
    policy: PolicyReference
    availability: EvidenceAvailability
    common_support: CommonSupportEvidence | None
    comparable_crops: tuple[ComparableCropEvidence, ...]

    def __post_init__(self) -> None:
        crop_ids = tuple(crop.crop_id for crop in self.comparable_crops)
        if len(crop_ids) != len(set(crop_ids)):
            raise DomainValidationError(
                "Comparable crop evidence must contain unique crop identifiers."
            )

        if self.availability is EvidenceAvailability.COMMON_SUPPORT_NOT_RECORDED:
            if self.common_support is not None or self.comparable_crops:
                raise DomainValidationError(
                    "Missing common support cannot contain comparison evidence."
                )
            return

        if self.common_support is None:
            raise DomainValidationError(
                "Recorded evidence availability requires common support metadata."
            )

        expected_support_status = {
            EvidenceAvailability.COMPARABLE_EVIDENCE_AVAILABLE: (
                CommonSupportStatus.COMPARABLE
            ),
            EvidenceAvailability.LEGACY_COMPARISON_MISSING: (
                CommonSupportStatus.COMPARABLE
            ),
            EvidenceAvailability.NO_COMMON_COVERAGE: (
                CommonSupportStatus.NO_COMMON_COVERAGE
            ),
            EvidenceAvailability.NO_SUCCESSFUL_CROPS: (
                CommonSupportStatus.NO_SUCCESSFUL_CROPS
            ),
        }[self.availability]
        if self.common_support.status is not expected_support_status:
            raise DomainValidationError(
                "Evidence availability must agree with common support status."
            )

        comparison_is_available = (
            self.availability is EvidenceAvailability.COMPARABLE_EVIDENCE_AVAILABLE
        )
        if comparison_is_available != bool(self.comparable_crops):
            raise DomainValidationError(
                "Only available comparison evidence may contain comparable crops."
            )
        if comparison_is_available and set(crop_ids) != set(
            self.common_support.eligible_crops
        ):
            raise DomainValidationError(
                "Comparable crop identifiers must exactly match eligible crops."
            )

    @property
    def can_apply_policy(self) -> bool:
        """Return whether a policy may consume this evidence without fabrication."""

        return self.availability is EvidenceAvailability.COMPARABLE_EVIDENCE_AVAILABLE


def _require_trimmed_identifier(value: object, label: str) -> None:
    if not isinstance(value, str) or not value or value != value.strip():
        raise DomainValidationError(
            f"{label} must be a non-empty, already-trimmed string."
        )


def _require_unique_identifiers(values: tuple[str, ...], label: str) -> None:
    for value in values:
        _require_trimmed_identifier(value, label)
    if len(values) != len(set(values)):
        raise DomainValidationError(f"{label} must be unique.")
