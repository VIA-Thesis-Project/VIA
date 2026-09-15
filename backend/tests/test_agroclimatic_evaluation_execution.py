"""Fast tests for synchronous Agroclimatic Evaluation orchestration."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.application import (
    AgroclimaticEvaluationExecutionService,
    CommonSupportResult,
    CommonSupportStatus,
    ComparableCropResult,
    CropComparisonExecutionError,
    CropComparisonRequest,
    CropComparisonResult,
    CropExecutionStatus,
    CropSuitabilityExecutionError,
    CropSuitabilityRequest,
    CropSuitabilityResult,
    ExecuteEvaluation,
    ResourceConflictError,
    ScientificArtifactDescriptor,
    ScientificArtifactGrid,
    ScientificArtifactRole,
    ScientificExecutionFailure,
    ScientificExecutionTrace,
    SuitabilityScoreSummary,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    CropOutcome,
    CropOutcomeStatus,
    Evaluation,
    EvaluationConflictError,
    EvaluationStatus,
    ParcelSnapshot,
    ScientificTrace,
    SnapshotGeometry,
    SuitabilitySummary,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    InMemoryEvaluationRepository,
)

NOW = datetime(2026, 9, 12, 15, 0, tzinfo=UTC)


def _snapshot() -> ParcelSnapshot:
    return ParcelSnapshot(
        project_id=uuid4(),
        parcel_id=uuid4(),
        parcel_version=3,
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


def _evaluation(crops: tuple[str, ...] = ("maize", "potato", "rice")) -> Evaluation:
    return Evaluation(
        id=uuid4(),
        parcel_snapshot=_snapshot(),
        requested_crops=crops,
        status=EvaluationStatus.QUEUED,
        created_at=NOW,
    )

def _artifact(crop_id: str) -> ScientificArtifactDescriptor:
    return ScientificArtifactDescriptor(
        role=ScientificArtifactRole.CROP_SUITABILITY,
        storage_reference=(
            f"evaluations/fake/crops/{crop_id}/crop_suitability.tif"
        ),
        sha256="a" * 64,
        media_type="image/tiff",
        size_bytes=128,
        grid=ScientificArtifactGrid(
            crs="EPSG:4326",
            width=1,
            height=1,
            transform=(
                0.01,
                0.0,
                -77.6,
                0.0,
                -0.01,
                -11.0,
            ),
            nodata=-1.0,
        ),
    )

def _result(
    crop_id: str,
    status: CropExecutionStatus = CropExecutionStatus.SUCCEEDED,
    *,
    mean: float | None = 72.5,
) -> CropSuitabilityResult:
    failed = status is CropExecutionStatus.FAILED
    suitability = (
        None
        if failed
        else SuitabilityScoreSummary(
            mean=mean,
            minimum=mean,
            maximum=mean,
            valid_cells=0 if status is CropExecutionStatus.NO_COVERAGE else 2,
            valid_area_m2=(
                0.0 if status is CropExecutionStatus.NO_COVERAGE else 25.0
            ),
            coverage_fraction=(
                0.0 if status is CropExecutionStatus.NO_COVERAGE else 0.5
            ),
            zero_suitability_area_m2=25.0 if mean == 0 else 0.0,
        )
    )
    return CropSuitabilityResult(
        crop_id=crop_id,
        status=status,
        suitability=suitability,
        failure=(
            ScientificExecutionFailure("reported crop failure") if failed else None
        ),
        trace=ScientificExecutionTrace(
            engine_identifier="CropSuiteLite",
            execution_reference=f"opaque-{crop_id}",
            started_at=NOW,
            finished_at=NOW,
            elapsed_seconds=1.25,
            execution_mode="sequential_isolated_processes",
            parcel_sha256="parcel-sha256",
            parameter_sha256=f"parameter-{crop_id}",
            configuration_sha256="configuration-sha256",
            source_files_unchanged=True,
        ),
        artifacts=() if failed else (_artifact(crop_id),),
    )


class FakeEngine:
    def __init__(
        self, responses: list[CropSuitabilityResult | Exception]
    ) -> None:
        self._responses = iter(responses)
        self.requests: list[CropSuitabilityRequest] = []

    def evaluate(self, request: CropSuitabilityRequest) -> CropSuitabilityResult:
        self.requests.append(request)
        response = next(self._responses)
        if isinstance(response, Exception):
            raise response
        return response

class FakeComparisonEngine:
    def __init__(
        self,
        error: Exception | None = None,
    ) -> None:
        self.error = error
        self.requests: list[CropComparisonRequest] = []

    def compare(
        self,
        request: CropComparisonRequest,
    ) -> CropComparisonResult:
        self.requests.append(request)

        if self.error is not None:
            raise self.error

        crop_ids = tuple(
            crop.crop_id
            for crop in request.crops
        )

        if not crop_ids:
            return CropComparisonResult(
                common_support=CommonSupportResult(
                    status=CommonSupportStatus.NO_SUCCESSFUL_CROPS,
                    method=None,
                    area_crs=None,
                    parcel_area_m2=100.0,
                    common_valid_area_m2=0.0,
                    common_coverage_fraction=0.0,
                    eligible_crops=(),
                    excluded_without_coverage=(),
                ),
                comparable_crops=(),
            )

        return CropComparisonResult(
            common_support=CommonSupportResult(
                status=CommonSupportStatus.COMPARABLE,
                method="area_weighted_mean_on_common_valid_cells",
                area_crs="EPSG:6933",
                parcel_area_m2=100.0,
                common_valid_area_m2=80.0,
                common_coverage_fraction=0.8,
                eligible_crops=crop_ids,
                excluded_without_coverage=(),
            ),
            comparable_crops=tuple(
                ComparableCropResult(
                    crop_id=crop_id,
                    mean=70.0 - index,
                    rank=index + 1,
                )
                for index, crop_id in enumerate(crop_ids)
            ),
        )

class RecordingRepository(InMemoryEvaluationRepository):
    def __init__(self) -> None:
        super().__init__()
        self.saved_statuses: list[EvaluationStatus] = []

    def save(
        self, evaluation: Evaluation, *, expected_status: EvaluationStatus
    ) -> None:
        super().save(evaluation, expected_status=expected_status)
        self.saved_statuses.append(evaluation.status)


def _execute(
    evaluation: Evaluation,
    responses: list[CropSuitabilityResult | Exception],
) -> tuple[RecordingRepository, FakeEngine]:
    repository = RecordingRepository()
    repository.add(evaluation)
    engine = FakeEngine(responses)
    AgroclimaticEvaluationExecutionService(
        repository,
        engine,
        FakeComparisonEngine(),
    ).execute_evaluation(
        ExecuteEvaluation(evaluation.id)
    )
    return repository, engine


def test_executes_one_request_per_crop_in_deterministic_order() -> None:
    evaluation = _evaluation()
    repository, engine = _execute(
        evaluation,
        [_result("maize"), _result("potato"), _result("rice")],
    )

    assert [request.crop_id for request in engine.requests] == [
        "maize",
        "potato",
        "rice",
    ]
    assert all(request.evaluation_id == evaluation.id for request in engine.requests)
    assert all(
        request.parcel_snapshot is evaluation.parcel_snapshot
        for request in engine.requests
    )
    assert repository.saved_statuses == [
        EvaluationStatus.PREPARING,
        EvaluationStatus.RUNNING,
        EvaluationStatus.SUMMARIZING,
        EvaluationStatus.SUCCEEDED,
    ]


@pytest.mark.parametrize(
    ("status", "mean"),
    [
        (CropExecutionStatus.SUCCEEDED, 64.5),
        (CropExecutionStatus.SUCCEEDED, 0.0),
        (CropExecutionStatus.NO_COVERAGE, None),
    ],
)
def test_completed_scientific_outcome_semantics_are_persisted(
    status: CropExecutionStatus,
    mean: float | None,
) -> None:
    evaluation = _evaluation(("maize",))
    repository, _ = _execute(evaluation, [_result("maize", status, mean=mean)])

    restored = repository.get(evaluation.id)
    assert restored is not None
    assert restored.status is EvaluationStatus.SUCCEEDED
    assert restored.outcomes[0].status.value == status.value
    assert restored.outcomes[0].suitability is not None
    assert restored.outcomes[0].suitability.mean == mean
    if mean == 0:
        assert restored.outcomes[0].suitability.zero_suitability_area_m2 == 25.0


def test_explicit_crop_failure_is_persisted_and_later_crops_continue() -> None:
    evaluation = _evaluation()
    repository, engine = _execute(
        evaluation,
        [
            _result("maize", CropExecutionStatus.FAILED),
            _result("potato"),
            _result("rice"),
        ],
    )

    restored = repository.get(evaluation.id)
    assert restored is not None
    assert [request.crop_id for request in engine.requests] == list(
        evaluation.requested_crops
    )
    assert restored.status is EvaluationStatus.SUCCEEDED
    assert restored.outcomes[0].status is CropOutcomeStatus.FAILED
    assert restored.outcomes[0].failure_message == "reported crop failure"
    assert len(restored.outcomes) == 3


def test_all_explicit_crop_failures_still_complete_the_orchestration() -> None:
    evaluation = _evaluation(("maize", "potato"))
    repository, _ = _execute(
        evaluation,
        [
            _result("maize", CropExecutionStatus.FAILED),
            _result("potato", CropExecutionStatus.FAILED),
        ],
    )

    restored = repository.get(evaluation.id)
    assert restored is not None
    assert restored.status is EvaluationStatus.SUCCEEDED
    assert all(
        outcome.status is CropOutcomeStatus.FAILED
        for outcome in restored.outcomes
    )


def test_fatal_engine_error_stops_execution_and_marks_evaluation_failed() -> None:
    evaluation = _evaluation()
    repository = RecordingRepository()
    repository.add(evaluation)
    engine = FakeEngine(
        [
            _result("maize"),
            CropSuitabilityExecutionError("engine boundary unavailable"),
            _result("rice"),
        ]
    )
    service = AgroclimaticEvaluationExecutionService(
        repository, 
        engine,
        FakeComparisonEngine()
    )

    with pytest.raises(
        CropSuitabilityExecutionError, match="engine boundary unavailable"
    ):
        service.execute_evaluation(ExecuteEvaluation(evaluation.id))

    restored = repository.get(evaluation.id)
    assert restored is not None
    assert [request.crop_id for request in engine.requests] == ["maize", "potato"]
    assert restored.status is EvaluationStatus.FAILED
    assert len(restored.outcomes) == 1
    assert restored.failure_reason == (
        "CropSuitabilityExecutionError: engine boundary unavailable"
    )


def test_non_queued_evaluation_is_rejected_without_engine_call() -> None:
    repository = RecordingRepository()
    evaluation = _evaluation().prepare()
    repository.add(evaluation)
    engine = FakeEngine([])

    with pytest.raises(ResourceConflictError, match="preparing"):
        AgroclimaticEvaluationExecutionService(
            repository, engine, FakeComparisonEngine(),
        ).execute_evaluation(ExecuteEvaluation(evaluation.id))

    assert engine.requests == []
    assert repository.saved_statuses == []


def test_duplicate_crop_outcome_is_rejected() -> None:
    evaluation = _evaluation(("maize",))
    repository = InMemoryEvaluationRepository()
    repository.add(evaluation)
    preparing = evaluation.prepare()
    repository.save(preparing, expected_status=EvaluationStatus.QUEUED)
    running = preparing.start_running()
    repository.save(running, expected_status=EvaluationStatus.PREPARING)
    outcome = CropOutcome(
        crop_id="maize",
        status=CropOutcomeStatus.SUCCEEDED,
        suitability=SuitabilitySummary(0.0, 0.0, 0.0, 1, 25.0, 1.0, 25.0),
        failure_message=None,
        trace=ScientificTrace(
            "CropSuiteLite",
            "opaque-reference",
            NOW,
            NOW,
            0.5,
            "sequential_isolated_processes",
            "parcel-sha256",
            None,
            None,
            True,
        ),
    )
    repository.add_outcome(evaluation.id, outcome)

    with pytest.raises(EvaluationConflictError):
        repository.add_outcome(evaluation.id, outcome)


def test_only_one_stale_queued_claim_can_be_saved() -> None:
    evaluation = _evaluation(("maize",))
    repository = InMemoryEvaluationRepository()
    repository.add(evaluation)
    first_claim = evaluation.prepare()
    stale_claim = evaluation.prepare()

    repository.save(first_claim, expected_status=EvaluationStatus.QUEUED)

    with pytest.raises(EvaluationConflictError):
        repository.save(stale_claim, expected_status=EvaluationStatus.QUEUED)


def test_all_reliable_outcome_and_trace_fields_round_trip_in_memory() -> None:
    evaluation = _evaluation(("maize",))
    repository, _ = _execute(evaluation, [_result("maize")])

    restored = repository.get(evaluation.id)
    assert restored is not None
    outcome = restored.outcomes[0]
    assert outcome.suitability == SuitabilitySummary(
        mean=72.5,
        minimum=72.5,
        maximum=72.5,
        valid_cells=2,
        valid_area_m2=25.0,
        coverage_fraction=0.5,
        zero_suitability_area_m2=0.0,
    )
    assert outcome.trace == ScientificTrace(
        engine_identifier="CropSuiteLite",
        execution_reference="opaque-maize",
        started_at=NOW,
        finished_at=NOW,
        elapsed_seconds=1.25,
        execution_mode="sequential_isolated_processes",
        parcel_sha256="parcel-sha256",
        parameter_sha256="parameter-maize",
        configuration_sha256="configuration-sha256",
        source_files_unchanged=True,
    )

def test_summarizing_compares_only_non_failed_crop_outcomes() -> None:
    evaluation = _evaluation()
    repository = RecordingRepository()
    repository.add(evaluation)

    engine = FakeEngine(
        [
            _result("maize", CropExecutionStatus.FAILED),
            _result("potato"),
            _result(
                "rice",
                CropExecutionStatus.NO_COVERAGE,
                mean=None,
            ),
        ]
    )
    comparison = FakeComparisonEngine()

    AgroclimaticEvaluationExecutionService(
        repository,
        engine,
        comparison,
    ).execute_evaluation(
        ExecuteEvaluation(evaluation.id)
    )

    assert len(comparison.requests) == 1

    request = comparison.requests[0]

    assert tuple(
        crop.crop_id
        for crop in request.crops
    ) == ("potato", "rice")

    restored = repository.get(evaluation.id)

    assert restored is not None
    assert restored.status is EvaluationStatus.SUCCEEDED
    assert restored.common_support is not None
    assert restored.common_support.eligible_crops == (
        "potato",
        "rice",
    )

def test_comparison_failure_marks_summarizing_evaluation_failed() -> None:
    evaluation = _evaluation(("maize",))
    repository = RecordingRepository()
    repository.add(evaluation)

    engine = FakeEngine([_result("maize")])
    comparison = FakeComparisonEngine(
        CropComparisonExecutionError(
            "comparison boundary unavailable"
        )
    )

    service = AgroclimaticEvaluationExecutionService(
        repository,
        engine,
        comparison,
    )

    with pytest.raises(
        CropComparisonExecutionError,
        match="comparison boundary unavailable",
    ):
        service.execute_evaluation(
            ExecuteEvaluation(evaluation.id)
        )

    restored = repository.get(evaluation.id)

    assert restored is not None
    assert restored.status is EvaluationStatus.FAILED
    assert len(restored.outcomes) == 1
    assert restored.common_support is None
    assert restored.failure_reason == (
        "CropComparisonExecutionError: "
        "comparison boundary unavailable"
    )

    assert repository.saved_statuses == [
        EvaluationStatus.PREPARING,
        EvaluationStatus.RUNNING,
        EvaluationStatus.SUMMARIZING,
        EvaluationStatus.FAILED,
    ]