# Graph Report - backend  (2026-09-16)

## Corpus Check
- 162 files · ~53,066 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1959 nodes · 5805 edges · 105 communities (72 shown, 19 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 805 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `94333a90`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AgroclimaticEvaluationExecutionService
- ConfiguredEnvironmentalInputIntegrityVerifier
- test_agroclimatic_evaluation_worker.py
- test_migration_host.py
- Evaluation
- Settings
- test_decision_support.py
- DomainValidationError
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
- test_database_test_support.py
- DatasetVersion
- test_agroclimatic_evaluation_api.py
- Parcel
- scientific_artifact_store.py
- decision_support/application/service.py
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- CoverageMeasurement
- execution.py
- ComparableCrop
- main
- Project
- test_agroclimatic_evaluation_domain.py
- test_architecture.py
- test_api_host.py
- EvaluationStatus
- InMemoryEvaluationRepository
- test_farm_management_postgresql.py
- Dataset
- CropComparisonRequest
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
- AgroclimaticEvaluationRecoveryService
- CropSuiteComparisonAdapter
- AgroclimaticEvaluationService
- via_backend/worker.py
- FilesystemScientificArtifactStore
- verify_runtime
- test_farm_management_api.py
- recovery.py
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
- agroclimatic_evaluation/application/ports.py
- FinalizedCommonSupportStatus
- GetPublishedDatasetVersion
- decision_support/application/ports.py
- test_environmental_information_postgresql.py
- run_forever
- migrate.py
- ScientificArtifactRole
- test_real_cropsuite_comparison_adapter_smoke
- .add_outcome
- health.py
- PolicyVersionConflictError
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

## Communities (105 total, 19 thin omitted)

### Community 0 - "AgroclimaticEvaluationExecutionService"
Cohesion: 0.15
Nodes (35): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, Exception, Execute requested crops and summarize them through Application-owned ports., _artifact(), _environmental_information_for(), _evaluation() (+27 more)

### Community 1 - "ConfiguredEnvironmentalInputIntegrityVerifier"
Cohesion: 0.09
Nodes (38): ConfiguredEnvironmentalInputIntegrityVerifier, CropSuiteEnvironmentalInputBinding, load_cropsuite_environmental_input_bindings(), Any, Path, Load and strictly validate deployment environmental-input binding JSON., Deployment mapping from one exact DatasetVersion to expected source hashes., Verify manifests using deployment-configured exact dataset-version bindings. (+30 more)

### Community 2 - "test_agroclimatic_evaluation_worker.py"
Cohesion: 0.15
Nodes (20): _artifact(), _evaluation(), FakeEnvironmentalInformation, _manifest(), _published(), datetime, Path, UUID (+12 more)

### Community 3 - "test_migration_host.py"
Cohesion: 0.19
Nodes (19): main(), Run the explicit release migration CLI., _configure_valid_production(), CaptureFixture, MonkeyPatch, parametrize, Path, Focused tests for the explicit VIA release migration host. (+11 more)

### Community 4 - "Evaluation"
Cohesion: 0.08
Nodes (17): EnvironmentalInputResolutionError, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved., Validate deterministic scientific ranking semantics., validate_comparable_crops(), EnvironmentalInputManifest, Immutable set of exact environmental inputs resolved for an evaluation., InvalidEvaluationTransitionError (+9 more)

### Community 5 - "Settings"
Cohesion: 0.11
Nodes (27): Settings needed by the current backend composition root., Require the durable persistence contract used by the production API., Settings for the PostgreSQL polling worker process., Settings, WorkerSettings, MonkeyPatch, parametrize, Path (+19 more)

### Community 6 - "test_decision_support.py"
Cohesion: 0.16
Nodes (22): ComparableCropEvidence, A provider-produced crop mean and rank over common valid support., _decision_evidence(), _domain_common_support(), _InMemoryViabilityPolicyRepository, parametrize, Focused tests for the Decision Support bounded-context foundation., test_common_support_rejects_duplicate_crop_membership() (+14 more)

### Community 7 - "DomainValidationError"
Cohesion: 0.09
Nodes (37): InvalidSpatialInputError, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, CoverageGeometry (+29 more)

### Community 8 - "DomainValidationError"
Cohesion: 0.09
Nodes (33): EnvironmentalInputSnapshot, _is_finite_number(), datetime, Immutable environmental input snapshots owned by Agroclimatic Evaluation., Historical environmental input metadata captured for one evaluation input., _validate_aware_datetime(), _validate_crs(), _validate_positive_number() (+25 more)

### Community 9 - "FarmManagementService"
Cohesion: 0.17
Nodes (11): ParcelResult, ParcelVersionResult, ProjectResult, Transport-neutral results returned by Farm Management use cases., FarmManagementService, InvalidCommandError, datetime, UUID (+3 more)

### Community 10 - "PostgreSQLEvaluationRepository"
Cohesion: 0.13
Nodes (51): EnvironmentalInputReference, Caller-selected exact environmental dataset version., PostgreSQLEvaluationRepository, SessionFactory, Durable adapter for immutable Evaluation aggregates., clean_evaluations(), _common_support(), _comparable_crops() (+43 more)

### Community 11 - "EnvironmentalInformationService"
Cohesion: 0.06
Nodes (65): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort, PublishedDatasetVersion (+57 more)

### Community 12 - "ViabilityPolicySnapshot"
Cohesion: 0.10
Nodes (31): PolicyEvaluationT, EvaluateConfiguredDecisionSupport, EvaluateDecisionSupport, StrEnum, Decision Support application query messages., Prepare evidence and apply one explicitly versioned policy when possible., How the viability policy configuration is selected for one execution., Select either VIA's current default policy or an explicit custom snapshot. (+23 more)

### Community 13 - "decision_support/domain/models.py"
Cohesion: 0.11
Nodes (25): DomainValidationError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Decision Support domain layer., CommonSupportEvidence, CropViabilityAssessment, DecisionEvidence (+17 more)

### Community 14 - "test_cropsuite_adapter.py"
Cohesion: 0.17
Nodes (38): CropExecutionStatus, Scientific outcomes reported independently of Evaluation lifecycle state., CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability., _adapter(), _environmental_input_manifest(), _geometry(), _integrity_verifier() (+30 more)

### Community 15 - "DomainValidationError"
Cohesion: 0.09
Nodes (33): DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+25 more)

