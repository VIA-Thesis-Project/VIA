"""Evaluation-level scientific common-support result."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

from .errors import DomainValidationError

_AREA_ABSOLUTE_TOLERANCE_M2 = 1e-6
_COVERAGE_FRACTION_TOLERANCE = 1e-9


def normalize_common_support_measurements(
    *,
    parcel_area_m2: float,
    common_valid_area_m2: float,
    common_coverage_fraction: float,
) -> tuple[float, float]:
    """Normalize impossible boundary overshoots caused only by float noise."""

    if not math.isfinite(parcel_area_m2) or parcel_area_m2 <= 0:
        raise DomainValidationError(
            "Parcel area must be a positive finite number."
        )

    if (
        not math.isfinite(common_valid_area_m2)
        or common_valid_area_m2 < 0
    ):
        raise DomainValidationError(
            "Common valid area must be finite and nonnegative."
        )

    if (
        not math.isfinite(common_coverage_fraction)
        or common_coverage_fraction < 0
    ):
        raise DomainValidationError(
            "Common coverage fraction must be between zero and one."
        )

    if common_valid_area_m2 > parcel_area_m2:
        if (
            common_valid_area_m2
            > parcel_area_m2 + _AREA_ABSOLUTE_TOLERANCE_M2
        ):
            raise DomainValidationError(
                "Common valid area cannot exceed parcel area."
            )
        common_valid_area_m2 = parcel_area_m2

    if common_coverage_fraction > 1.0:
        if common_coverage_fraction > 1.0 + _COVERAGE_FRACTION_TOLERANCE:
            raise DomainValidationError(
                "Common coverage fraction must be between zero and one."
            )
        common_coverage_fraction = 1.0

    expected_fraction = common_valid_area_m2 / parcel_area_m2

    if not math.isclose(
        common_coverage_fraction,
        expected_fraction,
        rel_tol=0.0,
        abs_tol=_COVERAGE_FRACTION_TOLERANCE,
    ):
        raise DomainValidationError(
            "Common coverage fraction is inconsistent with common valid area."
        )

    return common_valid_area_m2, common_coverage_fraction


class CommonSupportStatus(StrEnum):
    COMPARABLE = "comparable"
    NO_COMMON_COVERAGE = "no_common_coverage"
    NO_SUCCESSFUL_CROPS = "no_successful_crops"


@dataclass(frozen=True, slots=True)
class CommonSupport:
    """Spatial support shared by the usable crop suitability rasters."""

    status: CommonSupportStatus
    method: str | None
    area_crs: str | None
    parcel_area_m2: float
    common_valid_area_m2: float
    common_coverage_fraction: float
    eligible_crops: tuple[str, ...]
    excluded_without_coverage: tuple[str, ...]

    def __post_init__(self) -> None:
        eligible = tuple(self.eligible_crops)
        excluded = tuple(self.excluded_without_coverage)

        if (
            not math.isfinite(self.parcel_area_m2)
            or self.parcel_area_m2 <= 0
        ):
            raise DomainValidationError(
                "Parcel area must be a positive finite number."
            )

        if (
            not math.isfinite(self.common_valid_area_m2)
            or self.common_valid_area_m2 < 0
        ):
            raise DomainValidationError(
                "Common valid area must be finite and nonnegative."
            )

        if (
            not math.isfinite(self.common_coverage_fraction)
            or self.common_coverage_fraction < 0
        ):
            raise DomainValidationError(
                "Common coverage fraction must be between zero and one."
            )

        common_area, coverage = normalize_common_support_measurements(
            parcel_area_m2=self.parcel_area_m2,
            common_valid_area_m2=self.common_valid_area_m2,
            common_coverage_fraction=self.common_coverage_fraction,
        )

        object.__setattr__(self, "common_valid_area_m2", common_area)
        object.__setattr__(self, "common_coverage_fraction", coverage)

        for crop_id in (*eligible, *excluded):
            if (
                not crop_id
                or crop_id != crop_id.strip()
                or len(crop_id) > 120
            ):
                raise DomainValidationError(
                    "Common-support crop identifiers must be non-empty, "
                    "trimmed and at most 120 characters."
                )

        if len(set(eligible)) != len(eligible):
            raise DomainValidationError(
                "Eligible common-support crops must be unique."
            )

        if len(set(excluded)) != len(excluded):
            raise DomainValidationError(
                "Excluded common-support crops must be unique."
            )

        if set(eligible) & set(excluded):
            raise DomainValidationError(
                "A crop cannot be both eligible and excluded."
            )

        if self.status is CommonSupportStatus.NO_SUCCESSFUL_CROPS:
            if eligible or excluded:
                raise DomainValidationError(
                    "No-successful-crops cannot contain crop partitions."
                )
            if (
                self.common_valid_area_m2 != 0
                or self.common_coverage_fraction != 0
            ):
                raise DomainValidationError(
                    "No-successful-crops must have zero common support."
                )
            if self.method is not None or self.area_crs is not None:
                raise DomainValidationError(
                    "No-successful-crops cannot declare a comparison method."
                )
        else:
            if self.method != "area_weighted_mean_on_common_valid_cells":
                raise DomainValidationError(
                    "Unsupported common-support comparison method."
                )
            if self.area_crs != "EPSG:6933":
                raise DomainValidationError(
                    "Common-support areas must use EPSG:6933."
                )

        if self.status is CommonSupportStatus.COMPARABLE:
            if self.common_valid_area_m2 <= 0 or not eligible:
                raise DomainValidationError(
                    "Comparable common support requires positive area "
                    "and at least one eligible crop."
                )

        if self.status is CommonSupportStatus.NO_COMMON_COVERAGE:
            if (
                self.common_valid_area_m2 != 0
                or self.common_coverage_fraction != 0
            ):
                raise DomainValidationError(
                    "No-common-coverage must have zero common support."
                )

        object.__setattr__(self, "eligible_crops", eligible)
        object.__setattr__(
            self,
            "excluded_without_coverage",
            excluded,
        )

@dataclass(frozen=True, slots=True)
class ComparableCrop:
    """One crop ranked on the exact common valid spatial support."""

    crop_id: str
    mean: float
    rank: int

    def __post_init__(self) -> None:
        if (
            not self.crop_id
            or self.crop_id != self.crop_id.strip()
            or len(self.crop_id) > 120
        ):
            raise DomainValidationError(
                "Comparable crop identifier must be non-empty, trimmed, "
                "and at most 120 characters."
            )

        if (
            isinstance(self.mean, bool)
            or not isinstance(self.mean, (int, float))
            or not math.isfinite(self.mean)
            or not 0.0 <= self.mean <= 100.0
        ):
            raise DomainValidationError(
                "Comparable crop mean must be finite and between 0 and 100."
            )

        if (
            isinstance(self.rank, bool)
            or not isinstance(self.rank, int)
            or self.rank < 1
        ):
            raise DomainValidationError(
                "Comparable crop rank must be a positive integer."
            )


def validate_comparable_crops(
    common_support: CommonSupport,
    crops: tuple[ComparableCrop, ...],
) -> None:
    """Validate deterministic scientific ranking semantics."""

    if common_support.status is not CommonSupportStatus.COMPARABLE:
        if crops:
            raise DomainValidationError(
                "A non-comparable common support cannot contain ranked crops."
            )
        return

    if not crops:
        raise DomainValidationError(
            "Comparable common support requires ranked crops."
        )

    crop_ids = tuple(crop.crop_id for crop in crops)

    if len(crop_ids) != len(set(crop_ids)):
        raise DomainValidationError(
            "Comparable crop identifiers must be unique."
        )

    if set(crop_ids) != set(common_support.eligible_crops):
        raise DomainValidationError(
            "Comparable crops must match the common-support eligible crops."
        )

    previous: ComparableCrop | None = None
    expected_rank = 0

    for position, crop in enumerate(crops, start=1):
        if previous is None:
            expected_rank = 1
        else:
            if crop.mean > previous.mean:
                raise DomainValidationError(
                    "Comparable crop means must be ordered descending."
                )
            if (
                crop.mean == previous.mean
                and crop.crop_id < previous.crop_id
            ):
                raise DomainValidationError(
                    "Equal-mean comparable crops must be ordered by crop identifier."
                )

            if not math.isclose(
                crop.mean,
                previous.mean,
                rel_tol=0.0,
                abs_tol=1e-9,
            ):
                expected_rank = position

        if crop.rank != expected_rank:
            raise DomainValidationError(
                "Comparable crop ranks are inconsistent with scientific ordering."
            )

        previous = crop
