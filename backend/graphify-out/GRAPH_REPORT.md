# Graph Report - backend  (2026-09-16)

## Corpus Check
- 161 files · ~52,386 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1943 nodes · 5770 edges · 94 communities (60 shown, 20 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 804 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3f2586ee`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_agroclimatic_evaluation_execution.py
- ConfiguredEnvironmentalInputIntegrityVerifier
- test_agroclimatic_evaluation_worker.py
- test_migration_host.py
- Evaluation
- Settings
- decision_support/application/service.py
- DomainValidationError
- DomainValidationError
- FarmManagementService
- PostgreSQLEvaluationRepository
- EnvironmentalInformationService
- workflow.py
- decision_support/domain/models.py
- test_cropsuite_adapter.py
- DomainValidationError
- PolicyReference
- farm_management/application/service.py
- test_decision_support_postgresql.py
- test_agroclimatic_evaluation_queries.py
- ViabilityPolicySnapshot
- create_database
- DatasetVersion
- test_agroclimatic_evaluation_api.py
- Parcel
- scientific_artifact_store.py
- test_create_worker_fails_fast_on_invalid_scientific_input_bindings
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- CoverageMeasurement
- execution.py
- agroclimatic_evaluation/domain/__init__.py
- main
- Project
- test_agroclimatic_evaluation_domain.py
- test_architecture.py
- CropSuitabilityRequest
- EvaluationStatus
- environmental_information/interfaces/http.py
- test_farm_management_postgresql.py
- DatasetRepository
- test_crop_comparison_contracts.py
- cropsuite_adapter.py
- test_decision_support.py
- agroclimatic_evaluation/application/__init__.py
- GetPublishedDatasetVersion
- test_agroclimatic_environmental_inputs.py
- cropsuite_comparison_adapter.py
- test_environmental_information_api.py
- app.py
- config.py
- test_environmental_information_domain.py
- AgroclimaticEvaluationRecoveryService
- CropSuiteComparisonAdapter
- via_backend/worker.py
- scientific_input_integrity.py
- FilesystemScientificArtifactStore
- verify_runtime
- test_farm_management_api.py
- InMemoryEvaluationRepository
- test_health.py
- __main__.py
- ScientificArtifactStore
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
- EnvironmentalInputIntegrityError
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
- `run_once()` --calls--> `WorkerRunSummary`  [INFERRED]
  tests/test_worker_host.py → src/via_backend/contexts/agroclimatic_evaluation/application/worker.py
- `run_once()` --calls--> `WorkerRunSummary`  [INFERRED]
  tests/test_worker_host.py → src/via_backend/contexts/agroclimatic_evaluation/application/worker.py
- `test_environmental_input_reference_accepts_exact_version_identity()` --calls--> `EnvironmentalInputReference`  [INFERRED]
  tests/test_agroclimatic_environmental_inputs.py → src/via_backend/contexts/agroclimatic_evaluation/domain/environmental_inputs.py
- `test_environmental_input_manifest_rejects_empty_inputs()` --calls--> `EnvironmentalInputManifest`  [INFERRED]
  tests/test_agroclimatic_environmental_inputs.py → src/via_backend/contexts/agroclimatic_evaluation/domain/environmental_inputs.py
- `test_extent_must_be_ordered()` --calls--> `SpatialExtent`  [INFERRED]
  tests/test_environmental_information_domain.py → src/via_backend/contexts/environmental_information/domain/spatial.py

## Import Cycles
- None detected.

## Communities (94 total, 20 thin omitted)

### Community 0 - "test_agroclimatic_evaluation_execution.py"
Cohesion: 0.14
Nodes (35): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., EvaluationExecutor, Logger, Protocol, _artifact(), _environmental_information_for(), _evaluation() (+27 more)

### Community 1 - "ConfiguredEnvironmentalInputIntegrityVerifier"
Cohesion: 0.23
Nodes (22): ConfiguredEnvironmentalInputIntegrityVerifier, Verify manifests using deployment-configured exact dataset-version bindings., _binding(), _fingerprints(), _manifest(), parametrize, Path, ScientificSourceFingerprint (+14 more)

### Community 2 - "test_agroclimatic_evaluation_worker.py"
Cohesion: 0.15
Nodes (25): AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application., _artifact(), _engine_result(), _evaluation(), _executor(), FakeEngine, FakeEnvironmentalInformation (+17 more)

### Community 3 - "test_migration_host.py"
Cohesion: 0.06
Nodes (49): ApiServerSettings, main(), Production HTTP process host for VIA., Provider-neutral Uvicorn bind settings for the production API process., Load API bind settings from the process environment., Validate production configuration and run one Uvicorn API process., _build_parser(), main() (+41 more)

### Community 4 - "Evaluation"
Cohesion: 0.11
Nodes (10): ActiveEvaluationResult, InvalidEvaluationTransitionError, RuntimeError, Raised when an Evaluation lifecycle transition is not allowed., Evaluation, An immutable multicrop evaluation and its scientific outcomes., EvaluationRepository, Protocol (+2 more)

### Community 5 - "Settings"
Cohesion: 0.13
Nodes (18): Settings needed by the current backend composition root., Require the durable persistence contract used by the production API., Settings, MonkeyPatch, parametrize, Tests for environment-driven application composition settings., test_create_production_app_validates_before_composition(), test_database_url_selects_postgresql_by_default() (+10 more)

### Community 6 - "decision_support/application/service.py"
Cohesion: 0.11
Nodes (34): FinalizedCommonSupport, FinalizedCommonSupportStatus, FinalizedComparableCrop, FinalizedEvaluationResult, FinalizedEvaluationResultReader, GetFinalizedEvaluationResult, Protocol, StrEnum (+26 more)

### Community 7 - "DomainValidationError"
Cohesion: 0.09
Nodes (39): InvalidSpatialInputError, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, CoverageCompatibilityFailure (+31 more)

### Community 8 - "DomainValidationError"
Cohesion: 0.08
Nodes (32): EnvironmentalInputManifest, _is_finite_number(), datetime, Immutable environmental input snapshots owned by Agroclimatic Evaluation., Immutable set of exact environmental inputs resolved for an evaluation., _validate_aware_datetime(), _validate_crs(), _validate_positive_number() (+24 more)

### Community 9 - "FarmManagementService"
Cohesion: 0.17
Nodes (11): ParcelResult, ParcelVersionResult, ProjectResult, Transport-neutral results returned by Farm Management use cases., FarmManagementService, InvalidCommandError, datetime, UUID (+3 more)

### Community 10 - "PostgreSQLEvaluationRepository"
Cohesion: 0.10
Nodes (65): Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records., CropOutcomeRecord, EvaluationCommonSupportRecord, EvaluationComparableCropRecord, EvaluationCropRecord (+57 more)

### Community 11 - "EnvironmentalInformationService"
Cohesion: 0.10
Nodes (36): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort, GetDataset (+28 more)

### Community 12 - "workflow.py"
Cohesion: 0.08
Nodes (32): PolicyEvaluationT, Decision Support application layer., IDecisionPolicy, IDefaultViabilityPolicyProvider, IDefaultViabilityPolicyStore, Protocol, Application ports for deterministic Decision Support policies., Evaluate comparable evidence without changing its scientific values. (+24 more)

### Community 13 - "decision_support/domain/models.py"
Cohesion: 0.11
Nodes (26): PolicyEvaluationT_co, DomainValidationError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Decision Support domain layer., CommonSupportEvidence, CropViabilityAssessment (+18 more)

### Community 14 - "test_cropsuite_adapter.py"
Cohesion: 0.17
Nodes (38): CropExecutionStatus, Scientific outcomes reported independently of Evaluation lifecycle state., CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability., _adapter(), _environmental_input_manifest(), _geometry(), _integrity_verifier() (+30 more)

### Community 15 - "DomainValidationError"
Cohesion: 0.09
Nodes (33): DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+25 more)

### Community 16 - "PolicyReference"
Cohesion: 0.12
Nodes (29): DefaultViabilityPolicyConflictError, InvalidViabilityPolicyRevisionError, RuntimeError, ValueError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist., Raised when a requested viability-policy revision is not a new version., Raised when the default policy changed before an expected update. (+21 more)

### Community 17 - "farm_management/application/service.py"
Cohesion: 0.10
Nodes (42): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+34 more)

### Community 18 - "test_decision_support_postgresql.py"
Cohesion: 0.17
Nodes (30): Decision Support infrastructure adapters., PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+22 more)

### Community 19 - "test_agroclimatic_evaluation_queries.py"
Cohesion: 0.16
Nodes (11): _evaluation(), _outcome(), parametrize, UUID, Focused Application query tests for Agroclimatic Evaluation., Repository double that fails if a query touches a mutation/worker method., _ReadOnlySpyRepository, _service() (+3 more)

### Community 20 - "ViabilityPolicySnapshot"
Cohesion: 0.08
Nodes (22): DefaultViabilityPolicyNotConfiguredError, LookupError, Raised when VIA has no default viability policy configured., PolicyVersionConflictError, RuntimeError, Raised when one immutable policy reference is bound to different thresholds., Immutable identity and exact thresholds used for a policy execution., ViabilityPolicySnapshot (+14 more)

### Community 21 - "create_database"
Cohesion: 0.07
Nodes (46): create_database(), Engine, SessionFactory, Create the shared engine and short-lived session factory., Shared technical infrastructure used by the application composition root., ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe. (+38 more)

### Community 22 - "DatasetVersion"
Cohesion: 0.06
Nodes (39): CoverageComputation, DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., Dataset, DatasetVersion, Stable logical identity for a geoenvironmental dataset., Immutable reproducibility metadata for one dataset release. (+31 more)

### Community 23 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.20
Nodes (28): _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any, FastAPI (+20 more)

### Community 24 - "Parcel"
Cohesion: 0.08
Nodes (35): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online(), ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved. (+27 more)

### Community 25 - "scientific_artifact_store.py"
Cohesion: 0.15
Nodes (17): PurePosixPath, _file_identity(), _is_within(), PublishedScientificArtifact, Path, RuntimeError, Durable filesystem storage for scientific artifacts., Base error for durable scientific artifact storage failures. (+9 more)

### Community 27 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.10
Nodes (44): _to_outcome(), EvaluationConflictError, Raised when an evaluation identity already exists., CropOutcome, Durable per-crop outcome values owned by Agroclimatic Evaluation., Current reproducibility trace with opaque engine source evidence., One durable result associated with an Evaluation and requested crop., Scientific artifact role persisted by Agroclimatic Evaluation. (+36 more)

### Community 28 - "CoverageMeasurement"
Cohesion: 0.16
Nodes (21): CheckDatasetVersionCoverage, CoverageClassification, CoverageMeasurement, StrEnum, Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port., _multi_polygon(), _polygon() (+13 more)

### Community 29 - "execution.py"
Cohesion: 0.08
Nodes (31): AgroclimaticEvaluationExecutionService, _comparison_request(), EnvironmentalInputResolutionError, datetime, Exception, RuntimeError, Synchronous application orchestration for persisted evaluations., Raised when an exact caller-selected environmental version cannot be resolved. (+23 more)

### Community 30 - "agroclimatic_evaluation/domain/__init__.py"
Cohesion: 0.12
Nodes (29): _to_common_support(), CommonSupport, CommonSupportStatus, ComparableCrop, StrEnum, Evaluation-level scientific common-support result., One crop ranked on the exact common valid spatial support., Validate deterministic scientific ranking semantics. (+21 more)

### Community 31 - "main"
Cohesion: 0.09
Nodes (23): Event, FrameType, main(), make_shutdown_handler(), _print_active_evaluations(), Logger, Poll until cooperative shutdown, waiting only after a non-full batch., Return a signal handler that only requests cooperative process shutdown. (+15 more)

### Community 32 - "Project"
Cohesion: 0.13
Nodes (10): Project, An agricultural project that groups parcels., ParcelRepository, ProjectRepository, Protocol, UUID, Repository abstractions for Farm Management aggregates., _project_from_record() (+2 more)

### Community 33 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.18
Nodes (21): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+13 more)

### Community 34 - "test_architecture.py"
Cohesion: 0.15
Nodes (16): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+8 more)

### Community 35 - "CropSuitabilityRequest"
Cohesion: 0.22
Nodes (7): CropSuitabilityRequest, CropSuitabilityResult, One checked per-crop outcome from the scientific boundary., Transport-neutral input for evaluating one crop against an exact snapshot., scientific, Opt-in smoke test for the real CropSuiteLite adapter boundary., test_real_cropsuite_adapter_smoke()

### Community 36 - "EvaluationStatus"
Cohesion: 0.12
Nodes (29): EvaluationResultAvailability, StrEnum, Whether persisted outcomes are pending, partial, or final., EvaluationStatus, StrEnum, Architecture-approved lifecycle vocabulary., CropOutcomeStatus, StrEnum (+21 more)

### Community 37 - "environmental_information/interfaces/http.py"
Cohesion: 0.12
Nodes (25): CheckCoverageBody, CoverageGeometryBody, create_router(), check_dataset_version_coverage(), create_dataset(), create_dataset_version(), get_dataset(), get_dataset_version() (+17 more)

### Community 38 - "test_farm_management_postgresql.py"
Cohesion: 0.21
Nodes (22): PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel() (+14 more)

### Community 39 - "DatasetRepository"
Cohesion: 0.22
Nodes (6): DatasetRepository, DatasetVersionRepository, Protocol, UUID, Repository abstractions for Environmental Information aggregates., test_postgresql_adapters_satisfy_repository_method_contracts()

### Community 41 - "cropsuite_adapter.py"
Cohesion: 0.14
Nodes (37): InvalidEngineOutputError, Application-owned boundary for one crop suitability evaluation., Raised when the engine report does not satisfy the expected PoC contract., Opaque scientific source identity and its engine-reported SHA-256., Current PoC parcel summary for the crop-suitability output., Portable grid identity needed to verify comparable scientific rasters., Scientific artifact roles understood by VIA., Durable opaque reference to one verified scientific artifact. (+29 more)

### Community 42 - "test_decision_support.py"
Cohesion: 0.18
Nodes (23): ComparableCropEvidence, A provider-produced crop mean and rank over common valid support., _decision_evidence(), _domain_common_support(), parametrize, Focused tests for the Decision Support bounded-context foundation., test_common_support_rejects_duplicate_crop_membership(), test_common_support_rejects_malformed_crop_membership() (+15 more)

### Community 43 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.08
Nodes (47): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Commands expressing Agroclimatic Evaluation use-case intent., Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, Agroclimatic Evaluation application layer., FinalizedCropOutcome, FinalizedCropOutcomeStatus (+39 more)

### Community 44 - "GetPublishedDatasetVersion"
Cohesion: 0.20
Nodes (19): GetPublishedDatasetVersion, PublishedDatasetVersion, PublishedDatasetVersionReader, Protocol, Stable contracts deliberately published to other bounded contexts., Public cross-context reader for exact immutable dataset versions., _dataset(), datetime (+11 more)

### Community 45 - "test_agroclimatic_environmental_inputs.py"
Cohesion: 0.18
Nodes (22): parametrize, Focused domain tests for immutable environmental input manifests., _snapshot(), test_environmental_input_manifest_accepts_valid_inputs(), test_environmental_input_manifest_allows_same_version_for_distinct_input_keys(), test_environmental_input_manifest_rejects_duplicate_input_key(), test_environmental_input_manifest_rejects_empty_inputs(), test_environmental_input_manifest_rejects_input_registered_after_resolution() (+14 more)

### Community 46 - "cropsuite_comparison_adapter.py"
Cohesion: 0.16
Nodes (26): CommonSupportStatus, CommonSupportResult, CommonSupportStatus, ComparableCropResult, CropComparisonRequest, CropComparisonResult, InvalidComparisonOutputError, StrEnum (+18 more)

### Community 47 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 48 - "app.py"
Cohesion: 0.18
Nodes (11): get, create_app(), create_production_app(), FastAPI, Side-effect-free FastAPI application composition., Build the production API after enforcing durable persistence settings., Build the VIA API and register its technical interfaces., health() (+3 more)

### Community 49 - "config.py"
Cohesion: 0.19
Nodes (10): _environment_float(), _environment_integer(), _optional_path(), Path, Environment-backed configuration for the VIA application host., Settings for the PostgreSQL polling worker process., WorkerSettings, test_worker_run_requires_durable_artifact_root() (+2 more)

### Community 50 - "test_environmental_information_domain.py"
Cohesion: 0.36
Nodes (7): parametrize, Unit tests for Environmental Information invariants., test_dataset_version_is_immutable(), test_extent_must_be_ordered(), test_invalid_dataset_version_metadata_is_rejected(), test_resolution_must_be_finite_and_positive(), _version()

### Community 51 - "AgroclimaticEvaluationRecoveryService"
Cohesion: 0.15
Nodes (22): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Logger, Mark an operator-confirmed active orphan as failed without retrying it., list_active_evaluations(), UUID, List active evaluations without composing scientific execution dependencies. (+14 more)

### Community 52 - "CropSuiteComparisonAdapter"
Cohesion: 0.30
Nodes (17): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., _artifact(), Any, Path, _report(), _request(), _snapshot() (+9 more)

### Community 53 - "via_backend/worker.py"
Cohesion: 0.15
Nodes (13): Agroclimatic Evaluation infrastructure layer., load_configured_environmental_input_integrity_verifier(), Build the configured verifier from one deployment binding file., create_worker(), _parser(), _positive_integer(), ArgumentParser, Separate PostgreSQL polling-worker process and operator recovery CLI. (+5 more)

### Community 54 - "scientific_input_integrity.py"
Cohesion: 0.18
Nodes (13): CropSuiteEnvironmentalInputBinding, load_cropsuite_environmental_input_bindings(), _parse_uuid(), Any, Path, UUID, Configured binding between exact dataset versions and CropSuite source hashes., Load and strictly validate deployment environmental-input binding JSON. (+5 more)

### Community 55 - "FilesystemScientificArtifactStore"
Cohesion: 0.30
Nodes (14): FilesystemScientificArtifactStore, Filesystem-backed immutable artifact store., parametrize, Path, test_publish_creates_durable_artifact_with_opaque_reference(), test_publish_is_idempotent_for_identical_content(), test_publish_rejects_content_that_does_not_match_expected_checksum(), test_publish_rejects_different_content_for_existing_reference() (+6 more)

### Community 56 - "verify_runtime"
Cohesion: 0.39
Nodes (7): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_writable_directory(), _run_pip_check(), verify_runtime()

### Community 57 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 58 - "InMemoryEvaluationRepository"
Cohesion: 0.28
Nodes (5): InMemoryEvaluationRepository, _validate_limit(), parametrize, test_active_discovery_requires_positive_integer_limit(), test_queued_discovery_requires_positive_limit()

### Community 73 - "ScientificArtifactStore"
Cohesion: 0.18
Nodes (10): EngineRunner, CropSuitabilityExecutionError, IEnvironmentalInputIntegrityVerifier, Raised when the existing engine service cannot produce a report., Verify resolved environmental provenance against scientific source fingerprints., _is_within(), Path, Protocol (+2 more)

### Community 91 - "CropComparisonExecutionError"
Cohesion: 0.24
Nodes (8): ComparisonRunner, CropComparisonEngineError, CropComparisonExecutionError, RuntimeError, Base error for the scientific crop-comparison boundary., Raised when scientific common-support comparison cannot execute., _is_within(), Path

### Community 92 - "EnvironmentalInputIntegrityError"
Cohesion: 0.40
Nodes (4): CropSuitabilityEngineError, EnvironmentalInputIntegrityError, Base error for failures to invoke or understand the engine boundary., Raised when resolved environmental provenance does not match scientific inputs.

## Knowledge Gaps
- **1 isolated node(s):** `via-backend`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 525 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `environmental_information/interfaces/http.py`, `DomainValidationError`, `DatasetRepository`, `GetPublishedDatasetVersion`, `app.py`, `via_backend/worker.py`, `DatasetVersion`, `CoverageMeasurement`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `create_app()` connect `app.py` to `Project`, `Settings`, `environmental_information/interfaces/http.py`, `test_farm_management_postgresql.py`, `FarmManagementService`, `PostgreSQLEvaluationRepository`, `EnvironmentalInformationService`, `agroclimatic_evaluation/application/__init__.py`, `test_environmental_information_api.py`, `farm_management/application/service.py`, `create_database`, `DatasetVersion`, `test_agroclimatic_evaluation_api.py`, `Parcel`, `test_farm_management_api.py`, `InMemoryEvaluationRepository`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `AgroclimaticEvaluationService` connect `agroclimatic_evaluation/application/__init__.py` to `test_agroclimatic_evaluation_domain.py`, `Evaluation`, `EvaluationStatus`, `decision_support/application/service.py`, `DomainValidationError`, `app.py`, `test_agroclimatic_evaluation_queries.py`, `test_agroclimatic_evaluation_api.py`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `execution.py`, `agroclimatic_evaluation/domain/__init__.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `PostgreSQLEvaluationRepository` (e.g. with `EvaluationConflictError` and `Evaluation`) actually correct?**
  _`PostgreSQLEvaluationRepository` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `EvaluationStatus` (e.g. with `RecoverEvaluation` and `AgroclimaticEvaluationExecutionService`) actually correct?**
  _`EvaluationStatus` has 18 INFERRED edges - model-reasoned connections that need verification._