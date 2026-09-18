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
    CropLimitationEvidence,
    CropOutcome,
    CropOutcomeStatus,
    LimitationEvidenceAvailability,
    LimitingFactorEvidence,
    ScientificArtifact,
    ScientificArtifactGrid,
    ScientificArtifactRole,
    ScientificSourceFingerprint,
    ScientificTrace,
    SuitabilitySummary,
)
from .repositories import EvaluationRepository
from .snapshot import ParcelSnapshot, SnapshotGeometry
from .water_regime import WaterRegime

__all__ = [
    "CropLimitationEvidence",
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
    "LimitationEvidenceAvailability",
    "LimitingFactorEvidence",
    "ParcelSnapshot",
    "ScientificTrace",
    "ScientificArtifact",
    "ScientificArtifactGrid",
    "ScientificArtifactRole",
    "ScientificSourceFingerprint",
    "SnapshotGeometry",
    "SuitabilitySummary",
    "CommonSupport",
    "CommonSupportStatus",
    "ComparableCrop",
    "WaterRegime",
]
