"""Agroclimatic Evaluation domain layer."""

from .errors import (
    DomainValidationError,
    EvaluationConflictError,
    InvalidEvaluationTransitionError,
)
from .models import Evaluation, EvaluationStatus
from .outcomes import (
    CropOutcome,
    CropOutcomeStatus,
    ScientificTrace,
    SuitabilitySummary,
)
from .repositories import EvaluationRepository
from .snapshot import ParcelSnapshot, SnapshotGeometry

__all__ = [
    "CropOutcome",
    "CropOutcomeStatus",
    "DomainValidationError",
    "Evaluation",
    "EvaluationConflictError",
    "EvaluationRepository",
    "EvaluationStatus",
    "InvalidEvaluationTransitionError",
    "ParcelSnapshot",
    "ScientificTrace",
    "SnapshotGeometry",
    "SuitabilitySummary",
]
