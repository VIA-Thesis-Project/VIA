"""Farm Management command and query coordination."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timezone
from uuid import UUID, uuid4

from ..domain.errors import DomainValidationError, ParcelVersionConflictError
from ..domain.geometry import ParcelGeometry
from ..domain.models import Parcel, ParcelVersion, Project
from ..domain.repositories import ParcelRepository, ProjectRepository
from .commands import CreateParcel, CreateProject, ReviseParcelGeometry
from .queries import GetParcel, GetProject, ListParcels, ListProjects
from .results import ParcelResult, ProjectResult


class ResourceNotFoundError(LookupError):
    """Raised when a requested Farm Management resource does not exist."""


class InvalidCommandError(ValueError):
    """Raised when command data violates a Farm Management invariant."""


class ResourceConflictError(RuntimeError):
    """Raised when a resource changed during an application operation."""


class FarmManagementService:
    """Executes the minimum project and parcel management use cases."""

    def __init__(
        self,
        projects: ProjectRepository,
        parcels: ParcelRepository,
        *,
        new_id: Callable[[], UUID] = uuid4,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._projects = projects
        self._parcels = parcels
        self._new_id = new_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def create_project(self, command: CreateProject) -> ProjectResult:
        try:
            project = Project(
                id=self._new_id(),
                name=command.name,
                created_at=self._clock(),
            )
        except DomainValidationError as error:
            raise InvalidCommandError(str(error)) from error
        self._projects.add(project)
        return ProjectResult.from_domain(project)

    def list_projects(self, query: ListProjects) -> tuple[ProjectResult, ...]:
        del query
        return tuple(ProjectResult.from_domain(project) for project in self._projects.list_all())

    def get_project(self, query: GetProject) -> ProjectResult:
        return ProjectResult.from_domain(self._require_project(query.project_id))

    def create_parcel(self, command: CreateParcel) -> ParcelResult:
        self._require_project(command.project_id)
        created_at = self._clock()
        try:
            parcel = Parcel(
                id=self._new_id(),
                project_id=command.project_id,
                name=command.name,
                versions=(
                    ParcelVersion(
                        number=1,
                        geometry=ParcelGeometry.from_geojson(command.geometry),
                        created_at=created_at,
                    ),
                ),
                created_at=created_at,
            )
        except DomainValidationError as error:
            raise InvalidCommandError(str(error)) from error
        self._parcels.add(parcel)
        return ParcelResult.from_domain(parcel)

    def list_parcels(self, query: ListParcels) -> tuple[ParcelResult, ...]:
        self._require_project(query.project_id)
        return tuple(
            ParcelResult.from_domain(parcel)
            for parcel in self._parcels.list_for_project(query.project_id)
        )

    def get_parcel(self, query: GetParcel) -> ParcelResult:
        self._require_project(query.project_id)
        return ParcelResult.from_domain(
            self._require_parcel(query.project_id, query.parcel_id)
        )

    def revise_parcel_geometry(self, command: ReviseParcelGeometry) -> ParcelResult:
        self._require_project(command.project_id)
        parcel = self._require_parcel(command.project_id, command.parcel_id)
        try:
            revised = parcel.revise_geometry(
                ParcelGeometry.from_geojson(command.geometry), self._clock()
            )
        except DomainValidationError as error:
            raise InvalidCommandError(str(error)) from error
        try:
            self._parcels.save(
                revised, expected_version=parcel.current_version.number
            )
        except ParcelVersionConflictError as error:
            raise ResourceConflictError(str(error)) from error
        return ParcelResult.from_domain(revised)

    def _require_project(self, project_id: UUID) -> Project:
        project = self._projects.get(project_id)
        if project is None:
            raise ResourceNotFoundError(f"Project {project_id} was not found.")
        return project

    def _require_parcel(self, project_id: UUID, parcel_id: UUID) -> Parcel:
        parcel = self._parcels.get(parcel_id)
        if parcel is None or parcel.project_id != project_id:
            raise ResourceNotFoundError(
                f"Parcel {parcel_id} was not found in project {project_id}."
            )
        return parcel
