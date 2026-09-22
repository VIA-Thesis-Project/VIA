"""Farm Management command and query coordination."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import UUID, uuid4

from ..domain.errors import DomainValidationError, ParcelVersionConflictError
from ..domain.geometry import ParcelGeometry
from ..domain.models import Parcel, ParcelVersion, Project
from ..domain.repositories import ParcelRepository, ProjectRepository
from .commands import CreateParcel, CreateProject, ReviseParcelGeometry
from .ports import ParcelAreaOfInterestValidator
from .public import (
    AuthorizedParcelGeometry,
    AuthorizedParcelSnapshot,
    AuthorizedParcelSnapshotNotFoundError,
)
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
        area_of_interest: ParcelAreaOfInterestValidator,
        new_id: Callable[[], UUID] = uuid4,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._projects = projects
        self._parcels = parcels
        self._area_of_interest = area_of_interest
        self._new_id = new_id
        self._clock = clock or (lambda: datetime.now(UTC))

    def create_project(self, command: CreateProject) -> ProjectResult:
        try:
            project = Project(
                id=self._new_id(),
                name=command.name,
                created_at=self._clock(),
                owner_user_id=command.owner_user_id,
            )
        except DomainValidationError as error:
            raise InvalidCommandError(str(error)) from error
        self._projects.add(project)
        return ProjectResult.from_domain(project)

    def list_projects(self, query: ListProjects) -> tuple[ProjectResult, ...]:
        return tuple(
            ProjectResult.from_domain(project)
            for project in self._projects.list_for_owner(query.owner_user_id)
        )

    def get_project(self, query: GetProject) -> ProjectResult:
        return ProjectResult.from_domain(
            self._require_project(query.project_id, query.owner_user_id)
        )

    def create_parcel(self, command: CreateParcel) -> ParcelResult:
        self._require_project(command.project_id, command.owner_user_id)
        created_at = self._clock()
        try:
            geometry = ParcelGeometry.from_geojson(command.geometry)
            self._area_of_interest.validate(geometry)
            parcel = Parcel(
                id=self._new_id(),
                project_id=command.project_id,
                name=command.name,
                versions=(
                    ParcelVersion(
                        number=1,
                        geometry=geometry,
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
        self._require_project(query.project_id, query.owner_user_id)
        return tuple(
            ParcelResult.from_domain(parcel)
            for parcel in self._parcels.list_for_project(query.project_id)
        )

    def get_parcel(self, query: GetParcel) -> ParcelResult:
        self._require_project(query.project_id, query.owner_user_id)
        return ParcelResult.from_domain(
            self._require_parcel(query.project_id, query.parcel_id)
        )

    def revise_parcel_geometry(self, command: ReviseParcelGeometry) -> ParcelResult:
        self._require_project(command.project_id, command.owner_user_id)
        parcel = self._require_parcel(command.project_id, command.parcel_id)
        try:
            geometry = ParcelGeometry.from_geojson(command.geometry)
            self._area_of_interest.validate(geometry)
            revised = parcel.revise_geometry(
                geometry, self._clock()
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

    def resolve_authorized_parcel_snapshot(
        self,
        *,
        owner_user_id: UUID,
        project_id: UUID,
        parcel_id: UUID,
        parcel_version: int,
    ) -> AuthorizedParcelSnapshot:
        """Resolve one exact immutable parcel version inside an owned project."""
        if isinstance(parcel_version, bool) or parcel_version < 1:
            raise AuthorizedParcelSnapshotNotFoundError(
                "The requested parcel version was not found."
            )
        if self._projects.get_for_owner(owner_user_id, project_id) is None:
            raise AuthorizedParcelSnapshotNotFoundError(
                "The requested parcel version was not found."
            )
        parcel = self._parcels.get_for_project(project_id, parcel_id)
        if parcel is None:
            raise AuthorizedParcelSnapshotNotFoundError(
                "The requested parcel version was not found."
            )
        version = next(
            (item for item in parcel.versions if item.number == parcel_version),
            None,
        )
        if version is None:
            raise AuthorizedParcelSnapshotNotFoundError(
                "The requested parcel version was not found."
            )
        return AuthorizedParcelSnapshot(
            project_id=project_id,
            parcel_id=parcel_id,
            parcel_version=version.number,
            geometry=AuthorizedParcelGeometry(
                type=version.geometry.type,
                coordinates=version.geometry.coordinates,
            ),
            crs="EPSG:4326",
            captured_at=version.created_at,
        )

    def _require_project(self, project_id: UUID, owner_user_id: UUID) -> Project:
        project = self._projects.get_for_owner(owner_user_id, project_id)
        if project is None:
            raise ResourceNotFoundError(f"Project {project_id} was not found.")
        return project

    def _require_parcel(self, project_id: UUID, parcel_id: UUID) -> Parcel:
        parcel = self._parcels.get_for_project(project_id, parcel_id)
        if parcel is None:
            raise ResourceNotFoundError(
                f"Parcel {parcel_id} was not found in project {project_id}."
            )
        return parcel
