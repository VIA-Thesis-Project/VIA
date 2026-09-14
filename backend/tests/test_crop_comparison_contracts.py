from __future__ import annotations

from typing import Any

from via_backend.contexts.agroclimatic_evaluation.application import (
    CommonSupportResult,
    CommonSupportStatus,
    CropComparisonRequest,
    ICropComparisonEngine,
)


class StubComparisonEngine:
    def compare(
        self,
        request: CropComparisonRequest,
    ) -> CommonSupportResult:
        del request
        return CommonSupportResult(
            status=CommonSupportStatus.NO_SUCCESSFUL_CROPS,
            method=None,
            area_crs=None,
            parcel_area_m2=1.0,
            common_valid_area_m2=0.0,
            common_coverage_fraction=0.0,
            eligible_crops=(),
            excluded_without_coverage=(),
        )


def test_comparison_engine_contract_is_runtime_checkable() -> None:
    engine: Any = StubComparisonEngine()

    assert isinstance(engine, ICropComparisonEngine)