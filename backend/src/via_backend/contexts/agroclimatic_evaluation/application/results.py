"""Transport-neutral Agroclimatic Evaluation results."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from ..domain.models import Evaluation, EvaluationStatus


@dataclass(frozen=True, slots=True)
class ParcelSnapshotResult:
    project_id: UUID
    parcel_id: UUID
    parcel_version: int
    geometry: Mapping[str, Any]
    crs: str
    captured_at: datetime


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    id: UUID
    parcel_snapshot: ParcelSnapshotResult
    requested_crops: tuple[str, ...]
    status: EvaluationStatus
    created_at: datetime

    @classmethod
    def from_domain(cls, evaluation: Evaluation) -> EvaluationResult:
        snapshot = evaluation.parcel_snapshot
        return cls(
            id=evaluation.id,
            parcel_snapshot=ParcelSnapshotResult(
                project_id=snapshot.project_id,
                parcel_id=snapshot.parcel_id,
                parcel_version=snapshot.parcel_version,
                geometry=snapshot.geometry.to_geojson(),
                crs=snapshot.crs,
                captured_at=snapshot.captured_at,
            ),
            requested_crops=evaluation.requested_crops,
            status=evaluation.status,
            created_at=evaluation.created_at,
        )
