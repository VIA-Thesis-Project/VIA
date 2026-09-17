# Graph Report - backend  (2026-09-16)

## Corpus Check
- 154 files · ~50,374 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1853 nodes · 5597 edges · 93 communities (62 shown, 17 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 789 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c4409d4d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AgroclimaticEvaluationExecutionService
- EnvironmentalInputManifest
- InMemoryEvaluationRepository
- FilesystemScientificArtifactStore
- execution.py
- Settings
- test_decision_support.py
- DomainValidationError
- DomainValidationError
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- PostgreSQLEvaluationRepository
- EnvironmentalInformationService
- DecisionSupportWorkflow
- decision_support/domain/models.py
- cropsuite_adapter.py
- DomainValidationError
- PolicyReference
- FarmManagementService
- test_decision_support_postgresql.py
- Evaluation
- ViabilityPolicySnapshot
- require_test_database_url
- DatasetVersion
- test_agroclimatic_evaluation_api.py
- Parcel
- scientific_artifact_store.py
- main.py
- agroclimatic_evaluation/application/__init__.py
- CoverageMeasurement
- EvaluationResult
- ComparableCrop
- main
- Project
- test_agroclimatic_evaluation_domain.py
- test_architecture.py
- create_router
- agroclimatic_evaluation/interfaces/http.py
- test_environmental_information_coverage_postgresql.py
- test_farm_management_postgresql.py
- Dataset
- agroclimatic_evaluation/application/service.py
- agroclimatic_evaluation/application/ports.py
- create_database
- AgroclimaticEvaluationService
- EvaluationStatus
- test_agroclimatic_evaluation_queries.py
- cropsuite_comparison_adapter.py
- test_environmental_information_api.py
- via_backend/worker.py
- WorkerSettings
- InMemoryParcelRepository
- environmental_information/interfaces/http.py
- CropComparisonExecutionError
- DecisionSupportService
- test_scientific_artifact_store.py
- env.py
- run_forever
- test_farm_management_api.py
- CommonSupport
- test_health.py
- __main__.py
- test_explicit_recovery_uses_expected_status
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
- create_worker
- health.py
- .__init__

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
- `_test_app()` --uses--> `Settings`  [INFERRED]
  tests/test_agroclimatic_evaluation_api.py → src/via_backend/config.py
- `test_environmental_postgresql_selection_requires_database_url()` --uses--> `Settings`  [INFERRED]
  tests/test_config.py → src/via_backend/config.py
- `test_evaluation_postgresql_selection_requires_database_url()` --uses--> `Settings`  [INFERRED]
  tests/test_config.py → src/via_backend/config.py
- `test_postgresql_selection_requires_database_url()` --uses--> `Settings`  [INFERRED]
  tests/test_config.py → src/via_backend/config.py

## Import Cycles
- None detected.

## Communities (93 total, 17 thin omitted)

### Community 0 - "AgroclimaticEvaluationExecutionService"
Cohesion: 0.09
Nodes (57): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, datetime, Execute requested crops and summarize them through Application-owned ports., EnvironmentalInputReference, Caller-selected exact environmental dataset version., GetPublishedDatasetVersion (+49 more)

### Community 1 - "EnvironmentalInputManifest"
Cohesion: 0.06
Nodes (71): EnvironmentalInputResolutionError, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved., EnvironmentalInputIntegrityError, Raised when resolved environmental provenance does not match scientific inputs., EnvironmentalInputManifest, EnvironmentalInputSnapshot, Immutable set of exact environmental inputs resolved for an evaluation. (+63 more)

### Community 2 - "InMemoryEvaluationRepository"
Cohesion: 0.16
Nodes (28): AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application., InMemoryEvaluationRepository, _artifact(), _engine_result(), _evaluation(), _executor(), FakeComparisonEngine (+20 more)

### Community 3 - "FilesystemScientificArtifactStore"
Cohesion: 0.26
Nodes (20): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., Agroclimatic Evaluation infrastructure layer., FilesystemScientificArtifactStore, Filesystem-backed immutable artifact store., _artifact(), Any, Path (+12 more)

### Community 4 - "execution.py"
Cohesion: 0.10
Nodes (38): _comparison_request(), Synchronous application orchestration for persisted evaluations., _to_common_support(), _to_outcome(), Portable grid identity needed to verify comparable scientific rasters., ScientificArtifactGrid, CropOutcomeResult, Transport-neutral Agroclimatic Evaluation results. (+30 more)

### Community 5 - "Settings"
Cohesion: 0.17
Nodes (13): Settings needed by the current backend composition root., Settings, MonkeyPatch, parametrize, Tests for environment-driven application composition settings., test_database_url_selects_postgresql_by_default(), test_environmental_postgresql_selection_requires_database_url(), test_evaluation_postgresql_selection_requires_database_url() (+5 more)

### Community 6 - "test_decision_support.py"
Cohesion: 0.12
Nodes (40): FinalizedCommonSupportStatus, FinalizedComparableCrop, ComparableCropEvidence, A provider-produced crop mean and rank over common valid support., _common_support(), _decision_evidence(), _DefaultPolicyProvider, _domain_common_support() (+32 more)

### Community 7 - "DomainValidationError"
Cohesion: 0.14
Nodes (19): _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing, MultiPolygonCoordinates, PolygonCoordinates (+11 more)

### Community 8 - "DomainValidationError"
Cohesion: 0.11
Nodes (26): _is_finite_number(), datetime, Immutable environmental input snapshots owned by Agroclimatic Evaluation., _validate_aware_datetime(), _validate_crs(), _validate_positive_number(), _validate_text(), DomainValidationError (+18 more)

### Community 9 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.13
Nodes (38): Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records., CropOutcomeRecord, EvaluationCommonSupportRecord, EvaluationComparableCropRecord, EvaluationCropRecord (+30 more)

### Community 10 - "PostgreSQLEvaluationRepository"
Cohesion: 0.15
Nodes (49): PostgreSQLEvaluationRepository, SessionFactory, Durable adapter for immutable Evaluation aggregates., clean_evaluations(), _common_support(), _comparable_crops(), database(), _database_url() (+41 more)

### Community 11 - "EnvironmentalInformationService"
Cohesion: 0.08
Nodes (48): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort, GetDataset (+40 more)

### Community 12 - "DecisionSupportWorkflow"
Cohesion: 0.17
Nodes (12): EvaluateConfiguredDecisionSupport, StrEnum, Decision Support application query messages., How the viability policy configuration is selected for one execution., Select either VIA's current default policy or an explicit custom snapshot., Evaluate Decision Support using a selected viability-policy configuration., ViabilityPolicySelection, ViabilityPolicySelectionMode (+4 more)

### Community 13 - "decision_support/domain/models.py"
Cohesion: 0.08
Nodes (38): DecisionSupportResult, Decision Support evidence translation and policy coordination., Prepared evidence plus an optional externally supplied policy evaluation., _translate_common_support(), _translate_evidence(), ConfiguredDecisionSupportResult, Configured Decision Support policy-selection workflow., Decision Support result together with the policy selection actually used. (+30 more)

### Community 14 - "cropsuite_adapter.py"
Cohesion: 0.07
Nodes (83): EngineRunner, CropExecutionStatus, CropSuitabilityExecutionError, CropSuitabilityRequest, CropSuitabilityResult, ICropSuitabilityEngine, IEnvironmentalInputIntegrityVerifier, InvalidEngineOutputError (+75 more)

### Community 15 - "DomainValidationError"
Cohesion: 0.09
Nodes (33): DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+25 more)

