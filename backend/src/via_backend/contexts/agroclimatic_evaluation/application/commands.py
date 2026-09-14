"""Commands expressing Agroclimatic Evaluation use-case intent."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ParcelSnapshotInput:
    """Transport-neutral parcel state supplied by an authorized caller."""

    project_id: UUID
    parcel_id: UUID
    parcel_version: int
    geometry: Mapping[str, Any]
    crs: str
    captured_at: datetime


@dataclass(frozen=True, slots=True)
class RequestEvaluation:
    parcel_snapshot: ParcelSnapshotInput
    requested_crops: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ExecuteEvaluation:
    """Request synchronous execution of one already-persisted evaluation."""

    evaluation_id: UUID


@dataclass(frozen=True, slots=True)
class RecoverEvaluation:
    """Fail one operator-confirmed orphaned active evaluation."""

    evaluation_id: UUID
    reason: str
