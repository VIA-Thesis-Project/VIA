"""Durable per-crop outcome values owned by Agroclimatic Evaluation."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .errors import DomainValidationError


class CropOutcomeStatus(StrEnum):
    """Completed scientific outcome for one requested crop."""

    SUCCEEDED = "succeeded"
    NO_COVERAGE = "no_coverage"
    FAILED = "failed"


_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class ScientificArtifactRole(StrEnum):
    """Scientific artifact role persisted by Agroclimatic Evaluation."""

    CROP_SUITABILITY = "crop_suitability"


@dataclass(frozen=True, slots=True)
class ScientificArtifactGrid:
    """Immutable spatial grid identity for a scientific raster."""

    crs: str
    width: int
    height: int
    transform: tuple[float, float, float, float, float, float]
    nodata: float | None

    def __post_init__(self) -> None:
        if not self.crs or self.crs != self.crs.strip():
            raise DomainValidationError("Artifact CRS must be non-empty and trimmed.")
        if isinstance(self.width, bool) or self.width < 1:
            raise DomainValidationError("Artifact width must be a positive integer.")
        if isinstance(self.height, bool) or self.height < 1:
            raise DomainValidationError("Artifact height must be a positive integer.")
        if len(self.transform) != 6 or not all(math.isfinite(value) for value in self.transform):
            raise DomainValidationError(
                "Artifact affine transform must contain six finite values."
            )
        if self.nodata is not None and not math.isfinite(self.nodata):
            raise DomainValidationError("Artifact nodata must be finite when supplied.")


@dataclass(frozen=True, slots=True)
class ScientificArtifact:
    """Durable scientific evidence referenced without exposing filesystem paths."""

    role: ScientificArtifactRole
    storage_reference: str
    sha256: str
    media_type: str
    size_bytes: int
    grid: ScientificArtifactGrid

    def __post_init__(self) -> None:
        if (
            not self.storage_reference
            or self.storage_reference != self.storage_reference.strip()
        ):
            raise DomainValidationError(
                "Artifact storage reference must be non-empty and trimmed."
            )
        if not _SHA256_PATTERN.fullmatch(self.sha256):
            raise DomainValidationError("Artifact SHA-256 must be 64 lowercase hex characters.")
        if not self.media_type or self.media_type != self.media_type.strip():
            raise DomainValidationError("Artifact media type must be non-empty and trimmed.")
        if isinstance(self.size_bytes, bool) or self.size_bytes < 1:
            raise DomainValidationError("Artifact size must be a positive integer.")


@dataclass(frozen=True, slots=True)
class SuitabilitySummary:
    """The reliable parcel summary currently returned by the scientific boundary."""

    mean: float | None
    minimum: float | None
    maximum: float | None
    valid_cells: int
    valid_area_m2: float
    coverage_fraction: float
    zero_suitability_area_m2: float


@dataclass(frozen=True, slots=True)
class ScientificTrace:
    """Current reproducibility trace without engine-specific filesystem details."""

    engine_identifier: str
    execution_reference: str
    started_at: datetime
    finished_at: datetime
    elapsed_seconds: float
    execution_mode: str
    parcel_sha256: str
    parameter_sha256: str | None
    configuration_sha256: str | None
    source_files_unchanged: bool

    def __post_init__(self) -> None:
        if not self.engine_identifier or not self.execution_reference:
            raise DomainValidationError("Scientific trace identifiers must be non-empty.")
        if self.started_at.tzinfo is None or self.started_at.utcoffset() is None:
            raise DomainValidationError("Scientific trace start time must be timezone-aware.")
        if self.finished_at.tzinfo is None or self.finished_at.utcoffset() is None:
            raise DomainValidationError("Scientific trace finish time must be timezone-aware.")
        if self.elapsed_seconds < 0:
            raise DomainValidationError("Scientific trace elapsed time must be non-negative.")


@dataclass(frozen=True, slots=True)
class CropOutcome:
    """One durable result associated with an Evaluation and requested crop."""

    crop_id: str
    status: CropOutcomeStatus
    suitability: SuitabilitySummary | None
    failure_message: str | None
    trace: ScientificTrace
    artifacts: tuple[ScientificArtifact, ...] = ()

    def __post_init__(self) -> None:
        if not self.crop_id or self.crop_id != self.crop_id.strip():
            raise DomainValidationError("Outcome crop identifier must be non-empty and trimmed.")
        if self.status is CropOutcomeStatus.FAILED:
            if not self.failure_message or self.suitability is not None:
                raise DomainValidationError(
                    "A failed crop outcome requires a message and no suitability summary."
                )
        elif self.failure_message is not None or self.suitability is None:
            raise DomainValidationError(
                "A completed non-failed crop outcome requires a suitability summary."
            )
        roles = [artifact.role for artifact in self.artifacts]

        if len(set(roles)) != len(roles):
            raise DomainValidationError(
                "A crop outcome cannot contain duplicate scientific artifact roles."
            )

        if self.status is CropOutcomeStatus.FAILED and self.artifacts:
            raise DomainValidationError(
                "A failed crop outcome cannot contain scientific result artifacts."
            )
