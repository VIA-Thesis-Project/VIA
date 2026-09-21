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
from .scientific_artifact_store import FilesystemScientificArtifactStore
from .scientific_input_integrity import (
    ConfiguredEnvironmentalInputIntegrityVerifier,
    CropSuiteEnvironmentalInputBinding,
    load_configured_environmental_input_integrity_verifier,
    load_cropsuite_environmental_input_bindings,
)

__all__ = [
    "AGROCLIMATIC_EVALUATION_SCHEMA",
    "Base",
    "CropSuiteAdapter",
    "FilesystemCropCapabilityCatalog",
    "FilesystemScientificInputBindingCatalog",
    "FilesystemScientificArtifactStore",
    "InMemoryEvaluationRepository",
    "PostgreSQLEvaluationRepository",
    "CropSuiteComparisonAdapter",
    "ConfiguredEnvironmentalInputIntegrityVerifier",
    "CropSuiteEnvironmentalInputBinding",
    "load_configured_environmental_input_integrity_verifier",
    "load_cropsuite_environmental_input_bindings",
]
