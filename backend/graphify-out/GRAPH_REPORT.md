# Graph Report - backend  (2026-09-16)

## Corpus Check
- 154 files · ~50,621 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1863 nodes · 5619 edges · 85 communities (55 shown, 16 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 791 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e081eb56`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AgroclimaticEvaluationExecutionService
- EnvironmentalInputManifest
- InMemoryEvaluationRepository
- cropsuite_adapter.py
- agroclimatic_evaluation/domain/__init__.py
- Settings
- test_decision_support.py
- DomainValidationError
- DomainValidationError
- FarmManagementService
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- EnvironmentalInformationService
- workflow.py
- decision_support/domain/models.py
- test_cropsuite_adapter.py
- DomainValidationError
- PolicyReference
- farm_management/application/service.py
- test_decision_support_postgresql.py
- Evaluation
- PostgreSQLDefaultViabilityPolicyStore
- test_environmental_information_coverage_postgresql.py
- DatasetVersion
- test_agroclimatic_evaluation_api.py
- Parcel
- FilesystemScientificArtifactStore
- main.py
- InMemoryDatasetVersionRepository
- CoverageMeasurement
- recovery.py
- ComparableCrop
- main
- Project
- test_agroclimatic_evaluation_domain.py
- test_architecture.py
- ScientificArtifactStore
- EvaluationStatus
- .execute_evaluation
- test_farm_management_postgresql.py
- Dataset
- CommonSupportResult
- agroclimatic_evaluation/application/__init__.py
- test_environmental_information_postgresql.py
- agroclimatic_evaluation/application/service.py
- CoverageGeometry
- test_agroclimatic_evaluation_queries.py
- cropsuite_comparison_adapter.py
- test_environmental_information_api.py
- via_backend/worker.py
- WorkerSettings
- test_environmental_information_domain.py
- environmental_information/interfaces/http.py
- CropComparisonExecutionError
- test_run_forever_poll_wait_can_be_interrupted_by_stop
- test_farm_management_api.py
- test_health.py
- __main__.py
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
- `test_extent_must_be_ordered()` --calls--> `SpatialExtent`  [INFERRED]
  tests/test_environmental_information_domain.py → src/via_backend/contexts/environmental_information/domain/spatial.py
- `_test_app()` --uses--> `Settings`  [INFERRED]
  tests/test_agroclimatic_evaluation_api.py → src/via_backend/config.py
- `_test_app()` --uses--> `Settings`  [INFERRED]
  tests/test_environmental_information_api.py → src/via_backend/config.py
- `_test_app()` --uses--> `Settings`  [INFERRED]
  tests/test_farm_management_api.py → src/via_backend/config.py

## Import Cycles
- None detected.

## Communities (85 total, 16 thin omitted)

### Community 0 - "AgroclimaticEvaluationExecutionService"
Cohesion: 0.09
Nodes (57): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, Exception, Execute requested crops and summarize them through Application-owned ports., EnvironmentalInputReference, Caller-selected exact environmental dataset version., GetPublishedDatasetVersion (+49 more)

### Community 1 - "EnvironmentalInputManifest"
Cohesion: 0.05
Nodes (71): EnvironmentalInputManifest, EnvironmentalInputSnapshot, _is_finite_number(), datetime, Immutable environmental input snapshots owned by Agroclimatic Evaluation., Immutable set of exact environmental inputs resolved for an evaluation., Historical environmental input metadata captured for one evaluation input., _validate_aware_datetime() (+63 more)

### Community 2 - "InMemoryEvaluationRepository"
Cohesion: 0.08
Nodes (52): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Logger, Mark an operator-confirmed active orphan as failed without retrying it., AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application., InMemoryEvaluationRepository (+44 more)

### Community 3 - "cropsuite_adapter.py"
Cohesion: 0.21
Nodes (28): InvalidEngineOutputError, Raised when the engine report does not satisfy the expected PoC contract., Opaque scientific source identity and its engine-reported SHA-256., Current PoC parcel summary for the crop-suitability output., An engine-reported failure, distinct from no coverage and a zero score., ScientificExecutionFailure, ScientificSourceFingerprint, SuitabilityScoreSummary (+20 more)

### Community 4 - "agroclimatic_evaluation/domain/__init__.py"
Cohesion: 0.11
Nodes (24): CommonSupportReadResult, ComparableCropReadResult, CropEvidenceResult, PersistedCropOutcomeResult, Read-only Application views for Agroclimatic Evaluation., SuitabilitySummaryResult, CommonSupportStatus, StrEnum (+16 more)

### Community 5 - "Settings"
Cohesion: 0.13
Nodes (18): Settings needed by the current backend composition root., Require the durable persistence contract used by the production API., Settings, MonkeyPatch, parametrize, Tests for environment-driven application composition settings., test_create_production_app_validates_before_composition(), test_database_url_selects_postgresql_by_default() (+10 more)

### Community 6 - "test_decision_support.py"
Cohesion: 0.11
Nodes (43): FinalizedCommonSupportStatus, FinalizedComparableCrop, FinalizedEvaluationResult, GetFinalizedEvaluationResult, ComparableCropEvidence, A provider-produced crop mean and rank over common valid support., _common_support(), _decision_evidence() (+35 more)

### Community 7 - "DomainValidationError"
Cohesion: 0.12
Nodes (25): _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing, MultiPolygonCoordinates, PolygonCoordinates (+17 more)

### Community 8 - "DomainValidationError"
Cohesion: 0.11
Nodes (23): DomainValidationError, ValueError, Raised when evaluation data violates a domain invariant., Immutable spatial grid identity for a scientific raster., ScientificArtifactGrid, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+15 more)

### Community 9 - "FarmManagementService"
Cohesion: 0.17
Nodes (11): ParcelResult, ParcelVersionResult, ProjectResult, Transport-neutral results returned by Farm Management use cases., FarmManagementService, InvalidCommandError, datetime, UUID (+3 more)

### Community 10 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.07
Nodes (93): Durable scientific evidence referenced without exposing filesystem paths., Opaque engine-reported scientific source identity and SHA-256., ScientificArtifact, ScientificSourceFingerprint, Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records. (+85 more)

### Community 11 - "EnvironmentalInformationService"
Cohesion: 0.08
Nodes (46): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Stable contracts deliberately published to other bounded contexts., GetDataset, GetDatasetVersion, ListDatasets (+38 more)

### Community 12 - "workflow.py"
Cohesion: 0.08
Nodes (29): PolicyEvaluationT, FinalizedEvaluationResultReader, Protocol, Public local interface for a future Decision Support consumer., IDefaultViabilityPolicyProvider, Provide the current VIA default viability policy without owning its storage., EvaluateConfiguredDecisionSupport, EvaluateDecisionSupport (+21 more)

### Community 13 - "decision_support/domain/models.py"
Cohesion: 0.09
Nodes (37): PolicyEvaluationT_co, Decision Support evidence translation and policy coordination., _translate_common_support(), _translate_evidence(), DomainValidationError, PolicyVersionConflictError, RuntimeError, ValueError (+29 more)

### Community 14 - "test_cropsuite_adapter.py"
Cohesion: 0.18
Nodes (37): CropExecutionStatus, Scientific outcomes reported independently of Evaluation lifecycle state., CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability., _adapter(), _environmental_input_manifest(), _integrity_verifier(), Any (+29 more)

### Community 15 - "DomainValidationError"
Cohesion: 0.09
Nodes (33): DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+25 more)

### Community 16 - "PolicyReference"
Cohesion: 0.08
Nodes (34): InvalidViabilityPolicyRevisionError, ValueError, Raised when a requested viability-policy revision is not a new version., Decision Support application layer., Application lifecycle for immutable Decision Support viability policies., Register one explicitly identified immutable viability-policy version., Create a new immutable version derived from an existing policy identity., Coordinate registration and revision of immutable policy snapshots. (+26 more)

### Community 17 - "farm_management/application/service.py"
Cohesion: 0.10
Nodes (42): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+34 more)

### Community 18 - "test_decision_support_postgresql.py"
Cohesion: 0.23
Nodes (26): PostgreSQLViabilityPolicyRepository, Durable adapter for immutable viability-policy versions., clean_policy_versions(), database(), _database_url(), Engine, fixture, SessionFactory (+18 more)

### Community 19 - "Evaluation"
Cohesion: 0.09
Nodes (15): CommonSupport, Validate deterministic scientific ranking semantics., Spatial support shared by the usable crop suitability rasters., validate_comparable_crops(), EvaluationConflictError, InvalidEvaluationTransitionError, RuntimeError, Raised when an Evaluation lifecycle transition is not allowed. (+7 more)

### Community 20 - "PostgreSQLDefaultViabilityPolicyStore"
Cohesion: 0.09
Nodes (24): DefaultViabilityPolicyConflictError, DefaultViabilityPolicyNotConfiguredError, LookupError, RuntimeError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist., Raised when VIA has no default viability policy configured., Raised when the default policy changed before an expected update. (+16 more)

### Community 21 - "test_environmental_information_coverage_postgresql.py"
Cohesion: 0.11
Nodes (30): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., Read and validate the test-only database settings before any DB operation., require_test_database_url(), UnsafeTestDatabaseError, validate_test_database_url() (+22 more)

### Community 22 - "DatasetVersion"
Cohesion: 0.08
Nodes (36): InvalidSpatialInputError, RuntimeError, ValueError, Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, DatasetVersion, Immutable reproducibility metadata for one dataset release. (+28 more)

### Community 23 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.20
Nodes (28): _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any, FastAPI (+20 more)

### Community 24 - "Parcel"
Cohesion: 0.08
Nodes (35): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online(), ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved. (+27 more)

### Community 25 - "FilesystemScientificArtifactStore"
Cohesion: 0.09
Nodes (48): PurePosixPath, CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., _file_identity(), FilesystemScientificArtifactStore, _is_within(), PublishedScientificArtifact, Path (+40 more)

### Community 26 - "main.py"
Cohesion: 0.13
Nodes (15): get, create_database(), Engine, SessionFactory, Create the shared engine and short-lived session factory., Shared technical infrastructure used by the application composition root., health(), Host-level health endpoint. (+7 more)

### Community 27 - "InMemoryDatasetVersionRepository"
Cohesion: 0.18
Nodes (8): DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., InMemoryDatasetVersionRepository, UUID, Contract-focused Environmental Information repository tests., test_duplicate_version_identifier_is_rejected(), _version()

### Community 28 - "CoverageMeasurement"
Cohesion: 0.14
Nodes (23): CheckDatasetVersionCoverage, CoverageClassification, CoverageCompatibilityFailure, CoverageMeasurement, StrEnum, Structural metadata prevented a meaningful spatial measurement., Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port. (+15 more)

### Community 29 - "recovery.py"
Cohesion: 0.13
Nodes (15): Explicit fail-only recovery for abandoned evaluation executions., CropOutcomeResult, EvaluationResult, ParcelSnapshotResult, Transport-neutral Agroclimatic Evaluation results., InvalidCommandError, RuntimeError, ValueError (+7 more)

### Community 30 - "ComparableCrop"
Cohesion: 0.24
Nodes (17): ComparableCrop, One crop ranked on the exact common valid spatial support., _comparable_support(), _manifest(), _outcome(), parametrize, Domain tests for durable comparable crop results., _reference() (+9 more)

### Community 31 - "main"
Cohesion: 0.11
Nodes (17): Event, FrameType, main(), make_shutdown_handler(), Logger, Return a signal handler that only requests cooperative process shutdown., CaptureFixture, MonkeyPatch (+9 more)

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

### Community 36 - "EvaluationStatus"
Cohesion: 0.11
Nodes (34): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Commands expressing Agroclimatic Evaluation use-case intent., Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, _availability(), EvaluationResultAvailability, StrEnum (+26 more)

### Community 37 - ".execute_evaluation"
Cohesion: 0.20
Nodes (8): EnvironmentalInputResolutionError, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved., _to_common_support(), _to_comparable_crop(), LookupError, Raised when a requested evaluation does not exist., ResourceNotFoundError

### Community 38 - "test_farm_management_postgresql.py"
Cohesion: 0.21
Nodes (22): PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel() (+14 more)

### Community 39 - "Dataset"
Cohesion: 0.15
Nodes (10): Environmental Information domain layer., Dataset, Stable logical identity for a geoenvironmental dataset., DatasetRepository, DatasetVersionRepository, Protocol, UUID, Repository abstractions for Environmental Information aggregates. (+2 more)

### Community 40 - "CommonSupportResult"
Cohesion: 0.24
Nodes (6): CommonSupportResult, CropComparisonResult, Scientific support shared by all usable crop suitability rasters., Checked multicrop comparison returned by the scientific boundary., StubComparisonEngine, test_comparison_engine_contract_is_runtime_checkable()

### Community 41 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.07
Nodes (44): _comparison_request(), datetime, Synchronous application orchestration for persisted evaluations., _to_outcome(), Agroclimatic Evaluation application layer., CropComparisonInput, CropComparisonRequest, CropSuitabilityEngineError (+36 more)

### Community 42 - "test_environmental_information_postgresql.py"
Cohesion: 0.36
Nodes (11): clean_environmental_information(), database(), _dataset(), Engine, fixture, SessionFactory, PostgreSQL/PostGIS integration tests for Environmental Information., test_dataset_and_version_survive_new_repository_instances() (+3 more)

### Community 43 - "agroclimatic_evaluation/application/service.py"
Cohesion: 0.10
Nodes (32): FinalizedCommonSupport, FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedScientificTrace, FinalizedSuitabilitySummary, StrEnum, Stable contracts deliberately published to other bounded contexts., GetEvaluation (+24 more)

### Community 44 - "CoverageGeometry"
Cohesion: 0.28
Nodes (7): CoverageComputation, Protocol, Application ports for Environmental Information spatial collaboration., Measure an external geometry against a registered dataset extent., SpatialCoveragePort, CoverageGeometry, Transport-neutral geometry supplied at the collaboration boundary.

### Community 45 - "test_agroclimatic_evaluation_queries.py"
Cohesion: 0.16
Nodes (11): _evaluation(), _outcome(), parametrize, UUID, Focused Application query tests for Agroclimatic Evaluation., Repository double that fails if a query touches a mutation/worker method., _ReadOnlySpyRepository, _service() (+3 more)

### Community 46 - "cropsuite_comparison_adapter.py"
Cohesion: 0.26
Nodes (19): CommonSupportStatus, CommonSupportStatus, ComparableCropResult, InvalidComparisonOutputError, StrEnum, Scientific common-support outcome across evaluated crops., One crop summarized on the exact common spatial support., Raised when scientific comparison returns an invalid contract. (+11 more)

### Community 47 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 48 - "via_backend/worker.py"
Cohesion: 0.17
Nodes (12): ArgumentParser, ActiveEvaluationResult, list_active_evaluations(), _parser(), _positive_integer(), _print_active_evaluations(), UUID, Separate PostgreSQL polling-worker process and operator recovery CLI. (+4 more)

### Community 49 - "WorkerSettings"
Cohesion: 0.19
Nodes (10): _environment_float(), _environment_integer(), _optional_path(), Path, Environment-backed configuration for the VIA application host., Settings for the PostgreSQL polling worker process., WorkerSettings, test_worker_run_requires_durable_artifact_root() (+2 more)

### Community 50 - "test_environmental_information_domain.py"
Cohesion: 0.36
Nodes (7): parametrize, Unit tests for Environmental Information invariants., test_dataset_version_is_immutable(), test_extent_must_be_ordered(), test_invalid_dataset_version_metadata_is_rejected(), test_resolution_must_be_finite_and_positive(), _version()

### Community 51 - "environmental_information/interfaces/http.py"
Cohesion: 0.22
Nodes (13): CheckCoverageBody, CoverageGeometryBody, CreateDatasetBody, CreateDatasetVersionBody, DatasetResponse, DatasetVersionCoverageResponse, DatasetVersionResponse, BaseModel (+5 more)

### Community 52 - "CropComparisonExecutionError"
Cohesion: 0.24
Nodes (8): ComparisonRunner, CropComparisonEngineError, CropComparisonExecutionError, RuntimeError, Base error for the scientific crop-comparison boundary., Raised when scientific common-support comparison cannot execute., _is_within(), Path

### Community 56 - "test_run_forever_poll_wait_can_be_interrupted_by_stop"
Cohesion: 0.29
Nodes (4): WorkerRunSummary, run_once(), test_run_forever_poll_wait_can_be_interrupted_by_stop(), run_once()

### Community 57 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

## Knowledge Gaps
- **1 isolated node(s):** `via-backend`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 493 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `AgroclimaticEvaluationExecutionService`, `DomainValidationError`, `Dataset`, `CoverageGeometry`, `via_backend/worker.py`, `environmental_information/interfaces/http.py`, `DatasetVersion`, `main.py`, `InMemoryDatasetVersionRepository`, `CoverageMeasurement`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `create_app()` connect `main.py` to `Project`, `InMemoryEvaluationRepository`, `Settings`, `test_farm_management_postgresql.py`, `Dataset`, `FarmManagementService`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `EnvironmentalInformationService`, `agroclimatic_evaluation/application/service.py`, `test_environmental_information_api.py`, `farm_management/application/service.py`, `DatasetVersion`, `test_agroclimatic_evaluation_api.py`, `Parcel`, `test_farm_management_api.py`, `InMemoryDatasetVersionRepository`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `AgroclimaticEvaluationService` connect `agroclimatic_evaluation/application/service.py` to `AgroclimaticEvaluationExecutionService`, `EvaluationStatus`, `test_decision_support.py`, `DomainValidationError`, `agroclimatic_evaluation/application/__init__.py`, `test_agroclimatic_evaluation_queries.py`, `Evaluation`, `test_agroclimatic_evaluation_api.py`, `main.py`, `recovery.py`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `PostgreSQLEvaluationRepository` (e.g. with `EvaluationConflictError` and `Evaluation`) actually correct?**
  _`PostgreSQLEvaluationRepository` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `EvaluationStatus` (e.g. with `RecoverEvaluation` and `AgroclimaticEvaluationExecutionService`) actually correct?**
  _`EvaluationStatus` has 18 INFERRED edges - model-reasoned connections that need verification._