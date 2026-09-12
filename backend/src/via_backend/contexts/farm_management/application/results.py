"""Transport-neutral results returned by Farm Management use cases."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from ..domain.models import Parcel, Project


@dataclass(frozen=True, slots=True)
class ProjectResult:
    id: UUID
    name: str
    created_at: datetime

    @classmethod
    def from_domain(cls, project: Project) -> ProjectResult:
        return cls(id=project.id, name=project.name, created_at=project.created_at)


@dataclass(frozen=True, slots=True)
class ParcelVersionResult:
    number: int
    geometry: dict[str, Any]
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ParcelResult:
    id: UUID
    project_id: UUID
    name: str
    versions: tuple[ParcelVersionResult, ...]
    created_at: datetime

    @property
    def current_version(self) -> int:
        return self.versions[-1].number

    @classmethod
    def from_domain(cls, parcel: Parcel) -> ParcelResult:
        return cls(
            id=parcel.id,
            project_id=parcel.project_id,
            name=parcel.name,
            versions=tuple(
                ParcelVersionResult(
                    number=version.number,
                    geometry=version.geometry.to_geojson(),
                    created_at=version.created_at,
                )
                for version in parcel.versions
            ),
            created_at=parcel.created_at,
        )

