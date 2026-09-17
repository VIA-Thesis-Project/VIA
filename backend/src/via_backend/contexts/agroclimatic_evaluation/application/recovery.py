"""Explicit fail-only recovery for abandoned evaluation executions."""

from __future__ import annotations

import logging

from ..domain.errors import (
    DomainValidationError,
    EvaluationConflictError,
    InvalidEvaluationTransitionError,
)
from ..domain.models import EvaluationStatus
from ..domain.repositories import EvaluationRepository
from .commands import RecoverEvaluation
from .results import ActiveEvaluationResult, EvaluationResult
from .service import InvalidCommandError, ResourceConflictError, ResourceNotFoundError


class AgroclimaticEvaluationRecoveryService:
    """Mark an operator-confirmed active orphan as failed without retrying it."""

    _ACTIVE_STATUSES = {
        EvaluationStatus.PREPARING,
        EvaluationStatus.RUNNING,
        EvaluationStatus.SUMMARIZING,
    }

    def __init__(
        self,
        evaluations: EvaluationRepository,
        *,
        logger: logging.Logger | None = None,
    ) -> None:
        self._evaluations = evaluations
        self._logger = logger or logging.getLogger(__name__)

    def list_active_evaluations(self, *, limit: int) -> tuple[ActiveEvaluationResult, ...]:
        return tuple(
            ActiveEvaluationResult.from_domain(evaluation)
            for evaluation in self._evaluations.list_active(limit=limit)
        )

    def recover_evaluation(self, command: RecoverEvaluation) -> EvaluationResult:
        if (
            not isinstance(command.expected_status, EvaluationStatus)
            or command.expected_status not in self._ACTIVE_STATUSES
        ):
            raise InvalidCommandError(
                "Recovery expected status must be preparing, running, or summarizing."
            )
        evaluation = self._evaluations.get(command.evaluation_id)
        if evaluation is None:
            raise ResourceNotFoundError(f"Evaluation {command.evaluation_id} was not found.")

        if evaluation.status is not command.expected_status:
            self._logger.warning(
                "Evaluation recovery status conflict",
                extra={
                    "evaluation_id": str(command.evaluation_id),
                    "expected_status": command.expected_status.value,
                    "actual_status": evaluation.status.value,
                },
            )
            raise ResourceConflictError(
                f"Evaluation {command.evaluation_id} expected status "
                f"{command.expected_status.value} but actual status is "
                f"{evaluation.status.value}."
            )

        try:
            failed = evaluation.fail(command.reason)
        except (DomainValidationError, InvalidEvaluationTransitionError) as error:
            raise InvalidCommandError(str(error)) from error

        try:
            self._evaluations.save(failed, expected_status=command.expected_status)
        except EvaluationConflictError as error:
            self._logger.warning(
                "Evaluation recovery persistence conflict",
                extra={
                    "evaluation_id": str(command.evaluation_id),
                    "expected_status": command.expected_status.value,
                },
            )
            raise ResourceConflictError(str(error)) from error
        self._logger.info(
            "Evaluation recovered to failed",
            extra={
                "evaluation_id": str(command.evaluation_id),
                "expected_status": command.expected_status.value,
                "status": failed.status.value,
            },
        )
        return EvaluationResult.from_domain(failed)
