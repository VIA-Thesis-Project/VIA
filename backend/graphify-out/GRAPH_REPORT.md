# Graph Report - backend  (2026-09-16)

## Corpus Check
- 153 files · ~48,491 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1796 nodes · 5429 edges · 90 communities (59 shown, 17 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 760 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5449d51d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AgroclimaticEvaluationExecutionService
- EnvironmentalInputManifest
- InMemoryEvaluationRepository
- FilesystemScientificArtifactStore
- execution.py
- WorkerSettings
- test_decision_support.py
- DomainValidationError
- DomainValidationError
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- test_agroclimatic_evaluation_postgresql.py
- EnvironmentalInformationService
- workflow.py
- decision_support/domain/models.py
- test_cropsuite_adapter.py
- DomainValidationError
- PolicyReference
- FarmManagementService
- test_decision_support_postgresql.py
- Evaluation
- ViabilityPolicySnapshot
- test_environmental_information_postgresql.py
- environmental_information/infrastructure/postgresql_repositories.py
- test_agroclimatic_evaluation_api.py
- farm_management/infrastructure/postgresql_repositories.py
- cropsuite_adapter.py
- main.py
- agroclimatic_evaluation/application/__init__.py
- CoverageMeasurement
- ResourceConflictError
- EnvironmentalInputReference
- DatasetVersion
- Parcel
- test_agroclimatic_evaluation_domain.py
- test_architecture.py
- create_router
- agroclimatic_evaluation/interfaces/http.py
- SpatialExtent
- test_farm_management_postgresql.py
- Dataset
- CropSuitabilityRequest
- agroclimatic_evaluation/application/ports.py
- Project
- AgroclimaticEvaluationService
- farm_management/interfaces/http.py
- test_agroclimatic_evaluation_queries.py
- cropsuite_comparison_adapter.py
- create_router
- CropComparisonRequest
- create_router
- InMemoryParcelRepository
- environmental_information/interfaces/http.py
- ScientificArtifactStore
- IDefaultViabilityPolicyProvider
- test_environmental_information_domain.py
- env.py
- ScientificSourceFingerprint
- test_farm_management_domain.py
- SpatialCoveragePort
- test_health.py
- __main__.py
- test_crop_comparison_contracts.py
- agroclimatic_evaluation/__init__.py
- decision_support/__init__.py
- decision_support/interfaces/__init__.py
- environmental_information/__init__.py
- farm_management/__init__.py
- identity_access/application/__init__.py
- identity_access/domain/__init__.py
- identity_access/infrastructure/__init__.py
- identity_access/__init__.py
- identity_access/interfaces/__init__.py
- contexts/__init__.py
- http/__init__.py
- via_backend/interfaces/__init__.py
- via-backend

## God Nodes (most connected - your core abstractions)
1. `Evaluation` - 84 edges
2. `DomainValidationError` - 56 edges
3. `EnvironmentalInformationService` - 49 edges
4. `DatasetVersion` - 45 edges
5. `PostgreSQLEvaluationRepository` - 43 edges
6. `AgroclimaticEvaluationService` - 42 edges
7. `EvaluationStatus` - 40 edges
8. `PolicyReference` - 39 edges
9. `EnvironmentalInputManifest` - 38 edges
10. `ViabilityPolicySnapshot` - 38 edges

## Surprising Connections (you probably didn't know these)
- `test_environmental_input_reference_accepts_exact_version_identity()` --calls--> `EnvironmentalInputReference`  [INFERRED]
  tests/test_agroclimatic_environmental_inputs.py → src/via_backend/contexts/agroclimatic_evaluation/domain/environmental_inputs.py
- `test_extent_must_be_ordered()` --calls--> `SpatialExtent`  [INFERRED]
  tests/test_environmental_information_domain.py → src/via_backend/contexts/environmental_information/domain/spatial.py
- `_test_app()` --uses--> `Settings`  [INFERRED]
  tests/test_agroclimatic_evaluation_api.py → src/via_backend/config.py
- `test_environmental_postgresql_selection_requires_database_url()` --uses--> `Settings`  [INFERRED]
  tests/test_config.py → src/via_backend/config.py
- `test_evaluation_postgresql_selection_requires_database_url()` --uses--> `Settings`  [INFERRED]
  tests/test_config.py → src/via_backend/config.py

## Import Cycles
- None detected.

## Communities (90 total, 17 thin omitted)

### Community 0 - "AgroclimaticEvaluationExecutionService"
Cohesion: 0.08
Nodes (58): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, datetime, Execute requested crops and summarize them through Application-owned ports., EvaluationExecutor, Protocol, GetPublishedDatasetVersion (+50 more)

### Community 1 - "EnvironmentalInputManifest"
Cohesion: 0.07
Nodes (63): EnvironmentalInputIntegrityError, Raised when resolved environmental provenance does not match scientific inputs., EnvironmentalInputManifest, Immutable set of exact environmental inputs resolved for an evaluation., ConfiguredEnvironmentalInputIntegrityVerifier, CropSuiteEnvironmentalInputBinding, load_configured_environmental_input_integrity_verifier(), load_cropsuite_environmental_input_bindings() (+55 more)

### Community 2 - "InMemoryEvaluationRepository"
Cohesion: 0.07
Nodes (53): ArgumentParser, Logger, Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Mark an operator-confirmed active orphan as failed without retrying it., AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application. (+45 more)

### Community 3 - "FilesystemScientificArtifactStore"
Cohesion: 0.08
Nodes (52): PurePosixPath, CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., Agroclimatic Evaluation infrastructure layer., _file_identity(), FilesystemScientificArtifactStore, _is_within(), PublishedScientificArtifact (+44 more)

### Community 4 - "execution.py"
Cohesion: 0.08
Nodes (46): _comparison_request(), Synchronous application orchestration for persisted evaluations., _to_outcome(), CropComparisonInput, One durable crop suitability raster offered to scientific comparison., Portable grid identity needed to verify comparable scientific rasters., ScientificArtifactGrid, Explicit fail-only recovery for abandoned evaluation executions. (+38 more)

### Community 5 - "WorkerSettings"
Cohesion: 0.06
Nodes (48): _environment_float(), _environment_integer(), _optional_path(), Path, Environment-backed configuration for the VIA application host., Settings needed by the current backend composition root., Settings for the PostgreSQL polling worker process., Settings (+40 more)

### Community 6 - "test_decision_support.py"
Cohesion: 0.11
Nodes (45): FinalizedCommonSupport, FinalizedCommonSupportStatus, FinalizedComparableCrop, FinalizedEvaluationResult, GetFinalizedEvaluationResult, Stable contracts deliberately published to other bounded contexts., ComparableCropEvidence, A provider-produced crop mean and rank over common valid support. (+37 more)

### Community 7 - "DomainValidationError"
Cohesion: 0.09
Nodes (39): InvalidSpatialInputError, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, CoverageCompatibilityFailure (+31 more)

### Community 8 - "DomainValidationError"
Cohesion: 0.08
Nodes (38): EnvironmentalInputSnapshot, _is_finite_number(), datetime, Immutable environmental input snapshots owned by Agroclimatic Evaluation., Historical environmental input metadata captured for one evaluation input., _validate_aware_datetime(), _validate_crs(), _validate_positive_number() (+30 more)

### Community 9 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.11
Nodes (39): EvaluationConflictError, RuntimeError, Raised when an evaluation identity already exists., Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records., CropOutcomeRecord (+31 more)

### Community 10 - "test_agroclimatic_evaluation_postgresql.py"
Cohesion: 0.15
Nodes (45): ScientificSourceFingerprintRecord, PostgreSQLEvaluationRepository, SessionFactory, Durable adapter for immutable Evaluation aggregates., clean_evaluations(), _common_support(), _comparable_crops(), database() (+37 more)

### Community 11 - "EnvironmentalInformationService"
Cohesion: 0.11
Nodes (32): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., GetDataset, GetDatasetVersion, ListDatasets, ListDatasetVersions (+24 more)

### Community 12 - "workflow.py"
Cohesion: 0.07
Nodes (35): PolicyEvaluationT, PolicyEvaluationT_co, FinalizedEvaluationResultReader, Protocol, Public local interface for a future Decision Support consumer., Decision Support application layer., IDecisionPolicy, Evaluate comparable evidence without changing its scientific values. (+27 more)

### Community 13 - "decision_support/domain/models.py"
Cohesion: 0.09
Nodes (30): Application ports for deterministic Decision Support policies., Decision Support evidence translation and policy coordination., _translate_common_support(), _translate_evidence(), DomainValidationError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant. (+22 more)

### Community 14 - "test_cropsuite_adapter.py"
Cohesion: 0.17
Nodes (38): CropExecutionStatus, Scientific outcomes reported independently of Evaluation lifecycle state., CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability., _adapter(), _environmental_input_manifest(), _geometry(), _integrity_verifier() (+30 more)

### Community 15 - "DomainValidationError"
Cohesion: 0.11
Nodes (28): DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+20 more)

