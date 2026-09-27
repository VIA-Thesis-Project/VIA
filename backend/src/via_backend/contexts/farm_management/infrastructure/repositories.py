"""In-memory Farm Management repository adapters."""

from __future__ import annotations

from dataclasses import replace
from threading import RLock
from uuid import UUID

from ..domain.errors import ParcelVersionConflictError
from ..domain.models import Parcel, Project


class InMemoryProjectRepository:
    """Process-local project storage for the first vertical slice."""

    def __init__(self) -> None:
        self._projects: dict[UUID, Project] = {}
        self._lock = RLock()

    def add(self, project: Project) -> None:
        with self._lock:
            if project.id in self._projects:
                raise ValueError(f"Project {project.id} already exists.")
            self._projects[project.id] = project

    def get(self, project_id: UUID) -> Project | None:
        with self._lock:
            return self._projects.get(project_id)

    def get_for_owner(self, owner_user_id: UUID, project_id: UUID) -> Project | None:
        with self._lock:
            project = self._projects.get(project_id)
            if project is None or project.owner_user_id != owner_user_id:
                return None
            return project

    def list_all(self) -> tuple[Project, ...]:
        with self._lock:
            return tuple(
                sorted(self._projects.values(), key=lambda item: (item.created_at, item.id))
            )

    def list_for_owner(self, owner_user_id: UUID) -> tuple[Project, ...]:
        with self._lock:
            return tuple(
                sorted(
                    (
                        project
                        for project in self._projects.values()
                        if project.owner_user_id == owner_user_id
                    ),
                    key=lambda item: (item.created_at, item.id),
                )
            )


class InMemoryParcelRepository:
    """Process-local parcel storage that retains every geometry version."""

    def __init__(self) -> None:
        self._parcels: dict[UUID, Parcel] = {}
        self._lock = RLock()

    def add(self, parcel: Parcel) -> None:
        with self._lock:
            if parcel.id in self._parcels:
                raise ValueError(f"Parcel {parcel.id} already exists.")
            self._parcels[parcel.id] = parcel

    def save(self, parcel: Parcel, *, expected_version: int) -> None:
        with self._lock:
            current = self._parcels.get(parcel.id)
            if current is None or current.deleted_at is not None:
                raise ParcelVersionConflictError(f"Parcel {parcel.id} is unavailable.")
            if (
                current.current_version.number != expected_version
                or parcel.project_id != current.project_id
                or parcel.name != current.name
                or parcel.description != current.description
                or parcel.created_at != current.created_at
                or parcel.versions[:-1] != current.versions
                or parcel.current_version.number != expected_version + 1
            ):
                raise ParcelVersionConflictError(
                    f"Parcel {parcel.id} changed before its revision could be saved."
                )
            self._parcels[parcel.id] = parcel

    def update_metadata(
        self, parcel: Parcel, *, expected_name: str, expected_description: str | None
    ) -> None:
        with self._lock:
            current = self._parcels.get(parcel.id)
            if (
                current is None
                or current.deleted_at is not None
                or current.project_id != parcel.project_id
                or current.name != expected_name
                or current.description != expected_description
            ):
                raise ParcelVersionConflictError(
                    f"Parcel {parcel.id} changed during metadata update."
                )
            self._parcels[parcel.id] = replace(
                current, name=parcel.name, description=parcel.description
            )

    def soft_delete(self, parcel: Parcel) -> None:
        with self._lock:
            current = self._parcels.get(parcel.id)
            if current is None or current.deleted_at is not None:
                raise ParcelVersionConflictError(f"Parcel {parcel.id} is unavailable.")
            self._parcels[parcel.id] = replace(current, deleted_at=parcel.deleted_at)

    def get(self, parcel_id: UUID) -> Parcel | None:
        with self._lock:
            parcel = self._parcels.get(parcel_id)
            return parcel if parcel is not None and parcel.deleted_at is None else None

    def get_for_project(self, project_id: UUID, parcel_id: UUID) -> Parcel | None:
        with self._lock:
            parcel = self._parcels.get(parcel_id)
            if parcel is None or parcel.project_id != project_id or parcel.deleted_at is not None:
                return None
            return parcel

    def list_for_project(self, project_id: UUID) -> tuple[Parcel, ...]:
        with self._lock:
            return tuple(
                sorted(
                    (
                        parcel
                        for parcel in self._parcels.values()
                        if parcel.project_id == project_id and parcel.deleted_at is None
                    ),
                    key=lambda item: (item.created_at, item.id),
                )
            )
