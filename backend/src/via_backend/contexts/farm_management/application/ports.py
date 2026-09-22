"""Application ports owned by Farm Management."""

from __future__ import annotations

from typing import Protocol

from ..domain.geometry import ParcelGeometry


class ParcelAreaOfInterestValidator(Protocol):
    """Validate parcel geometry against the configured authoritative AOI."""

    def validate(self, geometry: ParcelGeometry) -> None: ...
