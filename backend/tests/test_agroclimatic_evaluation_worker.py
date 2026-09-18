"""Fast tests for PostgreSQL-polling worker coordination and orphan recovery."""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from via_backend.config import WorkerSettings
from via_backend.contexts.agroclimatic_evaluation.application import (
    AgroclimaticEvaluationExecutionService,
    AgroclimaticEvaluationRecoveryService,
    AgroclimaticEvaluationWorker,
    CommonSupportResult,
    CommonSupportStatus,
    ComparableCropResult,
    CropComparisonRequest,
    CropComparisonResult,
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
    CommonSupport as DomainCommonSupport,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    CommonSupportStatus as DomainCommonSupportStatus,
)
from via_backend.contexts.agroclimatic_evaluation.domain import (
    CropOutcome,
    CropOutcomeStatus,
    EnvironmentalInputManifest,
    EnvironmentalInputReference,
    EnvironmentalInputSnapshot,
    Evaluation,
    EvaluationStatus,
    ParcelSnapshot,
    ScientificTrace,
    SnapshotGeometry,
    SuitabilitySummary,
    WaterRegime,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    InMemoryEvaluationRepository,
)
from via_backend.contexts.environmental_information.application.public import (
    GetPublishedDatasetVersion,
    PublishedDatasetVersion,
)
from via_backend.worker import create_worker, run_forever

NOW = datetime(2026, 9, 13, 12, 0, tzinfo=UTC)
RESOLVED_AT = NOW + timedelta(minutes=1)
DATASET_ID = UUID("10000000-0000-0000-0000-000000000001")
DATASET_VERSION_ID = UUID("20000000-0000-0000-0000-000000000001")


def test_create_worker_fails_fast_on_invalid_scientific_input_bindings(
    tmp_path: Path,
) -> None:
    bindings = tmp_path / "bindings.json"
    bindings.write_text(json.dumps({"bindings": []}), encoding="utf-8")
    settings = WorkerSettings(
        database_url="postgresql+psycopg://example.invalid/via",
        cropsuite_root=tmp_path / "CropSuiteLite",
        cropsuite_python=tmp_path / "python.exe",
        cropsuite_workspace=tmp_path / "workspace",
        artifacts_root=tmp_path / "artifacts",
        cropsuite_input_bindings=bindings,
    )

    with pytest.raises(ValueError, match="non-empty 'bindings'"):
        create_worker(settings)


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


def _reference() -> EnvironmentalInputReference:
    return EnvironmentalInputReference(
        input_key="soil.ph",
        dataset_id=DATASET_ID,
        dataset_version_id=DATASET_VERSION_ID,
    )


def _published() -> PublishedDatasetVersion:
    return PublishedDatasetVersion(
        dataset_id=DATASET_ID,
        dataset_name="Soil pH",
        source="Open catalog",
        variable="phh2o",
        unit="pH",
        dataset_version_id=DATASET_VERSION_ID,
        version_identifier="2026-09",
        checksum="sha256:abc",
        storage_reference="catalog://soil/ph/2026-09",
        crs="EPSG:4326",
        resolution_x=0.01,
        resolution_y=0.01,
        resolution_unit="degree",
        extent_west=-77.8,
        extent_south=-12.7,
        extent_east=-76.2,
        extent_north=-10.4,
        valid_from=None,
        valid_to=None,
        scenario=None,
        registered_at=NOW,
    )


def _manifest() -> EnvironmentalInputManifest:
    published = _published()
    return EnvironmentalInputManifest(
        resolved_at=RESOLVED_AT,
        inputs=(
            EnvironmentalInputSnapshot(
                input_key="soil.ph",
                dataset_id=published.dataset_id,
                dataset_name=published.dataset_name,
                source=published.source,
                variable=published.variable,
                unit=published.unit,
                dataset_version_id=published.dataset_version_id,
                version_identifier=published.version_identifier,
                checksum=published.checksum,
                storage_reference=published.storage_reference,
                crs=published.crs,
                resolution_x=published.resolution_x,
                resolution_y=published.resolution_y,
                resolution_unit=published.resolution_unit,
                extent_west=published.extent_west,
                extent_south=published.extent_south,
                extent_east=published.extent_east,
                extent_north=published.extent_north,
                valid_from=published.valid_from,
                valid_to=published.valid_to,
                scenario=published.scenario,
                registered_at=published.registered_at,
            ),
        ),
    )


