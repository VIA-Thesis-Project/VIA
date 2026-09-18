"""Focused domain invariants for deterministic limiting-factor evidence."""

import pytest

from via_backend.contexts.agroclimatic_evaluation.domain import (
    CropLimitationEvidence,
    DomainValidationError,
    LimitationEvidenceAvailability,
    LimitingFactorEvidence,
)


def _factor(*, raw_code: object = 1, affected_cells: object = 2) -> LimitingFactorEvidence:
    return LimitingFactorEvidence(
        factor_code="precipitation",
        label="precipitation",
        raw_code=raw_code,  # type: ignore[arg-type]
        affected_cells=affected_cells,  # type: ignore[arg-type]
        affected_area_m2=25.0,
        affected_fraction=0.5,
        dominant=True,
        source_storage_reference="evaluations/e/scenarios/rainfed/crops/maize/crop_limiting_factor.tif",
        source_sha256="a" * 64,
    )


@pytest.mark.parametrize("raw_code", [True, 1.0])
def test_limiting_factor_rejects_non_integer_raw_code(raw_code: object) -> None:
    with pytest.raises(DomainValidationError, match="raw code"):
        _factor(raw_code=raw_code)


@pytest.mark.parametrize("affected_cells", [True, 1.0, -1])
def test_limiting_factor_rejects_invalid_affected_cells(affected_cells: object) -> None:
    with pytest.raises(DomainValidationError, match="Affected cell count"):
        _factor(affected_cells=affected_cells)


def test_available_limitation_evidence_requires_factor() -> None:
    with pytest.raises(DomainValidationError):
        CropLimitationEvidence(
            availability=LimitationEvidenceAvailability.AVAILABLE,
            reason=None,
        )


def test_available_limitation_evidence_accepts_traceable_factor() -> None:
    evidence = CropLimitationEvidence(
        availability=LimitationEvidenceAvailability.AVAILABLE,
        reason=None,
        factors=(_factor(),),
    )

    assert evidence.factors[0].factor_code == "precipitation"
