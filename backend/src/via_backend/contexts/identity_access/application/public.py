"""Deliberately small public contract exported by Identity Access."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from uuid import UUID

from ..domain.models import UserRole


@dataclass(frozen=True, slots=True)
class AuthenticatedPrincipal:
    user_id: UUID
    role: UserRole


PrincipalResolver = Callable[..., AuthenticatedPrincipal]
