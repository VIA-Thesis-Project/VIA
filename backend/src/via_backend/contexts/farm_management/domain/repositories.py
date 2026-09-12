"""Repository abstractions for Farm Management aggregates."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from .models import Parcel, Project


class ProjectRepository(Protocol):
    def add(self, project: Project) -> None: ...

    def get(self, project_id: UUID) -> Project | None: ...

    def list_all(self) -> tuple[Project, ...]: ...


class ParcelRepository(Protocol):
    def add(self, parcel: Parcel) -> None: ...

    def save(self, parcel: Parcel, *, expected_version: int) -> None: ...

    def get(self, parcel_id: UUID) -> Parcel | None: ...

    def list_for_project(self, project_id: UUID) -> tuple[Parcel, ...]: ...