### Community 16 - "PolicyReference"
Cohesion: 0.12
Nodes (30): DefaultViabilityPolicyConflictError, InvalidViabilityPolicyRevisionError, RuntimeError, ValueError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist., Raised when a requested viability-policy revision is not a new version., Raised when the default policy changed before an expected update. (+22 more)

### Community 17 - "FarmManagementService"
Cohesion: 0.13
Nodes (21): CreateParcel, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels, ListProjects (+13 more)

### Community 18 - "test_decision_support_postgresql.py"
Cohesion: 0.17
Nodes (30): Decision Support infrastructure adapters., PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+22 more)

### Community 19 - "Evaluation"
Cohesion: 0.10
Nodes (13): datetime, UUID, CommonSupport, Validate deterministic scientific ranking semantics., Spatial support shared by the usable crop suitability rasters., validate_comparable_crops(), InvalidEvaluationTransitionError, Raised when an Evaluation lifecycle transition is not allowed. (+5 more)

### Community 20 - "ViabilityPolicySnapshot"
Cohesion: 0.09
Nodes (20): DefaultViabilityPolicyNotConfiguredError, LookupError, Raised when VIA has no default viability policy configured., PolicyVersionConflictError, RuntimeError, Raised when one immutable policy reference is bound to different thresholds., Immutable identity and exact thresholds used for a policy execution., ViabilityPolicySnapshot (+12 more)

