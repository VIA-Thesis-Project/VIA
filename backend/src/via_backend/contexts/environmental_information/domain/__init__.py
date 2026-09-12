"""Environmental Information domain layer."""

from .coverage import (
    CoverageClassification,
    CoverageCompatibilityFailure,
    CoverageGeometry,
    CoverageMeasurement,
)
from .errors import DatasetVersionConflictError, DomainValidationError
from .models import Dataset, DatasetVersion
from .repositories import DatasetRepository, DatasetVersionRepository
from .spatial import SpatialExtent, SpatialResolution

__all__ = [
    "CoverageClassification",
    "CoverageCompatibilityFailure",
    "CoverageGeometry",
    "CoverageMeasurement",
    "Dataset",
    "DatasetRepository",
    "DatasetVersion",
    "DatasetVersionConflictError",
    "DatasetVersionRepository",
    "DomainValidationError",
    "SpatialExtent",
    "SpatialResolution",
]
