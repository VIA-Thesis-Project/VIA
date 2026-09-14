"""Agroclimatic Evaluation command and query coordination."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import UUID, uuid4

from ..domain.errors import DomainValidationError, EvaluationConflictError
from ..domain.models import Evaluation, EvaluationStatus
from ..domain.outcomes import CropOutcome
from ..domain.repositories import EvaluationRepository
from ..domain.snapshot import ParcelSnapshot, SnapshotGeometry
from .commands import RequestEvaluation
from .public import (
    FinalizedCropOutcome,
    FinalizedCropOutcomeStatus,
    FinalizedEvaluationResult,
    FinalizedScientificTrace,
    FinalizedSuitabilitySummary,
    GetFinalizedEvaluationResult,
)
from .queries import (
    GetEvaluation,
    GetEvaluationEvidence,
    GetEvaluationResult,
    ListEvaluations,
)
from .read_models import (
    EvaluationEvidenceResult,
    EvaluationReadResult,
    EvaluationStatusResult,
)
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

    def get_evaluation(self, query: GetEvaluation) -> EvaluationStatusResult:
        return EvaluationStatusResult.from_domain(self._get_evaluation(query.evaluation_id))

    def get_evaluation_result(self, query: GetEvaluationResult) -> EvaluationReadResult:
        return EvaluationReadResult.from_domain(self._get_evaluation(query.evaluation_id))

    def get_evaluation_evidence(self, query: GetEvaluationEvidence) -> EvaluationEvidenceResult:
        return EvaluationEvidenceResult.from_domain(self._get_evaluation(query.evaluation_id))

    def get_finalized_evaluation_result(
        self, query: GetFinalizedEvaluationResult
    ) -> FinalizedEvaluationResult:
        evaluation = self._get_evaluation(query.evaluation_id)
        if evaluation.status is not EvaluationStatus.SUCCEEDED:
            raise ResourceConflictError(
                f"Evaluation {evaluation.id} does not have a finalized result."
            )
        snapshot = evaluation.parcel_snapshot
        return FinalizedEvaluationResult(
            evaluation_id=evaluation.id,
            requested_crops=evaluation.requested_crops,
            project_id=snapshot.project_id,
            parcel_id=snapshot.parcel_id,
            parcel_version=snapshot.parcel_version,
            parcel_captured_at=snapshot.captured_at,
            created_at=evaluation.created_at,
            outcomes=tuple(_to_finalized_crop_outcome(outcome) for outcome in evaluation.outcomes),
        )

    def list_evaluations(
        self, query: ListEvaluations
    ) -> tuple[EvaluationResult, ...]:
        del query
        return tuple(
            EvaluationResult.from_domain(evaluation)
            for evaluation in self._evaluations.list_all()
        )

    def _get_evaluation(self, evaluation_id: UUID) -> Evaluation:
        evaluation = self._evaluations.get(evaluation_id)
        if evaluation is None:
            raise ResourceNotFoundError(f"Evaluation {evaluation_id} was not found.")
        return evaluation


def _to_finalized_crop_outcome(outcome: CropOutcome) -> FinalizedCropOutcome:
    summary = outcome.suitability
    trace = outcome.trace
    return FinalizedCropOutcome(
        crop_id=outcome.crop_id,
        status=FinalizedCropOutcomeStatus(outcome.status.value),
        suitability=(
            FinalizedSuitabilitySummary(
                mean=summary.mean,
                minimum=summary.minimum,
                maximum=summary.maximum,
                valid_cells=summary.valid_cells,
                valid_area_m2=summary.valid_area_m2,
                coverage_fraction=summary.coverage_fraction,
                zero_suitability_area_m2=summary.zero_suitability_area_m2,
            )
            if summary is not None
            else None
        ),
        trace=FinalizedScientificTrace(
            engine_identifier=trace.engine_identifier,
            started_at=trace.started_at,
            finished_at=trace.finished_at,
            elapsed_seconds=trace.elapsed_seconds,
            execution_mode=trace.execution_mode,
            parcel_sha256=trace.parcel_sha256,
            parameter_sha256=trace.parameter_sha256,
            configuration_sha256=trace.configuration_sha256,
            source_files_unchanged=trace.source_files_unchanged,
        ),
    )
