"""Application-owned boundary for one crop suitability evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol, runtime_checkable
from uuid import UUID

from ..domain.environmental_inputs import EnvironmentalInputManifest
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
    environmental_input_manifest: EnvironmentalInputManifest


@dataclass(frozen=True, slots=True)
class ScientificSourceFingerprint:
    """Opaque scientific source identity and its engine-reported SHA-256."""

    source_reference: str
    sha256: str


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
class ScientificArtifactGrid:
    """Portable grid identity needed to verify comparable scientific rasters."""

    crs: str
    width: int
    height: int
    transform: tuple[float, float, float, float, float, float]
    nodata: float | None


class ScientificArtifactRole(StrEnum):
    """Scientific artifact roles understood by VIA."""

    CROP_SUITABILITY = "crop_suitability"


@dataclass(frozen=True, slots=True)
class ScientificArtifactDescriptor:
    """Durable opaque reference to one verified scientific artifact."""

    role: ScientificArtifactRole
    storage_reference: str
    sha256: str
    media_type: str
    size_bytes: int
    grid: ScientificArtifactGrid

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
    source_fingerprints: tuple[ScientificSourceFingerprint, ...] = ()


@dataclass(frozen=True, slots=True)
class CropSuitabilityResult:
    """One checked per-crop outcome from the scientific boundary."""

    crop_id: str
    status: CropExecutionStatus
    suitability: SuitabilityScoreSummary | None
    failure: ScientificExecutionFailure | None
    trace: ScientificExecutionTrace
    artifacts: tuple[ScientificArtifactDescriptor, ...] = ()

class CommonSupportStatus(StrEnum):
    """Scientific common-support outcome across evaluated crops."""

    COMPARABLE = "comparable"
    NO_COMMON_COVERAGE = "no_common_coverage"
    NO_SUCCESSFUL_CROPS = "no_successful_crops"


@dataclass(frozen=True, slots=True)
class CropComparisonInput:
    """One durable crop suitability raster offered to scientific comparison."""

    crop_id: str
    artifact: ScientificArtifactDescriptor


@dataclass(frozen=True, slots=True)
class CropComparisonRequest:
    """Compare crop suitability only on identical valid spatial support."""

    evaluation_id: UUID
    parcel_snapshot: ParcelSnapshot
    crops: tuple[CropComparisonInput, ...]


@dataclass(frozen=True, slots=True)
class CommonSupportResult:
    """Scientific support shared by all usable crop suitability rasters."""

    status: CommonSupportStatus
    method: str | None
    area_crs: str | None
    parcel_area_m2: float
    common_valid_area_m2: float
    common_coverage_fraction: float
    eligible_crops: tuple[str, ...]
    excluded_without_coverage: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class ComparableCropResult:
    """One crop summarized on the exact common spatial support."""

    crop_id: str
    mean: float
    rank: int


@dataclass(frozen=True, slots=True)
class CropComparisonResult:
    """Checked multicrop comparison returned by the scientific boundary."""

    common_support: CommonSupportResult
    comparable_crops: tuple[ComparableCropResult, ...]

class CropComparisonEngineError(RuntimeError):
    """Base error for the scientific crop-comparison boundary."""


class CropComparisonExecutionError(CropComparisonEngineError):
    """Raised when scientific common-support comparison cannot execute."""


class InvalidComparisonOutputError(CropComparisonEngineError):
    """Raised when scientific comparison returns an invalid contract."""


@runtime_checkable
class ICropComparisonEngine(Protocol):
    """Compare durable crop outputs using the authoritative scientific engine."""

    def compare(
        self,
        request: CropComparisonRequest,
    ) -> CropComparisonResult: ...

class CropSuitabilityEngineError(RuntimeError):
    """Base error for failures to invoke or understand the engine boundary."""


class CropSuitabilityExecutionError(CropSuitabilityEngineError):
    """Raised when the existing engine service cannot produce a report."""


class InvalidEngineOutputError(CropSuitabilityEngineError):
    """Raised when the engine report does not satisfy the expected PoC contract."""


class EnvironmentalInputIntegrityError(CropSuitabilityEngineError):
    """Raised when resolved environmental provenance does not match scientific inputs."""


@runtime_checkable
class IEnvironmentalInputIntegrityVerifier(Protocol):
    """Verify resolved environmental provenance against scientific source fingerprints."""

    def verify(
        self,
        manifest: EnvironmentalInputManifest,
        source_fingerprints: tuple[ScientificSourceFingerprint, ...],
    ) -> None: ...


@runtime_checkable
class ICropSuitabilityEngine(Protocol):
    """Evaluate one crop without exposing engine process or filesystem details."""

    def evaluate(self, request: CropSuitabilityRequest) -> CropSuitabilityResult: ...
