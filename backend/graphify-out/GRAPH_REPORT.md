# Graph Report - backend  (2026-09-16)

## Corpus Check
- 159 files · ~51,665 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1906 nodes · 5694 edges · 88 communities (56 shown, 18 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 800 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e7566e4e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_agroclimatic_evaluation_execution.py
- EnvironmentalInputManifest
- AgroclimaticEvaluationWorker
- test_api_host.py
- agroclimatic_evaluation/domain/__init__.py
- Settings
- test_decision_support.py
- DomainValidationError
- DomainValidationError
- FarmManagementService
- PostgreSQLEvaluationRepository
- EnvironmentalInformationService
- decision_support/application/service.py
- decision_support/domain/models.py
- cropsuite_adapter.py
- DomainValidationError
- PolicyReference
- farm_management/application/service.py
- test_decision_support_postgresql.py
- Evaluation
- PostgreSQLDefaultViabilityPolicyStore
- test_database_test_support.py
- DatasetVersion
- test_agroclimatic_evaluation_api.py
- Parcel
- via_backend/worker.py
- test_agroclimatic_evaluation_worker.py
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- CoverageMeasurement
- EvaluationStatus
- ComparableCrop
- main
- Project
- test_agroclimatic_evaluation_domain.py
- test_architecture.py
- EnvironmentalInputSnapshot
- agroclimatic_evaluation/interfaces/http.py
- test_environmental_information_postgresql.py
- test_farm_management_postgresql.py
- Dataset
- test_crop_comparison_contracts.py
- execution.py
- create_router
- agroclimatic_evaluation/application/__init__.py
- SpatialCoveragePort
- run_forever
- cropsuite_comparison_adapter.py
- test_environmental_information_api.py
- app.py
- WorkerSettings
- SpatialExtent
- AgroclimaticEvaluationRecoveryService
- ScientificArtifact
- verify_runtime
- test_farm_management_api.py
- InMemoryEvaluationRepository
- test_health.py
- __main__.py
- health.py
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
- `_test_app()` --calls--> `create_app()`  [INFERRED]
  tests/test_agroclimatic_evaluation_api.py → src/via_backend/app.py
- `_test_app()` --calls--> `create_app()`  [INFERRED]
  tests/test_environmental_information_api.py → src/via_backend/app.py
- `_test_app()` --calls--> `create_app()`  [INFERRED]
  tests/test_farm_management_api.py → src/via_backend/app.py
- `_test_app()` --uses--> `Settings`  [INFERRED]
  tests/test_agroclimatic_evaluation_api.py → src/via_backend/config.py

## Import Cycles
- None detected.

## Communities (88 total, 18 thin omitted)

### Community 0 - "test_agroclimatic_evaluation_execution.py"
Cohesion: 0.09
Nodes (53): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., EvaluationExecutor, Protocol, GetPublishedDatasetVersion, PublishedDatasetVersion, PublishedDatasetVersionReader, Protocol (+45 more)

### Community 1 - "EnvironmentalInputManifest"
Cohesion: 0.07
Nodes (59): EnvironmentalInputManifest, Immutable set of exact environmental inputs resolved for an evaluation., ConfiguredEnvironmentalInputIntegrityVerifier, CropSuiteEnvironmentalInputBinding, load_cropsuite_environmental_input_bindings(), _parse_uuid(), Any, Path (+51 more)

### Community 2 - "AgroclimaticEvaluationWorker"
Cohesion: 0.17
Nodes (17): AgroclimaticEvaluationWorker, Logger, Discover queued IDs and delegate all execution semantics to Application., _artifact(), _engine_result(), _executor(), FakeEngine, FakeEnvironmentalInformation (+9 more)

### Community 3 - "test_api_host.py"
Cohesion: 0.14
Nodes (19): ApiServerSettings, main(), Production HTTP process host for VIA., Provider-neutral Uvicorn bind settings for the production API process., Load API bind settings from the process environment., Validate production configuration and run one Uvicorn API process., _clear_api_environment(), _configure_production_persistence() (+11 more)

### Community 4 - "agroclimatic_evaluation/domain/__init__.py"
Cohesion: 0.10
Nodes (22): CommonSupport, Evaluation-level scientific common-support result., Validate deterministic scientific ranking semantics., Spatial support shared by the usable crop suitability rasters., validate_comparable_crops(), InvalidEvaluationTransitionError, Domain errors for Agroclimatic Evaluation., Raised when an Evaluation lifecycle transition is not allowed. (+14 more)

### Community 5 - "Settings"
Cohesion: 0.14
Nodes (13): Settings needed by the current backend composition root., Require the durable persistence contract used by the production API., Settings, MonkeyPatch, test_create_production_app_validates_before_composition(), test_database_url_selects_postgresql_by_default(), test_development_settings_can_fall_back_to_memory(), test_environmental_postgresql_selection_requires_database_url() (+5 more)

### Community 6 - "test_decision_support.py"
Cohesion: 0.12
Nodes (42): FinalizedCommonSupportStatus, FinalizedComparableCrop, StrEnum, ComparableCropEvidence, A provider-produced crop mean and rank over common valid support., _common_support(), _decision_evidence(), _DefaultPolicyProvider (+34 more)

### Community 7 - "DomainValidationError"
Cohesion: 0.09
Nodes (39): InvalidSpatialInputError, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, CoverageCompatibilityFailure (+31 more)

### Community 8 - "DomainValidationError"
Cohesion: 0.14
Nodes (24): DomainValidationError, ValueError, Raised when evaluation data violates a domain invariant., ParcelSnapshot, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring() (+16 more)

### Community 9 - "FarmManagementService"
Cohesion: 0.17
Nodes (11): ParcelResult, ParcelVersionResult, ProjectResult, Transport-neutral results returned by Farm Management use cases., FarmManagementService, InvalidCommandError, datetime, UUID (+3 more)

### Community 10 - "PostgreSQLEvaluationRepository"
Cohesion: 0.13
Nodes (51): EnvironmentalInputReference, Caller-selected exact environmental dataset version., PostgreSQLEvaluationRepository, SessionFactory, Durable adapter for immutable Evaluation aggregates., clean_evaluations(), _common_support(), _comparable_crops() (+43 more)

### Community 11 - "EnvironmentalInformationService"
Cohesion: 0.07
Nodes (57): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Stable contracts deliberately published to other bounded contexts., GetDataset, GetDatasetVersion, ListDatasets (+49 more)

### Community 12 - "decision_support/application/service.py"
Cohesion: 0.08
Nodes (35): PolicyEvaluationT, PolicyEvaluationT_co, FinalizedEvaluationResultReader, Protocol, Public local interface for a future Decision Support consumer., IDecisionPolicy, Evaluate comparable evidence without changing its scientific values., EvaluateConfiguredDecisionSupport (+27 more)

### Community 13 - "decision_support/domain/models.py"
Cohesion: 0.10
Nodes (31): DomainValidationError, PolicyVersionConflictError, RuntimeError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Raised when one immutable policy reference is bound to different thresholds., Decision Support domain layer. (+23 more)

### Community 14 - "cropsuite_adapter.py"
Cohesion: 0.08
Nodes (72): EngineRunner, CropExecutionStatus, CropSuitabilityExecutionError, InvalidEngineOutputError, Scientific outcomes reported independently of Evaluation lifecycle state., Raised when the existing engine service cannot produce a report., Raised when the engine report does not satisfy the expected PoC contract., Opaque scientific source identity and its engine-reported SHA-256. (+64 more)

### Community 15 - "DomainValidationError"
Cohesion: 0.09
Nodes (33): DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+25 more)

