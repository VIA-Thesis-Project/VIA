"""Farm Management domain model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .errors import DomainValidationError
from .geometry import ParcelGeometry


@dataclass(frozen=True, slots=True)
class Project:
    """An agricultural project that groups parcels."""

    id: UUID
    name: str
    created_at: datetime
    owner_user_id: UUID | None = None

    def __post_init__(self) -> None:
        _validate_name(self.name, "Project")


@dataclass(frozen=True, slots=True)
class ParcelVersion:
    """An immutable version of a parcel geometry."""

    number: int
    geometry: ParcelGeometry
    created_at: datetime

    def __post_init__(self) -> None:
        if self.number < 1:
            raise DomainValidationError("Parcel version numbers start at one.")


@dataclass(frozen=True, slots=True)
class Parcel:
    """A named parcel whose geometry changes only by appending versions."""

    id: UUID
    project_id: UUID
    name: str
    versions: tuple[ParcelVersion, ...]
    created_at: datetime

    def __post_init__(self) -> None:
        _validate_name(self.name, "Parcel")
        if not self.versions:
            raise DomainValidationError("A parcel must have an initial geometry version.")
        expected_numbers = tuple(range(1, len(self.versions) + 1))
        if tuple(version.number for version in self.versions) != expected_numbers:
            raise DomainValidationError("Parcel versions must be contiguous and ordered.")

    @property
    def current_version(self) -> ParcelVersion:
        return self.versions[-1]

    def revise_geometry(self, geometry: ParcelGeometry, created_at: datetime) -> Parcel:
        version = ParcelVersion(
            number=self.current_version.number + 1,
            geometry=geometry,
            created_at=created_at,
        )
        return Parcel(
            id=self.id,
            project_id=self.project_id,
            name=self.name,
            versions=(*self.versions, version),
            created_at=self.created_at,
        )


def _validate_name(name: str, subject: str) -> None:
    if not name or name != name.strip():
        raise DomainValidationError(f"{subject} name must be non-empty and trimmed.")
    if len(name) > 120:
        raise DomainValidationError(f"{subject} name must be at most 120 characters.")
