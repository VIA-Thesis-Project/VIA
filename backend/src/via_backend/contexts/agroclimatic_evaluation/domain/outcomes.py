"""Durable per-crop outcome values owned by Agroclimatic Evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .errors import DomainValidationError


class CropOutcomeStatus(StrEnum):
    """Completed scientific outcome for one requested crop."""

    SUCCEEDED = "succeeded"
    NO_COVERAGE = "no_coverage"
    FAILED = "failed"


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
