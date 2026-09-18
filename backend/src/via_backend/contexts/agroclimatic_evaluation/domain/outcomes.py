"""Durable per-crop outcome values owned by Agroclimatic Evaluation."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .errors import DomainValidationError
from .water_regime import WaterRegime


class CropOutcomeStatus(StrEnum):
    """Completed scientific outcome for one requested crop."""

    SUCCEEDED = "succeeded"
    NO_COVERAGE = "no_coverage"
    FAILED = "failed"


_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class ScientificArtifactRole(StrEnum):
    """Scientific artifact role persisted by Agroclimatic Evaluation."""

    CROP_SUITABILITY = "crop_suitability"
    CROP_LIMITING_FACTOR = "crop_limiting_factor"


class LimitationEvidenceAvailability(StrEnum):
    """Availability of deterministic limiting-factor evidence."""

    AVAILABLE = "available"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class LimitingFactorEvidence:
    """Aggregated SAME-RUN evidence for one raw limiting-factor code."""

    factor_code: str
    label: str
    raw_code: int
    affected_cells: int
    affected_area_m2: float
    affected_fraction: float
    dominant: bool
    source_storage_reference: str | None
    source_sha256: str

    def __post_init__(self) -> None:
        if not self.factor_code or self.factor_code != self.factor_code.strip():
            raise DomainValidationError("Limiting factor code must be non-empty and trimmed.")
        if not self.label or self.label != self.label.strip():
            raise DomainValidationError("Limiting factor label must be non-empty and trimmed.")
        if isinstance(self.raw_code, bool) or not isinstance(self.raw_code, int):
            raise DomainValidationError("Limiting factor raw code must be an integer.")
        if (
            isinstance(self.affected_cells, bool)
            or not isinstance(self.affected_cells, int)
            or self.affected_cells < 0
        ):
            raise DomainValidationError(
                "Affected cell count must be a non-negative integer."
            )
        if not math.isfinite(self.affected_area_m2) or self.affected_area_m2 < 0:
            raise DomainValidationError("Affected area must be finite and non-negative.")
        if (
            not math.isfinite(self.affected_fraction)
            or self.affected_fraction < 0
            or self.affected_fraction > 1
        ):
            raise DomainValidationError("Affected fraction must be finite and within [0, 1].")
        if self.source_storage_reference is not None and (
            not self.source_storage_reference
            or self.source_storage_reference != self.source_storage_reference.strip()
        ):
            raise DomainValidationError(
                "Limiting-factor storage reference must be trimmed when supplied."
            )
        if _SHA256_PATTERN.fullmatch(self.source_sha256) is None:
            raise DomainValidationError(
                "Limiting-factor source SHA-256 must be 64 lowercase hex characters."
            )


@dataclass(frozen=True, slots=True)
class CropLimitationEvidence:
    """Deterministic explanatory evidence associated with one crop execution."""

    availability: LimitationEvidenceAvailability
    reason: str | None
    warnings: tuple[str, ...] = ()
    factors: tuple[LimitingFactorEvidence, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "warnings", tuple(self.warnings))
        object.__setattr__(self, "factors", tuple(self.factors))
        if self.reason is not None and (
            not self.reason or self.reason != self.reason.strip()
        ):
            raise DomainValidationError(
                "Limitation evidence reason must be trimmed when supplied."
            )
        if any(not warning or warning != warning.strip() for warning in self.warnings):
            raise DomainValidationError(
                "Limitation evidence warnings must be non-empty and trimmed."
            )
        if (
            self.availability is LimitationEvidenceAvailability.AVAILABLE
            and self.reason is not None
        ):
            raise DomainValidationError(
                "Available limitation evidence cannot have a failure reason."
            )
        if (
            self.availability is LimitationEvidenceAvailability.AVAILABLE
            and not self.factors
        ):
            raise DomainValidationError(
                "Available limitation evidence must contain at least one factor."
            )
        if (
            self.availability is not LimitationEvidenceAvailability.AVAILABLE
            and self.reason is None
        ):
            raise DomainValidationError(
                "Partial or unavailable limitation evidence requires a deterministic reason."
            )
        if self.availability is LimitationEvidenceAvailability.UNAVAILABLE and self.factors:
            raise DomainValidationError("Unavailable limitation evidence cannot contain factors.")
        raw_codes = [factor.raw_code for factor in self.factors]
        factor_codes = [factor.factor_code for factor in self.factors]
        if len(raw_codes) != len(set(raw_codes)) or len(factor_codes) != len(set(factor_codes)):
            raise DomainValidationError(
                "Limitation evidence cannot contain duplicate factor identities."
            )


DEFAULT_UNAVAILABLE_LIMITATION_EVIDENCE = CropLimitationEvidence(
    availability=LimitationEvidenceAvailability.UNAVAILABLE,
    reason="limitation_evidence_not_persisted",
)


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
class ScientificSourceFingerprint:
    """Opaque engine-reported scientific source identity and SHA-256."""

    source_reference: str
    sha256: str

    def __post_init__(self) -> None:
        if not self.source_reference or self.source_reference != self.source_reference.strip():
            raise DomainValidationError(
                "Scientific source reference must be non-empty and trimmed."
            )
        if _SHA256_PATTERN.fullmatch(self.sha256) is None:
            raise DomainValidationError(
                "Scientific source fingerprint must be lowercase hexadecimal SHA-256."
            )


@dataclass(frozen=True, slots=True)
class ScientificTrace:
    """Current reproducibility trace with opaque engine source evidence."""

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

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_fingerprints", tuple(self.source_fingerprints))
        if not self.engine_identifier or not self.execution_reference:
            raise DomainValidationError("Scientific trace identifiers must be non-empty.")
        if self.started_at.tzinfo is None or self.started_at.utcoffset() is None:
            raise DomainValidationError("Scientific trace start time must be timezone-aware.")
        if self.finished_at.tzinfo is None or self.finished_at.utcoffset() is None:
            raise DomainValidationError("Scientific trace finish time must be timezone-aware.")
        if self.elapsed_seconds < 0:
            raise DomainValidationError("Scientific trace elapsed time must be non-negative.")
        source_references = [
            fingerprint.source_reference for fingerprint in self.source_fingerprints
        ]
        if len(source_references) != len(set(source_references)):
            raise DomainValidationError(
                "Scientific trace cannot contain duplicate source references."
            )


@dataclass(frozen=True, slots=True)
class CropOutcome:
    """One durable result associated with an Evaluation and requested crop."""

    crop_id: str
    status: CropOutcomeStatus
    suitability: SuitabilitySummary | None
    failure_message: str | None
    trace: ScientificTrace
    water_regime: WaterRegime = WaterRegime.RAINFED
    artifacts: tuple[ScientificArtifact, ...] = ()
    limitation_evidence: CropLimitationEvidence = DEFAULT_UNAVAILABLE_LIMITATION_EVIDENCE

    def __post_init__(self) -> None:
        try:
            water_regime = WaterRegime(self.water_regime)
        except ValueError as error:
            raise DomainValidationError("Outcome water regime is not supported.") from error
        object.__setattr__(self, "water_regime", water_regime)
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
        if self.status is CropOutcomeStatus.FAILED and self.limitation_evidence.factors:
            raise DomainValidationError(
                "A failed crop outcome cannot contain limiting-factor evidence."
            )