### Community 16 - "PolicyReference"
Cohesion: 0.11
Nodes (32): DefaultViabilityPolicyConflictError, InvalidViabilityPolicyRevisionError, LookupError, RuntimeError, ValueError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist., Raised when a requested viability-policy revision is not a new version. (+24 more)

### Community 17 - "FarmManagementService"
Cohesion: 0.08
Nodes (52): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+44 more)

### Community 18 - "test_decision_support_postgresql.py"
Cohesion: 0.21
Nodes (26): Decision Support infrastructure adapters., PostgreSQLViabilityPolicyRepository, Durable adapter for immutable viability-policy versions., clean_policy_versions(), database(), _database_url(), Engine, fixture (+18 more)

### Community 19 - "Evaluation"
Cohesion: 0.07
Nodes (17): EvaluationConflictError, InvalidEvaluationTransitionError, RuntimeError, Raised when an Evaluation lifecycle transition is not allowed., Raised when an evaluation identity already exists., Evaluation, An immutable multicrop evaluation and its scientific outcomes., EvaluationRepository (+9 more)

### Community 20 - "ViabilityPolicySnapshot"
Cohesion: 0.09
Nodes (23): DefaultViabilityPolicyNotConfiguredError, Raised when VIA has no default viability policy configured., PolicyVersionConflictError, RuntimeError, Raised when one immutable policy reference is bound to different thresholds., Immutable identity and exact thresholds used for a policy execution., ViabilityPolicySnapshot, Base (+15 more)

