# Graph Report - backend  (2026-09-16)

## Corpus Check
- 156 files · ~51,097 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1875 nodes · 5633 edges · 91 communities (58 shown, 19 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 791 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4818fcc4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AgroclimaticEvaluationExecutionService
- EnvironmentalInputManifest
- InMemoryEvaluationRepository
- cropsuite_adapter.py
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- Settings
- test_decision_support.py
- DomainValidationError
- DomainValidationError
- FarmManagementService
- PostgreSQLEvaluationRepository
- EnvironmentalInformationService
- decision_support/application/service.py
- decision_support/domain/models.py
- test_cropsuite_adapter.py
- DomainValidationError
- PolicyReference
- farm_management/application/service.py
- test_decision_support_postgresql.py
- Evaluation
- decision_support/infrastructure/postgresql_repositories.py
- test_environmental_information_postgresql.py
- DatasetVersion
- test_agroclimatic_evaluation_api.py
- Parcel
- FilesystemScientificArtifactStore
- create_app
- EvaluationConflictError
- CoverageMeasurement
- EvaluationStatus
- ComparableCrop
- main
- Project
- test_agroclimatic_evaluation_domain.py
- test_architecture.py
- ScientificArtifactStore
- agroclimatic_evaluation/interfaces/http.py
- ._resolve_environmental_inputs
- test_farm_management_postgresql.py
- Dataset
- test_crop_comparison_contracts.py
- agroclimatic_evaluation/application/__init__.py
- AgroclimaticEvaluationService
- agroclimatic_evaluation/application/service.py
- SpatialCoveragePort
- test_agroclimatic_evaluation_queries.py
- cropsuite_comparison_adapter.py
- test_environmental_information_api.py
- via_backend/worker.py
- WorkerSettings
- SpatialExtent
- AgroclimaticEvaluationRecoveryService
- CropComparisonExecutionError
- read_models.py
- GetPublishedDatasetVersion
- CropSuitabilityRequest
- verify_runtime
- test_farm_management_api.py
- .add_outcome
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
- `_test_app()` --uses--> `Settings`  [INFERRED]
  tests/test_agroclimatic_evaluation_api.py → src/via_backend/config.py
- `_test_app()` --uses--> `Settings`  [INFERRED]
  tests/test_environmental_information_api.py → src/via_backend/config.py
- `_test_app()` --uses--> `Settings`  [INFERRED]
  tests/test_farm_management_api.py → src/via_backend/config.py
- `test_create_worker_fails_fast_on_invalid_scientific_input_bindings()` --uses--> `WorkerSettings`  [INFERRED]
  tests/test_agroclimatic_evaluation_worker.py → src/via_backend/config.py

## Import Cycles
- None detected.

## Communities (91 total, 19 thin omitted)

### Community 0 - "AgroclimaticEvaluationExecutionService"
Cohesion: 0.15
Nodes (37): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, Exception, Execute requested crops and summarize them through Application-owned ports., EnvironmentalInputReference, Caller-selected exact environmental dataset version., _artifact() (+29 more)

### Community 1 - "EnvironmentalInputManifest"
Cohesion: 0.06
Nodes (66): EnvironmentalInputManifest, EnvironmentalInputSnapshot, Immutable set of exact environmental inputs resolved for an evaluation., Historical environmental input metadata captured for one evaluation input., ConfiguredEnvironmentalInputIntegrityVerifier, CropSuiteEnvironmentalInputBinding, load_configured_environmental_input_integrity_verifier(), load_cropsuite_environmental_input_bindings() (+58 more)

### Community 2 - "InMemoryEvaluationRepository"
Cohesion: 0.15
Nodes (29): AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application., InMemoryEvaluationRepository, _artifact(), _engine_result(), _evaluation(), _executor(), FakeComparisonEngine (+21 more)

### Community 3 - "cropsuite_adapter.py"
Cohesion: 0.21
Nodes (28): InvalidEngineOutputError, Raised when the engine report does not satisfy the expected PoC contract., Opaque scientific source identity and its engine-reported SHA-256., Current PoC parcel summary for the crop-suitability output., An engine-reported failure, distinct from no coverage and a zero score., ScientificExecutionFailure, ScientificSourceFingerprint, SuitabilityScoreSummary (+20 more)

### Community 4 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.10
Nodes (32): CommonSupport, CommonSupportStatus, StrEnum, Evaluation-level scientific common-support result., Validate deterministic scientific ranking semantics., Spatial support shared by the usable crop suitability rasters., validate_comparable_crops(), Domain errors for Agroclimatic Evaluation. (+24 more)

### Community 5 - "Settings"
Cohesion: 0.14
Nodes (17): Settings needed by the current backend composition root., Require the durable persistence contract used by the production API., Settings, MonkeyPatch, parametrize, Tests for environment-driven application composition settings., test_create_production_app_validates_before_composition(), test_database_url_selects_postgresql_by_default() (+9 more)

### Community 6 - "test_decision_support.py"
Cohesion: 0.10
Nodes (47): FinalizedCommonSupportStatus, FinalizedComparableCrop, FinalizedEvaluationResult, GetFinalizedEvaluationResult, Select either VIA's current default policy or an explicit custom snapshot., ViabilityPolicySelection, ComparableCropEvidence, A provider-produced crop mean and rank over common valid support. (+39 more)

### Community 7 - "DomainValidationError"
Cohesion: 0.09
Nodes (39): InvalidSpatialInputError, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, CoverageCompatibilityFailure (+31 more)

### Community 8 - "DomainValidationError"
Cohesion: 0.09
Nodes (31): _is_finite_number(), datetime, Immutable environmental input snapshots owned by Agroclimatic Evaluation., _validate_aware_datetime(), _validate_crs(), _validate_positive_number(), _validate_text(), DomainValidationError (+23 more)

### Community 9 - "FarmManagementService"
Cohesion: 0.17
Nodes (11): ParcelResult, ParcelVersionResult, ProjectResult, Transport-neutral results returned by Farm Management use cases., FarmManagementService, InvalidCommandError, datetime, UUID (+3 more)

### Community 10 - "PostgreSQLEvaluationRepository"
Cohesion: 0.14
Nodes (49): PostgreSQLEvaluationRepository, SessionFactory, Durable adapter for immutable Evaluation aggregates., clean_evaluations(), _common_support(), _comparable_crops(), database(), _database_url() (+41 more)

### Community 11 - "EnvironmentalInformationService"
Cohesion: 0.07
Nodes (58): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., PublishedDatasetVersion, Stable contracts deliberately published to other bounded contexts., GetDataset, GetDatasetVersion (+50 more)

### Community 12 - "decision_support/application/service.py"
Cohesion: 0.08
Nodes (37): PolicyEvaluationT, FinalizedEvaluationResultReader, Protocol, Public local interface for a future Decision Support consumer., Decision Support application layer., IDecisionPolicy, Evaluate comparable evidence without changing its scientific values., EvaluateConfiguredDecisionSupport (+29 more)

### Community 13 - "decision_support/domain/models.py"
Cohesion: 0.11
Nodes (26): PolicyEvaluationT_co, DomainValidationError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Decision Support domain layer., CropViabilityAssessment, DecisionEvidence (+18 more)

### Community 14 - "test_cropsuite_adapter.py"
Cohesion: 0.18
Nodes (37): CropExecutionStatus, Scientific outcomes reported independently of Evaluation lifecycle state., CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability., _adapter(), _environmental_input_manifest(), _integrity_verifier(), Any (+29 more)

### Community 15 - "DomainValidationError"
Cohesion: 0.09
Nodes (33): DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+25 more)

