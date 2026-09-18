# Graph Report - poc_via_cslite  (2026-09-17)

## Corpus Check
- 316 files · ~165,268 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3045 nodes · 7697 edges · 217 communities (132 shown, 31 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 968 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4b823b6e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- farm_management/application/service.py
- CropSensitivity
- NexGenPreProcessing
- Huaura Dataset Preprocessing Configuration
- check_files.py
- DomainValidationError
- Parcel
- Crop Membership Functions
- multicrop.py
- workflow.py
- CropSuite.py
- DownloadCMIP6Data
- PostgreSQLEvaluationRepository
- climate_suitability_main_xarray.py
- CropSuiteLite
- test_migration_host.py
- climate_suitability_main.py
- cropsuite_adapter.py
- CoverageMeasurement
- decision_support/domain/models.py
- test_farm_management_postgresql.py
- VIA architecture guardrails
- Farm Management persistence
- read_crop_parameterizations_files
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
- EnvironmentalCoverageTest
- ConfiguredEnvironmentalInputIntegrityVerifier
- Q: PostgreSQL Farm Management repositories
- WaterRegime
- ADR-012: PostgreSQL/PostGIS persistence for Environmental Information
- PostGIS service
- GetPublishedDatasetVersion
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
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
- recovery.py
- via_backend/worker.py
- agroclimatic_evaluation/__init__.py
- environmental_information/application/service.py
- Project
- CommonSupport
- test_database_test_support.py
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
- FarmManagementService
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
- test_agroclimatic_environmental_inputs.py
- test_agroclimatic_evaluation_domain.py
- test_decision_support.py
- Production deployment runtime contract
- migrate.py
- Settings
- CropSuiteComparisonAdapter
- crop_rotation.py
- ViabilityPolicySnapshot
- DomainValidationError
- test_agroclimatic_evaluation_api.py
- test_cropsuite_adapter.py
- Agroclimatic Evaluation request, worker, recovery, and read slice
- Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation
- Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors
- crop_suitability_main.py
- SpatialExtent
- cropsuite_comparison_adapter.py
- Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment.
- scientific_input_integrity.py
- PolicyReference
- config.py
- DomainValidationError
- Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract
- agroclimatic_evaluation/application/__init__.py
- test_decision_support_postgresql.py
- InMemoryEvaluationRepository
- test_environmental_information_api.py
- verify_runtime
- run_cropsuitelite.py
- test_farm_management_api.py
- benchmark_production_runtime.sh
- .__init__
- test_agroclimatic_evaluation_worker.py
- test_container_image_contract.py
- test_digitalocean_deployment_contract.py
- deploy_digitalocean.sh
- verify_production_compose.sh
- agroclimatic_evaluation/infrastructure/__init__.py
- process_precday_interp
- test_resource_benchmark_contract.py
- CropExecutionStatus
- backup_postgres.sh
- CropSuitabilityRequest
- FilesystemScientificArtifactStore
- test_environmental_information_postgresql.py
- CropComparisonExecutionError
- PublishedDatasetVersion
- test_limiting_factor_domain.py
- health.py
- ScientificArtifactStore
- test_production_compose_contract.py
- IDecisionPolicy
- PolicyReferenceMismatchError

## God Nodes (most connected - your core abstractions)
1. `Evaluation` - 96 edges
2. `DomainValidationError` - 70 edges
3. `WaterRegime` - 60 edges
4. `PostgreSQLEvaluationRepository` - 57 edges
5. `EvaluationStatus` - 51 edges
6. `EnvironmentalInformationService` - 49 edges
7. `AgroclimaticEvaluationService` - 47 edges
8. `InMemoryEvaluationRepository` - 45 edges
9. `DatasetVersion` - 45 edges
10. `PolicyReference` - 39 edges

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

## Communities (217 total, 31 thin omitted)

### Community 0 - "farm_management/application/service.py"
Cohesion: 0.10
Nodes (42): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+34 more)

### Community 1 - "CropSensitivity"
Cohesion: 0.10
Nodes (14): change_otherst_parameters(), change_st1_parameter(), create_crop_parameters(), CropSensitivity, ndarray, A class to read, handle, and write crop sensitivity parameters from .inf files., Shifts and stretches the parameter suitability value to a new maximum . Args:…, Initializes the CropSensitivity class. Args: crop (str): The name of the crop… (+6 more)

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

