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
                raise EvaluationConflictError(
                    f"Evaluation {evaluation.id} already exists."
                )
            self._evaluations[evaluation.id] = evaluation

    def save(
        self, evaluation: Evaluation, *, expected_status: EvaluationStatus
    ) -> None:
        with self._lock:
            current = self._evaluations.get(evaluation.id)
            if (
                current is None
                or current.status is not expected_status
                or current.parcel_snapshot != evaluation.parcel_snapshot
                or current.requested_crops != evaluation.requested_crops
                or current.created_at != evaluation.created_at
                or current.outcomes != evaluation.outcomes
            ):
                raise EvaluationConflictError(
                    f"Evaluation {evaluation.id} changed before it could be saved."
                )
            self._evaluations[evaluation.id] = evaluation

    def add_outcome(self, evaluation_id: UUID, outcome: CropOutcome) -> None:
        with self._lock:
            current = self._evaluations.get(evaluation_id)
            if current is None:
                raise EvaluationConflictError(
                    f"Evaluation {evaluation_id} does not exist."
                )
            try:
                self._evaluations[evaluation_id] = current.record_outcome(outcome)
            except InvalidEvaluationTransitionError as error:
                raise EvaluationConflictError(str(error)) from error

    def get(self, evaluation_id: UUID) -> Evaluation | None:
        with self._lock:
            return self._evaluations.get(evaluation_id)

    def list_all(self) -> tuple[Evaluation, ...]:
        with self._lock:
            return tuple(
                sorted(
                    self._evaluations.values(),
                    key=lambda item: (item.created_at, item.id),
                )
            )