### Community 16 - "PolicyReference"
Cohesion: 0.10
Nodes (35): DefaultViabilityPolicyConflictError, DefaultViabilityPolicyNotConfiguredError, InvalidViabilityPolicyRevisionError, LookupError, RuntimeError, ValueError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist. (+27 more)

### Community 17 - "farm_management/application/service.py"
Cohesion: 0.10
Nodes (42): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+34 more)

### Community 18 - "test_decision_support_postgresql.py"
Cohesion: 0.17
Nodes (30): Decision Support infrastructure adapters., PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+22 more)

### Community 19 - "GetFinalizedEvaluationResult"
Cohesion: 0.33
Nodes (7): GetFinalizedEvaluationResult, _evaluation(), parametrize, Focused Application query tests for Agroclimatic Evaluation., _service(), test_finalized_public_contract_preserves_order_and_outcome_semantics(), test_public_contract_rejects_non_succeeded_evaluation()

### Community 20 - "ViabilityPolicyVersionRecord"
Cohesion: 0.24
Nodes (9): Base, DeclarativeBase, SQLAlchemy metadata owned by Decision Support Infrastructure., Declarative base for Decision Support persistence records., DefaultViabilityPolicyRecord, Database records for Decision Support; these are not domain entities., One immutable persisted viability-policy configuration., Singleton pointer to the currently selected VIA default policy version. (+1 more)

### Community 21 - "test_database_test_support.py"
Cohesion: 0.22
Nodes (14): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., UnsafeTestDatabaseError, validate_test_database_url(), CaptureFixture, parametrize (+6 more)

### Community 22 - "DatasetVersion"
Cohesion: 0.10
Nodes (27): CoverageComputation, DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., DatasetVersion, Immutable reproducibility metadata for one dataset release., Base, DeclarativeBase (+19 more)

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
Cohesion: 0.17
Nodes (14): FinalizedEvaluationResultReader, Protocol, Public local interface for a future Decision Support consumer., PolicyReferenceMismatchError, ValueError, Decision Support evidence translation and policy coordination., Raised when the supplied policy differs from the requested policy identity., _translate_common_support() (+6 more)

