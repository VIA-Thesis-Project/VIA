"""Environmental Information domain layer."""

from .errors import DatasetVersionConflictError, DomainValidationError
from .models import Dataset, DatasetVersion
from .repositories import DatasetRepository, DatasetVersionRepository
from .spatial import SpatialExtent, SpatialResolution

__all__ = [
    "Dataset",
    "DatasetRepository",
    "DatasetVersion",
    "DatasetVersionConflictError",
    "DatasetVersionRepository",
    "DomainValidationError",
    "SpatialExtent",
    "SpatialResolution",
]