### Community 9 - "workflow.py"
Cohesion: 0.12
Nodes (27): EvaluateConfiguredDecisionSupport, EvaluateDecisionSupport, StrEnum, Decision Support application query messages., Prepare evidence and apply one explicitly versioned policy when possible., How the viability policy configuration is selected for one execution., Select either VIA's current default policy or an explicit custom snapshot., Evaluate Decision Support using a selected viability-policy configuration. (+19 more)

### Community 10 - "CropSuite.py"
Cohesion: 0.10
Nodes (41): # NOTE: self.extent is modified here to align with grid, create_cog_from_geotiff(), extract_domain_from_global_3draster(), extract_domain_from_global_raster(), geotiff_to_smallest_datatype(), get_cpu_ram(), get_resolution_array(), get_shape_of_raster() (+33 more)

### Community 11 - "DownloadCMIP6Data"
Cohesion: 0.09
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+9 more)

### Community 12 - "PostgreSQLEvaluationRepository"
Cohesion: 0.11
Nodes (64): EnvironmentalInputReference, Caller-selected exact environmental dataset version., PostgreSQLEvaluationRepository, SessionFactory, Durable adapter for immutable Evaluation aggregates., Read and validate the test-only database settings before any DB operation., require_test_database_url(), clean_evaluations() (+56 more)

### Community 13 - "climate_suitability_main_xarray.py"
Cohesion: 0.10
Nodes (31): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+23 more)

### Community 14 - "CropSuiteLite"
Cohesion: 0.11
Nodes (13): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Calculates climate suitability based on temperature and precipitation.…, Combines climate suitability with soil/terrain data to calculate final crop…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Interpolates or retrieves downscaled climate data (precipitation and… (+5 more)

### Community 15 - "test_migration_host.py"
Cohesion: 0.19
Nodes (19): main(), Run the explicit release migration CLI., _configure_valid_production(), CaptureFixture, MonkeyPatch, parametrize, Path, Focused tests for the explicit VIA release migration host. (+11 more)

### Community 16 - "climate_suitability_main.py"
Cohesion: 0.09
Nodes (32): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+24 more)

### Community 17 - "cropsuite_adapter.py"
Cohesion: 0.11
Nodes (52): CropLimitationEvidence, CropSuitabilityEngineError, CropSuitabilityExecutionError, InvalidEngineOutputError, LimitingFactorEvidence, Application-owned boundary for one crop suitability evaluation., Durable opaque reference to one verified scientific artifact., An engine-reported failure, distinct from no coverage and a zero score. (+44 more)

### Community 18 - "CoverageMeasurement"
Cohesion: 0.14
Nodes (23): CheckDatasetVersionCoverage, CoverageClassification, CoverageCompatibilityFailure, CoverageMeasurement, StrEnum, Structural metadata prevented a meaningful spatial measurement., Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port. (+15 more)

### Community 19 - "decision_support/domain/models.py"
Cohesion: 0.11
Nodes (30): Decision Support evidence translation and policy coordination., _translate_common_support(), _translate_evidence(), DomainValidationError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Decision Support domain layer. (+22 more)

### Community 20 - "test_farm_management_postgresql.py"
Cohesion: 0.21
Nodes (22): PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel() (+14 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management persistence"
Cohesion: 0.12
Nodes (20): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, Optimistic parcel revision transaction, ParcelVersionConflictError, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations (+12 more)

### Community 23 - "read_crop_parameterizations_files"
Cohesion: 0.15
Nodes (12): get_formula(), get_id_list_start(), get_plant_param_interp_forms_dict(), print_crop_param_output(), print_sections(), Reads and parses crop parameterization files from a specified folder path.…, Prints the keys of a given dictionary as a list of sections or items. Args:…, Given two arrays of numerical values x_vals and y_vals representing data… (+4 more)

### Community 24 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.20
Nodes (10): Common-Support Ranking, ADR-002 Layered Bounded Contexts, ADR-003 Commands and Queries in Application, ADR-005 Background Worker, ADR-007 Initial Deployment, ADR-009 Multicrop Evaluation, Architecture and Backend for CropSuiteLite Huaura v2, Celery (+2 more)

### Community 25 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 26 - "scientific_artifact_store.py"
Cohesion: 0.15
Nodes (17): _file_identity(), _is_within(), PublishedScientificArtifact, Path, RuntimeError, Durable filesystem storage for scientific artifacts., Base error for durable scientific artifact storage failures., Raised when an immutable artifact reference already has different content. (+9 more)

### Community 27 - "test_architecture.py"
Cohesion: 0.14
Nodes (17): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+9 more)

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
Nodes (37): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, Execute requested crops and summarize them through Application-owned ports., _artifact(), _environmental_information_for(), _evaluation(), _execute() (+29 more)

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
Nodes (21): EnvironmentalInputResolutionError, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved., EnvironmentalInputManifest, Immutable set of exact environmental inputs resolved for an evaluation., EvaluationConflictError, InvalidEvaluationTransitionError, RuntimeError (+13 more)