### Community 16 - "PolicyReference"
Cohesion: 0.08
Nodes (30): InvalidViabilityPolicyRevisionError, ValueError, Raised when a requested viability-policy revision is not a new version., Application lifecycle for immutable Decision Support viability policies., Register one explicitly identified immutable viability-policy version., Create a new immutable version derived from an existing policy identity., Coordinate registration and revision of immutable policy snapshots., RegisterViabilityPolicyVersion (+22 more)

### Community 17 - "farm_management/application/service.py"
Cohesion: 0.10
Nodes (42): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+34 more)

### Community 18 - "test_decision_support_postgresql.py"
Cohesion: 0.17
Nodes (31): Decision Support infrastructure adapters., PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+23 more)

### Community 19 - "Evaluation"
Cohesion: 0.09
Nodes (11): InvalidEvaluationTransitionError, Raised when an Evaluation lifecycle transition is not allowed., Evaluation, An immutable multicrop evaluation and its scientific outcomes., EvaluationRepository, Protocol, UUID, In-memory Agroclimatic Evaluation repository adapter. (+3 more)

### Community 20 - "decision_support/infrastructure/postgresql_repositories.py"
Cohesion: 0.09
Nodes (22): DefaultViabilityPolicyConflictError, DefaultViabilityPolicyNotConfiguredError, LookupError, RuntimeError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist., Raised when VIA has no default viability policy configured., Raised when the default policy changed before an expected update. (+14 more)

