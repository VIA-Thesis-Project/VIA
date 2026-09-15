"""Domain tests for durable comparable crop results."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.domain import (
    CommonSupport,
    CommonSupportStatus,
    ComparableCrop,
    CropOutcome,
    CropOutcomeStatus,
    Evaluation,
    EvaluationStatus,
    ParcelSnapshot,
    ScientificTrace,
    SnapshotGeometry,
    SuitabilitySummary,
)
from via_backend.contexts.agroclimatic_evaluation.domain.errors import (
    DomainValidationError,
)

NOW = datetime(
    2026,
    9,
    14,
    20,
    0,
    tzinfo=UTC,
)


def _snapshot() -> ParcelSnapshot:
    return ParcelSnapshot(
        project_id=uuid4(),
        parcel_id=uuid4(),
        parcel_version=1,
        geometry=SnapshotGeometry.from_geojson(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-77.6, -11.1],
                        [-77.5, -11.1],
                        [-77.5, -11.0],
                        [-77.6, -11.1],
                    ]
                ],
            }
        ),
        crs="EPSG:4326",
        captured_at=NOW,
    )


def _outcome(
    crop_id: str,
) -> CropOutcome:
    return CropOutcome(
        crop_id=crop_id,
        status=CropOutcomeStatus.SUCCEEDED,
        suitability=SuitabilitySummary(
            mean=70.0,
            minimum=60.0,
            maximum=80.0,
            valid_cells=10,
            valid_area_m2=80.0,
            coverage_fraction=0.8,
            zero_suitability_area_m2=0.0,
        ),
        failure_message=None,
        trace=ScientificTrace(
            engine_identifier="CropSuiteLite",
            execution_reference=f"run-{crop_id}",
            started_at=NOW,
            finished_at=NOW,
            elapsed_seconds=1.0,
            execution_mode="test",
            parcel_sha256="parcel",
            parameter_sha256=f"parameter-{crop_id}",
            configuration_sha256="configuration",
            source_files_unchanged=True,
        ),
    )


def _summarizing(
    *crop_ids: str,
) -> Evaluation:
    evaluation = Evaluation(
        id=uuid4(),
        parcel_snapshot=_snapshot(),
        requested_crops=tuple(crop_ids),
        status=EvaluationStatus.QUEUED,
        created_at=NOW,
    )

    current = (
        evaluation
        .prepare()
        .start_running()
    )

    for crop_id in crop_ids:
        current = current.record_outcome(
            _outcome(crop_id)
        )

    return current.start_summarizing()


def _comparable_support(
    *eligible_crops: str,
    excluded_without_coverage: tuple[str, ...] = (),
) -> CommonSupport:
    return CommonSupport(
        status=CommonSupportStatus.COMPARABLE,
        method="area_weighted_mean_on_common_valid_cells",
        area_crs="EPSG:6933",
        parcel_area_m2=100.0,
        common_valid_area_m2=80.0,
        common_coverage_fraction=0.8,
        eligible_crops=tuple(eligible_crops),
        excluded_without_coverage=excluded_without_coverage,
    )


def test_record_comparison_accepts_competition_ranking_with_ties() -> None:
    evaluation = _summarizing(
        "barley",
        "maize",
        "rice",
    )

    common_support = _comparable_support(
        "barley",
        "maize",
        "rice",
    )

    crops = (
        ComparableCrop(
            crop_id="barley",
            mean=80.0,
            rank=1,
        ),
        ComparableCrop(
            crop_id="maize",
            mean=80.0,
            rank=1,
        ),
        ComparableCrop(
            crop_id="rice",
            mean=60.0,
            rank=3,
        ),
    )

    result = evaluation.record_comparison(
        common_support,
        crops,
    )

    assert result.common_support == common_support
    assert result.comparable_crops == crops
    assert [
        crop.rank
        for crop in result.comparable_crops
    ] == [1, 1, 3]


def test_record_comparison_rejects_inconsistent_tied_rank() -> None:
    evaluation = _summarizing(
        "barley",
        "maize",
    )

    common_support = _comparable_support(
        "barley",
        "maize",
    )

    with pytest.raises(
        DomainValidationError,
        match="rank",
    ):
        evaluation.record_comparison(
            common_support,
            (
                ComparableCrop(
                    crop_id="barley",
                    mean=80.0,
                    rank=1,
                ),
                ComparableCrop(
                    crop_id="maize",
                    mean=80.0,
                    rank=2,
                ),
            ),
        )


def test_record_comparison_rejects_crop_outside_eligible_support() -> None:
    evaluation = _summarizing(
        "maize",
        "rice",
    )

    common_support = _comparable_support(
        "maize",
        excluded_without_coverage=("rice",),
    )

    with pytest.raises(
        DomainValidationError,
        match="eligible",
    ):
        evaluation.record_comparison(
            common_support,
            (
                ComparableCrop(
                    crop_id="maize",
                    mean=75.0,
                    rank=1,
                ),
                ComparableCrop(
                    crop_id="rice",
                    mean=60.0,
                    rank=2,
                ),
            ),
        )


def test_record_comparison_rejects_duplicate_crop_identifier() -> None:
    evaluation = _summarizing(
        "maize",
        "rice",
    )

    common_support = _comparable_support(
        "maize",
        "rice",
    )

    with pytest.raises(
        DomainValidationError,
        match="unique",
    ):
        evaluation.record_comparison(
            common_support,
            (
                ComparableCrop(
                    crop_id="maize",
                    mean=80.0,
                    rank=1,
                ),
                ComparableCrop(
                    crop_id="maize",
                    mean=70.0,
                    rank=2,
                ),
            ),
        )


@pytest.mark.parametrize(
    ("mean", "rank"),
    [
        (-0.1, 1),
        (100.1, 1),
        (float("nan"), 1),
        (float("inf"), 1),
        (50.0, 0),
        (50.0, -1),
    ],
)
def test_comparable_crop_rejects_invalid_numeric_values(
    mean: float,
    rank: int,
) -> None:
    with pytest.raises(
        DomainValidationError,
    ):
        ComparableCrop(
            crop_id="maize",
            mean=mean,
            rank=rank,
        )


@pytest.mark.parametrize(
    "crop_id",
    [
        "",
        " ",
        " maize",
        "maize ",
    ],
)
def test_comparable_crop_requires_trimmed_identifier(
    crop_id: str,
) -> None:
    with pytest.raises(
        DomainValidationError,
    ):
        ComparableCrop(
            crop_id=crop_id,
            mean=80.0,
            rank=1,
        )


def test_historical_comparable_support_without_ranking_remains_valid() -> None:
    evaluation = _summarizing(
        "maize",
    )

    support = _comparable_support(
        "maize",
    )

    legacy = (
        evaluation
        .record_common_support(support)
        .succeed()
    )

    assert (
        legacy.status
        is EvaluationStatus.SUCCEEDED
    )
    assert legacy.common_support == support
    assert legacy.comparable_crops == ()