### Community 16 - "PolicyReference"
Cohesion: 0.08
Nodes (35): InvalidViabilityPolicyRevisionError, ValueError, Raised when a requested viability-policy revision is not a new version., Decision Support application layer., Application lifecycle for immutable Decision Support viability policies., Register one explicitly identified immutable viability-policy version., Create a new immutable version derived from an existing policy identity., Coordinate registration and revision of immutable policy snapshots. (+27 more)

### Community 17 - "farm_management/application/service.py"
Cohesion: 0.10
Nodes (42): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+34 more)

### Community 18 - "test_decision_support_postgresql.py"
Cohesion: 0.24
Nodes (25): PostgreSQLViabilityPolicyRepository, Durable adapter for immutable viability-policy versions., clean_policy_versions(), database(), _database_url(), Engine, fixture, SessionFactory (+17 more)

### Community 19 - "Evaluation"
Cohesion: 0.10
Nodes (16): Evaluation, An immutable multicrop evaluation and its scientific outcomes., EvaluationRepository, Protocol, UUID, _evaluation(), _outcome(), parametrize (+8 more)

### Community 20 - "PostgreSQLDefaultViabilityPolicyStore"
Cohesion: 0.10
Nodes (24): DefaultViabilityPolicyConflictError, DefaultViabilityPolicyNotConfiguredError, LookupError, RuntimeError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist., Raised when VIA has no default viability policy configured., Raised when the default policy changed before an expected update. (+16 more)

### Community 21 - "test_database_test_support.py"
Cohesion: 0.22
Nodes (14): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., UnsafeTestDatabaseError, validate_test_database_url(), CaptureFixture, parametrize (+6 more)

