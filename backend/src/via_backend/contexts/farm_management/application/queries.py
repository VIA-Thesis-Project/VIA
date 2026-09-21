"""Queries supported by the Farm Management application service."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetProject:
    project_id: UUID
    owner_user_id: UUID


@dataclass(frozen=True, slots=True)
class ListProjects:
    owner_user_id: UUID


@dataclass(frozen=True, slots=True)
class GetParcel:
    project_id: UUID
    owner_user_id: UUID
    parcel_id: UUID


@dataclass(frozen=True, slots=True)
class ListParcels:
    project_id: UUID
    owner_user_id: UUID