### Community 21 - "require_test_database_url"
Cohesion: 0.19
Nodes (16): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., Read and validate the test-only database settings before any DB operation., require_test_database_url(), UnsafeTestDatabaseError, validate_test_database_url() (+8 more)

### Community 22 - "DatasetVersion"
Cohesion: 0.09
Nodes (31): DatasetVersion, Immutable reproducibility metadata for one dataset release., Positive horizontal and vertical source-cell resolution., A rectangular extent expressed in the dataset version's CRS., SpatialExtent, SpatialResolution, Base, DeclarativeBase (+23 more)

### Community 23 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.20
Nodes (28): _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any, FastAPI (+20 more)

### Community 24 - "Parcel"
Cohesion: 0.12
Nodes (26): Parcel, A named parcel whose geometry changes only by appending versions., Base, DeclarativeBase, SQLAlchemy metadata owned by Farm Management Infrastructure., Declarative base for Farm Management persistence records., Farm Management infrastructure layer., ParcelRecord (+18 more)

### Community 25 - "scientific_artifact_store.py"
Cohesion: 0.14
Nodes (20): PurePosixPath, _file_identity(), _is_within(), PublishedScientificArtifact, Path, Protocol, RuntimeError, Durable filesystem storage for scientific artifacts. (+12 more)

### Community 26 - "main.py"
Cohesion: 0.10
Nodes (23): InvalidSpatialInputError, CoverageComputation, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError (+15 more)

### Community 27 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.23
Nodes (14): Agroclimatic Evaluation application layer., _availability(), CommonSupportReadResult, ComparableCropReadResult, CropEvidenceResult, EvaluationEvidenceResult, EvaluationReadResult, EvaluationResultAvailability (+6 more)

### Community 28 - "CoverageMeasurement"
Cohesion: 0.16
Nodes (21): CheckDatasetVersionCoverage, CoverageClassification, CoverageMeasurement, StrEnum, Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port., _multi_polygon(), _polygon() (+13 more)

### Community 29 - "EvaluationResult"
Cohesion: 0.12
Nodes (16): Exception, EvaluationResult, ParcelSnapshotResult, InvalidCommandError, LookupError, RuntimeError, ValueError, Raised when a requested evaluation does not exist. (+8 more)

### Community 30 - "ComparableCrop"
Cohesion: 0.22
Nodes (17): _to_comparable_crop(), ComparableCrop, One crop ranked on the exact common valid spatial support., _comparable_support(), _manifest(), parametrize, Domain tests for durable comparable crop results., _reference() (+9 more)

### Community 31 - "main"
Cohesion: 0.12
Nodes (15): FrameType, main(), make_shutdown_handler(), Logger, Return a signal handler that only requests cooperative process shutdown., CaptureFixture, MonkeyPatch, Fast tests for the VIA worker process host and operator CLI. (+7 more)

### Community 32 - "Project"
Cohesion: 0.12
Nodes (12): datetime, Project, An agricultural project that groups parcels., ParcelRepository, ProjectRepository, Protocol, UUID, Repository abstractions for Farm Management aggregates. (+4 more)

### Community 33 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.19
Nodes (20): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+12 more)

### Community 34 - "test_architecture.py"
Cohesion: 0.15
Nodes (16): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+8 more)

### Community 35 - "create_router"
Cohesion: 0.18
Nodes (18): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Commands expressing Agroclimatic Evaluation use-case intent., Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, ListEvaluations, create_router(), get_evaluation() (+10 more)

### Community 36 - "agroclimatic_evaluation/interfaces/http.py"
Cohesion: 0.16
Nodes (20): CommonSupportResponse, ComparableCropResponse, CropEvidenceResponse, CropOutcomeResponse, EnvironmentalInputReferenceBody, EvaluationEvidenceResponse, EvaluationResponse, EvaluationResultResponse (+12 more)

