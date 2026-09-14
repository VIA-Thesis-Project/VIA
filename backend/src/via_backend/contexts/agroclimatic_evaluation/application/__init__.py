"""Agroclimatic Evaluation application layer."""

from .commands import (
    ExecuteEvaluation,
    ParcelSnapshotInput,
    RecoverEvaluation,
    RequestEvaluation,
)
from .execution import AgroclimaticEvaluationExecutionService
from .ports import (
    CropExecutionStatus,
    CropSuitabilityEngineError,
    CropSuitabilityExecutionError,
    CropSuitabilityRequest,
    CropSuitabilityResult,
    ICropSuitabilityEngine,
    InvalidEngineOutputError,
    ScientificExecutionFailure,
    ScientificExecutionTrace,
    SuitabilityScoreSummary,
)
from .queries import GetEvaluation, ListEvaluations
from .recovery import AgroclimaticEvaluationRecoveryService
from .results import CropOutcomeResult, EvaluationResult, ParcelSnapshotResult
from .service import (
    AgroclimaticEvaluationService,
    InvalidCommandError,
    ResourceConflictError,
    ResourceNotFoundError,
)
from .worker import AgroclimaticEvaluationWorker, WorkerRunSummary

__all__ = [
    "AgroclimaticEvaluationExecutionService",
    "AgroclimaticEvaluationRecoveryService",
    "AgroclimaticEvaluationService",
    "AgroclimaticEvaluationWorker",
    "CropExecutionStatus",
    "CropOutcomeResult",
    "CropSuitabilityEngineError",
    "CropSuitabilityExecutionError",
    "CropSuitabilityRequest",
    "CropSuitabilityResult",
    "EvaluationResult",
    "ExecuteEvaluation",
    "GetEvaluation",
    "ICropSuitabilityEngine",
    "InvalidCommandError",
    "InvalidEngineOutputError",
    "ListEvaluations",
    "ParcelSnapshotInput",
    "ParcelSnapshotResult",
    "RecoverEvaluation",
    "RequestEvaluation",
    "ResourceConflictError",
    "ResourceNotFoundError",
    "ScientificExecutionFailure",
    "ScientificExecutionTrace",
    "SuitabilityScoreSummary",
    "WorkerRunSummary",
]