### Community 21 - "test_environmental_information_postgresql.py"
Cohesion: 0.12
Nodes (28): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., Read and validate the test-only database settings before any DB operation., require_test_database_url(), UnsafeTestDatabaseError, validate_test_database_url() (+20 more)

### Community 22 - "DatasetVersion"
Cohesion: 0.08
Nodes (32): DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., DatasetVersion, Immutable reproducibility metadata for one dataset release., Base, DeclarativeBase, SQLAlchemy metadata owned by Environmental Information Infrastructure. (+24 more)

### Community 23 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.20
Nodes (28): _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any, FastAPI (+20 more)

### Community 24 - "Parcel"
Cohesion: 0.08
Nodes (35): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online(), ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved. (+27 more)

### Community 25 - "FilesystemScientificArtifactStore"
Cohesion: 0.07
Nodes (56): PurePosixPath, CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., Agroclimatic Evaluation infrastructure layer., _file_identity(), FilesystemScientificArtifactStore, _is_within(), PublishedScientificArtifact (+48 more)

### Community 26 - "create_app"
Cohesion: 0.40
Nodes (5): create_app(), create_production_app(), FastAPI, Build the production API after enforcing durable persistence settings., Build the VIA API and register its technical interfaces.

### Community 27 - "EvaluationConflictError"
Cohesion: 0.10
Nodes (36): EvaluationConflictError, RuntimeError, Raised when an evaluation identity already exists., Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records., CropOutcomeRecord (+28 more)

### Community 28 - "CoverageMeasurement"
Cohesion: 0.15
Nodes (22): CheckDatasetVersionCoverage, CoverageClassification, CoverageMeasurement, StrEnum, Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port., Environmental Information interface layer., _multi_polygon() (+14 more)

### Community 29 - "EvaluationStatus"
Cohesion: 0.09
Nodes (23): Commands expressing Agroclimatic Evaluation use-case intent., Explicit fail-only recovery for abandoned evaluation executions., CropOutcomeResult, EvaluationResult, ParcelSnapshotResult, Transport-neutral Agroclimatic Evaluation results., InvalidCommandError, LookupError (+15 more)

### Community 30 - "ComparableCrop"
Cohesion: 0.24
Nodes (17): ComparableCrop, One crop ranked on the exact common valid spatial support., _comparable_support(), _manifest(), _outcome(), parametrize, Domain tests for durable comparable crop results., _reference() (+9 more)

### Community 31 - "main"
Cohesion: 0.08
Nodes (23): Event, FrameType, WorkerRunSummary, main(), make_shutdown_handler(), Logger, Poll until cooperative shutdown, waiting only after a non-full batch., Return a signal handler that only requests cooperative process shutdown. (+15 more)

