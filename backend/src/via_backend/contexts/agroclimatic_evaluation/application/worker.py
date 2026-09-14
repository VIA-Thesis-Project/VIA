"""Polling-worker coordination around the existing evaluation executor."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

from ..domain.models import EvaluationStatus
from ..domain.repositories import EvaluationRepository
from .commands import ExecuteEvaluation
from .results import EvaluationResult
from .service import ResourceConflictError


class EvaluationExecutor(Protocol):
    def execute_evaluation(self, command: ExecuteEvaluation) -> EvaluationResult: ...


@dataclass(frozen=True, slots=True)
class WorkerRunSummary:
    discovered: int
    completed: int
    conflicted: int
    failed: int


class AgroclimaticEvaluationWorker:
    """Discover queued IDs and delegate all execution semantics to Application."""

    def __init__(
        self,
        evaluations: EvaluationRepository,
        executor: EvaluationExecutor,
        *,
        batch_size: int,
        logger: logging.Logger | None = None,
    ) -> None:
        if isinstance(batch_size, bool) or batch_size < 1:
            raise ValueError("batch_size must be a positive integer.")
        self._evaluations = evaluations
        self._executor = executor
        self.batch_size = batch_size
        self._logger = logger or logging.getLogger(__name__)

    def run_once(self) -> WorkerRunSummary:
        evaluation_ids = self._evaluations.list_queued_ids(limit=self.batch_size)
        self._logger.info("Queue batch discovered", extra={"count": len(evaluation_ids)})
        completed = conflicted = failed = 0

        for evaluation_id in evaluation_ids:
            self._logger.info(
                "Evaluation selected for execution",
                extra={"evaluation_id": str(evaluation_id)},
            )
            try:
                self._executor.execute_evaluation(ExecuteEvaluation(evaluation_id))
            except ResourceConflictError:
                conflicted += 1
                self._logger.info(
                    "Evaluation claim conflict; skipping",
                    extra={"evaluation_id": str(evaluation_id)},
                    exc_info=True,
                )
            except Exception:
                current = self._evaluations.get(evaluation_id)
                if current is None or current.status is not EvaluationStatus.FAILED:
                    raise
                failed += 1
                self._logger.exception(
                    "Evaluation execution failed",
                    extra={"evaluation_id": str(evaluation_id)},
                )
            else:
                completed += 1
                self._logger.info(
                    "Evaluation execution completed",
                    extra={"evaluation_id": str(evaluation_id)},
                )

        return WorkerRunSummary(
            discovered=len(evaluation_ids),
            completed=completed,
            conflicted=conflicted,
            failed=failed,
        )