### Community 37 - "test_environmental_information_coverage_postgresql.py"
Cohesion: 0.27
Nodes (14): clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine, fixture, parametrize (+6 more)

### Community 38 - "test_farm_management_postgresql.py"
Cohesion: 0.28
Nodes (19): clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel(), _polygon(), _project(), datetime (+11 more)

### Community 39 - "Dataset"
Cohesion: 0.09
Nodes (20): DatasetVersionConflictError, RuntimeError, Domain errors raised by Environmental Information invariants., Raised when a dataset version identifier has already been registered., Environmental Information domain layer., Dataset, Environmental Information domain model., Stable logical identity for a geoenvironmental dataset. (+12 more)

### Community 40 - "agroclimatic_evaluation/application/service.py"
Cohesion: 0.18
Nodes (14): FinalizedCommonSupport, FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedEvaluationResult, FinalizedEvaluationResultReader, FinalizedScientificTrace, FinalizedSuitabilitySummary, GetFinalizedEvaluationResult (+6 more)

### Community 41 - "agroclimatic_evaluation/application/ports.py"
Cohesion: 0.09
Nodes (22): CropComparisonEngineError, CropComparisonInput, CropComparisonRequest, CropSuitabilityEngineError, ICropComparisonEngine, RuntimeError, StrEnum, Application-owned boundary for one crop suitability evaluation. (+14 more)

### Community 42 - "create_database"
Cohesion: 0.19
Nodes (17): create_database(), Engine, SessionFactory, Create the shared engine and short-lived session factory., Shared technical infrastructure used by the application composition root., clean_environmental_information(), database(), _database_url() (+9 more)

### Community 43 - "AgroclimaticEvaluationService"
Cohesion: 0.22
Nodes (10): GetEvaluation, GetEvaluationEvidence, GetEvaluationResult, Queries supported by Agroclimatic Evaluation., EvaluationStatusResult, AgroclimaticEvaluationService, datetime, UUID (+2 more)

### Community 44 - "EvaluationStatus"
Cohesion: 0.21
Nodes (16): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Logger, Explicit fail-only recovery for abandoned evaluation executions., Mark an operator-confirmed active orphan as failed without retrying it., EvaluationStatus, StrEnum (+8 more)

### Community 45 - "test_agroclimatic_evaluation_queries.py"
Cohesion: 0.52
Nodes (6): _evaluation(), parametrize, Focused Application query tests for Agroclimatic Evaluation., _service(), test_finalized_public_contract_preserves_order_and_outcome_semantics(), test_public_contract_rejects_non_succeeded_evaluation()

### Community 46 - "cropsuite_comparison_adapter.py"
Cohesion: 0.20
Nodes (22): CommonSupportStatus, CommonSupportResult, CommonSupportStatus, ComparableCropResult, CropComparisonResult, InvalidComparisonOutputError, Scientific common-support outcome across evaluated crops., Scientific support shared by all usable crop suitability rasters. (+14 more)

### Community 47 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 48 - "via_backend/worker.py"
Cohesion: 0.20
Nodes (11): ArgumentParser, ActiveEvaluationResult, list_active_evaluations(), _parser(), _positive_integer(), _print_active_evaluations(), UUID, Separate PostgreSQL polling-worker process and operator recovery CLI. (+3 more)

### Community 49 - "WorkerSettings"
Cohesion: 0.19
Nodes (10): _environment_float(), _environment_integer(), _optional_path(), Path, Environment-backed configuration for the VIA application host., Settings for the PostgreSQL polling worker process., WorkerSettings, test_worker_run_requires_durable_artifact_root() (+2 more)

### Community 50 - "InMemoryParcelRepository"
Cohesion: 0.19
Nodes (7): ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved., InMemoryParcelRepository, UUID, In-memory Farm Management repository adapters., Process-local parcel storage that retains every geometry version.

### Community 51 - "environmental_information/interfaces/http.py"
Cohesion: 0.22
Nodes (13): CheckCoverageBody, CoverageGeometryBody, CreateDatasetBody, CreateDatasetVersionBody, DatasetResponse, DatasetVersionCoverageResponse, DatasetVersionResponse, BaseModel (+5 more)

