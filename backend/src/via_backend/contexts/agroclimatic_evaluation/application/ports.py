"""Application-owned boundary for one crop suitability evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol, runtime_checkable
from uuid import UUID

from ..domain.snapshot import ParcelSnapshot


class CropExecutionStatus(StrEnum):
    """Scientific outcomes reported independently of Evaluation lifecycle state."""

    SUCCEEDED = "succeeded"
    NO_COVERAGE = "no_coverage"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class CropSuitabilityRequest:
    """Transport-neutral input for evaluating one crop against an exact snapshot."""

    evaluation_id: UUID
    parcel_snapshot: ParcelSnapshot
    crop_id: str


@dataclass(frozen=True, slots=True)
class SuitabilityScoreSummary:
    """Current PoC parcel summary for the crop-suitability output."""

    mean: float | None
    minimum: float | None
    maximum: float | None
    valid_cells: int
    valid_area_m2: float
    coverage_fraction: float
    zero_suitability_area_m2: float


@dataclass(frozen=True, slots=True)
class ScientificExecutionFailure:
    """An engine-reported failure, distinct from no coverage and a zero score."""

    message: str


@dataclass(frozen=True, slots=True)
class ScientificExecutionTrace:
    """Trace metadata the current PoC can supply without invented versions."""

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


@dataclass(frozen=True, slots=True)
class CropSuitabilityResult:
    """One checked per-crop outcome from the scientific boundary."""

    crop_id: str
    status: CropExecutionStatus
    suitability: SuitabilityScoreSummary | None
    failure: ScientificExecutionFailure | None
    trace: ScientificExecutionTrace


class CropSuitabilityEngineError(RuntimeError):
    """Base error for failures to invoke or understand the engine boundary."""


class CropSuitabilityExecutionError(CropSuitabilityEngineError):
    """Raised when the existing engine service cannot produce a report."""


class InvalidEngineOutputError(CropSuitabilityEngineError):
    """Raised when the engine report does not satisfy the expected PoC contract."""


@runtime_checkable
class ICropSuitabilityEngine(Protocol):
    """Evaluate one crop without exposing engine process or filesystem details."""

    def evaluate(self, request: CropSuitabilityRequest) -> CropSuitabilityResult: ...
