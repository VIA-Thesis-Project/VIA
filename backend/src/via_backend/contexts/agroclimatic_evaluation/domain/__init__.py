"""Agroclimatic Evaluation domain layer."""

from .comparison import (
    CommonSupport,
    CommonSupportStatus,
    ComparableCrop,
)
from .environmental_inputs import (
    EnvironmentalInputManifest,
    EnvironmentalInputReference,
    EnvironmentalInputSnapshot,
)
from .errors import (
    DomainValidationError,
    EvaluationConflictError,
    InvalidEvaluationTransitionError,
)
from .models import Evaluation, EvaluationStatus
from .outcomes import (
    CropOutcome,
    CropOutcomeStatus,
    ScientificArtifact,
    ScientificArtifactGrid,
    ScientificArtifactRole,
    ScientificTrace,
    SuitabilitySummary,
)
from .repositories import EvaluationRepository
from .snapshot import ParcelSnapshot, SnapshotGeometry

__all__ = [
    "CropOutcome",
    "CropOutcomeStatus",
    "DomainValidationError",
    "EnvironmentalInputManifest",
    "EnvironmentalInputReference",
    "EnvironmentalInputSnapshot",
    "Evaluation",
    "EvaluationConflictError",
    "EvaluationRepository",
    "EvaluationStatus",
    "InvalidEvaluationTransitionError",
    "ParcelSnapshot",
    "ScientificTrace",
    "ScientificArtifact",
    "ScientificArtifactGrid",
    "ScientificArtifactRole",
    "SnapshotGeometry",
    "SuitabilitySummary",
    "CommonSupport",
    "CommonSupportStatus",
    "ComparableCrop"
]