### Community 21 - "test_environmental_information_postgresql.py"
Cohesion: 0.12
Nodes (28): CaptureFixture, ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., Read and validate the test-only database settings before any DB operation., require_test_database_url(), UnsafeTestDatabaseError (+20 more)

### Community 22 - "environmental_information/infrastructure/postgresql_repositories.py"
Cohesion: 0.13
Nodes (17): Base, DeclarativeBase, SQLAlchemy metadata owned by Environmental Information Infrastructure., Declarative base for Environmental Information persistence records., Environmental Information infrastructure layer., DatasetRecord, DatasetVersionRecord, Database records for Environmental Information; not domain entities. (+9 more)

### Community 23 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.20
Nodes (28): _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any, FastAPI (+20 more)

### Community 24 - "farm_management/infrastructure/postgresql_repositories.py"
Cohesion: 0.15
Nodes (20): Base, DeclarativeBase, SQLAlchemy metadata owned by Farm Management Infrastructure., Declarative base for Farm Management persistence records., Farm Management infrastructure layer., ParcelRecord, ParcelVersionRecord, Database records for Farm Management; these are not domain entities. (+12 more)

### Community 25 - "cropsuite_adapter.py"
Cohesion: 0.23
Nodes (26): InvalidEngineOutputError, Raised when the engine report does not satisfy the expected PoC contract., Current PoC parcel summary for the crop-suitability output., Trace metadata the current PoC can supply without invented versions., ScientificExecutionTrace, SuitabilityScoreSummary, _boolean(), _fraction() (+18 more)

### Community 26 - "main.py"
Cohesion: 0.10
Nodes (17): get, PostGISCoverageCalculator, SessionFactory, Compare a supplied parcel geometry with a stored native-CRS extent., InMemoryDatasetRepository, create_database(), Engine, SessionFactory (+9 more)

### Community 27 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.16
Nodes (20): Agroclimatic Evaluation application layer., FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedScientificTrace, FinalizedSuitabilitySummary, StrEnum, _availability(), CommonSupportReadResult (+12 more)

### Community 28 - "CoverageMeasurement"
Cohesion: 0.18
Nodes (20): CheckDatasetVersionCoverage, CoverageClassification, CoverageMeasurement, StrEnum, Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port., _multi_polygon(), _polygon() (+12 more)

### Community 29 - "ResourceConflictError"
Cohesion: 0.11
Nodes (16): EnvironmentalInputResolutionError, Exception, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved., _to_common_support(), _to_comparable_crop(), ParcelSnapshotResult, InvalidCommandError (+8 more)

### Community 30 - "EnvironmentalInputReference"
Cohesion: 0.19
Nodes (18): ComparableCrop, One crop ranked on the exact common valid spatial support., EnvironmentalInputReference, Caller-selected exact environmental dataset version., _comparable_support(), _manifest(), parametrize, Domain tests for durable comparable crop results. (+10 more)

### Community 31 - "DatasetVersion"
Cohesion: 0.15
Nodes (13): DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., DatasetVersion, Immutable reproducibility metadata for one dataset release., _version_record(), InMemoryDatasetVersionRepository, UUID (+5 more)