### Community 37 - "EnvironmentalCoverageTest"
Cohesion: 0.19
Nodes (4): calculate_slope(), covered_gradient(), Central differences inside coverage, one-sided at its boundary. An axis with no…, EnvironmentalCoverageTest

### Community 38 - "ConfiguredEnvironmentalInputIntegrityVerifier"
Cohesion: 0.19
Nodes (24): EnvironmentalInputIntegrityError, Raised when resolved environmental provenance does not match scientific inputs., ConfiguredEnvironmentalInputIntegrityVerifier, Verify manifests using deployment-configured exact dataset-version bindings., _binding(), _fingerprints(), _manifest(), parametrize (+16 more)

### Community 40 - "Q: PostgreSQL Farm Management repositories"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: PostgreSQL Farm Management repositories, Source Nodes

### Community 41 - "WaterRegime"
Cohesion: 0.09
Nodes (42): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Commands expressing Agroclimatic Evaluation use-case intent., Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, EvaluationResultAvailability, StrEnum, Whether persisted outcomes are pending, partial, or final. (+34 more)

### Community 42 - "ADR-012: PostgreSQL/PostGIS persistence for Environmental Information"
Cohesion: 0.12
Nodes (18): ADR-012: PostgreSQL/PostGIS persistence for Environmental Information, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation, Decision Support (+10 more)

### Community 43 - "PostGIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "GetPublishedDatasetVersion"
Cohesion: 0.33
Nodes (14): GetPublishedDatasetVersion, _dataset(), datetime, UUID, Public cross-context contract tests for Environmental Information., _service(), test_exact_dataset_and_version_returns_all_published_metadata(), test_missing_dataset_returns_none() (+6 more)

### Community 45 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.10
Nodes (51): CropOutcome, Durable scientific evidence referenced without exposing filesystem paths., One durable result associated with an Evaluation and requested crop., ScientificArtifact, Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records. (+43 more)

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
Cohesion: 0.12
Nodes (17): DefaultViabilityPolicyNotConfiguredError, LookupError, Raised when VIA has no default viability policy configured., PolicyVersionConflictError, RuntimeError, Raised when one immutable policy reference is bound to different thresholds., Base, DeclarativeBase (+9 more)

### Community 64 - "recovery.py"
Cohesion: 0.11
Nodes (19): Exception, Explicit fail-only recovery for abandoned evaluation executions., ActiveEvaluationResult, CropOutcomeResult, EvaluationResult, ParcelSnapshotResult, Transport-neutral Agroclimatic Evaluation results., InvalidCommandError (+11 more)

### Community 65 - "via_backend/worker.py"
Cohesion: 0.11
Nodes (22): Settings for the PostgreSQL polling worker process., WorkerSettings, create_database(), Engine, SessionFactory, Create the shared engine and short-lived session factory., Shared technical infrastructure used by the application composition root., create_worker() (+14 more)

### Community 67 - "environmental_information/application/service.py"
Cohesion: 0.08
Nodes (32): CreateDataset, Commands expressing Environmental Information use-case intent., DatasetResult, DatasetVersionCoverageResult, Transport-neutral results returned by Environmental Information use cases., Extent-based coverage and structural compatibility result., Environmental Information command and query coordination., DatasetVersionConflictError (+24 more)

### Community 68 - "Project"
Cohesion: 0.13
Nodes (10): Project, An agricultural project that groups parcels., ParcelRepository, ProjectRepository, Protocol, UUID, Repository abstractions for Farm Management aggregates., _project_from_record() (+2 more)