### Community 27 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.11
Nodes (42): CommonSupport, Spatial support shared by the usable crop suitability rasters., EvaluationConflictError, RuntimeError, Raised when an evaluation identity already exists., Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure. (+34 more)

### Community 28 - "CoverageMeasurement"
Cohesion: 0.14
Nodes (23): CheckDatasetVersionCoverage, CoverageClassification, CoverageCompatibilityFailure, CoverageMeasurement, StrEnum, Structural metadata prevented a meaningful spatial measurement., Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port. (+15 more)

### Community 29 - "execution.py"
Cohesion: 0.12
Nodes (34): Synchronous application orchestration for persisted evaluations., _to_common_support(), _to_outcome(), CommonSupportStatus, StrEnum, Evaluation-level scientific common-support result., Domain errors for Agroclimatic Evaluation., Agroclimatic Evaluation domain layer. (+26 more)

### Community 30 - "ComparableCrop"
Cohesion: 0.22
Nodes (17): _to_comparable_crop(), ComparableCrop, One crop ranked on the exact common valid spatial support., _comparable_support(), _manifest(), parametrize, Domain tests for durable comparable crop results., _reference() (+9 more)

### Community 31 - "main"
Cohesion: 0.10
Nodes (19): FrameType, ActiveEvaluationResult, list_active_evaluations(), main(), make_shutdown_handler(), _print_active_evaluations(), Logger, Return a signal handler that only requests cooperative process shutdown. (+11 more)

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
Cohesion: 0.14
Nodes (25): EvaluationResultAvailability, StrEnum, Whether persisted outcomes are pending, partial, or final., EvaluationStatus, StrEnum, Architecture-approved lifecycle vocabulary., CommonSupportResponse, ComparableCropResponse (+17 more)

### Community 37 - "InMemoryEvaluationRepository"
Cohesion: 0.22
Nodes (14): AgroclimaticEvaluationWorker, Logger, Discover queued IDs and delegate all execution semantics to Application., InMemoryEvaluationRepository, _engine_result(), _executor(), FakeEngine, test_claim_conflict_is_benign_and_later_work_continues() (+6 more)

### Community 38 - "test_farm_management_postgresql.py"
Cohesion: 0.21
Nodes (22): PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel() (+14 more)

### Community 39 - "Dataset"
Cohesion: 0.11
Nodes (11): Dataset, Stable logical identity for a geoenvironmental dataset., DatasetRepository, DatasetVersionRepository, Protocol, UUID, Repository abstractions for Environmental Information aggregates., _dataset_from_record() (+3 more)

### Community 40 - "CropComparisonRequest"
Cohesion: 0.20
Nodes (9): CommonSupportResult, CropComparisonRequest, CropComparisonResult, Compare crop suitability only on identical valid spatial support., Scientific support shared by all usable crop suitability rasters., Checked multicrop comparison returned by the scientific boundary., FakeComparisonEngine, StubComparisonEngine (+1 more)

### Community 41 - "cropsuite_adapter.py"
Cohesion: 0.21
Nodes (28): InvalidEngineOutputError, Raised when the engine report does not satisfy the expected PoC contract., Current PoC parcel summary for the crop-suitability output., An engine-reported failure, distinct from no coverage and a zero score., Trace metadata the current PoC can supply without invented versions., ScientificExecutionFailure, ScientificExecutionTrace, SuitabilityScoreSummary (+20 more)

### Community 42 - "agroclimatic_evaluation/application/service.py"
Cohesion: 0.27
Nodes (10): FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedScientificTrace, FinalizedSuitabilitySummary, StrEnum, Stable contracts deliberately published to other bounded contexts., datetime, UUID (+2 more)

### Community 43 - "create_router"
Cohesion: 0.16
Nodes (19): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Commands expressing Agroclimatic Evaluation use-case intent., Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, ListEvaluations, create_router(), get_evaluation() (+11 more)

### Community 44 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.29
Nodes (11): Agroclimatic Evaluation application layer., _availability(), CommonSupportReadResult, ComparableCropReadResult, CropEvidenceResult, EvaluationEvidenceResult, EvaluationReadResult, PersistedCropOutcomeResult (+3 more)

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
Cohesion: 0.13
Nodes (16): create_app(), create_production_app(), FastAPI, Side-effect-free FastAPI application composition., Build the production API after enforcing durable persistence settings., Build the VIA API and register its technical interfaces., PostGISCoverageCalculator, SessionFactory (+8 more)

