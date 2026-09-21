"""In-memory Agroclimatic Evaluation repository adapter."""

from threading import RLock
from uuid import UUID

from ..domain.errors import EvaluationConflictError, InvalidEvaluationTransitionError
from ..domain.models import Evaluation, EvaluationStatus
from ..domain.outcomes import CropOutcome


class InMemoryEvaluationRepository:
    def __init__(self) -> None:
        self._evaluations: dict[UUID, Evaluation] = {}
        self._lock = RLock()

    def add(self, evaluation: Evaluation) -> None:
        with self._lock:
            if evaluation.id in self._evaluations:
                raise EvaluationConflictError(f"Evaluation {evaluation.id} already exists.")
            self._evaluations[evaluation.id] = evaluation

    def save(self, evaluation: Evaluation, *, expected_status: EvaluationStatus) -> None:
        with self._lock:
            current = self._evaluations.get(evaluation.id)
            if (
                current is None
                or current.status is not expected_status
                or current.parcel_snapshot != evaluation.parcel_snapshot
                or current.requested_crops != evaluation.requested_crops
                or current.requested_water_regimes
                != evaluation.requested_water_regimes
                or current.created_at != evaluation.created_at
                or current.owner_user_id != evaluation.owner_user_id
                or current.environmental_input_references
                != evaluation.environmental_input_references
                or (
                    current.environmental_input_manifest is not None
                    and current.environmental_input_manifest
                    != evaluation.environmental_input_manifest
                )
                or current.outcomes != evaluation.outcomes
                or current.scenarios
                != evaluation.scenarios[: len(current.scenarios)]
            ):
                raise EvaluationConflictError(
                    f"Evaluation {evaluation.id} changed before it could be saved."
                )
            self._evaluations[evaluation.id] = evaluation

    def add_outcome(self, evaluation_id: UUID, outcome: CropOutcome) -> None:
        with self._lock:
            current = self._evaluations.get(evaluation_id)
            if current is None:
                raise EvaluationConflictError(f"Evaluation {evaluation_id} does not exist.")
            try:
                self._evaluations[evaluation_id] = current.record_outcome(outcome)
            except InvalidEvaluationTransitionError as error:
                raise EvaluationConflictError(str(error)) from error

    def get(self, evaluation_id: UUID) -> Evaluation | None:
        with self._lock:
            return self._evaluations.get(evaluation_id)

    def list_queued_ids(self, *, limit: int) -> tuple[UUID, ...]:
        _validate_limit(limit)
        with self._lock:
            queued = (
                evaluation
                for evaluation in self._evaluations.values()
                if evaluation.status is EvaluationStatus.QUEUED
            )
            return tuple(
                evaluation.id
                for evaluation in sorted(
                    queued,
                    key=lambda item: (item.created_at, item.id),
                )[:limit]
            )

    def list_active(self, *, limit: int) -> tuple[Evaluation, ...]:
        _validate_limit(limit)
        active_statuses = {
            EvaluationStatus.PREPARING,
            EvaluationStatus.RUNNING,
            EvaluationStatus.SUMMARIZING,
        }
        with self._lock:
            active = (
                evaluation
                for evaluation in self._evaluations.values()
                if evaluation.status in active_statuses
            )
            return tuple(
                sorted(
                    active,
                    key=lambda item: (item.created_at, item.id),
                )[:limit]
            )

    def list_all(self) -> tuple[Evaluation, ...]:
        with self._lock:
            return tuple(
                sorted(
                    self._evaluations.values(),
                    key=lambda item: (item.created_at, item.id),
                )
            )


def _validate_limit(limit: int) -> None:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be a positive integer.")
