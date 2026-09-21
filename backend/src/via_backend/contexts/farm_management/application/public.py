"""Deliberately small public contract exported by Farm Management."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal, Protocol
from uuid import UUID


class AuthorizedParcelSnapshotNotFoundError(LookupError):
    """Raised when a parcel version is absent from an owner's project boundary."""


@dataclass(frozen=True, slots=True)
class AuthorizedParcelGeometry:
    """Deeply immutable geometry value published at the context boundary."""

    type: Literal["Polygon", "MultiPolygon"]
    coordinates: tuple[Any, ...]


@dataclass(frozen=True, slots=True)
class AuthorizedParcelSnapshot:
    """Minimum authoritative parcel state needed by Evaluation."""

    project_id: UUID
    parcel_id: UUID
    parcel_version: int
    geometry: AuthorizedParcelGeometry
    crs: str
    captured_at: datetime


class AuthorizedParcelSnapshotResolver(Protocol):
    def resolve_authorized_parcel_snapshot(
        self,
        *,
        owner_user_id: UUID,
        project_id: UUID,
        parcel_id: UUID,
        parcel_version: int,
    ) -> AuthorizedParcelSnapshot: ...