### Community 32 - "Parcel"
Cohesion: 0.17
Nodes (10): Transport-neutral results returned by Farm Management use cases., datetime, Farm Management command and query coordination., Parcel, A named parcel whose geometry changes only by appending versions., ParcelRepository, ProjectRepository, Protocol (+2 more)

### Community 33 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.19
Nodes (20): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+12 more)

### Community 34 - "test_architecture.py"
Cohesion: 0.15
Nodes (15): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+7 more)

### Community 35 - "create_router"
Cohesion: 0.16
Nodes (18): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Commands expressing Agroclimatic Evaluation use-case intent., Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, create_router(), get_evaluation(), get_evaluation_evidence() (+10 more)

### Community 36 - "agroclimatic_evaluation/interfaces/http.py"
Cohesion: 0.18
Nodes (19): CommonSupportResponse, ComparableCropResponse, CropEvidenceResponse, CropOutcomeResponse, EnvironmentalInputReferenceBody, EvaluationEvidenceResponse, EvaluationResponse, EvaluationResultResponse (+11 more)

### Community 37 - "SpatialExtent"
Cohesion: 0.20
Nodes (16): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine (+8 more)

### Community 38 - "test_farm_management_postgresql.py"
Cohesion: 0.28
Nodes (19): clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel(), _polygon(), _project(), datetime (+11 more)

### Community 39 - "Dataset"
Cohesion: 0.16
Nodes (8): datetime, Dataset, Stable logical identity for a geoenvironmental dataset., DatasetRepository, DatasetVersionRepository, Protocol, UUID, Repository abstractions for Environmental Information aggregates.

### Community 40 - "CropSuitabilityRequest"
Cohesion: 0.16
Nodes (11): EngineRunner, CropSuitabilityExecutionError, CropSuitabilityRequest, CropSuitabilityResult, ICropSuitabilityEngine, One checked per-crop outcome from the scientific boundary., Raised when the existing engine service cannot produce a report., Evaluate one crop without exposing engine process or filesystem details. (+3 more)

### Community 41 - "agroclimatic_evaluation/application/ports.py"
Cohesion: 0.13
Nodes (16): CommonSupportStatus, CropComparisonEngineError, CropSuitabilityEngineError, RuntimeError, StrEnum, Application-owned boundary for one crop suitability evaluation., Scientific common-support outcome across evaluated crops., Base error for the scientific crop-comparison boundary. (+8 more)

### Community 42 - "Project"
Cohesion: 0.18
Nodes (9): Project, An agricultural project that groups parcels., ProjectRecord, PostgreSQLProjectRepository, _project_from_record(), SessionFactory, Durable adapter for the Project aggregate., InMemoryProjectRepository (+1 more)

### Community 43 - "AgroclimaticEvaluationService"
Cohesion: 0.25
Nodes (9): GetEvaluation, GetEvaluationEvidence, GetEvaluationResult, ListEvaluations, Queries supported by Agroclimatic Evaluation., EvaluationStatusResult, AgroclimaticEvaluationService, Create and query durable immutable evaluation requests. (+1 more)

### Community 44 - "farm_management/interfaces/http.py"
Cohesion: 0.18
Nodes (14): RuntimeError, Raised when a resource changed during an application operation., ResourceConflictError, CreateParcelBody, CreateProjectBody, GeometryBody, ParcelResponse, ParcelVersionResponse (+6 more)

### Community 45 - "test_agroclimatic_evaluation_queries.py"
Cohesion: 0.19
Nodes (9): _evaluation(), parametrize, UUID, Focused Application query tests for Agroclimatic Evaluation., Repository double that fails if a query touches a mutation/worker method., _ReadOnlySpyRepository, _service(), test_finalized_public_contract_preserves_order_and_outcome_semantics() (+1 more)

### Community 46 - "cropsuite_comparison_adapter.py"
Cohesion: 0.39
Nodes (14): CommonSupportStatus, InvalidComparisonOutputError, Raised when scientific comparison returns an invalid contract., _fraction(), _map_comparable_crops(), _map_comparison_report(), _nonnegative_number(), _number() (+6 more)

### Community 47 - "create_router"
Cohesion: 0.26
Nodes (15): CreateProject, create_router(), create_parcel(), create_project(), get_parcel(), get_project(), list_parcels(), list_projects() (+7 more)

### Community 48 - "CropComparisonRequest"
Cohesion: 0.20
Nodes (10): CommonSupportResult, ComparableCropResult, CropComparisonRequest, CropComparisonResult, ICropComparisonEngine, Compare crop suitability only on identical valid spatial support., Scientific support shared by all usable crop suitability rasters., One crop summarized on the exact common spatial support. (+2 more)