### Community 69 - "CommonSupport"
Cohesion: 0.09
Nodes (36): _to_comparable_crop(), CommonSupport, ComparableCrop, normalize_common_support_measurements(), One crop ranked on the exact common valid spatial support., Normalize impossible boundary overshoots caused only by float noise., Validate deterministic scientific ranking semantics., Spatial support shared by the usable crop suitability rasters. (+28 more)

### Community 70 - "test_database_test_support.py"
Cohesion: 0.22
Nodes (14): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., UnsafeTestDatabaseError, validate_test_database_url(), CaptureFixture, parametrize (+6 more)

### Community 73 - "EnvironmentalInformationService"
Cohesion: 0.07
Nodes (51): CreateDatasetVersion, Environmental Information application layer., GetDataset, GetDatasetVersion, ListDatasets, ListDatasetVersions, Queries supported by the Environmental Information service., DatasetVersionResult (+43 more)

### Community 74 - "test_api_host.py"
Cohesion: 0.14
Nodes (19): ApiServerSettings, main(), Production HTTP process host for VIA., Provider-neutral Uvicorn bind settings for the production API process., Load API bind settings from the process environment., Validate production configuration and run one Uvicorn API process., _clear_api_environment(), _configure_production_persistence() (+11 more)

### Community 75 - "app.py"
Cohesion: 0.07
Nodes (37): create_app(), create_production_app(), FastAPI, Side-effect-free FastAPI application composition., Build the production API after enforcing durable persistence settings., Build the VIA API and register its technical interfaces., InvalidSpatialInputError, RuntimeError (+29 more)

### Community 77 - "Q: ParcelVersion persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ParcelVersion persistence, Source Nodes

### Community 93 - "Q: Domain-to-Infrastructure dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Domain-to-Infrastructure dependency violations, Source Nodes

### Community 135 - "FarmManagementService"
Cohesion: 0.17
Nodes (11): ParcelResult, ParcelVersionResult, ProjectResult, Transport-neutral results returned by Farm Management use cases., FarmManagementService, InvalidCommandError, datetime, UUID (+3 more)

### Community 136 - "Huaura scientific fixture recovery audit"
Cohesion: 0.08
Nodes (25): Benchmark compatibility, Boundary and reference mask, Climate, Current identity manifest, DEM, Executive status, Historical alternatives / abandoned paths, Huaura scientific fixture recovery audit (+17 more)

### Community 137 - "execution.py"
Cohesion: 0.11
Nodes (33): _comparison_request(), Synchronous application orchestration for persisted evaluations., _to_common_support(), _to_outcome(), CommonSupportStatus, StrEnum, Evaluation-level scientific common-support result., Domain errors for Agroclimatic Evaluation. (+25 more)

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

### Community 150 - "test_agroclimatic_environmental_inputs.py"
Cohesion: 0.18
Nodes (22): parametrize, Focused domain tests for immutable environmental input manifests., _snapshot(), test_environmental_input_manifest_accepts_valid_inputs(), test_environmental_input_manifest_allows_same_version_for_distinct_input_keys(), test_environmental_input_manifest_rejects_duplicate_input_key(), test_environmental_input_manifest_rejects_empty_inputs(), test_environmental_input_manifest_rejects_input_registered_after_resolution() (+14 more)

### Community 151 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.19
Nodes (20): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+12 more)

### Community 152 - "test_decision_support.py"
Cohesion: 0.12
Nodes (37): FinalizedCommonSupportStatus, FinalizedComparableCrop, ComparableCropEvidence, DecisionEvidence, Scientific evidence prepared for one explicit deterministic policy., Return whether a policy may consume this evidence without fabrication., A provider-produced crop mean and rank over common valid support., _common_support() (+29 more)

### Community 154 - "Production deployment runtime contract"
Cohesion: 0.17
Nodes (11): B2 reproducible Linux container image, B6.1 resource benchmark, B6 production-like Docker Compose smoke, B7 DigitalOcean single-Droplet deployment definition, Database and migration contract, Environment contract, Filesystem contract, Process responsibilities (+3 more)

### Community 155 - "migrate.py"
Cohesion: 0.23
Nodes (11): _build_parser(), ArgumentParser, Path, One-shot production schema migration host for VIA releases., Return the repository-local Alembic config when running from source., Resolve the Alembic config without depending on the process cwd., Validate production persistence and migrate the schema to Alembic head., _require_production_postgresql() (+3 more)

