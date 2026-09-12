"""Application ports for Environmental Information spatial collaboration."""

from __future__ import annotations

from typing import Protocol

from ..domain.coverage import (
    CoverageCompatibilityFailure,
    CoverageGeometry,
    CoverageMeasurement,
)
from ..domain.models import DatasetVersion

CoverageComputation = CoverageMeasurement | CoverageCompatibilityFailure


class InvalidSpatialInputError(ValueError):
    """Raised when supplied parcel geometry is not topologically usable."""


class SpatialCoverageUnavailableError(RuntimeError):
    """Raised when the configured spatial implementation cannot execute."""


class SpatialCoveragePort(Protocol):
    """Measure an external geometry against a registered dataset extent."""

    def measure(
        self, version: DatasetVersion, geometry: CoverageGeometry
    ) -> CoverageComputation: ...