class FakeEnvironmentalInformation:
    def get_published_dataset_version(
        self,
        query: GetPublishedDatasetVersion,
    ) -> PublishedDatasetVersion | None:
        if query == GetPublishedDatasetVersion(DATASET_ID, DATASET_VERSION_ID):
            return _published()
        return None


def _evaluation(
    *,
    evaluation_id: UUID | None = None,
    created_at: datetime = NOW,
    crops: tuple[str, ...] = ("maize",),
    water_regimes: tuple[WaterRegime, ...] = (WaterRegime.RAINFED,),
) -> Evaluation:
    return Evaluation(
        id=evaluation_id or uuid4(),
        parcel_snapshot=_snapshot(),
        requested_crops=crops,
        requested_water_regimes=water_regimes,
        status=EvaluationStatus.QUEUED,
        created_at=created_at,
        environmental_input_references=(_reference(),),
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
            valid_cells=(
                0
                if status is CropExecutionStatus.NO_COVERAGE
                else 1
            ),
            valid_area_m2=(
                0.0
                if status is CropExecutionStatus.NO_COVERAGE
                else 25.0
            ),
            coverage_fraction=(
                0.0
                if status is CropExecutionStatus.NO_COVERAGE
                else 1.0
            ),
            zero_suitability_area_m2=(
                25.0
                if mean == 0
                else 0.0
            ),
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
    def __init__(
        self,
        responses: list[CropSuitabilityResult | Exception],
    ) -> None:
        self._responses = iter(responses)
        self.requests: list[CropSuitabilityRequest] = []

    def evaluate(
        self,
        request: CropSuitabilityRequest,
    ) -> CropSuitabilityResult:
        self.requests.append(request)
        response = next(self._responses)

        if isinstance(response, Exception):
            raise response

        return response


class FakeComparisonEngine:
    def compare(
        self,
        request: CropComparisonRequest,
    ) -> CropComparisonResult:
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
                common_valid_area_m2=100.0,
                common_coverage_fraction=1.0,
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


def test_queued_discovery_filters_orders_and_limits() -> None:
    repository = InMemoryEvaluationRepository()
    older = _evaluation(
        evaluation_id=UUID(int=20),
        created_at=NOW - timedelta(minutes=1),
    )
    same_time_first = _evaluation(evaluation_id=UUID(int=1))
    same_time_second = _evaluation(evaluation_id=UUID(int=2))
    active = _evaluation(
        evaluation_id=UUID(int=0)
    ).prepare()

    for evaluation in (
        same_time_second,
        active,
        older,
        same_time_first,
    ):
        repository.add(evaluation)

    assert repository.list_queued_ids(limit=2) == (
        older.id,
        same_time_first.id,
    )


@pytest.mark.parametrize("limit", [0, -1, True])
def test_queued_discovery_requires_positive_limit(
    limit: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="positive",
    ):
        InMemoryEvaluationRepository().list_queued_ids(
            limit=limit
        )


def test_run_once_executes_through_existing_execution_service() -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = _evaluation()
    repository.add(evaluation)

    engine = FakeEngine(
        [_engine_result("maize")]
    )
    executor = _executor(
        repository,
        engine,
    )

    summary = AgroclimaticEvaluationWorker(
        repository,
        executor,
        batch_size=1,
    ).run_once()

    restored = repository.get(evaluation.id)

    assert summary.completed == 1
    assert summary.deferred == 0
    assert restored is not None
    assert restored.status is EvaluationStatus.SUCCEEDED
    assert [
        request.crop_id
        for request in engine.requests
    ] == ["maize"]


def test_worker_only_delegates_execution_semantics() -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = _evaluation()
    repository.add(evaluation)

    commands: list[ExecuteEvaluation] = []

    class RecordingExecutor:
        def execute_evaluation(
            self,
            command: ExecuteEvaluation,
        ) -> EvaluationResult:
            commands.append(command)
            return EvaluationResult.from_domain(
                evaluation
            )

    summary = AgroclimaticEvaluationWorker(
        repository,
        RecordingExecutor(),
        batch_size=1,
    ).run_once()

    assert commands == [
        ExecuteEvaluation(evaluation.id)
    ]
    assert (
        repository.get(evaluation.id)
        == evaluation
    )
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


def test_stop_before_first_item_defers_entire_discovered_batch() -> None:
    repository = InMemoryEvaluationRepository()
    first = _evaluation(evaluation_id=UUID(int=1))
    second = _evaluation(evaluation_id=UUID(int=2))
    repository.add(first)
    repository.add(second)
    engine = FakeEngine([])

    summary = AgroclimaticEvaluationWorker(
        repository,
        _executor(repository, engine),
        batch_size=2,
    ).run_once(stop_requested=lambda: True)

    assert summary.discovered == 2
    assert summary.completed == 0
    assert summary.conflicted == 0
    assert summary.failed == 0
    assert summary.deferred == 2
    assert engine.requests == []
    assert repository.get(first.id) == first
    assert repository.get(second.id) == second


def test_stop_after_first_item_defers_remaining_discovered_work() -> None:
    repository = InMemoryEvaluationRepository()
    first = _evaluation(evaluation_id=UUID(int=1))
    second = _evaluation(evaluation_id=UUID(int=2))
    repository.add(first)
    repository.add(second)
    engine = FakeEngine([_engine_result("maize")])

    summary = AgroclimaticEvaluationWorker(
        repository,
        _executor(repository, engine),
        batch_size=2,
    ).run_once(stop_requested=lambda: bool(engine.requests))

    assert summary.discovered == 2
    assert summary.completed == 1
    assert summary.conflicted == 0
    assert summary.failed == 0
    assert summary.deferred == 1
    first_after = repository.get(first.id)
    second_after = repository.get(second.id)
    assert first_after is not None
    assert first_after.status is EvaluationStatus.SUCCEEDED
    assert second_after == second


def test_claim_conflict_is_benign_and_later_work_continues() -> None:
    repository = InMemoryEvaluationRepository()

    first = _evaluation(
        evaluation_id=UUID(int=1)
    )
    second = _evaluation(
        evaluation_id=UUID(int=2)
    )

    repository.add(first)
    repository.add(second)

    engine = FakeEngine(
        [_engine_result("maize")]
    )
    executor = _executor(
        repository,
        engine,
    )

    class ContendingExecutor:
        def execute_evaluation(
            self,
            command: ExecuteEvaluation,
        ):
            if command.evaluation_id == first.id:
                repository.save(
                    first.prepare(),
                    expected_status=(
                        EvaluationStatus.QUEUED
                    ),
                )

            return executor.execute_evaluation(
                command
            )

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
    assert (
        first_after.status
        is EvaluationStatus.PREPARING
    )
    assert first_after.failure_reason is None

    assert second_after is not None
    assert (
        second_after.status
        is EvaluationStatus.SUCCEEDED
    )


def test_persisted_orchestration_failure_does_not_stop_later_work() -> None:
    repository = InMemoryEvaluationRepository()

    first = _evaluation(
        evaluation_id=UUID(int=1)
    )
    second = _evaluation(
        evaluation_id=UUID(int=2)
    )

    repository.add(first)
    repository.add(second)

    engine = FakeEngine(
        [
            CropSuitabilityExecutionError(
                "scientific process failed"
            ),
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
    assert (
        first_after.status
        is EvaluationStatus.FAILED
    )

    assert second_after is not None
    assert (
        second_after.status
        is EvaluationStatus.SUCCEEDED
    )


def test_unpersisted_unexpected_failure_escapes_as_systemic() -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = _evaluation()
    repository.add(evaluation)

    class BrokenExecutor:
        def execute_evaluation(
            self,
            command: ExecuteEvaluation,
        ):
            raise RuntimeError(
                "database unavailable for "
                f"{command.evaluation_id}"
            )

    worker = AgroclimaticEvaluationWorker(
        repository,
        BrokenExecutor(),
        batch_size=1,
    )

    with pytest.raises(
        RuntimeError,
        match="database unavailable",
    ):
        worker.run_once()


def test_run_forever_waits_after_non_full_batch() -> None:
    repository = InMemoryEvaluationRepository()

    worker = AgroclimaticEvaluationWorker(
        repository,
        _executor(
            repository,
            FakeEngine([]),
        ),
        batch_size=1,
    )

    waits: list[float] = []

    def interrupting_wait(
        seconds: float,
    ) -> bool:
        waits.append(seconds)
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        run_forever(
            worker,
            poll_interval_seconds=2.5,
            wait_for_stop=interrupting_wait,
        )

    assert waits == [2.5]


def _outcome(
    *,
    water_regime: WaterRegime = WaterRegime.RAINFED,
) -> CropOutcome:
    return CropOutcome(
        crop_id="maize",
        status=CropOutcomeStatus.SUCCEEDED,
        suitability=SuitabilitySummary(
            0.0,
            0.0,
            0.0,
            1,
            25.0,
            1.0,
            25.0,
        ),
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
        water_regime=water_regime,
    )


def _evaluation_in_status(
    status: EvaluationStatus,
) -> Evaluation:
    evaluation = _evaluation()

    if status is EvaluationStatus.QUEUED:
        return evaluation

    if status is EvaluationStatus.PREPARING:
        return evaluation.prepare()

    running = (
        evaluation
        .prepare()
        .attach_environmental_input_manifest(_manifest())
        .start_running()
    )

    if status is EvaluationStatus.RUNNING:
        return running

    running = running.record_outcome(
        _outcome()
    )

    if status is EvaluationStatus.SUMMARIZING:
        return running.start_summarizing()

    if status is EvaluationStatus.SUCCEEDED:
        return (
            running
            .start_summarizing()
            .record_common_support(
                DomainCommonSupport(
                    status=DomainCommonSupportStatus.COMPARABLE,
                    method="area_weighted_mean_on_common_valid_cells",
                    area_crs="EPSG:6933",
                    parcel_area_m2=25.0,
                    common_valid_area_m2=25.0,
                    common_coverage_fraction=1.0,
                    eligible_crops=("maize",),
                    excluded_without_coverage=(),
                )
            )
            .succeed()
        )

    if status is EvaluationStatus.FAILED:
        return running.fail(
            "existing failure"
        )

    return replace(
        evaluation,
        status=EvaluationStatus.CANCELLED,
    )


def test_active_discovery_filters_orders_limits_and_reports_counts() -> None:
    repository = InMemoryEvaluationRepository()
    older = replace(
        _evaluation_in_status(EvaluationStatus.PREPARING),
        id=UUID(int=20),
        created_at=NOW - timedelta(minutes=1),
    )
    same_time_first = replace(
        _evaluation_in_status(EvaluationStatus.RUNNING),
        id=UUID(int=1),
    )
    same_time_second = replace(
        _evaluation_in_status(EvaluationStatus.SUMMARIZING),
        id=UUID(int=2),
    )
    inactive = _evaluation_in_status(EvaluationStatus.FAILED)
    for evaluation in (same_time_second, inactive, older, same_time_first):
        repository.add(evaluation)

    results = AgroclimaticEvaluationRecoveryService(
        repository
    ).list_active_evaluations(limit=2)

    assert [result.evaluation_id for result in results] == [
        older.id,
        same_time_first.id,
    ]
    assert results[0].requested_crop_count == 1
    assert results[0].completed_crop_count == 0
    assert results[1].requested_crop_count == 1
    assert results[1].completed_crop_count == 0


@pytest.mark.parametrize("limit", [0, -1, True, 1.5])
def test_active_discovery_requires_positive_integer_limit(limit: object) -> None:
    with pytest.raises(ValueError, match="positive"):
        InMemoryEvaluationRepository().list_active(limit=limit)  # type: ignore[arg-type]


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

    result = (
        AgroclimaticEvaluationRecoveryService(
            repository
        ).recover_evaluation(
            RecoverEvaluation(
                evaluation.id,
                status,
                "worker process terminated",
            )
        )
    )

    restored = repository.get(
        evaluation.id
    )

    assert (
        result.status
        is EvaluationStatus.FAILED
    )
    assert restored is not None
    assert (
        restored.failure_reason
        == "worker process terminated"
    )
    assert (
        restored.outcomes
        == evaluation.outcomes
    )


def test_recovery_preserves_partial_two_regime_execution_without_duplication() -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = (
        _evaluation(
            water_regimes=(WaterRegime.RAINFED, WaterRegime.IRRIGATED),
        )
        .prepare()
        .attach_environmental_input_manifest(_manifest())
        .start_running()
        .record_outcome(_outcome(water_regime=WaterRegime.RAINFED))
    )
    repository.add(evaluation)

    AgroclimaticEvaluationRecoveryService(repository).recover_evaluation(
        RecoverEvaluation(
            evaluation.id,
            EvaluationStatus.RUNNING,
            "worker process terminated",
        )
    )

    restored = repository.get(evaluation.id)
    assert restored is not None
    assert restored.status is EvaluationStatus.FAILED
    assert restored.requested_water_regimes == (
        WaterRegime.RAINFED,
        WaterRegime.IRRIGATED,
    )
    assert [(outcome.crop_id, outcome.water_regime) for outcome in restored.outcomes] == [
        ("maize", WaterRegime.RAINFED),
    ]


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

    with pytest.raises(
        InvalidCommandError,
        match="expected status",
    ):
        (
            AgroclimaticEvaluationRecoveryService(
                repository
            ).recover_evaluation(
                RecoverEvaluation(
                    evaluation.id,
                    status,
                    "operator confirmed orphan",
                )
            )
        )


def test_explicit_recovery_requires_non_empty_reason() -> None:
    repository = InMemoryEvaluationRepository()

    evaluation = _evaluation().prepare()
    repository.add(evaluation)

    with pytest.raises(
        InvalidCommandError,
        match="non-empty",
    ):
        (
            AgroclimaticEvaluationRecoveryService(
                repository
            ).recover_evaluation(
                RecoverEvaluation(
                    evaluation.id,
                    EvaluationStatus.PREPARING,
                    "   ",
                )
            )
        )


def test_explicit_recovery_uses_expected_status() -> None:
    class RecordingRepository(
        InMemoryEvaluationRepository
    ):
        def __init__(self) -> None:
            super().__init__()
            self.expected_statuses: list[
                EvaluationStatus
            ] = []

        def save(
            self,
            evaluation: Evaluation,
            *,
            expected_status: EvaluationStatus,
        ) -> None:
            self.expected_statuses.append(
                expected_status
            )
            super().save(
                evaluation,
                expected_status=expected_status,
            )

    repository = RecordingRepository()

    evaluation = (
        _evaluation()
        .prepare()
        .attach_environmental_input_manifest(_manifest())
        .start_running()
    )
    repository.add(evaluation)

    AgroclimaticEvaluationRecoveryService(
        repository
    ).recover_evaluation(
        RecoverEvaluation(
            evaluation.id,
            EvaluationStatus.RUNNING,
            "worker process terminated",
        )
    )

    assert repository.expected_statuses == [
        EvaluationStatus.RUNNING
    ]


def test_concurrent_recovery_reports_conflict_without_overwrite() -> None:
    class ConcurrentRepository(
        InMemoryEvaluationRepository
    ):
        def save(
            self,
            evaluation: Evaluation,
            *,
            expected_status: EvaluationStatus,
        ) -> None:
            current = self.get(
                evaluation.id
            )
            assert current is not None

            super().save(
                current.fail(
                    "another operator recovered it"
                ),
                expected_status=expected_status,
            )

            super().save(
                evaluation,
                expected_status=expected_status,
            )

    repository = ConcurrentRepository()

    evaluation = (
        _evaluation()
        .prepare()
        .attach_environmental_input_manifest(_manifest())
        .start_running()
    )
    repository.add(evaluation)

    with pytest.raises(
        ResourceConflictError,
        match="changed",
    ):
        (
            AgroclimaticEvaluationRecoveryService(
                repository
            ).recover_evaluation(
                RecoverEvaluation(
                    evaluation.id,
                    EvaluationStatus.RUNNING,
                    "stale recovery command",
                )
            )
        )

    restored = repository.get(
        evaluation.id
    )

    assert restored is not None
    assert (
        restored.failure_reason
        == "another operator recovered it"
    )


def test_recovery_rejects_stale_observed_active_status_without_mutation() -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = _evaluation_in_status(EvaluationStatus.SUMMARIZING)
    repository.add(evaluation)

    with pytest.raises(
        ResourceConflictError,
        match="expected status running but actual status is summarizing",
    ):
        AgroclimaticEvaluationRecoveryService(repository).recover_evaluation(
            RecoverEvaluation(
                evaluation.id,
                EvaluationStatus.RUNNING,
                "stale operator observation",
            )
        )

    assert repository.get(evaluation.id) == evaluation


def test_recovery_rejects_terminal_state_changed_since_observation() -> None:
    repository = InMemoryEvaluationRepository()
    evaluation = _evaluation_in_status(EvaluationStatus.FAILED)
    repository.add(evaluation)

    with pytest.raises(
        ResourceConflictError,
        match="expected status preparing but actual status is failed",
    ):
        AgroclimaticEvaluationRecoveryService(repository).recover_evaluation(
            RecoverEvaluation(
                evaluation.id,
                EvaluationStatus.PREPARING,
                "stale operator observation",
            )
        )

    assert repository.get(evaluation.id) == evaluation


def _artifact(
    crop_id: str,
) -> ScientificArtifactDescriptor:
    return ScientificArtifactDescriptor(
        role=ScientificArtifactRole.CROP_SUITABILITY,
        storage_reference=(
            "evaluations/fake/crops/"
            f"{crop_id}/crop_suitability.tif"
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
        FakeEnvironmentalInformation(),
        clock=lambda: RESOLVED_AT,
    )
