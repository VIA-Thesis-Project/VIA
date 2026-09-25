"""Agroclimatic Evaluation infrastructure layer."""

from .cropsuite_adapter import CropSuiteAdapter
from .cropsuite_capabilities import (
    FilesystemCropCapabilityCatalog,
    FilesystemScientificInputBindingCatalog,
)
from .cropsuite_comparison_adapter import CropSuiteComparisonAdapter
from .database import AGROCLIMATIC_EVALUATION_SCHEMA, Base
from .postgresql_repositories import PostgreSQLEvaluationRepository
from .repositories import InMemoryEvaluationRepository
from .s3_compatible import create_s3_compatible_client
from .scientific_artifact_store import (
    FilesystemScientificArtifactStore,
    R2ScientificArtifactStore,
)
from .scientific_input_integrity import (
    ConfiguredEnvironmentalInputIntegrityVerifier,
    CropSuiteEnvironmentalInputBinding,
    load_configured_environmental_input_integrity_verifier,
    load_cropsuite_environmental_input_bindings,
)
from .scientific_source_store import (
    FilesystemScientificSourceStore,
    R2ScientificSourceStore,
    ScientificSourceIntegrityError,
    ScientificSourceMaterializer,
    ScientificSourceObject,
    ScientificSourceStorageError,
    ScientificSourceStore,
)

__all__ = [
    "AGROCLIMATIC_EVALUATION_SCHEMA",
    "Base",
    "CropSuiteAdapter",
    "FilesystemCropCapabilityCatalog",
    "FilesystemScientificInputBindingCatalog",
    "FilesystemScientificArtifactStore",
    "FilesystemScientificSourceStore",
    "InMemoryEvaluationRepository",
    "PostgreSQLEvaluationRepository",
    "R2ScientificArtifactStore",
    "R2ScientificSourceStore",
    "ScientificSourceIntegrityError",
    "ScientificSourceMaterializer",
    "ScientificSourceObject",
    "ScientificSourceStorageError",
    "ScientificSourceStore",
    "CropSuiteComparisonAdapter",
    "ConfiguredEnvironmentalInputIntegrityVerifier",
    "CropSuiteEnvironmentalInputBinding",
    "load_configured_environmental_input_integrity_verifier",
    "load_cropsuite_environmental_input_bindings",
    "create_s3_compatible_client",
]