### Community 157 - "Settings"
Cohesion: 0.11
Nodes (25): Settings needed by the current backend composition root., Require the durable persistence contract used by the production API., Settings, MonkeyPatch, parametrize, Path, Tests for environment-driven application composition settings., _scientific_worker_settings() (+17 more)

### Community 158 - "CropSuiteComparisonAdapter"
Cohesion: 0.30
Nodes (18): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., _artifact(), Any, Path, _report(), _request(), _snapshot() (+10 more)

### Community 159 - "crop_rotation.py"
Cohesion: 0.16
Nodes (17): calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):…, Read a GeoTIFF file with multiple bands into a NumPy array. Parameters: - fn… (+9 more)

### Community 160 - "ViabilityPolicySnapshot"
Cohesion: 0.11
Nodes (13): IDefaultViabilityPolicyProvider, IDefaultViabilityPolicyStore, IViabilityPolicyRepository, Protocol, Application ports for deterministic Decision Support policies., Provide the current VIA default viability policy without owning its storage., Store and restore immutable viability-policy versions., Read and change the current default viability-policy pointer. (+5 more)

### Community 161 - "DomainValidationError"
Cohesion: 0.09
Nodes (30): EnvironmentalInputSnapshot, _is_finite_number(), datetime, Immutable environmental input snapshots owned by Agroclimatic Evaluation., Historical environmental input metadata captured for one evaluation input., _validate_aware_datetime(), _validate_crs(), _validate_positive_number() (+22 more)

### Community 162 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.18
Nodes (32): _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any, FastAPI (+24 more)

### Community 163 - "test_cropsuite_adapter.py"
Cohesion: 0.15
Nodes (43): CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability., _adapter(), _default_base_config(), _environmental_input_manifest(), _integrity_verifier(), Any, fixture (+35 more)

### Community 164 - "Agroclimatic Evaluation request, worker, recovery, and read slice"
Cohesion: 0.15
Nodes (11): ADR-015: PostgreSQL polling for Agroclimatic Evaluation worker dispatch, Consequences, Context, Decision, Status, Agroclimatic Evaluation request, worker, recovery, and read slice, Current lifecycle and execution, Deliberately deferred (+3 more)

### Community 165 - "Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation, Source Nodes

### Community 166 - "Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors, Source Nodes

### Community 170 - "crop_suitability_main.py"
Cohesion: 0.13
Nodes (23): aggregate_soil_raster_lst(), calcification_map(), cropsuitability(), get_soil_data(), get_suitability_val_dict(), get_texture_class(), get_valid_dtype(), getTable() (+15 more)

### Community 172 - "SpatialExtent"
Cohesion: 0.13
Nodes (23): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine (+15 more)

### Community 174 - "cropsuite_comparison_adapter.py"
Cohesion: 0.21
Nodes (21): CommonSupportResult, CommonSupportStatus, ComparableCropResult, CropComparisonResult, InvalidComparisonOutputError, Scientific common-support outcome across evaluated crops., Scientific support shared by all usable crop suitability rasters., One crop summarized on the exact common spatial support. (+13 more)

### Community 175 - "Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment., Source Nodes

### Community 176 - "scientific_input_integrity.py"
Cohesion: 0.15
Nodes (16): CropSuiteEnvironmentalInputBinding, load_configured_environmental_input_integrity_verifier(), load_cropsuite_environmental_input_bindings(), _parse_uuid(), Any, Path, UUID, Configured binding between exact dataset versions and CropSuite source hashes. (+8 more)

### Community 177 - "PolicyReference"
Cohesion: 0.14
Nodes (28): DefaultViabilityPolicyConflictError, InvalidViabilityPolicyRevisionError, RuntimeError, ValueError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist., Raised when a requested viability-policy revision is not a new version., Raised when the default policy changed before an expected update. (+20 more)

### Community 178 - "config.py"
Cohesion: 0.33
Nodes (7): _environment_float(), _environment_integer(), _is_same_or_within(), _optional_path(), Path, Environment-backed configuration for the VIA application host., _validate_scientific_path_topology()

### Community 180 - "DomainValidationError"
Cohesion: 0.12
Nodes (26): CoverageComputation, Protocol, Application ports for Environmental Information spatial collaboration., Measure an external geometry against a registered dataset extent., SpatialCoveragePort, CoverageGeometry, _parse_multi_polygon(), _parse_polygon() (+18 more)

