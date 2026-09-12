"""In-memory Agroclimatic Evaluation repository adapter."""

from threading import RLock
from uuid import UUID

from ..domain.errors import EvaluationConflictError
from ..domain.models import Evaluation


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