### Community 49 - "create_router"
Cohesion: 0.21
Nodes (13): create_router(), check_dataset_version_coverage(), create_dataset(), create_dataset_version(), get_dataset(), get_dataset_version(), list_dataset_versions(), list_datasets() (+5 more)

### Community 50 - "InMemoryParcelRepository"
Cohesion: 0.19
Nodes (7): ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved., InMemoryParcelRepository, UUID, In-memory Farm Management repository adapters., Process-local parcel storage that retains every geometry version.

### Community 51 - "environmental_information/interfaces/http.py"
Cohesion: 0.27
Nodes (12): CheckCoverageBody, CoverageGeometryBody, CreateDatasetBody, CreateDatasetVersionBody, DatasetResponse, DatasetVersionCoverageResponse, DatasetVersionResponse, BaseModel (+4 more)

### Community 52 - "ScientificArtifactStore"
Cohesion: 0.24
Nodes (8): ComparisonRunner, CropComparisonExecutionError, Raised when scientific common-support comparison cannot execute., _is_within(), Path, Protocol, Publish immutable scientific files behind opaque logical references., ScientificArtifactStore

### Community 53 - "IDefaultViabilityPolicyProvider"
Cohesion: 0.29
Nodes (5): IDefaultViabilityPolicyProvider, IDefaultViabilityPolicyStore, Protocol, Provide the current VIA default viability policy without owning its storage., Read and change the current default viability-policy pointer.

### Community 54 - "test_environmental_information_domain.py"
Cohesion: 0.36
Nodes (7): parametrize, Unit tests for Environmental Information invariants., test_dataset_version_is_immutable(), test_extent_must_be_ordered(), test_invalid_dataset_version_metadata_is_rejected(), test_resolution_must_be_finite_and_positive(), _version()

### Community 55 - "env.py"
Cohesion: 0.47
Nodes (5): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online()

### Community 56 - "ScientificSourceFingerprint"
Cohesion: 0.33
Nodes (5): IEnvironmentalInputIntegrityVerifier, Protocol, Verify resolved environmental provenance against scientific source fingerprints., Opaque scientific source identity and its engine-reported SHA-256., ScientificSourceFingerprint

### Community 57 - "test_farm_management_domain.py"
Cohesion: 0.40
Nodes (5): _polygon(), parametrize, Unit tests for Farm Management invariants., test_invalid_geometry_is_rejected(), test_revising_geometry_appends_an_immutable_version()

### Community 58 - "SpatialCoveragePort"
Cohesion: 0.40
Nodes (4): CoverageComputation, Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort

## Knowledge Gaps
- **1 isolated node(s):** `via-backend`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 473 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `main.py` to `InMemoryEvaluationRepository`, `create_router`, `WorkerSettings`, `test_agroclimatic_evaluation_postgresql.py`, `AgroclimaticEvaluationService`, `EnvironmentalInformationService`, `Project`, `create_router`, `create_router`, `FarmManagementService`, `InMemoryParcelRepository`, `environmental_information/infrastructure/postgresql_repositories.py`, `test_agroclimatic_evaluation_api.py`, `farm_management/infrastructure/postgresql_repositories.py`, `DatasetVersion`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `AgroclimaticEvaluationExecutionService`, `InMemoryEvaluationRepository`, `main.py`, `FilesystemScientificArtifactStore`, `SpatialExtent`, `Dataset`, `DomainValidationError`, `create_router`, `environmental_information/interfaces/http.py`, `SpatialCoveragePort`, `CoverageMeasurement`, `DatasetVersion`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `Evaluation` connect `Evaluation` to `AgroclimaticEvaluationExecutionService`, `EnvironmentalInputManifest`, `InMemoryEvaluationRepository`, `test_agroclimatic_evaluation_domain.py`, `execution.py`, `DomainValidationError`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `test_agroclimatic_evaluation_postgresql.py`, `AgroclimaticEvaluationService`, `test_agroclimatic_evaluation_queries.py`, `test_agroclimatic_evaluation_api.py`, `agroclimatic_evaluation/application/__init__.py`, `ResourceConflictError`, `EnvironmentalInputReference`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `EnvironmentalInformationService` (e.g. with `CreateDataset` and `CreateDatasetVersion`) actually correct?**
  _`EnvironmentalInformationService` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `DatasetVersion` (e.g. with `SpatialCoveragePort` and `DatasetVersionResult`) actually correct?**
  _`DatasetVersion` has 12 INFERRED edges - model-reasoned connections that need verification._