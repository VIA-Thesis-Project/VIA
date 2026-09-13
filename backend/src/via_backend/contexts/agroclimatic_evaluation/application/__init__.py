"""Agroclimatic Evaluation application layer."""

from .commands import ExecuteEvaluation, ParcelSnapshotInput, RequestEvaluation
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
from .results import CropOutcomeResult, EvaluationResult, ParcelSnapshotResult
from .service import (
    AgroclimaticEvaluationService,
    InvalidCommandError,
    ResourceConflictError,
    ResourceNotFoundError,
)

__all__ = [
    "AgroclimaticEvaluationExecutionService",
    "AgroclimaticEvaluationService",
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
    "RequestEvaluation",
    "ResourceConflictError",
    "ResourceNotFoundError",
    "ScientificExecutionFailure",
    "ScientificExecutionTrace",
    "SuitabilityScoreSummary",
]
