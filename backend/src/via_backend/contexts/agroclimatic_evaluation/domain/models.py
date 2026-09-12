"""Agroclimatic Evaluation aggregate."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from .errors import DomainValidationError
from .snapshot import ParcelSnapshot


class EvaluationStatus(StrEnum):
    """Architecture-approved lifecycle vocabulary.

    This increment creates only queued evaluations; execution transitions remain
    deliberately deferred until worker semantics are designed.
    """

    QUEUED = "queued"
    PREPARING = "preparing"
    RUNNING = "running"
    SUMMARIZING = "summarizing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class Evaluation:
    """An immutable multicrop evaluation request and its parcel snapshot."""

    id: UUID
    parcel_snapshot: ParcelSnapshot
    requested_crops: tuple[str, ...]
    status: EvaluationStatus
    created_at: datetime

    def __post_init__(self) -> None:
        if isinstance(self.requested_crops, (str, bytes)):
            raise DomainValidationError("Requested crops must be a collection.")
        crops = tuple(self.requested_crops)
        if not crops:
            raise DomainValidationError("At least one crop must be requested.")
        for crop_id in crops:
            if not crop_id or crop_id != crop_id.strip():
                raise DomainValidationError(
                    "Crop identifiers must be non-empty and trimmed."
                )
            if len(crop_id) > 120:
                raise DomainValidationError(
                    "Crop identifiers must be at most 120 characters."
                )
        if len(set(crops)) != len(crops):
            raise DomainValidationError("Requested crop identifiers must be unique.")
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise DomainValidationError("Evaluation creation time must be timezone-aware.")
        object.__setattr__(self, "requested_crops", crops)
