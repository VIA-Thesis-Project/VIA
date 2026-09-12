"""Environmental Information application layer."""

from .commands import CreateDataset, CreateDatasetVersion
from .ports import (
    InvalidSpatialInputError,
    SpatialCoveragePort,
    SpatialCoverageUnavailableError,
)
from .queries import (
    CheckDatasetVersionCoverage,
    GetDataset,
    GetDatasetVersion,
    ListDatasets,
    ListDatasetVersions,
)
from .results import (
    DatasetResult,
    DatasetVersionCoverageResult,
    DatasetVersionResult,
    SpatialExtentResult,
    SpatialResolutionResult,
)
from .service import (
    CoverageUnavailableError,
    EnvironmentalInformationService,
    InvalidCommandError,
    ResourceConflictError,
    ResourceNotFoundError,
)

__all__ = [
    "CheckDatasetVersionCoverage",
    "CoverageUnavailableError",
    "CreateDataset",
    "CreateDatasetVersion",
    "DatasetResult",
    "DatasetVersionCoverageResult",
    "DatasetVersionResult",
    "EnvironmentalInformationService",
    "GetDataset",
    "GetDatasetVersion",
    "InvalidCommandError",
    "InvalidSpatialInputError",
    "ListDatasetVersions",
    "ListDatasets",
    "ResourceConflictError",
    "ResourceNotFoundError",
    "SpatialCoveragePort",
    "SpatialCoverageUnavailableError",
    "SpatialExtentResult",
    "SpatialResolutionResult",
]
