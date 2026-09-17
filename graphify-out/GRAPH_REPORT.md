# Graph Report - poc_via_cslite  (2026-09-17)

## Corpus Check
- 312 files · ~156,172 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2934 nodes · 7219 edges · 207 communities (124 shown, 31 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 874 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2ab68fde`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- farm_management/application/service.py
- run_cropsuitelite.py
- NexGenPreProcessing
- Huaura Dataset Preprocessing Configuration
- check_files.py
- DomainValidationError
- Parcel
- Crop Membership Functions
- multicrop.py
- ViabilityPolicySnapshot
- data_tools.py
- DownloadCMIP6Data
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- climate_suitability_main_xarray.py
- CropSuiteLite
- test_migration_host.py
- climate_suitability_main.py
- test_agroclimatic_evaluation_worker.py
- CoverageMeasurement
- decision_support/domain/models.py
- test_farm_management_postgresql.py
- VIA architecture guardrails
- Farm Management persistence
- read_plant_params.py
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
- test_environmental_coverage.py
- EnvironmentalInputManifest
- Q: PostgreSQL Farm Management repositories
- agroclimatic_evaluation/interfaces/http.py
- ADR-012: PostgreSQL/PostGIS persistence for Environmental Information
- PostGIS service
- CropSuitabilityRequest
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
- decision_support/infrastructure/postgresql_repositories.py
- nc_tools.py
- decision_support/application/service.py
- agroclimatic_evaluation/__init__.py
- DatasetVersion
- Project
- DomainValidationError
- test_database_test_support.py
- decision_support/__init__.py
- decision_support/interfaces/__init__.py
- EnvironmentalInformationService
- test_api_host.py
- environmental_information/infrastructure/postgresql_repositories.py
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
- test_config.py
- app.py
- ResourceConflictError
- CropSuite.py
- FarmManagementService
- ParcelSnapshot
- test_agroclimatic_evaluation_api.py
- test_cropsuite_adapter.py
- Agroclimatic Evaluation request, worker, recovery, and read slice
- Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation
- Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors
- environmental_information/interfaces/http.py
- crop_suitability_main.py
- create_database
- agroclimatic_evaluation/application/__init__.py
- Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment.
- via_backend/worker.py
- PolicyReference
- config.py
- DomainValidationError
- Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract
- AgroclimaticEvaluationService
- test_decision_support_postgresql.py
- InMemoryEvaluationRepository
- test_environmental_information_api.py
- verify_runtime
- run_forever
- test_farm_management_api.py
- benchmark_production_runtime.sh
- test_explicit_recovery_uses_expected_status
- test_create_worker_fails_fast_on_invalid_scientific_input_bindings
- test_container_image_contract.py
- test_digitalocean_deployment_contract.py
- deploy_digitalocean.sh
- verify_production_compose.sh
- write_to_netcdf
- test_resource_benchmark_contract.py
- environmental_inputs.py
- backup_postgres.sh
- AgroclimaticEvaluationRecoveryService
- test_environmental_information_postgresql.py
- health.py

## God Nodes (most connected - your core abstractions)
1. `Evaluation` - 90 edges
2. `DomainValidationError` - 63 edges
3. `PostgreSQLEvaluationRepository` - 51 edges
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

## Communities (207 total, 31 thin omitted)

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
Cohesion: 0.09
Nodes (33): DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+25 more)

### Community 6 - "Parcel"
Cohesion: 0.08
Nodes (35): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online(), ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved. (+27 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.10
Nodes (22): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+14 more)

### Community 9 - "ViabilityPolicySnapshot"
Cohesion: 0.10
Nodes (20): IDefaultViabilityPolicyProvider, Protocol, Provide the current VIA default viability policy without owning its storage., EvaluateConfiguredDecisionSupport, StrEnum, Decision Support application query messages., How the viability policy configuration is selected for one execution., Select either VIA's current default policy or an explicit custom snapshot. (+12 more)

### Community 10 - "data_tools.py"
Cohesion: 0.14
Nodes (26): Combines climate suitability with soil/terrain data to calculate final crop…, Interpolates or retrieves downscaled climate data (precipitation and…, extract_domain_from_global_3draster(), extract_domain_from_global_raster(), get_cpu_ram(), get_resolution_array(), get_shape_of_raster(), interpolate_nanmask() (+18 more)

### Community 11 - "DownloadCMIP6Data"
Cohesion: 0.09
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+9 more)

### Community 12 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.07
Nodes (91): EnvironmentalInputReference, Caller-selected exact environmental dataset version., EvaluationConflictError, Raised when an evaluation identity already exists., Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records. (+83 more)

### Community 13 - "climate_suitability_main_xarray.py"
Cohesion: 0.10
Nodes (31): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+23 more)

### Community 14 - "CropSuiteLite"
Cohesion: 0.13
Nodes (11): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Calculates climate suitability based on temperature and precipitation.…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Calculates grid tiling based on available RAM to prevent memory overflow.…, Private subprocess entry point; each invocation has its own working directory. (+3 more)

### Community 15 - "test_migration_host.py"
Cohesion: 0.11
Nodes (30): _build_parser(), main(), ArgumentParser, Path, One-shot production schema migration host for VIA releases., Return the repository-local Alembic config when running from source., Resolve the Alembic config without depending on the process cwd., Validate production persistence and migrate the schema to Alembic head. (+22 more)

### Community 16 - "climate_suitability_main.py"
Cohesion: 0.09
Nodes (31): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+23 more)

### Community 17 - "test_agroclimatic_evaluation_worker.py"
Cohesion: 0.18
Nodes (24): AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application., _artifact(), _engine_result(), _evaluation(), _executor(), FakeComparisonEngine, FakeEngine (+16 more)

### Community 18 - "CoverageMeasurement"
Cohesion: 0.16
Nodes (22): CheckDatasetVersionCoverage, CoverageClassification, CoverageCompatibilityFailure, CoverageMeasurement, StrEnum, Structural metadata prevented a meaningful spatial measurement., Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port. (+14 more)

### Community 19 - "decision_support/domain/models.py"
Cohesion: 0.11
Nodes (28): DomainValidationError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Decision Support domain layer., CommonSupportEvidence, CropViabilityAssessment, DecisionEvidence (+20 more)

### Community 20 - "test_farm_management_postgresql.py"
Cohesion: 0.21
Nodes (22): PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel() (+14 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management persistence"
Cohesion: 0.12
Nodes (20): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, Optimistic parcel revision transaction, ParcelVersionConflictError, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations (+12 more)

### Community 23 - "read_plant_params.py"
Cohesion: 0.15
Nodes (10): get_formula(), get_id_list_start(), get_plant_param_interp_forms_dict(), print_crop_param_output(), print_sections(), Prints the keys of a given dictionary as a list of sections or items. Args:…, Given two arrays of numerical values x_vals and y_vals representing data…, Prints the number of crop parameterizations found and the keys of a given… (+2 more)

### Community 24 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.20
Nodes (10): Common-Support Ranking, ADR-002 Layered Bounded Contexts, ADR-003 Commands and Queries in Application, ADR-005 Background Worker, ADR-007 Initial Deployment, ADR-009 Multicrop Evaluation, Architecture and Backend for CropSuiteLite Huaura v2, Celery (+2 more)

### Community 25 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 26 - "scientific_artifact_store.py"
Cohesion: 0.10
Nodes (32): _file_identity(), _is_within(), PublishedScientificArtifact, Path, Protocol, RuntimeError, Durable filesystem storage for scientific artifacts., Base error for durable scientific artifact storage failures. (+24 more)

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
Cohesion: 0.10
Nodes (53): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, Execute requested crops and summarize them through Application-owned ports., GetPublishedDatasetVersion, PublishedDatasetVersion, PublishedDatasetVersionReader, Protocol (+45 more)

### Community 32 - "Farm Management minimum vertical slice"
Cohesion: 0.13
Nodes (13): ADR-011: PostgreSQL/PostGIS persistence for Farm Management, Consequences, Context, Decision, Status, Architectural alignment, Slice exclusions and authorization dependency, Explicit exclusions and provisional choices (+5 more)

### Community 33 - "Application commands and queries"
Cohesion: 0.29
Nodes (8): Application commands and queries, FastAPI composition root, In-memory and durable Infrastructure adapters, Project and parcel HTTP resources, Farm Management repository abstractions, Transport-to-domain path, ProjectRepository, ParcelRepository, and in-memory adapters, Repository ports and in-memory adapters query

### Community 34 - "main"
Cohesion: 0.12
Nodes (15): main(), make_shutdown_handler(), Logger, Return a signal handler that only requests cooperative process shutdown., CaptureFixture, MonkeyPatch, Fast tests for the VIA worker process host and operator CLI., test_active_cli_emits_only_safe_stable_fields() (+7 more)

### Community 35 - "VIA architecture implementation roadmap"
Cohesion: 0.13
Nodes (16): Domain dependency rule, Layered modular monolith, Inward dependency direction, Architecture source and PoC preservation, Cross-stage architecture gates, Explanation and comparison increment, Modeling increment, Modular foundation increment (+8 more)

### Community 36 - "Evaluation"
Cohesion: 0.08
Nodes (10): InvalidEvaluationTransitionError, RuntimeError, Raised when an Evaluation lifecycle transition is not allowed., Evaluation, An immutable multicrop evaluation and its scientific outcomes., UUID, _validate_limit(), UUID (+2 more)

### Community 37 - "test_environmental_coverage.py"
Cohesion: 0.18
Nodes (8): calculate_slope(), process_tempday_interp(), covered_gradient(), Spatial operations that preserve missing coverage instead of creating zeros., Central differences inside coverage, one-sided at its boundary. An axis with no…, Temporarily nearest-fill gaps, resample, then restore the coverage mask., resample_valid(), EnvironmentalCoverageTest

### Community 38 - "EnvironmentalInputManifest"
Cohesion: 0.06
Nodes (67): EnvironmentalInputResolutionError, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved., EnvironmentalInputManifest, EnvironmentalInputSnapshot, Immutable set of exact environmental inputs resolved for an evaluation., Historical environmental input metadata captured for one evaluation input., ConfiguredEnvironmentalInputIntegrityVerifier (+59 more)

### Community 40 - "Q: PostgreSQL Farm Management repositories"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: PostgreSQL Farm Management repositories, Source Nodes

### Community 41 - "agroclimatic_evaluation/interfaces/http.py"
Cohesion: 0.09
Nodes (34): _availability(), CommonSupportReadResult, ComparableCropReadResult, CropEvidenceResult, EvaluationEvidenceResult, EvaluationResultAvailability, PersistedCropOutcomeResult, StrEnum (+26 more)

### Community 42 - "ADR-012: PostgreSQL/PostGIS persistence for Environmental Information"
Cohesion: 0.12
Nodes (18): ADR-012: PostgreSQL/PostGIS persistence for Environmental Information, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation, Decision Support (+10 more)

### Community 43 - "PostGIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "CropSuitabilityRequest"
Cohesion: 0.20
Nodes (8): datetime, CropSuitabilityRequest, CropSuitabilityResult, ICropSuitabilityEngine, Protocol, One checked per-crop outcome from the scientific boundary., Evaluate one crop without exposing engine process or filesystem details., Transport-neutral input for evaluating one crop against an exact snapshot.

### Community 45 - "test_agroclimatic_evaluation_queries.py"
Cohesion: 0.44
Nodes (8): _evaluation(), _outcome(), parametrize, Focused Application query tests for Agroclimatic Evaluation., _service(), test_finalized_public_contract_preserves_order_and_outcome_semantics(), test_public_contract_rejects_non_succeeded_evaluation(), test_query_messages_return_read_only_views_without_mutation()

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

### Community 63 - "decision_support/infrastructure/postgresql_repositories.py"
Cohesion: 0.09
Nodes (23): DefaultViabilityPolicyConflictError, DefaultViabilityPolicyNotConfiguredError, LookupError, RuntimeError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist., Raised when VIA has no default viability policy configured., Raised when the default policy changed before an expected update. (+15 more)

### Community 64 - "nc_tools.py"
Cohesion: 0.22
Nodes (12): create_cog_from_geotiff(), geotiff_to_smallest_datatype(), Convert image to COG., merge_outputs_no_overlap(), get_netcdf_extent(), merge_netcdf_files(), downscaled_files: list of netcdf files overlap: In Degree extent: [North, Left,…, Get the spatial extent (min and max) of the latitude and longitude in a NetCDF… (+4 more)

### Community 65 - "decision_support/application/service.py"
Cohesion: 0.09
Nodes (32): FinalizedCommonSupport, FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedEvaluationResult, FinalizedEvaluationResultReader, FinalizedScientificTrace, FinalizedSuitabilitySummary, GetFinalizedEvaluationResult (+24 more)

### Community 67 - "DatasetVersion"
Cohesion: 0.08
Nodes (22): CoverageComputation, DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., Dataset, DatasetVersion, Stable logical identity for a geoenvironmental dataset., Immutable reproducibility metadata for one dataset release. (+14 more)

### Community 68 - "Project"
Cohesion: 0.13
Nodes (10): Project, An agricultural project that groups parcels., ParcelRepository, ProjectRepository, Protocol, UUID, Repository abstractions for Farm Management aggregates., _project_from_record() (+2 more)

### Community 69 - "DomainValidationError"
Cohesion: 0.10
Nodes (38): CommonSupport, CommonSupportStatus, ComparableCrop, normalize_common_support_measurements(), StrEnum, Evaluation-level scientific common-support result., One crop ranked on the exact common valid spatial support., Normalize impossible boundary overshoots caused only by float noise. (+30 more)

### Community 70 - "test_database_test_support.py"
Cohesion: 0.22
Nodes (14): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., UnsafeTestDatabaseError, validate_test_database_url(), CaptureFixture, parametrize (+6 more)

### Community 73 - "EnvironmentalInformationService"
Cohesion: 0.07
Nodes (49): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort, Stable contracts deliberately published to other bounded contexts. (+41 more)

### Community 74 - "test_api_host.py"
Cohesion: 0.14
Nodes (19): ApiServerSettings, main(), Production HTTP process host for VIA., Provider-neutral Uvicorn bind settings for the production API process., Load API bind settings from the process environment., Validate production configuration and run one Uvicorn API process., _clear_api_environment(), _configure_production_persistence() (+11 more)

### Community 75 - "environmental_information/infrastructure/postgresql_repositories.py"
Cohesion: 0.08
Nodes (31): InvalidSpatialInputError, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, Base (+23 more)

### Community 77 - "Q: ParcelVersion persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ParcelVersion persistence, Source Nodes

### Community 93 - "Q: Domain-to-Infrastructure dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Domain-to-Infrastructure dependency violations, Source Nodes

### Community 135 - "cropsuite_adapter.py"
Cohesion: 0.11
Nodes (41): CropSuitabilityExecutionError, IEnvironmentalInputIntegrityVerifier, InvalidEngineOutputError, Raised when the existing engine service cannot produce a report., Raised when the engine report does not satisfy the expected PoC contract., Verify resolved environmental provenance against scientific source fingerprints., Opaque scientific source identity and its engine-reported SHA-256., Current PoC parcel summary for the crop-suitability output. (+33 more)

### Community 136 - "Huaura scientific fixture recovery audit"
Cohesion: 0.08
Nodes (25): Benchmark compatibility, Boundary and reference mask, Climate, Current identity manifest, DEM, Executive status, Historical alternatives / abandoned paths, Huaura scientific fixture recovery audit (+17 more)

### Community 137 - "execution.py"
Cohesion: 0.07
Nodes (43): Commands expressing Agroclimatic Evaluation use-case intent., Synchronous application orchestration for persisted evaluations., _to_outcome(), Explicit fail-only recovery for abandoned evaluation executions., EvaluationResult, Transport-neutral Agroclimatic Evaluation results., datetime, UUID (+35 more)

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
Cohesion: 0.15
Nodes (11): CropSuitabilityEngineError, EnvironmentalInputIntegrityError, RuntimeError, Base error for failures to invoke or understand the engine boundary., Raised when resolved environmental provenance does not match scientific inputs., _parse_uuid(), UUID, Configured binding between exact dataset versions and CropSuite source hashes. (+3 more)

### Community 151 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.19
Nodes (20): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+12 more)

### Community 152 - "test_decision_support.py"
Cohesion: 0.13
Nodes (41): FinalizedCommonSupportStatus, FinalizedComparableCrop, ComparableCropEvidence, A provider-produced crop mean and rank over common valid support., _common_support(), _decision_evidence(), _DefaultPolicyProvider, _domain_common_support() (+33 more)

### Community 154 - "Production deployment runtime contract"
Cohesion: 0.17
Nodes (11): B2 reproducible Linux container image, B6.1 resource benchmark, B6 production-like Docker Compose smoke, B7 DigitalOcean single-Droplet deployment definition, Database and migration contract, Environment contract, Filesystem contract, Process responsibilities (+3 more)

### Community 155 - "test_config.py"
Cohesion: 0.24
Nodes (14): Settings for the PostgreSQL polling worker process., WorkerSettings, parametrize, Path, Tests for environment-driven application composition settings., _scientific_worker_settings(), test_production_settings_reject_memory_repository(), test_worker_run_requires_durable_artifact_root() (+6 more)

### Community 157 - "app.py"
Cohesion: 0.11
Nodes (20): create_app(), create_production_app(), FastAPI, Side-effect-free FastAPI application composition., Build the production API after enforcing durable persistence settings., Build the VIA API and register its technical interfaces., Settings needed by the current backend composition root., Require the durable persistence contract used by the production API. (+12 more)

### Community 158 - "ResourceConflictError"
Cohesion: 0.13
Nodes (14): Exception, _to_common_support(), _to_comparable_crop(), CropOutcomeResult, ParcelSnapshotResult, InvalidCommandError, LookupError, RuntimeError (+6 more)

### Community 159 - "CropSuite.py"
Cohesion: 0.15
Nodes (20): # NOTE: self.extent is modified here to align with grid, calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):… (+12 more)

### Community 160 - "FarmManagementService"
Cohesion: 0.17
Nodes (11): ParcelResult, ParcelVersionResult, ProjectResult, Transport-neutral results returned by Farm Management use cases., FarmManagementService, InvalidCommandError, datetime, UUID (+3 more)

### Community 161 - "ParcelSnapshot"
Cohesion: 0.13
Nodes (22): ParcelSnapshot, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing, MultiPolygonCoordinates (+14 more)

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
Cohesion: 0.22
Nodes (13): CheckCoverageBody, CoverageGeometryBody, CreateDatasetBody, CreateDatasetVersionBody, DatasetResponse, DatasetVersionCoverageResponse, DatasetVersionResponse, BaseModel (+5 more)

### Community 170 - "crop_suitability_main.py"
Cohesion: 0.13
Nodes (23): aggregate_soil_raster_lst(), calcification_map(), cropsuitability(), get_soil_data(), get_suitability_val_dict(), get_texture_class(), get_valid_dtype(), getTable() (+15 more)

### Community 172 - "create_database"
Cohesion: 0.17
Nodes (19): create_database(), Engine, SessionFactory, Create the shared engine and short-lived session factory., Shared technical infrastructure used by the application composition root., clean_tables(), database(), _database_url() (+11 more)

### Community 174 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.08
Nodes (45): _comparison_request(), Agroclimatic Evaluation application layer., CommonSupportResult, CommonSupportStatus, ComparableCropResult, CropComparisonEngineError, CropComparisonExecutionError, CropComparisonInput (+37 more)

### Community 175 - "Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment., Source Nodes

### Community 176 - "via_backend/worker.py"
Cohesion: 0.16
Nodes (29): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., Agroclimatic Evaluation infrastructure layer., FilesystemScientificArtifactStore, Filesystem-backed immutable artifact store., load_configured_environmental_input_integrity_verifier(), Build the configured verifier from one deployment binding file., create_worker() (+21 more)

### Community 177 - "PolicyReference"
Cohesion: 0.11
Nodes (26): InvalidViabilityPolicyRevisionError, ValueError, Raised when a requested viability-policy revision is not a new version., Application lifecycle for immutable Decision Support viability policies., Register one explicitly identified immutable viability-policy version., Create a new immutable version derived from an existing policy identity., Coordinate registration and revision of immutable policy snapshots., RegisterViabilityPolicyVersion (+18 more)

### Community 178 - "config.py"
Cohesion: 0.33
Nodes (7): _environment_float(), _environment_integer(), _is_same_or_within(), _optional_path(), Path, Environment-backed configuration for the VIA application host., _validate_scientific_path_topology()

### Community 180 - "DomainValidationError"
Cohesion: 0.09
Nodes (36): CoverageGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing, MultiPolygonCoordinates (+28 more)

### Community 181 - "Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract, Source Nodes

### Community 182 - "AgroclimaticEvaluationService"
Cohesion: 0.13
Nodes (25): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, GetEvaluation, GetEvaluationEvidence, GetEvaluationResult, ListEvaluations (+17 more)

### Community 183 - "test_decision_support_postgresql.py"
Cohesion: 0.17
Nodes (31): Decision Support infrastructure adapters., PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+23 more)

### Community 184 - "InMemoryEvaluationRepository"
Cohesion: 0.26
Nodes (13): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, InMemoryEvaluationRepository, _evaluation_in_status(), parametrize, test_active_discovery_filters_orders_limits_and_reports_counts(), test_active_discovery_requires_positive_integer_limit(), test_explicit_recovery_fails_active_evaluation_and_preserves_outcomes() (+5 more)

### Community 185 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 187 - "verify_runtime"
Cohesion: 0.36
Nodes (10): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_read_only_directory(), _require_read_only_file(), _require_writable_directory(), _run_cropsuite_import_smoke() (+2 more)

### Community 188 - "run_forever"
Cohesion: 0.21
Nodes (8): WorkerRunSummary, Poll until cooperative shutdown, waiting only after a non-full batch., run_forever(), test_run_forever_does_not_poll_again_after_stop_is_requested(), run_once(), test_run_forever_poll_wait_can_be_interrupted_by_stop(), run_once(), Event

### Community 189 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 191 - "benchmark_production_runtime.sh"
Cohesion: 0.19
Nodes (16): artifact_bytes_for_evaluation(), COMPOSE_PROJECT_NAME, database_size_bytes(), fail(), monotonic_ns(), post_json(), record_stack_sample(), require_command() (+8 more)

### Community 192 - "test_explicit_recovery_uses_expected_status"
Cohesion: 0.32
Nodes (7): _manifest(), Exception, test_concurrent_recovery_reports_conflict_without_overwrite(), save(), test_explicit_recovery_uses_expected_status(), __init__(), save()

### Community 195 - "test_digitalocean_deployment_contract.py"
Cohesion: 0.36
Nodes (9): _read(), _service_block(), test_deployment_script_enforces_release_order_without_destructive_cleanup(), test_deployment_script_requires_stable_worker_liveness_across_poll_intervals(), test_digitalocean_compose_preserves_runtime_and_durability_contracts(), test_docker_build_context_excludes_scientific_data(), test_ghcr_publish_is_gated_by_successful_b2_b6_run_for_same_commit(), test_provider_files_do_not_embed_secrets_or_raw_huaura_paths() (+1 more)

### Community 196 - "deploy_digitalocean.sh"
Cohesion: 0.57
Nodes (7): fail(), require_command(), require_directory(), deploy_digitalocean.sh script, verify_worker_liveness(), VIA_IMAGE, wait_for_health()

### Community 197 - "verify_production_compose.sh"
Cohesion: 0.60
Nodes (4): assert_running(), assert_worker_liveness(), container_id(), verify_production_compose.sh script

### Community 199 - "write_to_netcdf"
Cohesion: 0.26
Nodes (5): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, write_to_netcdf(), PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall.

### Community 201 - "environmental_inputs.py"
Cohesion: 0.29
Nodes (7): _is_finite_number(), datetime, Immutable environmental input snapshots owned by Agroclimatic Evaluation., _validate_aware_datetime(), _validate_crs(), _validate_positive_number(), _validate_text()

### Community 205 - "AgroclimaticEvaluationRecoveryService"
Cohesion: 0.19
Nodes (10): AgroclimaticEvaluationRecoveryService, Logger, Mark an operator-confirmed active orphan as failed without retrying it., ActiveEvaluationResult, list_active_evaluations(), _print_active_evaluations(), UUID, List active evaluations without composing scientific execution dependencies. (+2 more)

### Community 208 - "test_environmental_information_postgresql.py"
Cohesion: 0.28
Nodes (14): Read and validate the test-only database settings before any DB operation., require_test_database_url(), clean_environmental_information(), database(), _database_url(), _dataset(), Engine, fixture (+6 more)

### Community 211 - "health.py"
Cohesion: 0.40
Nodes (4): health(), Host-level health endpoint., Report that the API process is ready to receive requests., get

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **220 isolated node(s):** `via-backend`, `backup_postgres.sh script`, `VIA_IMAGE`, `VIA_BENCHMARK_SOURCE_DIR`, `VIA_BENCHMARK_RUNTIME_CONFIG_DIR` (+215 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 995 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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
- **Why does `create_app()` connect `app.py` to `FarmManagementService`, `farm_management/application/service.py`, `test_agroclimatic_evaluation_api.py`, `DatasetVersion`, `Project`, `Parcel`, `EnvironmentalInformationService`, `environmental_information/infrastructure/postgresql_repositories.py`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `create_database`, `test_farm_management_postgresql.py`, `AgroclimaticEvaluationService`, `InMemoryEvaluationRepository`, `test_environmental_information_api.py`, `test_farm_management_api.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `DatasetVersion`, `environmental_information/interfaces/http.py`, `environmental_information/infrastructure/postgresql_repositories.py`, `create_database`, `via_backend/worker.py`, `CoverageMeasurement`, `DomainValidationError`, `app.py`, `AgroclimaticEvaluationExecutionService`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `AgroclimaticEvaluationService` connect `AgroclimaticEvaluationService` to `decision_support/application/service.py`, `ParcelSnapshot`, `test_agroclimatic_evaluation_api.py`, `Evaluation`, `DomainValidationError`, `execution.py`, `agroclimatic_evaluation/interfaces/http.py`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `test_agroclimatic_evaluation_queries.py`, `agroclimatic_evaluation/application/__init__.py`, `test_decision_support.py`, `app.py`, `ResourceConflictError`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `PostgreSQLEvaluationRepository` (e.g. with `EvaluationConflictError` and `Evaluation`) actually correct?**
  _`PostgreSQLEvaluationRepository` has 9 INFERRED edges - model-reasoned connections that need verification._