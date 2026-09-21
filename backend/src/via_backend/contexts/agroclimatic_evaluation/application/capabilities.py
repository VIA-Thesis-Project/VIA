"""Frontend-facing discovery of configured scientific evaluation capabilities."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, runtime_checkable
from uuid import UUID

from ..domain.water_regime import WaterRegime


class CapabilityStatus(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"


@dataclass(frozen=True, slots=True)
class CropCatalogEntry:
    crop_id: str
    display_name: str | None


@dataclass(frozen=True, slots=True)
class ScientificallyBoundDatasetVersion:
    dataset_id: UUID
    dataset_version_id: UUID


@runtime_checkable
class ICropCapabilityCatalog(Protocol):
    def list_crops(self) -> tuple[CropCatalogEntry, ...]: ...


@runtime_checkable
class IScientificInputBindingCatalog(Protocol):
    def list_bound_dataset_versions(
        self,
    ) -> tuple[ScientificallyBoundDatasetVersion, ...]: ...


class EvaluationCapabilitiesUnavailableError(RuntimeError):
    """Raised when configured scientific capabilities cannot be read."""


@dataclass(frozen=True, slots=True)
class CropEvaluationCapability:
    crop_id: str
    display_name: str | None
    water_regimes: tuple[WaterRegime, ...]


@dataclass(frozen=True, slots=True)
class EnvironmentalInputCapability:
    minimum_count: int
    maximum_input_key_length: int
    input_keys: tuple[str, ...]
    input_key_discovery: str
    requires_registered_dataset_version: bool
    requires_scientific_binding: bool
    scientifically_bound_dataset_versions: tuple[
        ScientificallyBoundDatasetVersion, ...
    ]


@dataclass(frozen=True, slots=True)
class EvaluationCapabilities:
    status: CapabilityStatus
    crops: tuple[CropEvaluationCapability, ...]
    environmental_inputs: EnvironmentalInputCapability
    limitations: tuple[str, ...]


class EvaluationCapabilitiesService:
    """Publish only capabilities backed by current runtime configuration."""

    def __init__(
        self,
        crop_catalog: ICropCapabilityCatalog | None,
        scientific_input_bindings: IScientificInputBindingCatalog | None,
    ) -> None:
        self._crop_catalog = crop_catalog
        self._scientific_input_bindings = scientific_input_bindings

    def get_capabilities(self) -> EvaluationCapabilities:
        if self._crop_catalog is None:
            raise EvaluationCapabilitiesUnavailableError(
                "Scientific crop capability discovery is not configured."
            )
        if self._scientific_input_bindings is None:
            raise EvaluationCapabilitiesUnavailableError(
                "Scientific environmental input binding discovery is not configured."
            )

        try:
            entries = self._crop_catalog.list_crops()
        except (OSError, ValueError) as error:
            raise EvaluationCapabilitiesUnavailableError(
                "Scientific crop capability discovery is unavailable."
            ) from error

        if not entries:
            raise EvaluationCapabilitiesUnavailableError(
                "The configured scientific crop catalog is empty."
            )

        try:
            bound_versions = self._scientific_input_bindings.list_bound_dataset_versions()
        except (OSError, ValueError) as error:
            raise EvaluationCapabilitiesUnavailableError(
                "Scientific environmental input binding discovery is unavailable."
            ) from error

        if not bound_versions:
            raise EvaluationCapabilitiesUnavailableError(
                "The configured scientific environmental input binding catalog is empty."
            )

        regimes = (WaterRegime.RAINFED, WaterRegime.IRRIGATED)
        crops = tuple(
            CropEvaluationCapability(
                crop_id=entry.crop_id,
                display_name=entry.display_name,
                water_regimes=regimes,
            )
            for entry in entries
        )

        limitation = (
            "Environmental input_key values are caller-defined unique logical "
            "identifiers and do not select scientific bindings. Dataset versions "
            "listed as scientifically bound are configured for this deployment, "
            "but execution may still fail later if runtime integrity checks fail."
        )

        return EvaluationCapabilities(
            status=CapabilityStatus.PARTIAL,
            crops=crops,
            environmental_inputs=EnvironmentalInputCapability(
                minimum_count=1,
                maximum_input_key_length=120,
                input_keys=(),
                input_key_discovery="arbitrary_unique",
                requires_registered_dataset_version=True,
                requires_scientific_binding=True,
                scientifically_bound_dataset_versions=bound_versions,
            ),
            limitations=(limitation,),
        )
