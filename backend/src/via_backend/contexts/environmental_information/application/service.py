"""Environmental Information command and query coordination."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timezone
from uuid import UUID, uuid4

from ..domain.errors import DatasetVersionConflictError, DomainValidationError
from ..domain.models import Dataset, DatasetVersion
from ..domain.repositories import DatasetRepository, DatasetVersionRepository
from ..domain.spatial import SpatialExtent, SpatialResolution
from .commands import CreateDataset, CreateDatasetVersion
from .queries import (
    GetDataset,
    GetDatasetVersion,
    ListDatasets,
    ListDatasetVersions,
)
from .results import DatasetResult, DatasetVersionResult


class ResourceNotFoundError(LookupError):
    """Raised when requested environmental metadata does not exist."""


class InvalidCommandError(ValueError):
    """Raised when command data violates an environmental invariant."""


class ResourceConflictError(RuntimeError):
    """Raised when immutable environmental metadata already exists."""


class EnvironmentalInformationService:
    """Execute dataset catalog and immutable-version use cases."""

    def __init__(
        self,
        datasets: DatasetRepository,
        versions: DatasetVersionRepository,
        *,
        new_id: Callable[[], UUID] = uuid4,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._datasets = datasets
        self._versions = versions
        self._new_id = new_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))

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
        version = self._versions.get(query.version_id)
        if version is None or version.dataset_id != query.dataset_id:
            raise ResourceNotFoundError(
                f"Dataset version {query.version_id} was not found in dataset "
                f"{query.dataset_id}."
            )
        return DatasetVersionResult.from_domain(version)

    def _require_dataset(self, dataset_id: UUID) -> Dataset:
        dataset = self._datasets.get(dataset_id)
        if dataset is None:
            raise ResourceNotFoundError(f"Dataset {dataset_id} was not found.")
        return dataset