### Community 52 - "CropComparisonExecutionError"
Cohesion: 0.36
Nodes (5): ComparisonRunner, CropComparisonExecutionError, Raised when scientific common-support comparison cannot execute., _is_within(), Path

### Community 53 - "DecisionSupportService"
Cohesion: 0.10
Nodes (17): PolicyEvaluationT, PolicyEvaluationT_co, IDecisionPolicy, IDefaultViabilityPolicyProvider, IDefaultViabilityPolicyStore, Protocol, Application ports for deterministic Decision Support policies., Evaluate comparable evidence without changing its scientific values. (+9 more)

### Community 54 - "test_scientific_artifact_store.py"
Cohesion: 0.27
Nodes (12): parametrize, Path, test_publish_creates_durable_artifact_with_opaque_reference(), test_publish_is_idempotent_for_identical_content(), test_publish_rejects_content_that_does_not_match_expected_checksum(), test_publish_rejects_different_content_for_existing_reference(), test_publish_rejects_missing_source(), test_publish_rejects_unsafe_storage_reference() (+4 more)

### Community 55 - "env.py"
Cohesion: 0.47
Nodes (5): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online()

### Community 56 - "run_forever"
Cohesion: 0.21
Nodes (8): Event, WorkerRunSummary, Poll until cooperative shutdown, waiting only after a non-full batch., run_forever(), test_run_forever_does_not_poll_again_after_stop_is_requested(), run_once(), test_run_forever_poll_wait_can_be_interrupted_by_stop(), run_once()

### Community 57 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 58 - "CommonSupport"
Cohesion: 0.32
Nodes (4): CommonSupport, Validate deterministic scientific ranking semantics., Spatial support shared by the usable crop suitability rasters., validate_comparable_crops()

### Community 73 - "test_explicit_recovery_uses_expected_status"
Cohesion: 0.32
Nodes (7): _manifest(), Exception, test_concurrent_recovery_reports_conflict_without_overwrite(), save(), test_explicit_recovery_uses_expected_status(), __init__(), save()

### Community 90 - "create_worker"
Cohesion: 0.33
Nodes (5): create_worker(), Compose the production worker and fail fast on missing scientific settings., WorkerRuntime, Path, test_create_worker_fails_fast_on_invalid_scientific_input_bindings()

### Community 91 - "health.py"
Cohesion: 0.40
Nodes (4): get, health(), Host-level health endpoint., Report that the API process is ready to receive requests.

## Knowledge Gaps
- **1 isolated node(s):** `via-backend`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 490 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `main.py` to `Project`, `InMemoryEvaluationRepository`, `create_router`, `Settings`, `Dataset`, `PostgreSQLEvaluationRepository`, `AgroclimaticEvaluationService`, `EnvironmentalInformationService`, `create_database`, `test_environmental_information_api.py`, `FarmManagementService`, `InMemoryParcelRepository`, `DatasetVersion`, `test_agroclimatic_evaluation_api.py`, `Parcel`, `test_farm_management_api.py`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `AgroclimaticEvaluationService` connect `AgroclimaticEvaluationService` to `AgroclimaticEvaluationExecutionService`, `create_router`, `agroclimatic_evaluation/interfaces/http.py`, `test_decision_support.py`, `agroclimatic_evaluation/application/service.py`, `DomainValidationError`, `agroclimatic_evaluation/application/ports.py`, `EvaluationStatus`, `test_agroclimatic_evaluation_queries.py`, `Evaluation`, `test_agroclimatic_evaluation_api.py`, `main.py`, `agroclimatic_evaluation/application/__init__.py`, `EvaluationResult`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `AgroclimaticEvaluationExecutionService`, `create_worker`, `test_environmental_information_coverage_postgresql.py`, `DomainValidationError`, `Dataset`, `via_backend/worker.py`, `environmental_information/interfaces/http.py`, `DatasetVersion`, `main.py`, `CoverageMeasurement`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `PostgreSQLEvaluationRepository` (e.g. with `EvaluationConflictError` and `Evaluation`) actually correct?**
  _`PostgreSQLEvaluationRepository` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `EvaluationStatus` (e.g. with `RecoverEvaluation` and `AgroclimaticEvaluationExecutionService`) actually correct?**
  _`EvaluationStatus` has 18 INFERRED edges - model-reasoned connections that need verification._