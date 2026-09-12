"""Commands expressing Farm Management use-case intent."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateProject:
    name: str


@dataclass(frozen=True, slots=True)
class CreateParcel:
    project_id: UUID
    name: str
    geometry: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class ReviseParcelGeometry:
    project_id: UUID
    parcel_id: UUID
    geometry: Mapping[str, Any]