### Community 49 - "config.py"
Cohesion: 0.33
Nodes (7): _environment_float(), _environment_integer(), _is_same_or_within(), _optional_path(), Path, Environment-backed configuration for the VIA application host., _validate_scientific_path_topology()

### Community 50 - "SpatialExtent"
Cohesion: 0.12
Nodes (25): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, Read and validate the test-only database settings before any DB operation., require_test_database_url(), clean_tables(), database(), _database_url(), _multi_polygon() (+17 more)

### Community 51 - "AgroclimaticEvaluationRecoveryService"
Cohesion: 0.17
Nodes (18): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Logger, Mark an operator-confirmed active orphan as failed without retrying it., UUID, Run explicit fail-only orphan recovery without composing CropSuiteLite., recover_evaluation() (+10 more)

### Community 52 - "CropSuiteComparisonAdapter"
Cohesion: 0.30
Nodes (17): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., _artifact(), Any, Path, _report(), _request(), _snapshot() (+9 more)

### Community 53 - "AgroclimaticEvaluationService"
Cohesion: 0.29
Nodes (8): GetEvaluation, GetEvaluationEvidence, GetEvaluationResult, Queries supported by Agroclimatic Evaluation., EvaluationStatusResult, AgroclimaticEvaluationService, Create and query durable immutable evaluation requests., test_query_messages_return_read_only_views_without_mutation()

### Community 54 - "via_backend/worker.py"
Cohesion: 0.21
Nodes (10): Agroclimatic Evaluation infrastructure layer., load_configured_environmental_input_integrity_verifier(), Build the configured verifier from one deployment binding file., create_worker(), _parser(), _positive_integer(), ArgumentParser, Separate PostgreSQL polling-worker process and operator recovery CLI. (+2 more)

### Community 55 - "FilesystemScientificArtifactStore"
Cohesion: 0.30
Nodes (14): FilesystemScientificArtifactStore, Filesystem-backed immutable artifact store., parametrize, Path, test_publish_creates_durable_artifact_with_opaque_reference(), test_publish_is_idempotent_for_identical_content(), test_publish_rejects_content_that_does_not_match_expected_checksum(), test_publish_rejects_different_content_for_existing_reference() (+6 more)

### Community 56 - "verify_runtime"
Cohesion: 0.39
Nodes (8): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_read_only_directory(), _require_writable_directory(), _run_pip_check(), verify_runtime()

### Community 57 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 58 - "recovery.py"
Cohesion: 0.13
Nodes (17): Explicit fail-only recovery for abandoned evaluation executions., CropOutcomeResult, EvaluationResult, ParcelSnapshotResult, Transport-neutral Agroclimatic Evaluation results., InvalidCommandError, LookupError, RuntimeError (+9 more)

### Community 73 - "ScientificArtifactStore"
Cohesion: 0.24
Nodes (8): EngineRunner, CropSuitabilityExecutionError, Raised when the existing engine service cannot produce a report., _is_within(), Path, Protocol, Publish immutable scientific files behind opaque logical references., ScientificArtifactStore

### Community 91 - "CropComparisonExecutionError"
Cohesion: 0.24
Nodes (8): ComparisonRunner, CropComparisonEngineError, CropComparisonExecutionError, RuntimeError, Base error for the scientific crop-comparison boundary., Raised when scientific common-support comparison cannot execute., _is_within(), Path

### Community 92 - "agroclimatic_evaluation/application/ports.py"
Cohesion: 0.09
Nodes (23): datetime, CropSuitabilityEngineError, CropSuitabilityRequest, CropSuitabilityResult, EnvironmentalInputIntegrityError, ICropComparisonEngine, ICropSuitabilityEngine, IEnvironmentalInputIntegrityVerifier (+15 more)

### Community 93 - "FinalizedCommonSupportStatus"
Cohesion: 0.27
Nodes (15): FinalizedCommonSupport, FinalizedCommonSupportStatus, FinalizedComparableCrop, FinalizedEvaluationResult, _common_support(), _evaluate(), _finalized_result(), Any (+7 more)

### Community 94 - "GetPublishedDatasetVersion"
Cohesion: 0.37
Nodes (14): GetPublishedDatasetVersion, _dataset(), datetime, UUID, Public cross-context contract tests for Environmental Information., _service(), test_exact_dataset_and_version_returns_all_published_metadata(), test_missing_dataset_returns_none() (+6 more)

