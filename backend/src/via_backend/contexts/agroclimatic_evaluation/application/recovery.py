"""Explicit fail-only recovery for abandoned evaluation executions."""

from __future__ import annotations

from ..domain.errors import (
    DomainValidationError,
    EvaluationConflictError,
    InvalidEvaluationTransitionError,
)
from ..domain.repositories import EvaluationRepository
from .commands import RecoverEvaluation
from .results import EvaluationResult
from .service import InvalidCommandError, ResourceConflictError, ResourceNotFoundError


class AgroclimaticEvaluationRecoveryService:
    """Mark an operator-confirmed active orphan as failed without retrying it."""

    def __init__(self, evaluations: EvaluationRepository) -> None:
        self._evaluations = evaluations

    def recover_evaluation(self, command: RecoverEvaluation) -> EvaluationResult:
        evaluation = self._evaluations.get(command.evaluation_id)
        if evaluation is None:
            raise ResourceNotFoundError(f"Evaluation {command.evaluation_id} was not found.")

        try:
            failed = evaluation.fail(command.reason)
        except (DomainValidationError, InvalidEvaluationTransitionError) as error:
            raise InvalidCommandError(str(error)) from error

        try:
            self._evaluations.save(failed, expected_status=evaluation.status)
        except EvaluationConflictError as error:
            raise ResourceConflictError(str(error)) from error
        return EvaluationResult.from_domain(failed)