### Community 22 - "DatasetVersion"
Cohesion: 0.09
Nodes (29): DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., DatasetVersion, Immutable reproducibility metadata for one dataset release., Base, DeclarativeBase, SQLAlchemy metadata owned by Environmental Information Infrastructure. (+21 more)

### Community 23 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.20
Nodes (28): _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any, FastAPI (+20 more)

### Community 24 - "Parcel"
Cohesion: 0.08
Nodes (35): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online(), ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved. (+27 more)

### Community 25 - "via_backend/worker.py"
Cohesion: 0.07
Nodes (58): ArgumentParser, PurePosixPath, CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., Agroclimatic Evaluation infrastructure layer., _file_identity(), FilesystemScientificArtifactStore, _is_within() (+50 more)

### Community 26 - "test_agroclimatic_evaluation_worker.py"
Cohesion: 0.16
Nodes (19): _evaluation(), FakeComparisonEngine, _manifest(), datetime, Path, UUID, Fast tests for PostgreSQL-polling worker coordination and orphan recovery., _reference() (+11 more)

### Community 27 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.12
Nodes (40): EvaluationConflictError, RuntimeError, Raised when an evaluation identity already exists., Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records., CropOutcomeRecord (+32 more)

### Community 28 - "CoverageMeasurement"
Cohesion: 0.16
Nodes (21): CheckDatasetVersionCoverage, CoverageClassification, CoverageMeasurement, StrEnum, Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port., _multi_polygon(), _polygon() (+13 more)

### Community 29 - "EvaluationStatus"
Cohesion: 0.10
Nodes (23): AgroclimaticEvaluationExecutionService, Exception, Execute requested crops and summarize them through Application-owned ports., Explicit fail-only recovery for abandoned evaluation executions., ActiveEvaluationResult, CropOutcomeResult, EvaluationResult, ParcelSnapshotResult (+15 more)

### Community 30 - "ComparableCrop"
Cohesion: 0.22
Nodes (17): ComparableCrop, One crop ranked on the exact common valid spatial support., _comparable_support(), _manifest(), _outcome(), parametrize, Domain tests for durable comparable crop results., _reference() (+9 more)

### Community 31 - "main"
Cohesion: 0.10
Nodes (18): FrameType, list_active_evaluations(), main(), make_shutdown_handler(), _print_active_evaluations(), Logger, Return a signal handler that only requests cooperative process shutdown., List active evaluations without composing scientific execution dependencies. (+10 more)

### Community 32 - "Project"
Cohesion: 0.13
Nodes (10): Project, An agricultural project that groups parcels., ParcelRepository, ProjectRepository, Protocol, UUID, Repository abstractions for Farm Management aggregates., _project_from_record() (+2 more)

### Community 33 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.19
Nodes (20): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+12 more)

### Community 34 - "test_architecture.py"
Cohesion: 0.14
Nodes (17): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+9 more)

### Community 35 - "EnvironmentalInputSnapshot"
Cohesion: 0.18
Nodes (12): EnvironmentalInputSnapshot, _is_finite_number(), datetime, Immutable environmental input snapshots owned by Agroclimatic Evaluation., Historical environmental input metadata captured for one evaluation input., _validate_aware_datetime(), _validate_crs(), _validate_positive_number() (+4 more)

### Community 36 - "agroclimatic_evaluation/interfaces/http.py"
Cohesion: 0.09
Nodes (36): _to_common_support(), _availability(), CommonSupportReadResult, ComparableCropReadResult, CropEvidenceResult, EvaluationResultAvailability, PersistedCropOutcomeResult, StrEnum (+28 more)

### Community 37 - "test_environmental_information_postgresql.py"
Cohesion: 0.28
Nodes (14): Read and validate the test-only database settings before any DB operation., require_test_database_url(), clean_environmental_information(), database(), _database_url(), _dataset(), Engine, fixture (+6 more)

### Community 38 - "test_farm_management_postgresql.py"
Cohesion: 0.21
Nodes (22): PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel() (+14 more)

### Community 39 - "Dataset"
Cohesion: 0.14
Nodes (9): datetime, Dataset, Stable logical identity for a geoenvironmental dataset., DatasetRepository, DatasetVersionRepository, Protocol, UUID, Repository abstractions for Environmental Information aggregates. (+1 more)

### Community 41 - "execution.py"
Cohesion: 0.06
Nodes (42): _comparison_request(), EnvironmentalInputResolutionError, datetime, RuntimeError, Synchronous application orchestration for persisted evaluations., Raised when an exact caller-selected environmental version cannot be resolved., _to_comparable_crop(), _to_outcome() (+34 more)

### Community 42 - "create_router"
Cohesion: 0.16
Nodes (18): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Commands expressing Agroclimatic Evaluation use-case intent., Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, create_router(), get_evaluation(), get_evaluation_evidence() (+10 more)