### Community 95 - "decision_support/application/ports.py"
Cohesion: 0.16
Nodes (9): PolicyEvaluationT_co, IDecisionPolicy, IDefaultViabilityPolicyProvider, IDefaultViabilityPolicyStore, Protocol, Application ports for deterministic Decision Support policies., Evaluate comparable evidence without changing its scientific values., Provide the current VIA default viability policy without owning its storage. (+1 more)

### Community 96 - "test_environmental_information_postgresql.py"
Cohesion: 0.33
Nodes (12): clean_environmental_information(), database(), _database_url(), _dataset(), Engine, fixture, SessionFactory, PostgreSQL/PostGIS integration tests for Environmental Information. (+4 more)

### Community 97 - "run_forever"
Cohesion: 0.21
Nodes (8): Event, WorkerRunSummary, Poll until cooperative shutdown, waiting only after a non-full batch., run_forever(), test_run_forever_does_not_poll_again_after_stop_is_requested(), run_once(), test_run_forever_poll_wait_can_be_interrupted_by_stop(), run_once()

### Community 98 - "migrate.py"
Cohesion: 0.23
Nodes (11): _build_parser(), ArgumentParser, Path, One-shot production schema migration host for VIA releases., Return the repository-local Alembic config when running from source., Resolve the Alembic config without depending on the process cwd., Validate production persistence and migrate the schema to Alembic head., _require_production_postgresql() (+3 more)

### Community 99 - "ScientificArtifactRole"
Cohesion: 0.29
Nodes (7): _comparison_request(), Portable grid identity needed to verify comparable scientific rasters., Scientific artifact roles understood by VIA., Durable opaque reference to one verified scientific artifact., ScientificArtifactDescriptor, ScientificArtifactGrid, ScientificArtifactRole

### Community 100 - "test_real_cropsuite_comparison_adapter_smoke"
Cohesion: 0.33
Nodes (5): CropComparisonInput, One durable crop suitability raster offered to scientific comparison., scientific, Opt-in smoke test for the real CropSuiteLite comparison boundary., test_real_cropsuite_comparison_adapter_smoke()

### Community 102 - "health.py"
Cohesion: 0.40
Nodes (4): get, health(), Host-level health endpoint., Report that the API process is ready to receive requests.

### Community 103 - "PolicyVersionConflictError"
Cohesion: 0.50
Nodes (3): PolicyVersionConflictError, RuntimeError, Raised when one immutable policy reference is bound to different thresholds.

## Knowledge Gaps
- **1 isolated node(s):** `via-backend`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 528 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create_app()` connect `app.py` to `Project`, `InMemoryEvaluationRepository`, `Settings`, `Dataset`, `test_farm_management_postgresql.py`, `FarmManagementService`, `PostgreSQLEvaluationRepository`, `create_router`, `EnvironmentalInformationService`, `test_environmental_information_api.py`, `farm_management/application/service.py`, `AgroclimaticEvaluationService`, `DatasetVersion`, `test_agroclimatic_evaluation_api.py`, `Parcel`, `test_farm_management_api.py`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `DomainValidationError`, `Dataset`, `app.py`, `SpatialExtent`, `DatasetVersion`, `via_backend/worker.py`, `CoverageMeasurement`, `GetPublishedDatasetVersion`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `AgroclimaticEvaluationService` connect `AgroclimaticEvaluationService` to `Evaluation`, `EvaluationStatus`, `DomainValidationError`, `agroclimatic_evaluation/application/service.py`, `create_router`, `agroclimatic_evaluation/application/__init__.py`, `PostgreSQLEvaluationRepository`, `app.py`, `GetFinalizedEvaluationResult`, `test_agroclimatic_evaluation_api.py`, `recovery.py`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `FinalizedCommonSupportStatus`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `PostgreSQLEvaluationRepository` (e.g. with `EvaluationConflictError` and `Evaluation`) actually correct?**
  _`PostgreSQLEvaluationRepository` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `EvaluationStatus` (e.g. with `RecoverEvaluation` and `AgroclimaticEvaluationExecutionService`) actually correct?**
  _`EvaluationStatus` has 18 INFERRED edges - model-reasoned connections that need verification._