### Community 181 - "Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract, Source Nodes

### Community 182 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.07
Nodes (64): Agroclimatic Evaluation application layer., FinalizedCommonSupport, FinalizedCropLimitationEvidence, FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedEvaluationResult, FinalizedEvaluationResultReader, FinalizedLimitationEvidenceAvailability (+56 more)

### Community 183 - "test_decision_support_postgresql.py"
Cohesion: 0.17
Nodes (30): Decision Support infrastructure adapters., PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+22 more)

### Community 184 - "InMemoryEvaluationRepository"
Cohesion: 0.16
Nodes (23): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Logger, Mark an operator-confirmed active orphan as failed without retrying it., InMemoryEvaluationRepository, _evaluation_in_status(), _manifest() (+15 more)

### Community 185 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 187 - "verify_runtime"
Cohesion: 0.36
Nodes (10): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_read_only_directory(), _require_read_only_file(), _require_writable_directory(), _run_cropsuite_import_smoke() (+2 more)

### Community 188 - "run_cropsuitelite.py"
Cohesion: 0.19
Nodes (15): change_otherst_parameters(), change_st1_parameter(), create_crop_parameters(), create_crop_suite_configuration_file(), find_solution_type(), main(), modify_extent(), modify_general_files() (+7 more)

### Community 189 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 191 - "benchmark_production_runtime.sh"
Cohesion: 0.19
Nodes (16): artifact_bytes_for_evaluation(), COMPOSE_PROJECT_NAME, database_size_bytes(), fail(), monotonic_ns(), post_json(), record_stack_sample(), require_command() (+8 more)

### Community 193 - "test_agroclimatic_evaluation_worker.py"
Cohesion: 0.15
Nodes (26): AgroclimaticEvaluationWorker, Logger, Discover queued IDs and delegate all execution semantics to Application., _artifact(), _engine_result(), _evaluation(), _executor(), FakeComparisonEngine (+18 more)

### Community 195 - "test_digitalocean_deployment_contract.py"
Cohesion: 0.36
Nodes (9): _read(), _service_block(), test_deployment_script_enforces_release_order_without_destructive_cleanup(), test_deployment_script_requires_stable_worker_liveness_across_poll_intervals(), test_digitalocean_compose_preserves_runtime_and_durability_contracts(), test_docker_build_context_excludes_scientific_data(), test_ghcr_publish_is_gated_by_successful_b2_b6_run_for_same_commit(), test_provider_files_do_not_embed_secrets_or_raw_huaura_paths() (+1 more)

### Community 196 - "deploy_digitalocean.sh"
Cohesion: 0.57
Nodes (7): fail(), require_command(), require_directory(), deploy_digitalocean.sh script, verify_worker_liveness(), VIA_IMAGE, wait_for_health()

### Community 197 - "verify_production_compose.sh"
Cohesion: 0.60
Nodes (4): assert_running(), assert_worker_liveness(), container_id(), verify_production_compose.sh script

### Community 198 - "agroclimatic_evaluation/infrastructure/__init__.py"
Cohesion: 0.13
Nodes (12): CropComparisonInput, CropComparisonRequest, One durable crop suitability raster offered to scientific comparison., Compare crop suitability only on identical valid spatial support., ParcelSnapshot, The exact Farm Management parcel state accepted for an evaluation., Agroclimatic Evaluation infrastructure layer., StubComparisonEngine (+4 more)

### Community 199 - "process_precday_interp"
Cohesion: 0.26
Nodes (4): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall.

### Community 201 - "CropExecutionStatus"
Cohesion: 0.22
Nodes (16): CropExecutionStatus, LimitationEvidenceAvailability, StrEnum, Scientific outcomes reported independently of Evaluation lifecycle state., Scientific artifact roles understood by VIA., Availability of deterministic SAME-RUN limiting-factor evidence., ScientificArtifactRole, _real_limitation_adapter() (+8 more)

### Community 205 - "CropSuitabilityRequest"
Cohesion: 0.16
Nodes (10): datetime, CropSuitabilityRequest, CropSuitabilityResult, ICropComparisonEngine, ICropSuitabilityEngine, Protocol, One checked per-crop outcome from the scientific boundary., Compare durable crop outputs using the authoritative scientific engine. (+2 more)

