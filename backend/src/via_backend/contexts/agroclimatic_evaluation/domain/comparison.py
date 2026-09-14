"""Evaluation-level scientific common-support result."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

from .errors import DomainValidationError


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

        if self.common_valid_area_m2 > self.parcel_area_m2 + 1e-6:
            raise DomainValidationError(
                "Common valid area cannot exceed parcel area."
            )

        if (
            not math.isfinite(self.common_coverage_fraction)
            or not 0 <= self.common_coverage_fraction <= 1
        ):
            raise DomainValidationError(
                "Common coverage fraction must be between zero and one."
            )

        expected_fraction = min(
            self.common_valid_area_m2 / self.parcel_area_m2,
            1.0,
        )

        if not math.isclose(
            self.common_coverage_fraction,
            expected_fraction,
            rel_tol=0.0,
            abs_tol=1e-9,
        ):
            raise DomainValidationError(
                "Common coverage fraction is inconsistent with common valid area."
            )

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