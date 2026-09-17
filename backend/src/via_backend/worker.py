"""Separate PostgreSQL polling-worker process and operator recovery CLI."""

from __future__ import annotations

import argparse
import json
import logging
import signal
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from threading import Event
from types import FrameType
from uuid import UUID

from sqlalchemy import Engine

from via_backend.config import WorkerSettings
from via_backend.contexts.agroclimatic_evaluation.application import (
    ActiveEvaluationResult,
    AgroclimaticEvaluationExecutionService,
    AgroclimaticEvaluationRecoveryService,
    AgroclimaticEvaluationWorker,
    RecoverEvaluation,
)
from via_backend.contexts.agroclimatic_evaluation.domain import EvaluationStatus
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    CropSuiteAdapter,
    CropSuiteComparisonAdapter,
    FilesystemScientificArtifactStore,
    PostgreSQLEvaluationRepository,
    load_configured_environmental_input_integrity_verifier,
)
from via_backend.contexts.environmental_information.application import (
    EnvironmentalInformationService,
)
from via_backend.contexts.environmental_information.infrastructure import (
    PostgreSQLDatasetRepository,
    PostgreSQLDatasetVersionRepository,
)
from via_backend.infrastructure import create_database

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class WorkerRuntime:
    database_engine: Engine
    worker: AgroclimaticEvaluationWorker

    def close(self) -> None:
        self.database_engine.dispose()


def create_worker(settings: WorkerSettings) -> WorkerRuntime:
    """Compose the production worker and fail fast on missing scientific settings."""
    (
        engine_root,
        python_executable,
        workspace_root,
        artifacts_root,
        input_bindings_path,
    ) = (
        settings.require_scientific_execution()
    )
    input_integrity_verifier = load_configured_environmental_input_integrity_verifier(
        input_bindings_path
    )
    database_engine, sessions = create_database(settings.database_url)
    evaluations = PostgreSQLEvaluationRepository(sessions)
    environmental_information = EnvironmentalInformationService(
        PostgreSQLDatasetRepository(sessions),
        PostgreSQLDatasetVersionRepository(sessions),
    )
    artifact_store = FilesystemScientificArtifactStore(artifacts_root)
    scientific_engine = CropSuiteAdapter(
        engine_root=engine_root,
        python_executable=python_executable,
        workspace_root=workspace_root,
        source_config=settings.cropsuite_source_config,
        catalog=settings.cropsuite_catalog,
        max_workers=settings.cropsuite_max_workers,
        artifact_store=artifact_store,
        input_integrity_verifier=input_integrity_verifier,
    )
    comparison_engine = CropSuiteComparisonAdapter(
        engine_root=engine_root,
        python_executable=python_executable,
        workspace_root=workspace_root,
        artifact_store=artifact_store,
    )
    executor = AgroclimaticEvaluationExecutionService(
        evaluations=evaluations,
        engine=scientific_engine,
        comparison_engine=comparison_engine,
        environmental_information=environmental_information,
    )
    return WorkerRuntime(
        database_engine=database_engine,
        worker=AgroclimaticEvaluationWorker(
            evaluations=evaluations,
            executor=executor,
            batch_size=settings.batch_size,
            logger=LOGGER,
        ),
    )


def run_forever(
    worker: AgroclimaticEvaluationWorker,
    *,
    poll_interval_seconds: float,
    stop_event: Event | None = None,
    wait_for_stop: Callable[[float], bool] | None = None,
) -> None:
    """Poll until cooperative shutdown, waiting only after a non-full batch."""
    coordinated_stop = stop_event or Event()
    wait = wait_for_stop or coordinated_stop.wait
    LOGGER.info(
        "Worker started",
        extra={
            "batch_size": worker.batch_size,
            "poll_interval_seconds": poll_interval_seconds,
        },
    )
    try:
        while not coordinated_stop.is_set():
            summary = worker.run_once(stop_requested=coordinated_stop.is_set)
            if coordinated_stop.is_set():
                break
            if summary.discovered < worker.batch_size:
                wait(poll_interval_seconds)
    except Exception:
        LOGGER.exception("Worker stopped after systemic failure")
        raise
    LOGGER.info("Worker stopped", extra={"stop_kind": "graceful"})


