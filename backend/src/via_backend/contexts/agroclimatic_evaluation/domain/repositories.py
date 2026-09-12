"""Repository abstraction for the Evaluation aggregate."""

from typing import Protocol
from uuid import UUID

from .models import Evaluation


class EvaluationRepository(Protocol):
    def add(self, evaluation: Evaluation) -> None: ...

    def get(self, evaluation_id: UUID) -> Evaluation | None: ...

    def list_all(self) -> tuple[Evaluation, ...]: ...