### Community 43 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.15
Nodes (23): Agroclimatic Evaluation application layer., FinalizedCommonSupport, FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedEvaluationResult, FinalizedScientificTrace, FinalizedSuitabilitySummary, GetFinalizedEvaluationResult (+15 more)

### Community 44 - "SpatialCoveragePort"
Cohesion: 0.40
Nodes (4): CoverageComputation, Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort

### Community 45 - "run_forever"
Cohesion: 0.21
Nodes (8): Event, WorkerRunSummary, Poll until cooperative shutdown, waiting only after a non-full batch., run_forever(), test_run_forever_does_not_poll_again_after_stop_is_requested(), run_once(), test_run_forever_poll_wait_can_be_interrupted_by_stop(), run_once()

### Community 46 - "cropsuite_comparison_adapter.py"
Cohesion: 0.13
Nodes (30): CommonSupportStatus, ComparisonRunner, CommonSupportResult, CommonSupportStatus, ComparableCropResult, CropComparisonEngineError, CropComparisonExecutionError, CropComparisonResult (+22 more)

### Community 47 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 48 - "app.py"
Cohesion: 0.13
Nodes (16): create_app(), create_production_app(), FastAPI, Side-effect-free FastAPI application composition., Build the production API after enforcing durable persistence settings., Build the VIA API and register its technical interfaces., PostGISCoverageCalculator, SessionFactory (+8 more)

### Community 49 - "WorkerSettings"
Cohesion: 0.16
Nodes (15): _environment_float(), _environment_integer(), _optional_path(), Path, Environment-backed configuration for the VIA application host., Settings for the PostgreSQL polling worker process., WorkerSettings, parametrize (+7 more)

### Community 50 - "SpatialExtent"
Cohesion: 0.13
Nodes (23): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine (+15 more)

### Community 51 - "AgroclimaticEvaluationRecoveryService"
Cohesion: 0.18
Nodes (17): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Logger, Mark an operator-confirmed active orphan as failed without retrying it., UUID, Run explicit fail-only orphan recovery without composing CropSuiteLite., recover_evaluation() (+9 more)

### Community 52 - "ScientificArtifact"
Cohesion: 0.29
Nodes (5): Immutable spatial grid identity for a scientific raster., Durable scientific evidence referenced without exposing filesystem paths., ScientificArtifact, ScientificArtifactGrid, _artifact_from_record()

### Community 56 - "verify_runtime"
Cohesion: 0.39
Nodes (7): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_writable_directory(), _run_pip_check(), verify_runtime()

### Community 57 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 58 - "InMemoryEvaluationRepository"
Cohesion: 0.27
Nodes (3): InMemoryEvaluationRepository, UUID, _validate_limit()

### Community 73 - "health.py"
Cohesion: 0.40
Nodes (4): get, health(), Host-level health endpoint., Report that the API process is ready to receive requests.

## Knowledge Gaps
- **1 isolated node(s):** `via-backend`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 511 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `test_agroclimatic_evaluation_execution.py`, `DomainValidationError`, `Dataset`, `SpatialCoveragePort`, `app.py`, `SpatialExtent`, `DatasetVersion`, `via_backend/worker.py`, `CoverageMeasurement`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `create_app()` connect `app.py` to `Project`, `Settings`, `test_farm_management_postgresql.py`, `Dataset`, `FarmManagementService`, `create_router`, `PostgreSQLEvaluationRepository`, `agroclimatic_evaluation/application/__init__.py`, `EnvironmentalInformationService`, `test_environmental_information_api.py`, `farm_management/application/service.py`, `DatasetVersion`, `test_agroclimatic_evaluation_api.py`, `Parcel`, `test_farm_management_api.py`, `InMemoryEvaluationRepository`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `Evaluation` connect `Evaluation` to `test_agroclimatic_evaluation_execution.py`, `EnvironmentalInputManifest`, `test_agroclimatic_evaluation_domain.py`, `test_agroclimatic_evaluation_worker.py`, `agroclimatic_evaluation/domain/__init__.py`, `agroclimatic_evaluation/interfaces/http.py`, `DomainValidationError`, `execution.py`, `PostgreSQLEvaluationRepository`, `agroclimatic_evaluation/application/__init__.py`, `test_agroclimatic_evaluation_api.py`, `InMemoryEvaluationRepository`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `EvaluationStatus`, `ComparableCrop`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `PostgreSQLEvaluationRepository` (e.g. with `EvaluationConflictError` and `Evaluation`) actually correct?**
  _`PostgreSQLEvaluationRepository` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `EvaluationStatus` (e.g. with `RecoverEvaluation` and `AgroclimaticEvaluationExecutionService`) actually correct?**
  _`EvaluationStatus` has 18 INFERRED edges - model-reasoned connections that need verification._