def make_shutdown_handler(
    stop_event: Event,
    *,
    logger: logging.Logger = LOGGER,
) -> Callable[[int, FrameType | None], None]:
    """Return a signal handler that only requests cooperative process shutdown."""

    def request_shutdown(signum: int, _frame: FrameType | None) -> None:
        stop_event.set()
        try:
            signal_name = signal.Signals(signum).name
        except ValueError:
            signal_name = str(signum)
        logger.info("Worker shutdown requested", extra={"signal": signal_name})

    return request_shutdown


def list_active_evaluations(
    settings: WorkerSettings,
    *,
    limit: int,
) -> tuple[ActiveEvaluationResult, ...]:
    """List active evaluations without composing scientific execution dependencies."""
    database_engine, sessions = create_database(settings.database_url)
    try:
        evaluations = PostgreSQLEvaluationRepository(sessions)
        return AgroclimaticEvaluationRecoveryService(evaluations).list_active_evaluations(
            limit=limit
        )
    finally:
        database_engine.dispose()


def _print_active_evaluations(evaluations: Sequence[ActiveEvaluationResult]) -> None:
    for evaluation in evaluations:
        print(
            json.dumps(
                {
                    "evaluation_id": str(evaluation.evaluation_id),
                    "status": evaluation.status.value,
                    "created_at": evaluation.created_at.isoformat(),
                    "requested_crop_count": evaluation.requested_crop_count,
                    "completed_crop_count": evaluation.completed_crop_count,
                }
            )
        )


def recover_evaluation(
    settings: WorkerSettings,
    *,
    evaluation_id: UUID,
    expected_status: EvaluationStatus,
    reason: str,
) -> None:
    """Run explicit fail-only orphan recovery without composing CropSuiteLite."""
    database_engine, sessions = create_database(settings.database_url)
    try:
        evaluations = PostgreSQLEvaluationRepository(sessions)
        AgroclimaticEvaluationRecoveryService(evaluations, logger=LOGGER).recover_evaluation(
            RecoverEvaluation(evaluation_id, expected_status, reason)
        )
    finally:
        database_engine.dispose()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="via-worker")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("run", help="Poll PostgreSQL and execute queued evaluations.")
    active = commands.add_parser(
        "active",
        help="List active evaluations for operator inspection.",
    )
    active.add_argument("--limit", type=_positive_integer, default=50)
    recovery = commands.add_parser(
        "recover",
        help="Mark an operator-confirmed orphaned active evaluation as failed.",
    )
    recovery.add_argument("evaluation_id", type=UUID)
    recovery.add_argument(
        "--expected-status",
        required=True,
        choices=("preparing", "running", "summarizing"),
    )
    recovery.add_argument("--reason", required=True)
    return parser


def _positive_integer(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a positive integer") from error
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def main(argv: Sequence[str] | None = None) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    arguments = _parser().parse_args(argv)
    settings = WorkerSettings.from_env()

    if arguments.command == "active":
        _print_active_evaluations(
            list_active_evaluations(
                settings,
                limit=arguments.limit,
            )
        )
        return

    if arguments.command == "recover":
        recover_evaluation(
            settings,
            evaluation_id=arguments.evaluation_id,
            expected_status=EvaluationStatus(arguments.expected_status),
            reason=arguments.reason,
        )
        return

    runtime = create_worker(settings)
    stop_event = Event()
    shutdown_handler = make_shutdown_handler(stop_event)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    try:
        run_forever(
            runtime.worker,
            poll_interval_seconds=settings.poll_interval_seconds,
            stop_event=stop_event,
        )
    finally:
        runtime.close()


if __name__ == "__main__":
    main()
