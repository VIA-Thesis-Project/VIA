# Graph Report - backend  (2026-09-16)

## Corpus Check
- 161 files · ~52,733 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1951 nodes · 5793 edges · 93 communities (62 shown, 17 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 804 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6fc536ff`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AgroclimaticEvaluationExecutionService
- ConfiguredEnvironmentalInputIntegrityVerifier
- InMemoryEvaluationRepository
- test_migration_host.py
- Evaluation
- Settings
- test_decision_support.py
- environmental_information/application/service.py
- DomainValidationError
- FarmManagementService
- PostgreSQLEvaluationRepository
- EnvironmentalInformationService
- ViabilityPolicySnapshot
- decision_support/domain/models.py
- test_cropsuite_adapter.py
- DomainValidationError
- PolicyReference
- farm_management/application/service.py
- test_decision_support_postgresql.py
- GetFinalizedEvaluationResult
- ViabilityPolicyVersionRecord
- require_test_database_url
- via_backend/worker.py
- test_agroclimatic_evaluation_api.py
- Parcel
- scientific_artifact_store.py
- decision_support/application/service.py
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- CoverageMeasurement
- execution.py
- EnvironmentalInputReference
- main
- Project
- test_agroclimatic_evaluation_domain.py
- test_architecture.py
- test_api_host.py
- EvaluationStatus
- .from_geojson
- test_farm_management_postgresql.py
- DatasetVersion
- CommonSupportResult
- cropsuite_adapter.py
- agroclimatic_evaluation/application/service.py
- create_router
- agroclimatic_evaluation/application/__init__.py
- test_agroclimatic_environmental_inputs.py
- cropsuite_comparison_adapter.py
- test_environmental_information_api.py
- app.py
- config.py
- SpatialExtent
- test_config.py
- CropSuiteComparisonAdapter
- AgroclimaticEvaluationService
- agroclimatic_evaluation/infrastructure/__init__.py
- FilesystemScientificArtifactStore
- verify_runtime
- test_farm_management_api.py
- ResourceConflictError
- test_health.py
- __main__.py
- CropSuitabilityResult
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
- test_container_image_contract.py
- CropComparisonExecutionError
- ScientificSourceFingerprint

## God Nodes (most connected - your core abstractions)
1. `Evaluation` - 90 edges
2. `DomainValidationError` - 56 edges
3. `PostgreSQLEvaluationRepository` - 50 edges
4. `EvaluationStatus` - 49 edges
5. `EnvironmentalInformationService` - 49 edges
6. `DatasetVersion` - 45 edges
7. `InMemoryEvaluationRepository` - 44 edges
8. `AgroclimaticEvaluationService` - 42 edges
9. `PolicyReference` - 39 edges
10. `EnvironmentalInputManifest` - 38 edges

## Surprising Connections (you probably didn't know these)
- `test_environmental_input_reference_accepts_exact_version_identity()` --calls--> `EnvironmentalInputReference`  [INFERRED]
  tests/test_agroclimatic_environmental_inputs.py → src/via_backend/contexts/agroclimatic_evaluation/domain/environmental_inputs.py
- `test_environmental_input_manifest_rejects_empty_inputs()` --calls--> `EnvironmentalInputManifest`  [INFERRED]
  tests/test_agroclimatic_environmental_inputs.py → src/via_backend/contexts/agroclimatic_evaluation/domain/environmental_inputs.py
- `_test_app()` --calls--> `create_app()`  [INFERRED]
  tests/test_agroclimatic_evaluation_api.py → src/via_backend/app.py
- `_test_app()` --calls--> `create_app()`  [INFERRED]
  tests/test_environmental_information_api.py → src/via_backend/app.py
- `_test_app()` --calls--> `create_app()`  [INFERRED]
  tests/test_farm_management_api.py → src/via_backend/app.py

## Import Cycles
- None detected.

## Communities (93 total, 17 thin omitted)

### Community 0 - "AgroclimaticEvaluationExecutionService"
Cohesion: 0.08
Nodes (56): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, datetime, Execute requested crops and summarize them through Application-owned ports., EvaluationExecutor, Protocol, GetPublishedDatasetVersion (+48 more)

### Community 1 - "ConfiguredEnvironmentalInputIntegrityVerifier"
Cohesion: 0.23
Nodes (22): ConfiguredEnvironmentalInputIntegrityVerifier, Verify manifests using deployment-configured exact dataset-version bindings., _binding(), _fingerprints(), _manifest(), parametrize, Path, ScientificSourceFingerprint (+14 more)

### Community 2 - "InMemoryEvaluationRepository"
Cohesion: 0.08
Nodes (52): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Logger, Mark an operator-confirmed active orphan as failed without retrying it., AgroclimaticEvaluationWorker, Logger, Discover queued IDs and delegate all execution semantics to Application. (+44 more)

### Community 3 - "test_migration_host.py"
Cohesion: 0.11
Nodes (30): _build_parser(), main(), ArgumentParser, Path, One-shot production schema migration host for VIA releases., Return the repository-local Alembic config when running from source., Resolve the Alembic config without depending on the process cwd., Validate production persistence and migrate the schema to Alembic head. (+22 more)

### Community 4 - "Evaluation"
Cohesion: 0.08
Nodes (15): Exception, Validate deterministic scientific ranking semantics., validate_comparable_crops(), EvaluationConflictError, InvalidEvaluationTransitionError, RuntimeError, Raised when an Evaluation lifecycle transition is not allowed., Raised when an evaluation identity already exists. (+7 more)

### Community 5 - "Settings"
Cohesion: 0.14
Nodes (13): Settings needed by the current backend composition root., Require the durable persistence contract used by the production API., Settings, MonkeyPatch, test_create_production_app_validates_before_composition(), test_database_url_selects_postgresql_by_default(), test_development_settings_can_fall_back_to_memory(), test_environmental_postgresql_selection_requires_database_url() (+5 more)

### Community 6 - "test_decision_support.py"
Cohesion: 0.11
Nodes (42): FinalizedCommonSupportStatus, FinalizedComparableCrop, StrEnum, ComparableCropEvidence, A provider-produced crop mean and rank over common valid support., _common_support(), _decision_evidence(), _DefaultPolicyProvider (+34 more)

### Community 7 - "environmental_information/application/service.py"
Cohesion: 0.09
Nodes (40): InvalidSpatialInputError, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, Environmental Information command and query coordination. (+32 more)

### Community 8 - "DomainValidationError"
Cohesion: 0.08
Nodes (28): EnvironmentalInputResolutionError, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved., CropComparisonRequest, CropSuitabilityRequest, Compare crop suitability only on identical valid spatial support., Transport-neutral input for evaluating one crop against an exact snapshot., EnvironmentalInputManifest (+20 more)

### Community 9 - "FarmManagementService"
Cohesion: 0.17
Nodes (11): ParcelResult, ParcelVersionResult, ProjectResult, Transport-neutral results returned by Farm Management use cases., FarmManagementService, InvalidCommandError, datetime, UUID (+3 more)

### Community 10 - "PostgreSQLEvaluationRepository"
Cohesion: 0.15
Nodes (49): PostgreSQLEvaluationRepository, SessionFactory, Durable adapter for immutable Evaluation aggregates., clean_evaluations(), _common_support(), _comparable_crops(), database(), _database_url() (+41 more)

### Community 11 - "EnvironmentalInformationService"
Cohesion: 0.06
Nodes (61): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort, Stable contracts deliberately published to other bounded contexts. (+53 more)

### Community 12 - "ViabilityPolicySnapshot"
Cohesion: 0.10
Nodes (23): IDefaultViabilityPolicyProvider, IDefaultViabilityPolicyStore, Protocol, Provide the current VIA default viability policy without owning its storage., Read and change the current default viability-policy pointer., EvaluateConfiguredDecisionSupport, StrEnum, Decision Support application query messages. (+15 more)

### Community 13 - "decision_support/domain/models.py"
Cohesion: 0.10
Nodes (28): DomainValidationError, PolicyVersionConflictError, RuntimeError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Raised when one immutable policy reference is bound to different thresholds., Decision Support domain layer. (+20 more)

### Community 14 - "test_cropsuite_adapter.py"
Cohesion: 0.17
Nodes (38): CropExecutionStatus, Scientific outcomes reported independently of Evaluation lifecycle state., CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability., _adapter(), _environmental_input_manifest(), _geometry(), _integrity_verifier() (+30 more)

### Community 15 - "DomainValidationError"
Cohesion: 0.09
Nodes (33): DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+25 more)

### Community 16 - "PolicyReference"
Cohesion: 0.10
Nodes (34): DefaultViabilityPolicyConflictError, DefaultViabilityPolicyNotConfiguredError, InvalidViabilityPolicyRevisionError, LookupError, RuntimeError, ValueError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist. (+26 more)

### Community 17 - "farm_management/application/service.py"
Cohesion: 0.10
Nodes (42): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+34 more)

### Community 18 - "test_decision_support_postgresql.py"
Cohesion: 0.17
Nodes (30): Decision Support infrastructure adapters., PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+22 more)

### Community 19 - "GetFinalizedEvaluationResult"
Cohesion: 0.15
Nodes (10): GetFinalizedEvaluationResult, _evaluation(), parametrize, UUID, Focused Application query tests for Agroclimatic Evaluation., Repository double that fails if a query touches a mutation/worker method., _ReadOnlySpyRepository, _service() (+2 more)

### Community 20 - "ViabilityPolicyVersionRecord"
Cohesion: 0.24
Nodes (9): Base, DeclarativeBase, SQLAlchemy metadata owned by Decision Support Infrastructure., Declarative base for Decision Support persistence records., DefaultViabilityPolicyRecord, Database records for Decision Support; these are not domain entities., One immutable persisted viability-policy configuration., Singleton pointer to the currently selected VIA default policy version. (+1 more)

### Community 21 - "require_test_database_url"
Cohesion: 0.19
Nodes (16): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., Read and validate the test-only database settings before any DB operation., require_test_database_url(), UnsafeTestDatabaseError, validate_test_database_url() (+8 more)

### Community 22 - "via_backend/worker.py"
Cohesion: 0.06
Nodes (49): ActiveEvaluationResult, Base, DeclarativeBase, SQLAlchemy metadata owned by Environmental Information Infrastructure., Declarative base for Environmental Information persistence records., Environmental Information infrastructure layer., DatasetRecord, DatasetVersionRecord (+41 more)

### Community 23 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.20
Nodes (28): _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any, FastAPI (+20 more)

### Community 24 - "Parcel"
Cohesion: 0.08
Nodes (35): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online(), ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved. (+27 more)

### Community 25 - "scientific_artifact_store.py"
Cohesion: 0.15
Nodes (17): PurePosixPath, _file_identity(), _is_within(), PublishedScientificArtifact, Path, RuntimeError, Durable filesystem storage for scientific artifacts., Base error for durable scientific artifact storage failures. (+9 more)

### Community 26 - "decision_support/application/service.py"
Cohesion: 0.12
Nodes (23): PolicyEvaluationT, PolicyEvaluationT_co, Decision Support application layer., IDecisionPolicy, Application ports for deterministic Decision Support policies., Evaluate comparable evidence without changing its scientific values., EvaluateDecisionSupport, Prepare evidence and apply one explicitly versioned policy when possible. (+15 more)

### Community 27 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.13
Nodes (38): Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records., CropOutcomeRecord, EvaluationCommonSupportRecord, EvaluationComparableCropRecord, EvaluationCropRecord (+30 more)

### Community 28 - "CoverageMeasurement"
Cohesion: 0.18
Nodes (20): CheckDatasetVersionCoverage, CoverageClassification, CoverageMeasurement, StrEnum, Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port., _multi_polygon(), _polygon() (+12 more)

### Community 29 - "execution.py"
Cohesion: 0.09
Nodes (43): _comparison_request(), Synchronous application orchestration for persisted evaluations., _to_common_support(), _to_comparable_crop(), _to_outcome(), CropComparisonInput, One durable crop suitability raster offered to scientific comparison., Explicit fail-only recovery for abandoned evaluation executions. (+35 more)

### Community 30 - "EnvironmentalInputReference"
Cohesion: 0.19
Nodes (18): ComparableCrop, One crop ranked on the exact common valid spatial support., EnvironmentalInputReference, Caller-selected exact environmental dataset version., _comparable_support(), _manifest(), parametrize, Domain tests for durable comparable crop results. (+10 more)

### Community 31 - "main"
Cohesion: 0.07
Nodes (27): Event, FrameType, get, WorkerRunSummary, health(), Host-level health endpoint., Report that the API process is ready to receive requests., main() (+19 more)

### Community 32 - "Project"
Cohesion: 0.13
Nodes (10): Project, An agricultural project that groups parcels., ParcelRepository, ProjectRepository, Protocol, UUID, Repository abstractions for Farm Management aggregates., _project_from_record() (+2 more)

### Community 33 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.19
Nodes (20): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+12 more)

### Community 34 - "test_architecture.py"
Cohesion: 0.14
Nodes (17): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+9 more)

### Community 35 - "test_api_host.py"
Cohesion: 0.14
Nodes (19): ApiServerSettings, main(), Production HTTP process host for VIA., Provider-neutral Uvicorn bind settings for the production API process., Load API bind settings from the process environment., Validate production configuration and run one Uvicorn API process., _clear_api_environment(), _configure_production_persistence() (+11 more)

### Community 36 - "EvaluationStatus"
Cohesion: 0.17
Nodes (22): EvaluationStatus, StrEnum, Architecture-approved lifecycle vocabulary., CommonSupportResponse, ComparableCropResponse, CropEvidenceResponse, CropOutcomeResponse, EnvironmentalInputReferenceBody (+14 more)

### Community 37 - ".from_geojson"
Cohesion: 0.18
Nodes (17): _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing, MultiPolygonCoordinates, PolygonCoordinates (+9 more)

### Community 38 - "test_farm_management_postgresql.py"
Cohesion: 0.21
Nodes (22): PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel() (+14 more)

### Community 39 - "DatasetVersion"
Cohesion: 0.08
Nodes (21): CoverageComputation, DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., Dataset, DatasetVersion, Stable logical identity for a geoenvironmental dataset., Immutable reproducibility metadata for one dataset release. (+13 more)

### Community 40 - "CommonSupportResult"
Cohesion: 0.18
Nodes (8): CommonSupportResult, CropComparisonResult, ICropComparisonEngine, Scientific support shared by all usable crop suitability rasters., Checked multicrop comparison returned by the scientific boundary., Compare durable crop outputs using the authoritative scientific engine., StubComparisonEngine, test_comparison_engine_contract_is_runtime_checkable()

### Community 41 - "cropsuite_adapter.py"
Cohesion: 0.14
Nodes (36): InvalidEngineOutputError, Application-owned boundary for one crop suitability evaluation., Raised when the engine report does not satisfy the expected PoC contract., Current PoC parcel summary for the crop-suitability output., Portable grid identity needed to verify comparable scientific rasters., Scientific artifact roles understood by VIA., Durable opaque reference to one verified scientific artifact., An engine-reported failure, distinct from no coverage and a zero score. (+28 more)

### Community 42 - "agroclimatic_evaluation/application/service.py"
Cohesion: 0.17
Nodes (14): FinalizedCommonSupport, FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedEvaluationResult, FinalizedEvaluationResultReader, FinalizedScientificTrace, FinalizedSuitabilitySummary, Protocol (+6 more)

### Community 43 - "create_router"
Cohesion: 0.16
Nodes (18): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Commands expressing Agroclimatic Evaluation use-case intent., Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, create_router(), get_evaluation(), get_evaluation_evidence() (+10 more)

### Community 44 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.23
Nodes (14): Agroclimatic Evaluation application layer., _availability(), CommonSupportReadResult, ComparableCropReadResult, CropEvidenceResult, EvaluationEvidenceResult, EvaluationReadResult, EvaluationResultAvailability (+6 more)

### Community 45 - "test_agroclimatic_environmental_inputs.py"
Cohesion: 0.18
Nodes (22): parametrize, Focused domain tests for immutable environmental input manifests., _snapshot(), test_environmental_input_manifest_accepts_valid_inputs(), test_environmental_input_manifest_allows_same_version_for_distinct_input_keys(), test_environmental_input_manifest_rejects_duplicate_input_key(), test_environmental_input_manifest_rejects_empty_inputs(), test_environmental_input_manifest_rejects_input_registered_after_resolution() (+14 more)

### Community 46 - "cropsuite_comparison_adapter.py"
Cohesion: 0.26
Nodes (19): CommonSupportStatus, CommonSupportStatus, ComparableCropResult, InvalidComparisonOutputError, StrEnum, Scientific common-support outcome across evaluated crops., One crop summarized on the exact common spatial support., Raised when scientific comparison returns an invalid contract. (+11 more)

### Community 47 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 48 - "app.py"
Cohesion: 0.21
Nodes (10): create_app(), create_production_app(), FastAPI, Side-effect-free FastAPI application composition., Build the production API after enforcing durable persistence settings., Build the VIA API and register its technical interfaces., PostGISCoverageCalculator, SessionFactory (+2 more)

### Community 49 - "config.py"
Cohesion: 0.33
Nodes (7): _environment_float(), _environment_integer(), _is_same_or_within(), _optional_path(), Path, Environment-backed configuration for the VIA application host., _validate_scientific_path_topology()

### Community 50 - "SpatialExtent"
Cohesion: 0.13
Nodes (23): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine (+15 more)

### Community 51 - "test_config.py"
Cohesion: 0.24
Nodes (14): Settings for the PostgreSQL polling worker process., WorkerSettings, parametrize, Path, Tests for environment-driven application composition settings., _scientific_worker_settings(), test_production_settings_reject_memory_repository(), test_worker_run_requires_durable_artifact_root() (+6 more)

### Community 52 - "CropSuiteComparisonAdapter"
Cohesion: 0.30
Nodes (17): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., _artifact(), Any, Path, _report(), _request(), _snapshot() (+9 more)

### Community 53 - "AgroclimaticEvaluationService"
Cohesion: 0.25
Nodes (9): GetEvaluation, GetEvaluationEvidence, GetEvaluationResult, ListEvaluations, Queries supported by Agroclimatic Evaluation., EvaluationStatusResult, AgroclimaticEvaluationService, Create and query durable immutable evaluation requests. (+1 more)

### Community 54 - "agroclimatic_evaluation/infrastructure/__init__.py"
Cohesion: 0.16
Nodes (16): Agroclimatic Evaluation infrastructure layer., CropSuiteEnvironmentalInputBinding, load_configured_environmental_input_integrity_verifier(), load_cropsuite_environmental_input_bindings(), _parse_uuid(), Any, Path, UUID (+8 more)

### Community 55 - "FilesystemScientificArtifactStore"
Cohesion: 0.30
Nodes (14): FilesystemScientificArtifactStore, Filesystem-backed immutable artifact store., parametrize, Path, test_publish_creates_durable_artifact_with_opaque_reference(), test_publish_is_idempotent_for_identical_content(), test_publish_rejects_content_that_does_not_match_expected_checksum(), test_publish_rejects_different_content_for_existing_reference() (+6 more)

### Community 56 - "verify_runtime"
Cohesion: 0.39
Nodes (8): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_read_only_directory(), _require_writable_directory(), _run_pip_check(), verify_runtime()

### Community 57 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 58 - "ResourceConflictError"
Cohesion: 0.17
Nodes (10): InvalidCommandError, LookupError, RuntimeError, ValueError, Raised when a requested evaluation does not exist., Raised when request data violates an evaluation invariant., Raised when an evaluation identity already exists., ResourceConflictError (+2 more)

### Community 73 - "CropSuitabilityResult"
Cohesion: 0.12
Nodes (15): EngineRunner, CropSuitabilityExecutionError, CropSuitabilityResult, ICropSuitabilityEngine, IEnvironmentalInputIntegrityVerifier, Protocol, One checked per-crop outcome from the scientific boundary., Raised when the existing engine service cannot produce a report. (+7 more)

### Community 91 - "CropComparisonExecutionError"
Cohesion: 0.24
Nodes (8): ComparisonRunner, CropComparisonEngineError, CropComparisonExecutionError, RuntimeError, Base error for the scientific crop-comparison boundary., Raised when scientific common-support comparison cannot execute., _is_within(), Path

### Community 92 - "ScientificSourceFingerprint"
Cohesion: 0.29
Nodes (6): CropSuitabilityEngineError, EnvironmentalInputIntegrityError, Base error for failures to invoke or understand the engine boundary., Raised when resolved environmental provenance does not match scientific inputs., Opaque scientific source identity and its engine-reported SHA-256., ScientificSourceFingerprint

## Knowledge Gaps
- **1 isolated node(s):** `via-backend`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 526 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `app.py` to `Project`, `InMemoryEvaluationRepository`, `Settings`, `test_farm_management_postgresql.py`, `DatasetVersion`, `FarmManagementService`, `PostgreSQLEvaluationRepository`, `create_router`, `EnvironmentalInformationService`, `test_environmental_information_api.py`, `farm_management/application/service.py`, `AgroclimaticEvaluationService`, `via_backend/worker.py`, `test_agroclimatic_evaluation_api.py`, `Parcel`, `test_farm_management_api.py`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `AgroclimaticEvaluationExecutionService`, `DatasetVersion`, `environmental_information/application/service.py`, `app.py`, `SpatialExtent`, `via_backend/worker.py`, `CoverageMeasurement`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `AgroclimaticEvaluationService` connect `AgroclimaticEvaluationService` to `Evaluation`, `EvaluationStatus`, `test_decision_support.py`, `.from_geojson`, `DomainValidationError`, `agroclimatic_evaluation/application/service.py`, `create_router`, `agroclimatic_evaluation/application/__init__.py`, `app.py`, `GetFinalizedEvaluationResult`, `test_agroclimatic_evaluation_api.py`, `execution.py`, `EnvironmentalInputReference`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `PostgreSQLEvaluationRepository` (e.g. with `EvaluationConflictError` and `Evaluation`) actually correct?**
  _`PostgreSQLEvaluationRepository` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `EvaluationStatus` (e.g. with `RecoverEvaluation` and `AgroclimaticEvaluationExecutionService`) actually correct?**
  _`EvaluationStatus` has 18 INFERRED edges - model-reasoned connections that need verification._