"""Separate PostgreSQL polling-worker process and operator recovery CLI."""

from __future__ import annotations

import argparse
import logging
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import Engine

from via_backend.config import WorkerSettings
from via_backend.contexts.agroclimatic_evaluation.application import (
    AgroclimaticEvaluationExecutionService,
    AgroclimaticEvaluationRecoveryService,
    AgroclimaticEvaluationWorker,
    RecoverEvaluation,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    CropSuiteAdapter,
    CropSuiteComparisonAdapter,
    FilesystemScientificArtifactStore,
    PostgreSQLEvaluationRepository,
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
    engine_root, python_executable, workspace_root, artifacts_root = (
        settings.require_scientific_execution()
    )
    database_engine, sessions = create_database(settings.database_url)
    evaluations = PostgreSQLEvaluationRepository(sessions)
    artifact_store = FilesystemScientificArtifactStore(artifacts_root)
    scientific_engine = CropSuiteAdapter(
        engine_root=engine_root,
        python_executable=python_executable,
        workspace_root=workspace_root,
        source_config=settings.cropsuite_source_config,
        catalog=settings.cropsuite_catalog,
        max_workers=settings.cropsuite_max_workers,
        artifact_store=artifact_store,
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
    sleeper: Callable[[float], None] = time.sleep,
) -> None:
    """Poll continuously, sleeping only after a non-full batch."""
    LOGGER.info(
        "Worker started",
        extra={
            "batch_size": worker.batch_size,
            "poll_interval_seconds": poll_interval_seconds,
        },
    )
    while True:
        summary = worker.run_once()
        if summary.discovered < worker.batch_size:
            sleeper(poll_interval_seconds)


def recover_evaluation(
    settings: WorkerSettings,
    *,
    evaluation_id: UUID,
    reason: str,
) -> None:
    """Run explicit fail-only orphan recovery without composing CropSuiteLite."""
    database_engine, sessions = create_database(settings.database_url)
    try:
        evaluations = PostgreSQLEvaluationRepository(sessions)
        result = AgroclimaticEvaluationRecoveryService(evaluations).recover_evaluation(
            RecoverEvaluation(evaluation_id, reason)
        )
        LOGGER.info(
            "Evaluation recovered to failed",
            extra={
                "evaluation_id": str(result.id),
                "status": result.status.value,
            },
        )
    finally:
        database_engine.dispose()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="via-worker")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("run", help="Poll PostgreSQL and execute queued evaluations.")
    recovery = commands.add_parser(
        "recover",
        help="Mark an operator-confirmed orphaned active evaluation as failed.",
    )
    recovery.add_argument("evaluation_id", type=UUID)
    recovery.add_argument("--reason", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    arguments = _parser().parse_args(argv)
    settings = WorkerSettings.from_env()

    if arguments.command == "recover":
        recover_evaluation(
            settings,
            evaluation_id=arguments.evaluation_id,
            reason=arguments.reason,
        )
        return

    runtime = create_worker(settings)
    try:
        run_forever(
            runtime.worker,
            poll_interval_seconds=settings.poll_interval_seconds,
        )
    except KeyboardInterrupt:
        LOGGER.info("Worker stopping; active scientific execution may require explicit recovery")
    finally:
        runtime.close()


if __name__ == "__main__":
    main()
