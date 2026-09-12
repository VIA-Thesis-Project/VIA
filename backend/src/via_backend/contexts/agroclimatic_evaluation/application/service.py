"""Agroclimatic Evaluation command and query coordination."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import UUID, uuid4

from ..domain.errors import DomainValidationError, EvaluationConflictError
from ..domain.models import Evaluation, EvaluationStatus
from ..domain.repositories import EvaluationRepository
from ..domain.snapshot import ParcelSnapshot, SnapshotGeometry
from .commands import RequestEvaluation
from .queries import GetEvaluation, ListEvaluations
from .results import EvaluationResult


class ResourceNotFoundError(LookupError):
    """Raised when a requested evaluation does not exist."""


class InvalidCommandError(ValueError):
    """Raised when request data violates an evaluation invariant."""


class ResourceConflictError(RuntimeError):
    """Raised when an evaluation identity already exists."""


class AgroclimaticEvaluationService:
    """Create and query durable immutable evaluation requests."""

    def __init__(
        self,
        evaluations: EvaluationRepository,
        *,
        new_id: Callable[[], UUID] = uuid4,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._evaluations = evaluations
        self._new_id = new_id
        self._clock = clock or (lambda: datetime.now(UTC))

    def request_evaluation(self, command: RequestEvaluation) -> EvaluationResult:
        supplied = command.parcel_snapshot
        try:
            snapshot = ParcelSnapshot(
                project_id=supplied.project_id,
                parcel_id=supplied.parcel_id,
                parcel_version=supplied.parcel_version,
                geometry=SnapshotGeometry.from_geojson(supplied.geometry),
                crs=supplied.crs,
                captured_at=supplied.captured_at,
            )
            evaluation = Evaluation(
                id=self._new_id(),
                parcel_snapshot=snapshot,
                requested_crops=command.requested_crops,
                status=EvaluationStatus.QUEUED,
                created_at=self._clock(),
            )
        except DomainValidationError as error:
            raise InvalidCommandError(str(error)) from error

        try:
            self._evaluations.add(evaluation)
        except EvaluationConflictError as error:
            raise ResourceConflictError(str(error)) from error
        return EvaluationResult.from_domain(evaluation)

    def get_evaluation(self, query: GetEvaluation) -> EvaluationResult:
        evaluation = self._evaluations.get(query.evaluation_id)
        if evaluation is None:
            raise ResourceNotFoundError(
                f"Evaluation {query.evaluation_id} was not found."
            )
        return EvaluationResult.from_domain(evaluation)

    def list_evaluations(
        self, query: ListEvaluations
    ) -> tuple[EvaluationResult, ...]:
        del query
        return tuple(
            EvaluationResult.from_domain(evaluation)
            for evaluation in self._evaluations.list_all()
        )
