"""Fast tests for PostgreSQL-polling worker coordination and orphan recovery."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from via_backend.contexts.agroclimatic_evaluation.application import (
    AgroclimaticEvaluationExecutionService,
    AgroclimaticEvaluationRecoveryService,
    AgroclimaticEvaluationWorker,
    CommonSupportResult,
    CommonSupportStatus,
    CropComparisonRequest,
    CropExecutionStatus,
    CropSuitabilityExecutionError,
    CropSuitabilityRequest,
    CropSuitabilityResult,
    EvaluationResult,
    ExecuteEvaluation,
    InvalidCommandError,
    RecoverEvaluation,
    ResourceConflictError,
    ScientificArtifactDescriptor,
    ScientificArtifactGrid,
    ScientificArtifactRole,
    ScientificExecutionTrace,
    SuitabilityScoreSummary,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    CropOutcome,
    CropOutcomeStatus,
    Evaluation,
    EvaluationStatus,
    ParcelSnapshot,
    ScientificTrace,
    SnapshotGeometry,
    SuitabilitySummary,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    InMemoryEvaluationRepository,
)
from via_backend.worker import run_forever

NOW = datetime(2026, 9, 13, 12, 0, tzinfo=UTC)


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


def _evaluation(
    *,
    evaluation_id: UUID | None = None,
    created_at: datetime = NOW,
    crops: tuple[str, ...] = ("maize",),
) -> Evaluation:
    return Evaluation(
        id=evaluation_id or uuid4(),
        parcel_snapshot=_snapshot(),
        requested_crops=crops,
        status=EvaluationStatus.QUEUED,
        created_at=created_at,
    )


def _engine_result(
    crop_id: str,
    *,
    status: CropExecutionStatus = CropExecutionStatus.SUCCEEDED,
    mean: float | None = 40.0,
) -> CropSuitabilityResult:
    return CropSuitabilityResult(
        crop_id=crop_id,
        status=status,
        suitability=SuitabilityScoreSummary(
            mean=mean,
            minimum=mean,
            maximum=mean,
            valid_cells=0 if status is CropExecutionStatus.NO_COVERAGE else 1,
            valid_area_m2=0.0 if status is CropExecutionStatus.NO_COVERAGE else 25.0,
            coverage_fraction=0.0 if status is CropExecutionStatus.NO_COVERAGE else 1.0,
            zero_suitability_area_m2=25.0 if mean == 0 else 0.0,
        ),
        failure=None,
        trace=ScientificExecutionTrace(
            engine_identifier="fake",
            execution_reference=f"run-{crop_id}",
            started_at=NOW,
            finished_at=NOW,
            elapsed_seconds=0.1,
            execution_mode="test",
            parcel_sha256="parcel",
            parameter_sha256=None,
            configuration_sha256=None,
            source_files_unchanged=True,
        ),
        artifacts=(_artifact(crop_id),),
    )


class FakeEngine:
    def __init__(self, responses: list[CropSuitabilityResult | Exception]) -> None:
        self._responses = iter(responses)
        self.requests: list[CropSuitabilityRequest] = []

    def evaluate(self, request: CropSuitabilityRequest) -> CropSuitabilityResult:
        self.requests.append(request)
        response = next(self._responses)
        if isinstance(response, Exception):
            raise response
        return response

class FakeComparisonEngine:
    def compare(
        self,
        request: CropComparisonRequest,
    ) -> CommonSupportResult:
        crop_ids = tuple(
            crop.crop_id
            for crop in request.crops
        )

        if not crop_ids:
            return CommonSupportResult(
                status=CommonSupportStatus.NO_SUCCESSFUL_CROPS,
                method=None,
                area_crs=None,
                parcel_area_m2=100.0,
                common_valid_area_m2=0.0,
                common_coverage_fraction=0.0,
                eligible_crops=(),
                excluded_without_coverage=(),
            )

        return CommonSupportResult(
            status=CommonSupportStatus.COMPARABLE,
            method="area_weighted_mean_on_common_valid_cells",
            area_crs="EPSG:6933",
            parcel_area_m2=100.0,
            common_valid_area_m2=100.0,
            common_coverage_fraction=1.0,
            eligible_crops=crop_ids,
            excluded_without_coverage=(),
        )

def test_queued_discovery_filters_orders_and_limits() -> None:
    repository = InMemoryEvaluationRepository()
    older = _evaluation(
        evaluation_id=UUID(int=20),
        created_at=NOW - timedelta(minutes=1),
    )
    same_time_first = _evaluation(evaluation_id=UUID(int=1))
    same_time_second = _evaluation(evaluation_id=UUID(int=2))
    active = _evaluation(evaluation_id=UUID(int=0)).prepare()
    for evaluation in (same_time_second, active, older, same_time_first):
        repository.add(evaluation)

    assert repository.list_queued_ids(limit=2) == (
        older.id,
        same_time_first.id,
    )


@pytest.mark.parametrize("limit", [0, -1, True])
def test_queued_discovery_requires_positive_limit(limit: int) -> None:
    with pytest.raises(ValueError, match="positive"):
        InMemoryEvaluationRepository().list_queued_ids(limit=limit)


def test_run_once_executes_through_existing_execution_service() -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = _evaluation()
    repository.add(evaluation)
    engine = FakeEngine([_engine_result("maize")])
    executor = _executor(repository, engine)

    summary = AgroclimaticEvaluationWorker(
        repository,
        executor,
        batch_size=1,
    ).run_once()

    restored = repository.get(evaluation.id)
    assert summary.completed == 1
    assert restored is not None
    assert restored.status is EvaluationStatus.SUCCEEDED
    assert [request.crop_id for request in engine.requests] == ["maize"]


def test_worker_only_delegates_execution_semantics() -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = _evaluation()
    repository.add(evaluation)
    commands: list[ExecuteEvaluation] = []

    class RecordingExecutor:
        def execute_evaluation(self, command: ExecuteEvaluation) -> EvaluationResult:
            commands.append(command)
            return EvaluationResult.from_domain(evaluation)

    summary = AgroclimaticEvaluationWorker(
        repository,
        RecordingExecutor(),
        batch_size=1,
    ).run_once()

    assert commands == [ExecuteEvaluation(evaluation.id)]
    assert repository.get(evaluation.id) == evaluation
    assert summary.completed == 1


def test_no_queued_work_never_calls_engine() -> None:
    repository = InMemoryEvaluationRepository()
    engine = FakeEngine([])
    worker = AgroclimaticEvaluationWorker(
        repository,
        _executor(repository, engine),
        batch_size=2,
    )

    assert worker.run_once().discovered == 0
    assert engine.requests == []


def test_claim_conflict_is_benign_and_later_work_continues() -> None:
    repository = InMemoryEvaluationRepository()
    first = _evaluation(evaluation_id=UUID(int=1))
    second = _evaluation(evaluation_id=UUID(int=2))
    repository.add(first)
    repository.add(second)
    engine = FakeEngine([_engine_result("maize")])
    executor = _executor(repository, engine)

    class ContendingExecutor:
        def execute_evaluation(self, command: ExecuteEvaluation):
            if command.evaluation_id == first.id:
                repository.save(
                    first.prepare(),
                    expected_status=EvaluationStatus.QUEUED,
                )
            return executor.execute_evaluation(command)

    summary = AgroclimaticEvaluationWorker(
        repository,
        ContendingExecutor(),
        batch_size=2,
    ).run_once()

    first_after = repository.get(first.id)
    second_after = repository.get(second.id)
    assert summary.conflicted == 1
    assert summary.completed == 1
    assert first_after is not None
    assert first_after.status is EvaluationStatus.PREPARING
    assert first_after.failure_reason is None
    assert second_after is not None
    assert second_after.status is EvaluationStatus.SUCCEEDED


def test_persisted_orchestration_failure_does_not_stop_later_work() -> None:
    repository = InMemoryEvaluationRepository()
    first = _evaluation(evaluation_id=UUID(int=1))
    second = _evaluation(evaluation_id=UUID(int=2))
    repository.add(first)
    repository.add(second)
    engine = FakeEngine(
        [
            CropSuitabilityExecutionError("scientific process failed"),
            _engine_result("maize"),
        ]
    )
    worker = AgroclimaticEvaluationWorker(
        repository,
        _executor(repository, engine),
        batch_size=2,
    )

    summary = worker.run_once()

    first_after = repository.get(first.id)
    second_after = repository.get(second.id)
    assert summary.failed == 1
    assert summary.completed == 1
    assert first_after is not None
    assert first_after.status is EvaluationStatus.FAILED
    assert second_after is not None
    assert second_after.status is EvaluationStatus.SUCCEEDED


def test_unpersisted_unexpected_failure_escapes_as_systemic() -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = _evaluation()
    repository.add(evaluation)

    class BrokenExecutor:
        def execute_evaluation(self, command: ExecuteEvaluation):
            raise RuntimeError(f"database unavailable for {command.evaluation_id}")

    worker = AgroclimaticEvaluationWorker(
        repository,
        BrokenExecutor(),
        batch_size=1,
    )

    with pytest.raises(RuntimeError, match="database unavailable"):
        worker.run_once()


def test_run_forever_sleeps_after_non_full_batch() -> None:
    repository = InMemoryEvaluationRepository()
    worker = AgroclimaticEvaluationWorker(
        repository,
        _executor(repository, FakeEngine([])),
        batch_size=1,
    )
    sleeps: list[float] = []

    def interrupting_sleep(seconds: float) -> None:
        sleeps.append(seconds)
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        run_forever(
            worker,
            poll_interval_seconds=2.5,
            sleeper=interrupting_sleep,
        )

    assert sleeps == [2.5]


def _outcome() -> CropOutcome:
    return CropOutcome(
        crop_id="maize",
        status=CropOutcomeStatus.SUCCEEDED,
        suitability=SuitabilitySummary(0.0, 0.0, 0.0, 1, 25.0, 1.0, 25.0),
        failure_message=None,
        trace=ScientificTrace(
            "fake",
            "run-maize",
            NOW,
            NOW,
            0.1,
            "test",
            "parcel",
            None,
            None,
            True,
        ),
    )


def _evaluation_in_status(status: EvaluationStatus) -> Evaluation:
    evaluation = _evaluation()
    if status is EvaluationStatus.QUEUED:
        return evaluation
    if status is EvaluationStatus.PREPARING:
        return evaluation.prepare()
    running = evaluation.prepare().start_running()
    if status is EvaluationStatus.RUNNING:
        return running
    running = running.record_outcome(_outcome())
    if status is EvaluationStatus.SUMMARIZING:
        return running.start_summarizing()
    if status is EvaluationStatus.SUCCEEDED:
        return running.start_summarizing().succeed()
    if status is EvaluationStatus.FAILED:
        return running.fail("existing failure")
    return replace(evaluation, status=EvaluationStatus.CANCELLED)


@pytest.mark.parametrize(
    "status",
    [
        EvaluationStatus.PREPARING,
        EvaluationStatus.RUNNING,
        EvaluationStatus.SUMMARIZING,
    ],
)
def test_explicit_recovery_fails_active_evaluation_and_preserves_outcomes(
    status: EvaluationStatus,
) -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = _evaluation_in_status(status)
    repository.add(evaluation)

    result = AgroclimaticEvaluationRecoveryService(repository).recover_evaluation(
        RecoverEvaluation(evaluation.id, "worker process terminated")
    )

    restored = repository.get(evaluation.id)
    assert result.status is EvaluationStatus.FAILED
    assert restored is not None
    assert restored.failure_reason == "worker process terminated"
    assert restored.outcomes == evaluation.outcomes


@pytest.mark.parametrize(
    "status",
    [
        EvaluationStatus.QUEUED,
        EvaluationStatus.SUCCEEDED,
        EvaluationStatus.FAILED,
        EvaluationStatus.CANCELLED,
    ],
)
def test_explicit_recovery_rejects_non_active_status(
    status: EvaluationStatus,
) -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = _evaluation_in_status(status)
    repository.add(evaluation)

    with pytest.raises(InvalidCommandError, match="cannot fail"):
        AgroclimaticEvaluationRecoveryService(repository).recover_evaluation(
            RecoverEvaluation(evaluation.id, "operator confirmed orphan")
        )


def test_explicit_recovery_requires_non_empty_reason() -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = _evaluation().prepare()
    repository.add(evaluation)

    with pytest.raises(InvalidCommandError, match="non-empty"):
        AgroclimaticEvaluationRecoveryService(repository).recover_evaluation(
            RecoverEvaluation(evaluation.id, "   ")
        )


def test_explicit_recovery_uses_expected_status() -> None:
    class RecordingRepository(InMemoryEvaluationRepository):
        def __init__(self) -> None:
            super().__init__()
            self.expected_statuses: list[EvaluationStatus] = []

        def save(
            self,
            evaluation: Evaluation,
            *,
            expected_status: EvaluationStatus,
        ) -> None:
            self.expected_statuses.append(expected_status)
            super().save(evaluation, expected_status=expected_status)

    repository = RecordingRepository()
    evaluation = _evaluation().prepare().start_running()
    repository.add(evaluation)

    AgroclimaticEvaluationRecoveryService(repository).recover_evaluation(
        RecoverEvaluation(evaluation.id, "worker process terminated")
    )

    assert repository.expected_statuses == [EvaluationStatus.RUNNING]


def test_concurrent_recovery_reports_conflict_without_overwrite() -> None:
    class ConcurrentRepository(InMemoryEvaluationRepository):
        def save(
            self,
            evaluation: Evaluation,
            *,
            expected_status: EvaluationStatus,
        ) -> None:
            current = self.get(evaluation.id)
            assert current is not None
            super().save(
                current.fail("another operator recovered it"),
                expected_status=expected_status,
            )
            super().save(evaluation, expected_status=expected_status)

    repository = ConcurrentRepository()
    evaluation = _evaluation().prepare().start_running()
    repository.add(evaluation)

    with pytest.raises(ResourceConflictError, match="changed"):
        AgroclimaticEvaluationRecoveryService(repository).recover_evaluation(
            RecoverEvaluation(evaluation.id, "stale recovery command")
        )

    restored = repository.get(evaluation.id)
    assert restored is not None
    assert restored.failure_reason == "another operator recovered it"

def _artifact(crop_id: str) -> ScientificArtifactDescriptor:
    return ScientificArtifactDescriptor(
        role=ScientificArtifactRole.CROP_SUITABILITY,
        storage_reference=(
            f"evaluations/fake/crops/{crop_id}/crop_suitability.tif"
        ),
        sha256="b" * 64,
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

def _executor(
    repository: InMemoryEvaluationRepository,
    engine: FakeEngine,
) -> AgroclimaticEvaluationExecutionService:
    return AgroclimaticEvaluationExecutionService(
        repository,
        engine,
        FakeComparisonEngine(),
    )