### Community 32 - "Project"
Cohesion: 0.13
Nodes (10): Project, An agricultural project that groups parcels., ParcelRepository, ProjectRepository, Protocol, UUID, Repository abstractions for Farm Management aggregates., _project_from_record() (+2 more)

### Community 33 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.19
Nodes (20): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+12 more)

### Community 34 - "test_architecture.py"
Cohesion: 0.15
Nodes (16): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+8 more)

### Community 35 - "ScientificArtifactStore"
Cohesion: 0.24
Nodes (8): EngineRunner, CropSuitabilityExecutionError, Raised when the existing engine service cannot produce a report., _is_within(), Path, Protocol, Publish immutable scientific files behind opaque logical references., ScientificArtifactStore

### Community 36 - "agroclimatic_evaluation/interfaces/http.py"
Cohesion: 0.16
Nodes (20): CommonSupportResponse, ComparableCropResponse, CropEvidenceResponse, CropOutcomeResponse, EnvironmentalInputReferenceBody, EvaluationEvidenceResponse, EvaluationResponse, EvaluationResultResponse (+12 more)

### Community 37 - "._resolve_environmental_inputs"
Cohesion: 0.50
Nodes (3): EnvironmentalInputResolutionError, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved.

### Community 38 - "test_farm_management_postgresql.py"
Cohesion: 0.21
Nodes (22): PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel() (+14 more)

### Community 39 - "Dataset"
Cohesion: 0.14
Nodes (10): datetime, Dataset, Stable logical identity for a geoenvironmental dataset., DatasetRepository, DatasetVersionRepository, Protocol, UUID, Repository abstractions for Environmental Information aggregates. (+2 more)

### Community 41 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.10
Nodes (33): _comparison_request(), Synchronous application orchestration for persisted evaluations., _to_common_support(), _to_comparable_crop(), _to_outcome(), Agroclimatic Evaluation application layer., CommonSupportResult, ComparableCropResult (+25 more)

### Community 42 - "AgroclimaticEvaluationService"
Cohesion: 0.16
Nodes (23): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, GetEvaluation, GetEvaluationEvidence, GetEvaluationResult, ListEvaluations (+15 more)

### Community 43 - "agroclimatic_evaluation/application/service.py"
Cohesion: 0.19
Nodes (12): FinalizedCommonSupport, FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedScientificTrace, FinalizedSuitabilitySummary, StrEnum, Stable contracts deliberately published to other bounded contexts., EvaluationStatusResult (+4 more)

### Community 44 - "SpatialCoveragePort"
Cohesion: 0.40
Nodes (4): CoverageComputation, Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort

### Community 45 - "test_agroclimatic_evaluation_queries.py"
Cohesion: 0.44
Nodes (8): _evaluation(), _outcome(), parametrize, Focused Application query tests for Agroclimatic Evaluation., _service(), test_finalized_public_contract_preserves_order_and_outcome_semantics(), test_public_contract_rejects_non_succeeded_evaluation(), test_query_messages_return_read_only_views_without_mutation()

### Community 46 - "cropsuite_comparison_adapter.py"
Cohesion: 0.30
Nodes (17): CommonSupportStatus, CommonSupportStatus, InvalidComparisonOutputError, StrEnum, Scientific common-support outcome across evaluated crops., Raised when scientific comparison returns an invalid contract., _fraction(), _map_comparable_crops() (+9 more)

### Community 47 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 48 - "via_backend/worker.py"
Cohesion: 0.14
Nodes (16): ArgumentParser, ActiveEvaluationResult, create_database(), Engine, SessionFactory, Create the shared engine and short-lived session factory., Shared technical infrastructure used by the application composition root., list_active_evaluations() (+8 more)

### Community 49 - "WorkerSettings"
Cohesion: 0.18
Nodes (11): _environment_float(), _environment_integer(), _optional_path(), Path, Environment-backed configuration for the VIA application host., Settings for the PostgreSQL polling worker process., WorkerSettings, test_worker_run_requires_durable_artifact_root() (+3 more)

