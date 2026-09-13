"""Synchronous application orchestration for persisted evaluations."""

from __future__ import annotations

from ..domain.errors import EvaluationConflictError
from ..domain.models import Evaluation, EvaluationStatus
from ..domain.outcomes import (
    CropOutcome,
    CropOutcomeStatus,
    ScientificTrace,
    SuitabilitySummary,
)
from ..domain.repositories import EvaluationRepository
from .commands import ExecuteEvaluation
from .ports import (
    CropSuitabilityRequest,
    CropSuitabilityResult,
    ICropSuitabilityEngine,
    InvalidEngineOutputError,
)
from .results import EvaluationResult
from .service import ResourceConflictError, ResourceNotFoundError


class AgroclimaticEvaluationExecutionService:
    """Execute requested crops sequentially through the Application-owned port."""

    def __init__(
        self,
        evaluations: EvaluationRepository,
        engine: ICropSuitabilityEngine,
    ) -> None:
        self._evaluations = evaluations
        self._engine = engine

    def execute_evaluation(self, command: ExecuteEvaluation) -> EvaluationResult:
        evaluation = self._evaluations.get(command.evaluation_id)
        if evaluation is None:
            raise ResourceNotFoundError(
                f"Evaluation {command.evaluation_id} was not found."
            )
        if evaluation.status is not EvaluationStatus.QUEUED:
            raise ResourceConflictError(
                f"Evaluation {evaluation.id} cannot execute from "
                f"{evaluation.status.value}."
            )

        preparing = evaluation.prepare()
        try:
            self._evaluations.save(
                preparing,
                expected_status=EvaluationStatus.QUEUED,
            )
        except EvaluationConflictError as error:
            raise ResourceConflictError(str(error)) from error

        current = preparing
        try:
            running = current.start_running()
            self._evaluations.save(
                running,
                expected_status=EvaluationStatus.PREPARING,
            )
            current = running

            for crop_id in current.requested_crops:
                result = self._engine.evaluate(
                    CropSuitabilityRequest(
                        evaluation_id=current.id,
                        parcel_snapshot=current.parcel_snapshot,
                        crop_id=crop_id,
                    )
                )
                if result.crop_id != crop_id:
                    raise InvalidEngineOutputError(
                        "Engine result did not preserve the requested crop identity."
                    )
                outcome = _to_outcome(result)
                updated = current.record_outcome(outcome)
                self._evaluations.add_outcome(current.id, outcome)
                current = updated

            summarizing = current.start_summarizing()
            self._evaluations.save(
                summarizing,
                expected_status=EvaluationStatus.RUNNING,
            )
            current = summarizing

            succeeded = current.succeed()
            self._evaluations.save(
                succeeded,
                expected_status=EvaluationStatus.SUMMARIZING,
            )
            return EvaluationResult.from_domain(succeeded)
        except Exception as error:
            self._persist_failure(current, error)
            raise

    def _persist_failure(self, evaluation: Evaluation, error: Exception) -> None:
        failed = evaluation.fail(f"{type(error).__name__}: {error}")
        try:
            self._evaluations.save(
                failed,
                expected_status=evaluation.status,
            )
        except EvaluationConflictError as persistence_error:
            error.add_note(
                "The orchestration failure state could not be persisted: "
                f"{type(persistence_error).__name__}: {persistence_error}"
            )


def _to_outcome(result: CropSuitabilityResult) -> CropOutcome:
    suitability = result.suitability
    trace = result.trace
    return CropOutcome(
        crop_id=result.crop_id,
        status=CropOutcomeStatus(result.status.value),
        suitability=(
            SuitabilitySummary(
                mean=suitability.mean,
                minimum=suitability.minimum,
                maximum=suitability.maximum,
                valid_cells=suitability.valid_cells,
                valid_area_m2=suitability.valid_area_m2,
                coverage_fraction=suitability.coverage_fraction,
                zero_suitability_area_m2=suitability.zero_suitability_area_m2,
            )
            if suitability is not None
            else None
        ),
        failure_message=result.failure.message if result.failure is not None else None,
        trace=ScientificTrace(
            engine_identifier=trace.engine_identifier,
            execution_reference=trace.execution_reference,
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