### Community 206 - "FilesystemScientificArtifactStore"
Cohesion: 0.30
Nodes (14): FilesystemScientificArtifactStore, Filesystem-backed immutable artifact store., parametrize, Path, test_publish_creates_durable_artifact_with_opaque_reference(), test_publish_is_idempotent_for_identical_content(), test_publish_rejects_content_that_does_not_match_expected_checksum(), test_publish_rejects_different_content_for_existing_reference() (+6 more)

### Community 207 - "test_environmental_information_postgresql.py"
Cohesion: 0.33
Nodes (12): clean_environmental_information(), database(), _database_url(), _dataset(), Engine, fixture, SessionFactory, PostgreSQL/PostGIS integration tests for Environmental Information. (+4 more)

### Community 208 - "CropComparisonExecutionError"
Cohesion: 0.24
Nodes (8): CropComparisonEngineError, CropComparisonExecutionError, RuntimeError, Base error for the scientific crop-comparison boundary., Raised when scientific common-support comparison cannot execute., _is_within(), Path, ComparisonRunner

### Community 209 - "PublishedDatasetVersion"
Cohesion: 0.27
Nodes (7): PublishedDatasetVersion, PublishedDatasetVersionReader, Protocol, Stable contracts deliberately published to other bounded contexts., Public cross-context reader for exact immutable dataset versions., FakeEnvironmentalInformation, _published()

### Community 210 - "test_limiting_factor_domain.py"
Cohesion: 0.33
Nodes (7): _factor(), LimitingFactorEvidence, parametrize, Focused domain invariants for deterministic limiting-factor evidence., test_available_limitation_evidence_accepts_traceable_factor(), test_limiting_factor_rejects_invalid_affected_cells(), test_limiting_factor_rejects_non_integer_raw_code()

### Community 211 - "health.py"
Cohesion: 0.40
Nodes (4): health(), Host-level health endpoint., Report that the API process is ready to receive requests., get

### Community 212 - "ScientificArtifactStore"
Cohesion: 0.25
Nodes (6): IEnvironmentalInputIntegrityVerifier, Verify resolved environmental provenance against scientific source fingerprints., Protocol, Publish immutable scientific files behind opaque logical references., ScientificArtifactStore, EngineRunner

### Community 213 - "test_production_compose_contract.py"
Cohesion: 0.36
Nodes (6): _mapping_keys(), Static invariants for the provider-neutral B6 production-like Compose smoke., _service_block(), test_b6_compose_encodes_release_ordering_and_runtime_mount_semantics(), test_b6_compose_has_exact_process_topology_and_same_image_contract(), test_b6_worker_bindings_fixture_is_valid_for_startup()

### Community 214 - "IDecisionPolicy"
Cohesion: 0.40
Nodes (3): IDecisionPolicy, Evaluate comparable evidence without changing its scientific values., PolicyEvaluationT_co

### Community 216 - "PolicyReferenceMismatchError"
Cohesion: 0.67
Nodes (3): PolicyReferenceMismatchError, ValueError, Raised when the supplied policy differs from the requested policy identity.

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **220 isolated node(s):** `via-backend`, `backup_postgres.sh script`, `VIA_IMAGE`, `VIA_BENCHMARK_SOURCE_DIR`, `VIA_BENCHMARK_RUNTIME_CONFIG_DIR` (+215 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1020 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
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
- **Why does `FarmManagementService` connect `FarmManagementService` to `farm_management/application/service.py`, `Project`, `DomainValidationError`, `Parcel`, `app.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `via_backend/worker.py`, `environmental_information/application/service.py`, `app.py`, `GetPublishedDatasetVersion`, `SpatialExtent`, `PublishedDatasetVersion`, `CoverageMeasurement`, `DomainValidationError`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `PostgreSQLEvaluationRepository` connect `PostgreSQLEvaluationRepository` to `via_backend/worker.py`, `Evaluation`, `agroclimatic_evaluation/infrastructure/__init__.py`, `WaterRegime`, `app.py`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 35 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 37 inferred relationships involving `WaterRegime` (e.g. with `RequestEvaluation` and `_comparison_request()`) actually correct?**
  _`WaterRegime` has 37 INFERRED edges - model-reasoned connections that need verification._