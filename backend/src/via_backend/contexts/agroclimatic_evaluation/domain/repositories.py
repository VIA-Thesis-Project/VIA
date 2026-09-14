"""Repository abstraction for the Evaluation aggregate."""

from typing import Protocol
from uuid import UUID

from .models import Evaluation, EvaluationStatus
from .outcomes import CropOutcome


class EvaluationRepository(Protocol):
    def add(self, evaluation: Evaluation) -> None: ...

    def save(self, evaluation: Evaluation, *, expected_status: EvaluationStatus) -> None: ...

    def add_outcome(self, evaluation_id: UUID, outcome: CropOutcome) -> None: ...

    def get(self, evaluation_id: UUID) -> Evaluation | None: ...

    def list_queued_ids(self, *, limit: int) -> tuple[UUID, ...]: ...

    def list_all(self) -> tuple[Evaluation, ...]: ...