### Community 50 - "SpatialExtent"
Cohesion: 0.13
Nodes (23): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine (+15 more)

### Community 51 - "AgroclimaticEvaluationRecoveryService"
Cohesion: 0.17
Nodes (19): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Logger, Mark an operator-confirmed active orphan as failed without retrying it., _evaluation_in_status(), _manifest(), Exception (+11 more)

### Community 52 - "CropComparisonExecutionError"
Cohesion: 0.24
Nodes (8): ComparisonRunner, CropComparisonEngineError, CropComparisonExecutionError, RuntimeError, Base error for the scientific crop-comparison boundary., Raised when scientific common-support comparison cannot execute., _is_within(), Path

### Community 53 - "read_models.py"
Cohesion: 0.16
Nodes (16): _availability(), CommonSupportReadResult, ComparableCropReadResult, CropEvidenceResult, EvaluationEvidenceResult, EvaluationReadResult, EvaluationResultAvailability, PersistedCropOutcomeResult (+8 more)

### Community 54 - "GetPublishedDatasetVersion"
Cohesion: 0.25
Nodes (17): GetPublishedDatasetVersion, PublishedDatasetVersionReader, Protocol, Public cross-context reader for exact immutable dataset versions., _dataset(), datetime, UUID, Public cross-context contract tests for Environmental Information. (+9 more)

### Community 55 - "CropSuitabilityRequest"
Cohesion: 0.16
Nodes (10): datetime, CropSuitabilityRequest, CropSuitabilityResult, ICropSuitabilityEngine, IEnvironmentalInputIntegrityVerifier, Protocol, One checked per-crop outcome from the scientific boundary., Verify resolved environmental provenance against scientific source fingerprints. (+2 more)

### Community 56 - "verify_runtime"
Cohesion: 0.39
Nodes (7): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_writable_directory(), _run_pip_check(), verify_runtime()

### Community 57 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 73 - "health.py"
Cohesion: 0.40
Nodes (4): get, health(), Host-level health endpoint., Report that the API process is ready to receive requests.

## Knowledge Gaps
- **1 isolated node(s):** `via-backend`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 498 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `Dataset`, `DomainValidationError`, `SpatialCoveragePort`, `via_backend/worker.py`, `SpatialExtent`, `GetPublishedDatasetVersion`, `DatasetVersion`, `FilesystemScientificArtifactStore`, `create_app`, `CoverageMeasurement`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `Project`, `InMemoryEvaluationRepository`, `Settings`, `test_farm_management_postgresql.py`, `Dataset`, `FarmManagementService`, `AgroclimaticEvaluationService`, `EnvironmentalInformationService`, `PostgreSQLEvaluationRepository`, `test_environmental_information_api.py`, `via_backend/worker.py`, `farm_management/application/service.py`, `DatasetVersion`, `test_agroclimatic_evaluation_api.py`, `Parcel`, `test_farm_management_api.py`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `AgroclimaticEvaluationService` connect `AgroclimaticEvaluationService` to `AgroclimaticEvaluationExecutionService`, `agroclimatic_evaluation/interfaces/http.py`, `test_decision_support.py`, `DomainValidationError`, `agroclimatic_evaluation/application/__init__.py`, `agroclimatic_evaluation/application/service.py`, `test_agroclimatic_evaluation_queries.py`, `Evaluation`, `read_models.py`, `DatasetVersion`, `test_agroclimatic_evaluation_api.py`, `create_app`, `EvaluationConflictError`, `EvaluationStatus`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `PostgreSQLEvaluationRepository` (e.g. with `EvaluationConflictError` and `Evaluation`) actually correct?**
  _`PostgreSQLEvaluationRepository` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `EvaluationStatus` (e.g. with `RecoverEvaluation` and `AgroclimaticEvaluationExecutionService`) actually correct?**
  _`EvaluationStatus` has 18 INFERRED edges - model-reasoned connections that need verification._