# Graph Report - poc_via_cslite  (2026-09-17)

## Corpus Check
- 312 files · ~155,743 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2922 nodes · 7173 edges · 212 communities (130 shown, 30 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 873 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `07b9a0e5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- farm_management/application/service.py
- run_cropsuitelite.py
- NexGenPreProcessing
- Huaura Dataset Preprocessing Configuration
- check_files.py
- DomainValidationError
- farm_management/infrastructure/postgresql_repositories.py
- Crop Membership Functions
- multicrop.py
- workflow.py
- data_tools.py
- DownloadCMIP6Data
- PostgreSQLEvaluationRepository
- climate_suitability_main_xarray.py
- CropSuiteLite
- test_migration_host.py
- climate_suitability_main.py
- InMemoryEvaluationRepository
- CoverageMeasurement
- decision_support/domain/models.py
- test_farm_management_postgresql.py
- VIA architecture guardrails
- Farm Management persistence
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- Architecture and Backend for CropSuiteLite Huaura v2
- Huaura Environmental Correction
- scientific_artifact_store.py
- test_architecture.py
- Farm Management schema ownership
- Bounded-context layered structure
- Python and FastAPI backend decision
- AgroclimaticEvaluationExecutionService
- Farm Management minimum vertical slice
- Application commands and queries
- main
- VIA architecture implementation roadmap
- Evaluation
- ConfiguredEnvironmentalInputIntegrityVerifier
- test_agroclimatic_environmental_inputs.py
- Q: PostgreSQL Farm Management repositories
- agroclimatic_evaluation/interfaces/http.py
- ADR-012: PostgreSQL/PostGIS persistence for Environmental Information
- PostGIS service
- agroclimatic_evaluation/application/ports.py
- test_agroclimatic_evaluation_queries.py
- Q: Verify that the new VIA backend foundation is discoverable and consistent with the intended architecture.
- Q: optimistic stale-write handling introduced in the current slice
- Q: repository ports and current in-memory adapters
- Q: Farm Management ownership and persistence boundaries
- Q: dependency direction involving Domain, Application and Infrastructure
- Q: Project, Parcel, ParcelVersion, ParcelGeometry
- Q: Continue the Farm Management durable persistence increment from the current repository state
- test_health.py
- CropSuiteLite Python Dependency Manifest
- download_soilgrids_huaura.py
- Knowledge Graph Pipeline
- __main__.py
- Atlas A Logo
- read_remote_chunk
- ViabilityPolicySnapshot
- nc_tools.py
- agroclimatic_evaluation/application/service.py
- agroclimatic_evaluation/__init__.py
- DatasetVersion
- Parcel
- ComparableCrop
- require_test_database_url
- decision_support/__init__.py
- decision_support/interfaces/__init__.py
- EnvironmentalInformationService
- test_api_host.py
- app.py
- environmental_information/__init__.py
- Q: ParcelVersion persistence
- farm_management/__init__.py
- identity_access/application/__init__.py
- identity_access/domain/__init__.py
- identity_access/infrastructure/__init__.py
- identity_access/__init__.py
- identity_access/interfaces/__init__.py
- contexts/__init__.py
- http/__init__.py
- via_backend/interfaces/__init__.py
- Bounded Context
- Initial Deployment Stack
- Graphify-first repository workflow
- Q: Domain-to-Infrastructure dependency violations
- Documentation Deployment Workflow
- Suitability and Limiting-Factor Outputs
- Nodata Coverage Conservation
- Membership Functions Diagram
- Modified Membership Functions Diagram
- CropSuiteLite Conda Environment
- Logical and deployment boundary separation
- cropsuite_adapter.py
- Huaura scientific fixture recovery audit
- execution.py
- Environmental Information coverage and compatibility
- Q: Confirm backend package and layer structure, Domain/Application/Infrastructure/Interfaces boundaries, current dependency rules, and verification configuration
- ADR-013: Extent coverage and CRS comparison
- Q: dataset version coverage parcel geometry contract
- Q: Cross-context dependency violations
- Q: Environmental Information persistence
- Q: Dataset and DatasetVersion
- Q: coverage classification dataset version geometry compatible
- Q: postgis transform crs geography coverage
- Q: environmental information farm management imports dependency violations
- via-backend
- ADR-014: PostgreSQL/PostGIS persistence for Agroclimatic Evaluation
- scientific_input_integrity.py
- test_agroclimatic_evaluation_domain.py
- test_decision_support.py
- Production deployment runtime contract
- GetPublishedDatasetVersion
- Settings
- EvaluationResult
- CropSuite.py
- FarmManagementService
- .from_geojson
- test_agroclimatic_evaluation_api.py
- test_cropsuite_adapter.py
- Agroclimatic Evaluation request, worker, recovery, and read slice
- Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation
- Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors
- environmental_information/interfaces/http.py
- crop_suitability_main.py
- SpatialExtent
- cropsuite_comparison_adapter.py
- Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment.
- CropSuiteComparisonAdapter
- PolicyReference
- config.py
- DomainValidationError
- Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract
- create_router
- test_decision_support_postgresql.py
- env.py
- test_environmental_information_api.py
- verify_runtime
- agroclimatic_evaluation/application/__init__.py
- test_farm_management_api.py
- benchmark_production_runtime.sh
- create_app
- migrate.py
- test_container_image_contract.py
- test_digitalocean_deployment_contract.py
- deploy_digitalocean.sh
- verify_production_compose.sh
- AgroclimaticEvaluationService
- process_precday_interp
- test_resource_benchmark_contract.py
- DomainValidationError
- backup_postgres.sh
- via_backend/worker.py
- FilesystemScientificArtifactStore
- CropComparisonRequest
- test_environmental_information_postgresql.py
- CommonSupport
- CropComparisonExecutionError
- health.py

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
- `PostgreSQL/PostGIS durable persistence workflow` --semantically_similar_to--> `Farm Management persistence`  [INFERRED] [semantically similar]
  graphify-out/memory/query_20260912_070850_44f16014_continue_the_farm_management_durable_persistence_i.md → docs/architecture/farm-management-persistence.md
- `ParcelRepository stale-write conflict handling` --semantically_similar_to--> `Revision concurrency`  [INFERRED] [semantically similar]
  graphify-out/memory/query_20260912_060606_5f4afb72_optimistic_stale_write_handling_introduced_in_the.md → docs/architecture/farm-management-persistence.md
- `ADR-006 Scientific Traceability` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-006-scientific-traceability.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md
- `Recoverable job mechanism` --semantically_similar_to--> `Recoverable background worker flow`  [INFERRED] [semantically similar]
  docs/architecture/overview.md → AGENTS.md
- `ADR-001 Modular Monolith` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-001-modular-monolith.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Bounded-context layered architecture** — docs_architecture_backend_structure_bounded_context_layering, docs_architecture_backend_structure_domain_layer, docs_architecture_backend_structure_application_layer, docs_architecture_backend_structure_infrastructure_layer, docs_architecture_backend_structure_interfaces_layer [EXTRACTED 1.00]
- **Farm Management durable persistence contract** — docs_adr_adr_011_postgresql_postgis_farm_persistence_persistence_technology_stack, docs_adr_adr_011_postgresql_postgis_farm_persistence_farm_management_schema_ownership, docs_adr_adr_011_postgresql_postgis_farm_persistence_postgis_geometry_storage, docs_adr_adr_011_postgresql_postgis_farm_persistence_optimistic_revision_transaction [EXTRACTED 1.00]
- **Farm Management vertical slice flow** — docs_architecture_farm_management_slice_project_and_parcel_http_resources, docs_architecture_farm_management_slice_application_commands_and_queries, docs_architecture_farm_management_slice_project_parcel_and_parcelversion_domain_model, docs_architecture_farm_management_slice_repository_abstractions, docs_architecture_farm_management_slice_in_memory_and_durable_adapters [EXTRACTED 1.00]
- **Scientific isolation and execution boundary** — agents_icropsuitabilityengine, docs_architecture_cropsuite_integration_cropsuiteadapter, agents_recoverable_background_worker, docs_architecture_overview_recoverable_job_mechanism [EXTRACTED 1.00]
- **VIA seven-increment delivery sequence** — docs_implementation_roadmap_modeling_increment, docs_implementation_roadmap_modular_foundation_increment, docs_implementation_roadmap_parcel_and_environmental_coverage_increment, docs_implementation_roadmap_result_querying_increment, docs_implementation_roadmap_on_demand_execution_increment, docs_implementation_roadmap_public_deployment_increment, docs_implementation_roadmap_explanation_and_comparison_increment [EXTRACTED 1.00]
- **Atlas Adaptation Evidence Pipeline** — cropsuitelite_docs_atlas_solutions_supporting_material_manual_source_validation, cropsuitelite_docs_atlas_solutions_atlas_solution_example_response_functions_yaml, cropsuitelite_docs_atlas_solutions_atlas_solution_example_improved_crop_varieties [INFERRED 0.85]
- **Huaura Environmental Bundle Data Flow** — data_huaura_readme_huaura_environmental_bundle, data_huaura_huaura_config_environmental_dataset_directory_map, cropsuitelite_yaml_configurations_crop_suite_datasets_huaura_0041667_huaura_processed_0041667_outputs, cropsuitelite_yaml_configurations_general_config_huaura_huaura_simulation_inputs [INFERRED 0.85]
- **Reproducible Multicrop Execution** — docs_adr_adr_005_background_worker_background_worker, docs_adr_adr_006_scientific_traceability_scientific_traceability, docs_adr_adr_008_sequential_crop_execution_sequential_crop_execution, docs_adr_adr_009_multicrop_evaluation_multicrop_evaluation, docs_architecture_evaluation_flow_target_evaluation_flow [INFERRED 0.85]
- **Adaptation Solution Configuration Framework** — cropsuitelite_yaml_configurations_response_functions_adaptation_response_catalog, cropsuitelite_yaml_configurations_general_config_huaura_solution_framework_integration, cropsuitelite_yaml_configurations_general_config_solutions_solution_framework_integration [INFERRED 0.95]
- **CropSuiteLite Climate Data Pipeline** — cropsuitelite_docs_getting_started_download_cmp6_nex_gddp_cmip6, cropsuitelite_docs_getting_started_from_climatedata_tocrsdatatype_input_data_preprocessing, cropsuitelite_docs_getting_started_from_climatedata_tocrsdatatype_climatological_daily_rasters, cropsuitelite_docs_getting_started_running_cropsuite_cropsuitelite_execution [INFERRED 0.95]
- **Huaura CMIP6 Download Preprocess Simulation Pipeline** — cropsuitelite_yaml_configurations_download_cmip6_huaura_huaura_cmip6_download_configuration, cropsuitelite_yaml_configurations_crop_suite_datasets_huaura_0041667_huaura_high_resolution_preprocessing_configuration, cropsuitelite_yaml_configurations_general_config_huaura_huaura_simulation_configuration [INFERRED 0.95]
- **Scientific Engine Boundary** — docs_adr_adr_004_cropsuite_port_adapter_cropsuite_port_and_adapter, docs_architecture_cropsuite_integration_icropsuitabilityengine, docs_architecture_cropsuite_integration_cropsuiteadapter, docs_implementation_poc_preservation_cropsuitelite_poc_preservation_contract [INFERRED 0.95]

## Communities (212 total, 30 thin omitted)

### Community 0 - "farm_management/application/service.py"
Cohesion: 0.10
Nodes (42): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+34 more)

### Community 1 - "run_cropsuitelite.py"
Cohesion: 0.07
Nodes (29): change_otherst_parameters(), change_st1_parameter(), create_crop_parameters(), create_crop_suite_configuration_file(), find_solution_type(), main(), modify_extent(), modify_general_files() (+21 more)

### Community 2 - "NexGenPreProcessing"
Cohesion: 0.07
Nodes (23): create_climatology_from_nexgen(), main(), mask_single_layer(), resample_soilgrids_data(), BaseProcessor, compute_averaged_temp(), NexGen, NexGenPreProcessing (+15 more)

### Community 3 - "Huaura Dataset Preprocessing Configuration"
Cohesion: 0.05
Nodes (43): Africa Processing Profile, Soil DEM and Land-Sea Layer Plan, Africa Climate Preprocessing Plan, Dataset Preprocessing Configuration, ACCESS-ESM1-5 SSP126 Climate Processing, Huaura 0.041667 Degree Processing Profile, Huaura High-Resolution Preprocessing Configuration, Huaura Processed 0.041667 Outputs (+35 more)

### Community 4 - "check_files.py"
Cohesion: 0.09
Nodes (38): calculate_area(), check_all_inputs(), check_climate_data(), check_soil(), check_within_one(), get_geotiff_datatype(), get_geotiff_extent(), get_geotiff_resolution() (+30 more)

### Community 5 - "DomainValidationError"
Cohesion: 0.10
Nodes (30): DomainValidationError, ValueError, Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring() (+22 more)

### Community 6 - "farm_management/infrastructure/postgresql_repositories.py"
Cohesion: 0.13
Nodes (22): Base, DeclarativeBase, SQLAlchemy metadata owned by Farm Management Infrastructure., Declarative base for Farm Management persistence records., Farm Management infrastructure layer., ParcelRecord, ParcelVersionRecord, ProjectRecord (+14 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.10
Nodes (22): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+14 more)

### Community 9 - "workflow.py"
Cohesion: 0.09
Nodes (26): IDefaultViabilityPolicyProvider, Provide the current VIA default viability policy without owning its storage., EvaluateConfiguredDecisionSupport, EvaluateDecisionSupport, StrEnum, Decision Support application query messages., Prepare evidence and apply one explicitly versioned policy when possible., How the viability policy configuration is selected for one execution. (+18 more)

### Community 10 - "data_tools.py"
Cohesion: 0.10
Nodes (35): Combines climate suitability with soil/terrain data to calculate final crop…, Interpolates or retrieves downscaled climate data (precipitation and…, aggregate_soil_raster_lst(), get_soil_data(), Get soil data based on specified climate configuration parameters. Parameters:…, Aggregate soil raster data from a list of files based on specified parameters.…, extract_domain_from_global_3draster(), extract_domain_from_global_raster() (+27 more)

### Community 11 - "DownloadCMIP6Data"
Cohesion: 0.09
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+9 more)

### Community 12 - "PostgreSQLEvaluationRepository"
Cohesion: 0.13
Nodes (51): EnvironmentalInputReference, Caller-selected exact environmental dataset version., PostgreSQLEvaluationRepository, SessionFactory, Durable adapter for immutable Evaluation aggregates., clean_evaluations(), _common_support(), _comparable_crops() (+43 more)

### Community 13 - "climate_suitability_main_xarray.py"
Cohesion: 0.09
Nodes (32): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+24 more)

### Community 14 - "CropSuiteLite"
Cohesion: 0.13
Nodes (11): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Calculates climate suitability based on temperature and precipitation.…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Calculates grid tiling based on available RAM to prevent memory overflow.…, Private subprocess entry point; each invocation has its own working directory. (+3 more)

### Community 15 - "test_migration_host.py"
Cohesion: 0.19
Nodes (19): main(), Run the explicit release migration CLI., _configure_valid_production(), CaptureFixture, MonkeyPatch, parametrize, Path, Focused tests for the explicit VIA release migration host. (+11 more)

### Community 16 - "climate_suitability_main.py"
Cohesion: 0.07
Nodes (39): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+31 more)

### Community 17 - "InMemoryEvaluationRepository"
Cohesion: 0.06
Nodes (68): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Logger, Mark an operator-confirmed active orphan as failed without retrying it., InvalidCommandError, LookupError, ValueError (+60 more)

### Community 18 - "CoverageMeasurement"
Cohesion: 0.14
Nodes (24): CheckDatasetVersionCoverage, CoverageClassification, CoverageCompatibilityFailure, CoverageMeasurement, StrEnum, Structural metadata prevented a meaningful spatial measurement., Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port. (+16 more)

### Community 19 - "decision_support/domain/models.py"
Cohesion: 0.10
Nodes (29): DomainValidationError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Decision Support domain layer., CommonSupportEvidence, CropViabilityAssessment, DecisionEvidence (+21 more)

### Community 20 - "test_farm_management_postgresql.py"
Cohesion: 0.22
Nodes (21): PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., clean_farm_management(), database(), _database_url(), _parcel(), _polygon() (+13 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management persistence"
Cohesion: 0.12
Nodes (20): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, Optimistic parcel revision transaction, ParcelVersionConflictError, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations (+12 more)

### Community 23 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.14
Nodes (37): Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records., CropOutcomeRecord, EvaluationCommonSupportRecord, EvaluationComparableCropRecord, EvaluationCropRecord (+29 more)

### Community 24 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.20
Nodes (10): Common-Support Ranking, ADR-002 Layered Bounded Contexts, ADR-003 Commands and Queries in Application, ADR-005 Background Worker, ADR-007 Initial Deployment, ADR-009 Multicrop Evaluation, Architecture and Backend for CropSuiteLite Huaura v2, Celery (+2 more)

### Community 25 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 26 - "scientific_artifact_store.py"
Cohesion: 0.14
Nodes (20): _file_identity(), _is_within(), PublishedScientificArtifact, Path, Protocol, RuntimeError, Durable filesystem storage for scientific artifacts., Base error for durable scientific artifact storage failures. (+12 more)

### Community 27 - "test_architecture.py"
Cohesion: 0.15
Nodes (16): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+8 more)

### Community 28 - "Farm Management schema ownership"
Cohesion: 0.20
Nodes (10): Farm Management schema ownership, Projects, parcels, and parcel_versions tables, farm_management schema and owned tables, Optional durable repository adapter, Project, Parcel, and ParcelVersion domain model, Result querying increment, Bounded-context ownership and Farm Management repositories, Farm Management ownership query (+2 more)

### Community 29 - "Bounded-context layered structure"
Cohesion: 0.28
Nodes (9): Bounded-context ownership, Anti-corruption layer, Application layer, Bounded-context layered structure, Domain layer, Illustrative Evaluation module structure, Infrastructure layer, Interfaces layer (+1 more)

### Community 30 - "Python and FastAPI backend decision"
Cohesion: 0.22
Nodes (14): Multicrop Parcel Evaluation, run_evaluation Service, ADR-004 CropSuiteLite Port and Adapter, ADR-008 Sequential Crop Execution, Background worker execution, CropSuiteLite isolation boundary, FastAPI, Python (+6 more)

### Community 31 - "AgroclimaticEvaluationExecutionService"
Cohesion: 0.17
Nodes (34): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, Execute requested crops and summarize them through Application-owned ports., _artifact(), _environmental_information_for(), _evaluation(), _execute() (+26 more)

### Community 32 - "Farm Management minimum vertical slice"
Cohesion: 0.13
Nodes (13): ADR-011: PostgreSQL/PostGIS persistence for Farm Management, Consequences, Context, Decision, Status, Architectural alignment, Slice exclusions and authorization dependency, Explicit exclusions and provisional choices (+5 more)

### Community 33 - "Application commands and queries"
Cohesion: 0.29
Nodes (8): Application commands and queries, FastAPI composition root, In-memory and durable Infrastructure adapters, Project and parcel HTTP resources, Farm Management repository abstractions, Transport-to-domain path, ProjectRepository, ParcelRepository, and in-memory adapters, Repository ports and in-memory adapters query

### Community 34 - "main"
Cohesion: 0.08
Nodes (23): WorkerRunSummary, main(), make_shutdown_handler(), Logger, Poll until cooperative shutdown, waiting only after a non-full batch., Return a signal handler that only requests cooperative process shutdown., run_forever(), CaptureFixture (+15 more)

### Community 35 - "VIA architecture implementation roadmap"
Cohesion: 0.13
Nodes (16): Domain dependency rule, Layered modular monolith, Inward dependency direction, Architecture source and PoC preservation, Cross-stage architecture gates, Explanation and comparison increment, Modeling increment, Modular foundation increment (+8 more)

### Community 36 - "Evaluation"
Cohesion: 0.06
Nodes (26): Exception, Explicit fail-only recovery for abandoned evaluation executions., ActiveEvaluationResult, EvaluationConflictError, InvalidEvaluationTransitionError, RuntimeError, Domain errors for Agroclimatic Evaluation., Raised when an Evaluation lifecycle transition is not allowed. (+18 more)

### Community 37 - "ConfiguredEnvironmentalInputIntegrityVerifier"
Cohesion: 0.29
Nodes (18): ConfiguredEnvironmentalInputIntegrityVerifier, Verify manifests using deployment-configured exact dataset-version bindings., _binding(), _fingerprints(), _manifest(), parametrize, ScientificSourceFingerprint, UUID (+10 more)

### Community 38 - "test_agroclimatic_environmental_inputs.py"
Cohesion: 0.18
Nodes (22): parametrize, Focused domain tests for immutable environmental input manifests., _snapshot(), test_environmental_input_manifest_accepts_valid_inputs(), test_environmental_input_manifest_allows_same_version_for_distinct_input_keys(), test_environmental_input_manifest_rejects_duplicate_input_key(), test_environmental_input_manifest_rejects_empty_inputs(), test_environmental_input_manifest_rejects_input_registered_after_resolution() (+14 more)

### Community 40 - "Q: PostgreSQL Farm Management repositories"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: PostgreSQL Farm Management repositories, Source Nodes

### Community 41 - "agroclimatic_evaluation/interfaces/http.py"
Cohesion: 0.16
Nodes (20): CommonSupportResponse, ComparableCropResponse, CropEvidenceResponse, CropOutcomeResponse, EnvironmentalInputReferenceBody, EvaluationEvidenceResponse, EvaluationResponse, EvaluationResultResponse (+12 more)

### Community 42 - "ADR-012: PostgreSQL/PostGIS persistence for Environmental Information"
Cohesion: 0.12
Nodes (18): ADR-012: PostgreSQL/PostGIS persistence for Environmental Information, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation, Decision Support (+10 more)

### Community 43 - "PostGIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "agroclimatic_evaluation/application/ports.py"
Cohesion: 0.07
Nodes (33): datetime, CropComparisonInput, CropSuitabilityEngineError, CropSuitabilityRequest, CropSuitabilityResult, EnvironmentalInputIntegrityError, ICropComparisonEngine, ICropSuitabilityEngine (+25 more)

### Community 45 - "test_agroclimatic_evaluation_queries.py"
Cohesion: 0.52
Nodes (6): _evaluation(), parametrize, Focused Application query tests for Agroclimatic Evaluation., _service(), test_finalized_public_contract_preserves_order_and_outcome_semantics(), test_public_contract_rejects_non_succeeded_evaluation()

### Community 46 - "Q: Verify that the new VIA backend foundation is discoverable and consistent with the intended architecture."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Verify that the new VIA backend foundation is discoverable and consistent with the intended architecture., Source Nodes

### Community 47 - "Q: optimistic stale-write handling introduced in the current slice"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: optimistic stale-write handling introduced in the current slice, Source Nodes

### Community 48 - "Q: repository ports and current in-memory adapters"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: repository ports and current in-memory adapters, Source Nodes

### Community 49 - "Q: Farm Management ownership and persistence boundaries"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Farm Management ownership and persistence boundaries, Source Nodes

### Community 50 - "Q: dependency direction involving Domain, Application and Infrastructure"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: dependency direction involving Domain, Application and Infrastructure, Source Nodes

### Community 51 - "Q: Project, Parcel, ParcelVersion, ParcelGeometry"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Project, Parcel, ParcelVersion, ParcelGeometry, Source Nodes

### Community 52 - "Q: Continue the Farm Management durable persistence increment from the current repository state"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Continue the Farm Management durable persistence increment from the current repository state, Source Nodes

### Community 54 - "CropSuiteLite Python Dependency Manifest"
Cohesion: 0.50
Nodes (4): CropSuiteLite Python Dependency Manifest, Geospatial Processing Stack, Runtime and Utility Stack, Scientific Computing Stack

### Community 55 - "download_soilgrids_huaura.py"
Cohesion: 0.83
Nodes (3): crop_reproject(), get_vrt(), main()

### Community 56 - "Knowledge Graph Pipeline"
Cohesion: 0.67
Nodes (3): Graphify, Honest Audit Trail, Knowledge Graph Pipeline

### Community 59 - "Atlas A Logo"
Cohesion: 0.67
Nodes (3): Atlas A Logo, Atlas Branding, Stylized Green Letter A

### Community 63 - "ViabilityPolicySnapshot"
Cohesion: 0.09
Nodes (20): DefaultViabilityPolicyNotConfiguredError, LookupError, Raised when VIA has no default viability policy configured., PolicyVersionConflictError, RuntimeError, Raised when one immutable policy reference is bound to different thresholds., Immutable identity and exact thresholds used for a policy execution., ViabilityPolicySnapshot (+12 more)

### Community 64 - "nc_tools.py"
Cohesion: 0.22
Nodes (12): create_cog_from_geotiff(), geotiff_to_smallest_datatype(), Convert image to COG., merge_outputs_no_overlap(), get_netcdf_extent(), merge_netcdf_files(), downscaled_files: list of netcdf files overlap: In Degree extent: [North, Left,…, Get the spatial extent (min and max) of the latitude and longitude in a NetCDF… (+4 more)

### Community 65 - "agroclimatic_evaluation/application/service.py"
Cohesion: 0.18
Nodes (18): FinalizedCommonSupport, FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedEvaluationResult, FinalizedEvaluationResultReader, FinalizedScientificTrace, FinalizedSuitabilitySummary, GetFinalizedEvaluationResult (+10 more)

### Community 67 - "DatasetVersion"
Cohesion: 0.09
Nodes (22): CoverageComputation, Environmental Information domain layer., DatasetVersion, Immutable reproducibility metadata for one dataset release., DatasetRepository, DatasetVersionRepository, Protocol, UUID (+14 more)

### Community 68 - "Parcel"
Cohesion: 0.08
Nodes (23): ParcelVersionConflictError, RuntimeError, Domain errors raised by Farm Management invariants., Raised when persisted parcel history changed before a revision was saved., Farm Management domain layer., Parcel, Project, Farm Management domain model. (+15 more)

### Community 69 - "ComparableCrop"
Cohesion: 0.24
Nodes (16): ComparableCrop, One crop ranked on the exact common valid spatial support., _comparable_support(), _manifest(), parametrize, Domain tests for durable comparable crop results., _reference(), _snapshot() (+8 more)

### Community 70 - "require_test_database_url"
Cohesion: 0.19
Nodes (16): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., Read and validate the test-only database settings before any DB operation., require_test_database_url(), UnsafeTestDatabaseError, validate_test_database_url() (+8 more)

### Community 73 - "EnvironmentalInformationService"
Cohesion: 0.07
Nodes (47): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., InvalidSpatialInputError, Protocol, RuntimeError, ValueError (+39 more)

### Community 74 - "test_api_host.py"
Cohesion: 0.14
Nodes (19): ApiServerSettings, main(), Production HTTP process host for VIA., Provider-neutral Uvicorn bind settings for the production API process., Load API bind settings from the process environment., Validate production configuration and run one Uvicorn API process., _clear_api_environment(), _configure_production_persistence() (+11 more)

### Community 75 - "app.py"
Cohesion: 0.06
Nodes (38): Side-effect-free FastAPI application composition., DatasetVersionConflictError, RuntimeError, Domain errors raised by Environmental Information invariants., Raised when a dataset version identifier has already been registered., Dataset, Environmental Information domain model., Stable logical identity for a geoenvironmental dataset. (+30 more)

### Community 77 - "Q: ParcelVersion persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ParcelVersion persistence, Source Nodes

### Community 93 - "Q: Domain-to-Infrastructure dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Domain-to-Infrastructure dependency violations, Source Nodes

### Community 135 - "cropsuite_adapter.py"
Cohesion: 0.14
Nodes (35): CropSuitabilityExecutionError, InvalidEngineOutputError, Raised when the existing engine service cannot produce a report., Raised when the engine report does not satisfy the expected PoC contract., Current PoC parcel summary for the crop-suitability output., Durable opaque reference to one verified scientific artifact., An engine-reported failure, distinct from no coverage and a zero score., Trace metadata the current PoC can supply without invented versions. (+27 more)

### Community 136 - "Huaura scientific fixture recovery audit"
Cohesion: 0.08
Nodes (25): Benchmark compatibility, Boundary and reference mask, Climate, Current identity manifest, DEM, Executive status, Historical alternatives / abandoned paths, Huaura scientific fixture recovery audit (+17 more)

### Community 137 - "execution.py"
Cohesion: 0.13
Nodes (31): _comparison_request(), Synchronous application orchestration for persisted evaluations., _to_comparable_crop(), _to_outcome(), Portable grid identity needed to verify comparable scientific rasters., ScientificArtifactGrid, Transport-neutral Agroclimatic Evaluation results., Agroclimatic Evaluation domain layer. (+23 more)

### Community 138 - "Environmental Information coverage and compatibility"
Cohesion: 0.29
Nodes (6): Capability, Compatibility now, Coverage semantics, CRS and area policy, Deferred work, Environmental Information coverage and compatibility

### Community 139 - "Q: Confirm backend package and layer structure, Domain/Application/Infrastructure/Interfaces boundaries, current dependency rules, and verification configuration"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Confirm backend package and layer structure, Domain/Application/Infrastructure/Interfaces boundaries, current dependency rules, and verification configuration, Source Nodes

### Community 140 - "ADR-013: Extent coverage and CRS comparison"
Cohesion: 0.33
Nodes (5): ADR-013: Extent coverage and CRS comparison, Consequences, Context, Decision, Status

### Community 141 - "Q: dataset version coverage parcel geometry contract"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: dataset version coverage parcel geometry contract, Source Nodes

### Community 142 - "Q: Cross-context dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Cross-context dependency violations, Source Nodes

### Community 143 - "Q: Environmental Information persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Environmental Information persistence, Source Nodes

### Community 144 - "Q: Dataset and DatasetVersion"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Dataset and DatasetVersion, Source Nodes

### Community 145 - "Q: coverage classification dataset version geometry compatible"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: coverage classification dataset version geometry compatible, Source Nodes

### Community 146 - "Q: postgis transform crs geography coverage"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: postgis transform crs geography coverage, Source Nodes

### Community 147 - "Q: environmental information farm management imports dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: environmental information farm management imports dependency violations, Source Nodes

### Community 149 - "ADR-014: PostgreSQL/PostGIS persistence for Agroclimatic Evaluation"
Cohesion: 0.20
Nodes (9): ADR-006 Scientific Traceability, ADR-014: PostgreSQL/PostGIS persistence for Agroclimatic Evaluation, Consequences, Context, Decision, Source, Status, Immutable ParcelSnapshot (+1 more)

### Community 150 - "scientific_input_integrity.py"
Cohesion: 0.14
Nodes (19): CropSuiteEnvironmentalInputBinding, load_configured_environmental_input_integrity_verifier(), load_cropsuite_environmental_input_bindings(), _parse_uuid(), Any, Path, UUID, Configured binding between exact dataset versions and CropSuite source hashes. (+11 more)

### Community 151 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.19
Nodes (20): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+12 more)

### Community 152 - "test_decision_support.py"
Cohesion: 0.12
Nodes (43): FinalizedCommonSupportStatus, FinalizedComparableCrop, StrEnum, ComparableCropEvidence, A provider-produced crop mean and rank over common valid support., _common_support(), _decision_evidence(), _DefaultPolicyProvider (+35 more)

### Community 154 - "Production deployment runtime contract"
Cohesion: 0.17
Nodes (11): B2 reproducible Linux container image, B6.1 resource benchmark, B6 production-like Docker Compose smoke, B7 DigitalOcean single-Droplet deployment definition, Database and migration contract, Environment contract, Filesystem contract, Process responsibilities (+3 more)

### Community 155 - "GetPublishedDatasetVersion"
Cohesion: 0.37
Nodes (14): GetPublishedDatasetVersion, _dataset(), datetime, UUID, Public cross-context contract tests for Environmental Information., _service(), test_exact_dataset_and_version_returns_all_published_metadata(), test_missing_dataset_returns_none() (+6 more)

### Community 157 - "Settings"
Cohesion: 0.11
Nodes (27): Settings needed by the current backend composition root., Require the durable persistence contract used by the production API., Settings for the PostgreSQL polling worker process., Settings, WorkerSettings, MonkeyPatch, parametrize, Path (+19 more)

### Community 158 - "EvaluationResult"
Cohesion: 0.20
Nodes (9): CropOutcomeResult, EvaluationResult, ParcelSnapshotResult, RuntimeError, Raised when an evaluation identity already exists., ResourceConflictError, EvaluationExecutor, Protocol (+1 more)

### Community 159 - "CropSuite.py"
Cohesion: 0.11
Nodes (27): # NOTE: self.extent is modified here to align with grid, calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):… (+19 more)

### Community 160 - "FarmManagementService"
Cohesion: 0.17
Nodes (11): ParcelResult, ParcelVersionResult, ProjectResult, Transport-neutral results returned by Farm Management use cases., FarmManagementService, InvalidCommandError, datetime, UUID (+3 more)

### Community 161 - ".from_geojson"
Cohesion: 0.17
Nodes (18): _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing, MultiPolygonCoordinates, PolygonCoordinates (+10 more)

### Community 162 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.20
Nodes (28): _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any, FastAPI (+20 more)

### Community 163 - "test_cropsuite_adapter.py"
Cohesion: 0.18
Nodes (37): CropExecutionStatus, Scientific outcomes reported independently of Evaluation lifecycle state., CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability., _adapter(), _environmental_input_manifest(), _integrity_verifier(), Any (+29 more)

### Community 164 - "Agroclimatic Evaluation request, worker, recovery, and read slice"
Cohesion: 0.15
Nodes (11): ADR-015: PostgreSQL polling for Agroclimatic Evaluation worker dispatch, Consequences, Context, Decision, Status, Agroclimatic Evaluation request, worker, recovery, and read slice, Current lifecycle and execution, Deliberately deferred (+3 more)

### Community 165 - "Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation, Source Nodes

### Community 166 - "Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors, Source Nodes

### Community 167 - "environmental_information/interfaces/http.py"
Cohesion: 0.12
Nodes (25): CheckCoverageBody, CoverageGeometryBody, create_router(), check_dataset_version_coverage(), create_dataset(), create_dataset_version(), get_dataset(), get_dataset_version() (+17 more)

### Community 170 - "crop_suitability_main.py"
Cohesion: 0.18
Nodes (16): calcification_map(), cropsuitability(), get_suitability_val_dict(), get_texture_class(), get_valid_dtype(), getTable(), output_param_data(), ndarray (+8 more)

### Community 172 - "SpatialExtent"
Cohesion: 0.20
Nodes (16): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine (+8 more)

### Community 174 - "cropsuite_comparison_adapter.py"
Cohesion: 0.26
Nodes (19): CommonSupportStatus, ComparableCropResult, InvalidComparisonOutputError, StrEnum, Scientific common-support outcome across evaluated crops., One crop summarized on the exact common spatial support., Raised when scientific comparison returns an invalid contract., _fraction() (+11 more)

### Community 175 - "Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment., Source Nodes

### Community 176 - "CropSuiteComparisonAdapter"
Cohesion: 0.30
Nodes (17): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., _artifact(), Any, Path, _report(), _request(), _snapshot() (+9 more)

### Community 177 - "PolicyReference"
Cohesion: 0.09
Nodes (36): DefaultViabilityPolicyConflictError, InvalidViabilityPolicyRevisionError, RuntimeError, ValueError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist., Raised when a requested viability-policy revision is not a new version., Raised when the default policy changed before an expected update. (+28 more)

### Community 178 - "config.py"
Cohesion: 0.33
Nodes (7): _environment_float(), _environment_integer(), _is_same_or_within(), _optional_path(), Path, Environment-backed configuration for the VIA application host., _validate_scientific_path_topology()

### Community 180 - "DomainValidationError"
Cohesion: 0.16
Nodes (19): Application ports for Environmental Information spatial collaboration., CoverageGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing (+11 more)

### Community 181 - "Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract, Source Nodes

### Community 182 - "create_router"
Cohesion: 0.18
Nodes (18): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Commands expressing Agroclimatic Evaluation use-case intent., Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, ListEvaluations, create_router(), get_evaluation() (+10 more)

### Community 183 - "test_decision_support_postgresql.py"
Cohesion: 0.17
Nodes (30): Decision Support infrastructure adapters., PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+22 more)

### Community 184 - "env.py"
Cohesion: 0.47
Nodes (5): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online()

### Community 185 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 187 - "verify_runtime"
Cohesion: 0.36
Nodes (10): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_read_only_directory(), _require_read_only_file(), _require_writable_directory(), _run_cropsuite_import_smoke() (+2 more)

### Community 188 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.23
Nodes (14): Agroclimatic Evaluation application layer., _availability(), CommonSupportReadResult, ComparableCropReadResult, CropEvidenceResult, EvaluationEvidenceResult, EvaluationReadResult, EvaluationResultAvailability (+6 more)

### Community 189 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 191 - "benchmark_production_runtime.sh"
Cohesion: 0.19
Nodes (16): artifact_bytes_for_evaluation(), COMPOSE_PROJECT_NAME, database_size_bytes(), fail(), monotonic_ns(), post_json(), record_stack_sample(), require_command() (+8 more)

### Community 192 - "create_app"
Cohesion: 0.32
Nodes (6): create_app(), create_production_app(), FastAPI, Build the production API after enforcing durable persistence settings., Build the VIA API and register its technical interfaces., Development-compatible ASGI module.

### Community 193 - "migrate.py"
Cohesion: 0.23
Nodes (11): _build_parser(), ArgumentParser, Path, One-shot production schema migration host for VIA releases., Return the repository-local Alembic config when running from source., Resolve the Alembic config without depending on the process cwd., Validate production persistence and migrate the schema to Alembic head., _require_production_postgresql() (+3 more)

### Community 195 - "test_digitalocean_deployment_contract.py"
Cohesion: 0.36
Nodes (9): _read(), _service_block(), test_deployment_script_enforces_release_order_without_destructive_cleanup(), test_deployment_script_requires_stable_worker_liveness_across_poll_intervals(), test_digitalocean_compose_preserves_runtime_and_durability_contracts(), test_docker_build_context_excludes_scientific_data(), test_ghcr_publish_is_gated_by_successful_b2_b6_run_for_same_commit(), test_provider_files_do_not_embed_secrets_or_raw_huaura_paths() (+1 more)

### Community 196 - "deploy_digitalocean.sh"
Cohesion: 0.57
Nodes (7): fail(), require_command(), require_directory(), deploy_digitalocean.sh script, verify_worker_liveness(), VIA_IMAGE, wait_for_health()

### Community 197 - "verify_production_compose.sh"
Cohesion: 0.60
Nodes (4): assert_running(), assert_worker_liveness(), container_id(), verify_production_compose.sh script

### Community 198 - "AgroclimaticEvaluationService"
Cohesion: 0.22
Nodes (10): GetEvaluation, GetEvaluationEvidence, GetEvaluationResult, Queries supported by Agroclimatic Evaluation., EvaluationStatusResult, AgroclimaticEvaluationService, datetime, UUID (+2 more)

### Community 199 - "process_precday_interp"
Cohesion: 0.16
Nodes (5): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall., PrecipitationUnitsTest

### Community 201 - "DomainValidationError"
Cohesion: 0.12
Nodes (15): EnvironmentalInputResolutionError, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved., EnvironmentalInputSnapshot, _is_finite_number(), datetime, Immutable environmental input snapshots owned by Agroclimatic Evaluation., Historical environmental input metadata captured for one evaluation input. (+7 more)

### Community 205 - "via_backend/worker.py"
Cohesion: 0.15
Nodes (14): create_database(), Engine, SessionFactory, Create the shared engine and short-lived session factory., Shared technical infrastructure used by the application composition root., create_worker(), list_active_evaluations(), _parser() (+6 more)

### Community 206 - "FilesystemScientificArtifactStore"
Cohesion: 0.30
Nodes (14): FilesystemScientificArtifactStore, Filesystem-backed immutable artifact store., parametrize, Path, test_publish_creates_durable_artifact_with_opaque_reference(), test_publish_is_idempotent_for_identical_content(), test_publish_rejects_content_that_does_not_match_expected_checksum(), test_publish_rejects_different_content_for_existing_reference() (+6 more)

### Community 207 - "CropComparisonRequest"
Cohesion: 0.22
Nodes (8): CommonSupportResult, CropComparisonRequest, CropComparisonResult, Compare crop suitability only on identical valid spatial support., Scientific support shared by all usable crop suitability rasters., Checked multicrop comparison returned by the scientific boundary., StubComparisonEngine, test_comparison_engine_contract_is_runtime_checkable()

### Community 208 - "test_environmental_information_postgresql.py"
Cohesion: 0.33
Nodes (12): clean_environmental_information(), database(), _database_url(), _dataset(), Engine, fixture, SessionFactory, PostgreSQL/PostGIS integration tests for Environmental Information. (+4 more)

### Community 209 - "CommonSupport"
Cohesion: 0.22
Nodes (8): _to_common_support(), CommonSupport, CommonSupportStatus, StrEnum, Evaluation-level scientific common-support result., Validate deterministic scientific ranking semantics., Spatial support shared by the usable crop suitability rasters., validate_comparable_crops()

### Community 210 - "CropComparisonExecutionError"
Cohesion: 0.24
Nodes (8): CropComparisonEngineError, CropComparisonExecutionError, RuntimeError, Base error for the scientific crop-comparison boundary., Raised when scientific common-support comparison cannot execute., _is_within(), Path, ComparisonRunner

### Community 211 - "health.py"
Cohesion: 0.40
Nodes (4): health(), Host-level health endpoint., Report that the API process is ready to receive requests., get

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **220 isolated node(s):** `via-backend`, `backup_postgres.sh script`, `VIA_IMAGE`, `VIA_BENCHMARK_SOURCE_DIR`, `VIA_BENCHMARK_RUNTIME_CONFIG_DIR` (+215 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 994 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `Domain dependency rule` (5× useful, score=4.693450858)
- `Application layer` (4× useful, score=3.751913588)
- `EnvironmentalInformationService` (3× useful, score=2.835517884) _(code changed — re-verify)_
- `ParcelGeometry` (3× useful, score=2.828113307)
- `ParcelVersion` (3× useful, score=2.804591321)
- `InMemoryParcelRepository` (3× useful, score=2.803347018)
- `ParcelRepository` (3× useful, score=2.803347017)
- `EvaluationResult` (2× useful, score=1.955274885) _(code changed — re-verify)_
- `Settings` (2× useful, score=1.948868371) _(code changed — re-verify)_
- `Farm Management schema ownership` (2× useful, score=1.909664433)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Crop Code Catalog` and `Undefined Crop Code c32`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `create_app()` connect `create_app` to `FarmManagementService`, `farm_management/application/service.py`, `test_agroclimatic_evaluation_api.py`, `Parcel`, `AgroclimaticEvaluationService`, `environmental_information/interfaces/http.py`, `farm_management/infrastructure/postgresql_repositories.py`, `EnvironmentalInformationService`, `app.py`, `PostgreSQLEvaluationRepository`, `via_backend/worker.py`, `InMemoryEvaluationRepository`, `test_farm_management_postgresql.py`, `create_router`, `test_farm_management_api.py`, `test_environmental_information_api.py`, `Settings`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `create_app`, `DatasetVersion`, `environmental_information/interfaces/http.py`, `app.py`, `SpatialExtent`, `via_backend/worker.py`, `CoverageMeasurement`, `DomainValidationError`, `GetPublishedDatasetVersion`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `Evaluation` connect `Evaluation` to `agroclimatic_evaluation/application/service.py`, `test_agroclimatic_evaluation_api.py`, `.from_geojson`, `ComparableCrop`, `AgroclimaticEvaluationService`, `execution.py`, `DomainValidationError`, `agroclimatic_evaluation/application/ports.py`, `PostgreSQLEvaluationRepository`, `test_agroclimatic_evaluation_queries.py`, `CommonSupport`, `InMemoryEvaluationRepository`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `test_agroclimatic_evaluation_domain.py`, `agroclimatic_evaluation/application/__init__.py`, `EvaluationResult`, `AgroclimaticEvaluationExecutionService`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `PostgreSQLEvaluationRepository` (e.g. with `EvaluationConflictError` and `Evaluation`) actually correct?**
  _`PostgreSQLEvaluationRepository` has 9 INFERRED edges - model-reasoned connections that need verification._