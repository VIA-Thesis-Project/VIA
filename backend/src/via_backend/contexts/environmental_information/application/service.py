"""Environmental Information command and query coordination."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import UUID, uuid4

from ..domain.coverage import (
    CoverageClassification,
    CoverageCompatibilityFailure,
    CoverageGeometry,
)
from ..domain.errors import DatasetVersionConflictError, DomainValidationError
from ..domain.models import Dataset, DatasetVersion
from ..domain.repositories import DatasetRepository, DatasetVersionRepository
from ..domain.spatial import SpatialExtent, SpatialResolution
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
)

_EXTENT_WARNING = (
    "Coverage is based on the registered rectangular extent only; it does not "
    "establish pixel-level scientific data availability."
)


class ResourceNotFoundError(LookupError):
    """Raised when requested environmental metadata does not exist."""


class InvalidCommandError(ValueError):
    """Raised when command data violates an environmental invariant."""


class ResourceConflictError(RuntimeError):
    """Raised when immutable environmental metadata already exists."""


class CoverageUnavailableError(RuntimeError):
    """Raised when no spatial coverage implementation is configured."""


class EnvironmentalInformationService:
    """Execute dataset catalog and immutable-version use cases."""

    def __init__(
        self,
        datasets: DatasetRepository,
        versions: DatasetVersionRepository,
        *,
        coverage: SpatialCoveragePort | None = None,
        new_id: Callable[[], UUID] = uuid4,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._datasets = datasets
        self._versions = versions
        self._coverage = coverage
        self._new_id = new_id
        self._clock = clock or (lambda: datetime.now(UTC))

    def create_dataset(self, command: CreateDataset) -> DatasetResult:
        try:
            dataset = Dataset(
                id=self._new_id(),
                name=command.name,
                source=command.source,
                variable=command.variable,
                unit=command.unit,
                created_at=self._clock(),
            )
        except DomainValidationError as error:
            raise InvalidCommandError(str(error)) from error
        self._datasets.add(dataset)
        return DatasetResult.from_domain(dataset)

    def list_datasets(self, query: ListDatasets) -> tuple[DatasetResult, ...]:
        del query
        return tuple(
            DatasetResult.from_domain(dataset) for dataset in self._datasets.list_all()
        )

    def get_dataset(self, query: GetDataset) -> DatasetResult:
        return DatasetResult.from_domain(self._require_dataset(query.dataset_id))

    def create_dataset_version(
        self, command: CreateDatasetVersion
    ) -> DatasetVersionResult:
        self._require_dataset(command.dataset_id)
        try:
            version = DatasetVersion(
                id=self._new_id(),
                dataset_id=command.dataset_id,
                version_identifier=command.version_identifier,
                crs=command.crs,
                resolution=SpatialResolution(
                    command.resolution_x,
                    command.resolution_y,
                    command.resolution_unit,
                ),
                extent=SpatialExtent(
                    command.extent_west,
                    command.extent_south,
                    command.extent_east,
                    command.extent_north,
                ),
                valid_from=command.valid_from,
                valid_to=command.valid_to,
                scenario=command.scenario,
                checksum=command.checksum,
                storage_reference=command.storage_reference,
                registered_at=self._clock(),
            )
        except DomainValidationError as error:
            raise InvalidCommandError(str(error)) from error
        try:
            self._versions.add(version)
        except DatasetVersionConflictError as error:
            raise ResourceConflictError(str(error)) from error
        return DatasetVersionResult.from_domain(version)

    def list_dataset_versions(
        self, query: ListDatasetVersions
    ) -> tuple[DatasetVersionResult, ...]:
        self._require_dataset(query.dataset_id)
        return tuple(
            DatasetVersionResult.from_domain(version)
            for version in self._versions.list_for_dataset(query.dataset_id)
        )

    def get_dataset_version(self, query: GetDatasetVersion) -> DatasetVersionResult:
        self._require_dataset(query.dataset_id)
        return DatasetVersionResult.from_domain(
            self._require_version(query.dataset_id, query.version_id)
        )

    def check_dataset_version_coverage(
        self, query: CheckDatasetVersionCoverage
    ) -> DatasetVersionCoverageResult:
        """Check extent coverage without mutating registered metadata."""
        self._require_dataset(query.dataset_id)
        version = self._require_version(query.dataset_id, query.version_id)
        try:
            geometry = CoverageGeometry.from_geojson(
                query.geometry, crs=query.geometry_crs
            )
        except DomainValidationError as error:
            raise InvalidCommandError(str(error)) from error
        if self._coverage is None:
            raise CoverageUnavailableError(
                "Coverage checks require the PostgreSQL/PostGIS configuration."
            )
        try:
            computation = self._coverage.measure(version, geometry)
        except InvalidSpatialInputError as error:
            raise InvalidCommandError(str(error)) from error
        except SpatialCoverageUnavailableError as error:
            raise CoverageUnavailableError(str(error)) from error

        warnings = tuple(dict.fromkeys((*computation.warnings, _EXTENT_WARNING)))
        if isinstance(computation, CoverageCompatibilityFailure):
            return DatasetVersionCoverageResult(
                dataset_id=version.dataset_id,
                dataset_version_id=version.id,
                compatible=False,
                coverage=CoverageClassification.NOT_ASSESSED,
                parcel_area_m2=None,
                covered_area_m2=None,
                coverage_percentage=None,
                dataset_crs=version.crs,
                parcel_crs=geometry.crs,
                comparison_crs=None,
                area_method=None,
                transformations=(),
                warnings=warnings,
                reasons=computation.reasons,
            )

        return DatasetVersionCoverageResult(
            dataset_id=version.dataset_id,
            dataset_version_id=version.id,
            compatible=True,
            coverage=computation.classification,
            parcel_area_m2=computation.parcel_area_m2,
            covered_area_m2=(
                computation.parcel_area_m2
                if computation.fully_covered
                else computation.covered_area_m2
            ),
            coverage_percentage=computation.coverage_percentage,
            dataset_crs=version.crs,
            parcel_crs=geometry.crs,
            comparison_crs=computation.comparison_crs,
            area_method=computation.area_method,
            transformations=computation.transformations,
            warnings=warnings,
            reasons=(),
        )

    def _require_dataset(self, dataset_id: UUID) -> Dataset:
        dataset = self._datasets.get(dataset_id)
        if dataset is None:
            raise ResourceNotFoundError(f"Dataset {dataset_id} was not found.")
        return dataset

    def _require_version(
        self, dataset_id: UUID, version_id: UUID
    ) -> DatasetVersion:
        version = self._versions.get(version_id)
        if version is None or version.dataset_id != dataset_id:
            raise ResourceNotFoundError(
                f"Dataset version {version_id} was not found in dataset {dataset_id}."
            )
        return version
