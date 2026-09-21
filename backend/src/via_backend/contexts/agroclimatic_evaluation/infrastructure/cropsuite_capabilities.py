"""Read scientific capability metadata without importing the CropSuite engine."""

from __future__ import annotations

import re
from pathlib import Path

from ..application.capabilities import (
    CropCatalogEntry,
    ScientificallyBoundDatasetVersion,
)
from .scientific_input_integrity import (
    load_cropsuite_environmental_input_bindings,
)

_SAFE_CROP_ID = re.compile(r"^[A-Za-z0-9_-]+$")


class FilesystemCropCapabilityCatalog:
    """Adapter over the exact deployment-selected CropSuite parameter directory."""

    def __init__(self, catalog: Path) -> None:
        self._catalog = catalog

    def list_crops(self) -> tuple[CropCatalogEntry, ...]:
        if not self._catalog.is_dir():
            raise ValueError("Configured CropSuite catalog is not a directory.")

        entries: list[CropCatalogEntry] = []

        for path in sorted(self._catalog.glob("*.inf")):
            crop_id = path.stem

            if _SAFE_CROP_ID.fullmatch(crop_id) is None:
                raise ValueError(
                    f"Unsafe crop identifier in catalog: {path.name}."
                )

            values = _read_parameter_values(path)
            engine_name = values.get("name")

            if (
                engine_name is not None
                and _SAFE_CROP_ID.fullmatch(engine_name) is None
            ):
                raise ValueError(
                    f"Invalid engine crop name in {path.name}."
                )

            entries.append(
                CropCatalogEntry(
                    crop_id=crop_id,
                    display_name=engine_name,
                )
            )

        return tuple(entries)


class FilesystemScientificInputBindingCatalog:
    """Expose only public dataset identities from deployment bindings."""

    def __init__(self, bindings_path: Path) -> None:
        self._bindings_path = bindings_path

    def list_bound_dataset_versions(
        self,
    ) -> tuple[ScientificallyBoundDatasetVersion, ...]:
        bindings = load_cropsuite_environmental_input_bindings(
            self._bindings_path
        )

        identities = {
            (
                binding.dataset_id,
                binding.dataset_version_id,
            )
            for binding in bindings
        }

        return tuple(
            ScientificallyBoundDatasetVersion(
                dataset_id=dataset_id,
                dataset_version_id=dataset_version_id,
            )
            for dataset_id, dataset_version_id in sorted(
                identities,
                key=lambda item: (
                    str(item[0]),
                    str(item[1]),
                ),
            )
        )


def _read_parameter_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()

    return values
