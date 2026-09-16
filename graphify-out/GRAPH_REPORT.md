# Graph Report - poc_via_cslite  (2026-09-16)

## Corpus Check
- 284 files · ~126,585 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2461 nodes · 5915 edges · 181 communities (104 shown, 29 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 734 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d37720c6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FarmManagementService
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
- Parcel
- climate_suitability_main_xarray.py
- CropSuiteLite
- cropsuite_adapter.py
- climate_suitability_main.py
- process_precday_interp
- CoverageMeasurement
- decision_support/domain/models.py
- test_farm_management_postgresql.py
- VIA architecture guardrails
- Farm Management persistence
- EvaluationRepository
- Architecture and Backend for CropSuiteLite Huaura v2
- Huaura Environmental Correction
- scientific_artifact_store.py
- test_architecture.py
- Farm Management schema ownership
- Bounded-context layered structure
- Python and FastAPI backend decision
- CropSuite.py
- Farm Management minimum vertical slice
- Application commands and queries
- via_backend/worker.py
- VIA architecture implementation roadmap
- InMemoryEvaluationRepository
- AgroclimaticEvaluationExecutionService
- Project
- CropSuiteComparisonAdapter
- Q: PostgreSQL Farm Management repositories
- agroclimatic_evaluation/interfaces/http.py
- ADR-012: PostgreSQL/PostGIS persistence for Environmental Information
- PostGIS service
- cropsuite_comparison_adapter.py
- create_database
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
- execution.py
- test_decision_support.py
- agroclimatic_evaluation/__init__.py
- DomainValidationError
- health.py
- ComparableCrop
- FilesystemScientificArtifactStore
- decision_support/__init__.py
- decision_support/interfaces/__init__.py
- EnvironmentalInformationService
- decision_support/application/ports.py
- DatasetVersion
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
- Dataset
- test_environmental_information_api.py
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
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
- DomainValidationError
- test_agroclimatic_evaluation_domain.py
- agroclimatic_evaluation/infrastructure/__init__.py
- Evaluation
- ExecuteEvaluation
- FinalizedEvaluationResultReader
- agroclimatic_evaluation/application/__init__.py
- nc_tools.py
- test_explicit_recovery_uses_expected_status
- UUID
- test_agroclimatic_evaluation_api.py
- ._persist_failure
- Agroclimatic Evaluation request, worker, recovery, and read slice
- Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation
- Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors
- PostgreSQLEvaluationRepository
- crop_suitability_main.py
- SpatialExtent
- Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment.
- PolicyReference
- CropComparisonRequest
- Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract
- test_decision_support_postgresql.py

## God Nodes (most connected - your core abstractions)
1. `Evaluation` - 75 edges
2. `DomainValidationError` - 44 edges
3. `EnvironmentalInformationService` - 43 edges
4. `DatasetVersion` - 43 edges
5. `AgroclimaticEvaluationService` - 40 edges
6. `EvaluationStatus` - 40 edges
7. `PolicyReference` - 39 edges
8. `ViabilityPolicySnapshot` - 38 edges
9. `Parcel` - 38 edges
10. `InMemoryEvaluationRepository` - 36 edges

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

## Communities (181 total, 29 thin omitted)

### Community 0 - "FarmManagementService"
Cohesion: 0.08
Nodes (53): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+45 more)

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

### Community 6 - "farm_management/infrastructure/postgresql_repositories.py"
Cohesion: 0.15
Nodes (21): Base, DeclarativeBase, SQLAlchemy metadata owned by Farm Management Infrastructure., Declarative base for Farm Management persistence records., Farm Management infrastructure layer., ParcelRecord, ParcelVersionRecord, ProjectRecord (+13 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.10
Nodes (22): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+14 more)

### Community 9 - "workflow.py"
Cohesion: 0.09
Nodes (40): FinalizedCommonSupportStatus, FinalizedComparableCrop, StrEnum, EvaluateConfiguredDecisionSupport, EvaluateDecisionSupport, StrEnum, Decision Support application query messages., Prepare evidence and apply one explicitly versioned policy when possible. (+32 more)

### Community 10 - "data_tools.py"
Cohesion: 0.10
Nodes (35): Combines climate suitability with soil/terrain data to calculate final crop…, Interpolates or retrieves downscaled climate data (precipitation and…, aggregate_soil_raster_lst(), get_soil_data(), Get soil data based on specified climate configuration parameters. Parameters:…, Aggregate soil raster data from a list of files based on specified parameters.…, extract_domain_from_global_3draster(), extract_domain_from_global_raster() (+27 more)

### Community 11 - "DownloadCMIP6Data"
Cohesion: 0.09
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+9 more)

### Community 12 - "Parcel"
Cohesion: 0.14
Nodes (12): ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved., Parcel, A named parcel whose geometry changes only by appending versions., ParcelRepository, UUID, Repository abstractions for Farm Management aggregates. (+4 more)

### Community 13 - "climate_suitability_main_xarray.py"
Cohesion: 0.09
Nodes (32): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+24 more)

### Community 14 - "CropSuiteLite"
Cohesion: 0.13
Nodes (11): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Calculates climate suitability based on temperature and precipitation.…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Calculates grid tiling based on available RAM to prevent memory overflow.…, Private subprocess entry point; each invocation has its own working directory. (+3 more)

### Community 15 - "cropsuite_adapter.py"
Cohesion: 0.06
Nodes (83): CropExecutionStatus, CropSuitabilityEngineError, CropSuitabilityExecutionError, CropSuitabilityRequest, CropSuitabilityResult, ICropSuitabilityEngine, InvalidEngineOutputError, Protocol (+75 more)

### Community 16 - "climate_suitability_main.py"
Cohesion: 0.07
Nodes (39): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+31 more)

### Community 17 - "process_precday_interp"
Cohesion: 0.16
Nodes (5): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall., PrecipitationUnitsTest

### Community 18 - "CoverageMeasurement"
Cohesion: 0.15
Nodes (22): CheckDatasetVersionCoverage, CoverageClassification, CoverageMeasurement, StrEnum, Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port., Environmental Information interface layer., _multi_polygon() (+14 more)

### Community 19 - "decision_support/domain/models.py"
Cohesion: 0.10
Nodes (33): Decision Support evidence translation and policy coordination., _translate_common_support(), _translate_evidence(), DomainValidationError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Decision Support domain layer. (+25 more)

### Community 20 - "test_farm_management_postgresql.py"
Cohesion: 0.28
Nodes (19): clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel(), _polygon(), _project(), datetime (+11 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management persistence"
Cohesion: 0.12
Nodes (20): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, Optimistic parcel revision transaction, ParcelVersionConflictError, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations (+12 more)

### Community 23 - "EvaluationRepository"
Cohesion: 0.09
Nodes (24): Commands expressing Agroclimatic Evaluation use-case intent., Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Explicit fail-only recovery for abandoned evaluation executions., Mark an operator-confirmed active orphan as failed without retrying it., EvaluationResult, InvalidCommandError (+16 more)

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
Cohesion: 0.16
Nodes (13): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+5 more)

### Community 28 - "Farm Management schema ownership"
Cohesion: 0.20
Nodes (10): Farm Management schema ownership, Projects, parcels, and parcel_versions tables, farm_management schema and owned tables, Optional durable repository adapter, Project, Parcel, and ParcelVersion domain model, Result querying increment, Bounded-context ownership and Farm Management repositories, Farm Management ownership query (+2 more)

### Community 29 - "Bounded-context layered structure"
Cohesion: 0.28
Nodes (9): Bounded-context ownership, Anti-corruption layer, Application layer, Bounded-context layered structure, Domain layer, Illustrative Evaluation module structure, Infrastructure layer, Interfaces layer (+1 more)

### Community 30 - "Python and FastAPI backend decision"
Cohesion: 0.22
Nodes (14): Multicrop Parcel Evaluation, run_evaluation Service, ADR-004 CropSuiteLite Port and Adapter, ADR-008 Sequential Crop Execution, Background worker execution, CropSuiteLite isolation boundary, FastAPI, Python (+6 more)

### Community 31 - "CropSuite.py"
Cohesion: 0.11
Nodes (27): # NOTE: self.extent is modified here to align with grid, calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):… (+19 more)

### Community 32 - "Farm Management minimum vertical slice"
Cohesion: 0.13
Nodes (13): ADR-011: PostgreSQL/PostGIS persistence for Farm Management, Consequences, Context, Decision, Status, Architectural alignment, Slice exclusions and authorization dependency, Explicit exclusions and provisional choices (+5 more)

### Community 33 - "Application commands and queries"
Cohesion: 0.29
Nodes (8): Application commands and queries, FastAPI composition root, In-memory and durable Infrastructure adapters, Project and parcel HTTP resources, Farm Management repository abstractions, Transport-to-domain path, ProjectRepository, ParcelRepository, and in-memory adapters, Repository ports and in-memory adapters query

### Community 34 - "via_backend/worker.py"
Cohesion: 0.13
Nodes (19): ArgumentParser, _environment_float(), _environment_integer(), _optional_path(), Path, Environment-backed configuration for the VIA application host., Settings for the PostgreSQL polling worker process., WorkerSettings (+11 more)

### Community 35 - "VIA architecture implementation roadmap"
Cohesion: 0.13
Nodes (16): Domain dependency rule, Layered modular monolith, Inward dependency direction, Architecture source and PoC preservation, Cross-stage architecture gates, Explanation and comparison increment, Modeling increment, Modular foundation increment (+8 more)

### Community 36 - "InMemoryEvaluationRepository"
Cohesion: 0.16
Nodes (25): AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application., InMemoryEvaluationRepository, _artifact(), _engine_result(), _evaluation(), _executor(), FakeComparisonEngine (+17 more)

### Community 37 - "AgroclimaticEvaluationExecutionService"
Cohesion: 0.20
Nodes (23): AgroclimaticEvaluationExecutionService, Execute requested crops and summarize them through Application-owned ports., _artifact(), _evaluation(), _execute(), FakeComparisonEngine, FakeEngine, Exception (+15 more)

### Community 38 - "Project"
Cohesion: 0.14
Nodes (10): Project, An agricultural project that groups parcels., ProjectRepository, Protocol, PostgreSQLProjectRepository, _project_from_record(), SessionFactory, Durable adapter for the Project aggregate. (+2 more)

### Community 39 - "CropSuiteComparisonAdapter"
Cohesion: 0.30
Nodes (17): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., _artifact(), Any, Path, _report(), _request(), _snapshot() (+9 more)

### Community 40 - "Q: PostgreSQL Farm Management repositories"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: PostgreSQL Farm Management repositories, Source Nodes

### Community 41 - "agroclimatic_evaluation/interfaces/http.py"
Cohesion: 0.15
Nodes (22): EvaluationStatus, StrEnum, Architecture-approved lifecycle vocabulary., CommonSupportResponse, ComparableCropResponse, CropEvidenceResponse, CropOutcomeResponse, EvaluationEvidenceResponse (+14 more)

### Community 42 - "ADR-012: PostgreSQL/PostGIS persistence for Environmental Information"
Cohesion: 0.12
Nodes (18): ADR-012: PostgreSQL/PostGIS persistence for Environmental Information, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation, Decision Support (+10 more)

### Community 43 - "PostGIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "cropsuite_comparison_adapter.py"
Cohesion: 0.29
Nodes (18): CommonSupportStatus, ComparableCropResult, InvalidComparisonOutputError, Scientific common-support outcome across evaluated crops., One crop summarized on the exact common spatial support., Raised when scientific comparison returns an invalid contract., _fraction(), _map_comparable_crops() (+10 more)

### Community 45 - "create_database"
Cohesion: 0.19
Nodes (17): create_database(), Engine, SessionFactory, Create the shared engine and short-lived session factory., Shared technical infrastructure used by the application composition root., clean_environmental_information(), database(), _database_url() (+9 more)

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
Cohesion: 0.08
Nodes (22): DefaultViabilityPolicyNotConfiguredError, LookupError, Raised when VIA has no default viability policy configured., PolicyVersionConflictError, RuntimeError, Raised when one immutable policy reference is bound to different thresholds., Immutable identity and exact thresholds used for a policy execution., ViabilityPolicySnapshot (+14 more)

### Community 64 - "execution.py"
Cohesion: 0.08
Nodes (40): _comparison_request(), Synchronous application orchestration for persisted evaluations., _to_common_support(), _to_outcome(), CropComparisonInput, One durable crop suitability raster offered to scientific comparison., CropOutcomeResult, ParcelSnapshotResult (+32 more)

### Community 65 - "test_decision_support.py"
Cohesion: 0.20
Nodes (22): ComparableCropEvidence, A provider-produced crop mean and rank over common valid support., _decision_evidence(), _domain_common_support(), parametrize, Focused tests for the Decision Support bounded-context foundation., test_common_support_rejects_duplicate_crop_membership(), test_common_support_rejects_malformed_crop_membership() (+14 more)

### Community 67 - "DomainValidationError"
Cohesion: 0.08
Nodes (36): InvalidSpatialInputError, CoverageComputation, Protocol, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute. (+28 more)

### Community 68 - "health.py"
Cohesion: 0.40
Nodes (4): health(), Host-level health endpoint., Report that the API process is ready to receive requests., get

### Community 69 - "ComparableCrop"
Cohesion: 0.23
Nodes (16): _to_comparable_crop(), ComparableCrop, One crop ranked on the exact common valid spatial support., _comparable_support(), _outcome(), parametrize, Domain tests for durable comparable crop results., _snapshot() (+8 more)

### Community 70 - "FilesystemScientificArtifactStore"
Cohesion: 0.30
Nodes (14): FilesystemScientificArtifactStore, Filesystem-backed immutable artifact store., parametrize, Path, test_publish_creates_durable_artifact_with_opaque_reference(), test_publish_is_idempotent_for_identical_content(), test_publish_rejects_content_that_does_not_match_expected_checksum(), test_publish_rejects_different_content_for_existing_reference() (+6 more)

### Community 73 - "EnvironmentalInformationService"
Cohesion: 0.07
Nodes (56): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., GetDataset, GetDatasetVersion, ListDatasets, ListDatasetVersions (+48 more)

### Community 74 - "decision_support/application/ports.py"
Cohesion: 0.15
Nodes (9): IDecisionPolicy, IDefaultViabilityPolicyProvider, IDefaultViabilityPolicyStore, Protocol, Application ports for deterministic Decision Support policies., Evaluate comparable evidence without changing its scientific values., Provide the current VIA default viability policy without owning its storage., Read and change the current default viability-policy pointer. (+1 more)

### Community 75 - "DatasetVersion"
Cohesion: 0.07
Nodes (38): DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., DatasetVersion, Immutable reproducibility metadata for one dataset release., Positive horizontal and vertical source-cell resolution., SpatialResolution, Base (+30 more)

### Community 77 - "Q: ParcelVersion persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ParcelVersion persistence, Source Nodes

### Community 93 - "Q: Domain-to-Infrastructure dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Domain-to-Infrastructure dependency violations, Source Nodes

### Community 135 - "Dataset"
Cohesion: 0.11
Nodes (15): datetime, Domain errors raised by Environmental Information invariants., Environmental Information domain layer., Dataset, Environmental Information domain model., Stable logical identity for a geoenvironmental dataset., DatasetRepository, DatasetVersionRepository (+7 more)

### Community 136 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 137 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.11
Nodes (35): EvaluationConflictError, RuntimeError, Raised when an evaluation identity already exists., Durable scientific evidence referenced without exposing filesystem paths., ScientificArtifact, Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure. (+27 more)

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

### Community 150 - "DomainValidationError"
Cohesion: 0.13
Nodes (22): DomainValidationError, ValueError, Raised when evaluation data violates a domain invariant., ParcelSnapshot, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring() (+14 more)

### Community 151 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.36
Nodes (9): _evaluation(), _polygon(), parametrize, Focused domain tests for immutable evaluation requests., _snapshot(), test_empty_or_duplicate_requested_crops_are_rejected(), test_parcel_snapshot_is_deeply_immutable_and_detached_from_input(), test_polygon_and_multipolygon_snapshot_geometry_are_supported() (+1 more)

### Community 152 - "agroclimatic_evaluation/infrastructure/__init__.py"
Cohesion: 0.32
Nodes (6): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online(), Agroclimatic Evaluation infrastructure layer.

### Community 154 - "Evaluation"
Cohesion: 0.15
Nodes (5): Evaluation, An immutable multicrop evaluation and its scientific outcomes., UUID, Repository double that fails if a query touches a mutation/worker method., _ReadOnlySpyRepository

### Community 155 - "ExecuteEvaluation"
Cohesion: 0.29
Nodes (5): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., EvaluationExecutor, Protocol, Logger

### Community 157 - "FinalizedEvaluationResultReader"
Cohesion: 0.24
Nodes (6): FinalizedEvaluationResultReader, Protocol, Public local interface for a future Decision Support consumer., PolicyReferenceMismatchError, ValueError, Raised when the supplied policy differs from the requested policy identity.

### Community 158 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.07
Nodes (57): ParcelSnapshotInput, Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, Agroclimatic Evaluation application layer., FinalizedCommonSupport, FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedEvaluationResult (+49 more)

### Community 159 - "nc_tools.py"
Cohesion: 0.22
Nodes (12): create_cog_from_geotiff(), geotiff_to_smallest_datatype(), Convert image to COG., merge_outputs_no_overlap(), get_netcdf_extent(), merge_netcdf_files(), downscaled_files: list of netcdf files overlap: In Degree extent: [North, Left,…, Get the spatial extent (min and max) of the latitude and longitude in a NetCDF… (+4 more)

### Community 160 - "test_explicit_recovery_uses_expected_status"
Cohesion: 0.40
Nodes (5): Exception, save(), test_explicit_recovery_uses_expected_status(), __init__(), save()

### Community 162 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.07
Nodes (50): Settings needed by the current backend composition root., Settings, _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome() (+42 more)

### Community 164 - "Agroclimatic Evaluation request, worker, recovery, and read slice"
Cohesion: 0.15
Nodes (11): ADR-015: PostgreSQL polling for Agroclimatic Evaluation worker dispatch, Consequences, Context, Decision, Status, Agroclimatic Evaluation request, worker, recovery, and read slice, Current lifecycle and execution, Deliberately deferred (+3 more)

### Community 165 - "Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation, Source Nodes

### Community 166 - "Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors, Source Nodes

### Community 167 - "PostgreSQLEvaluationRepository"
Cohesion: 0.10
Nodes (45): PostgreSQLEvaluationRepository, SessionFactory, Durable adapter for immutable Evaluation aggregates., ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., Read and validate the test-only database settings before any DB operation. (+37 more)

### Community 170 - "crop_suitability_main.py"
Cohesion: 0.18
Nodes (16): calcification_map(), cropsuitability(), get_suitability_val_dict(), get_texture_class(), get_valid_dtype(), getTable(), output_param_data(), ndarray (+8 more)

### Community 172 - "SpatialExtent"
Cohesion: 0.13
Nodes (23): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine (+15 more)

### Community 175 - "Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment., Source Nodes

### Community 177 - "PolicyReference"
Cohesion: 0.12
Nodes (30): DefaultViabilityPolicyConflictError, InvalidViabilityPolicyRevisionError, RuntimeError, ValueError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist., Raised when a requested viability-policy revision is not a new version., Raised when the default policy changed before an expected update. (+22 more)

### Community 178 - "CropComparisonRequest"
Cohesion: 0.09
Nodes (20): CommonSupportResult, CropComparisonEngineError, CropComparisonExecutionError, CropComparisonRequest, CropComparisonResult, ICropComparisonEngine, RuntimeError, Compare crop suitability only on identical valid spatial support. (+12 more)

### Community 181 - "Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract, Source Nodes

### Community 183 - "test_decision_support_postgresql.py"
Cohesion: 0.17
Nodes (30): Decision Support infrastructure adapters., PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+22 more)

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **181 isolated node(s):** `via-backend`, `Status`, `Context`, `Decision`, `Consequences` (+176 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 854 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `Domain dependency rule` (5× useful, score=4.693450858)
- `Application layer` (4× useful, score=3.751913588)
- `EnvironmentalInformationService` (3× useful, score=2.835517884)
- `ParcelGeometry` (3× useful, score=2.828113307)
- `ParcelVersion` (3× useful, score=2.804591321)
- `InMemoryParcelRepository` (3× useful, score=2.803347018)
- `ParcelRepository` (3× useful, score=2.803347017)
- `EvaluationResult` (2× useful, score=1.955274885)
- `Settings` (2× useful, score=1.948868371)
- `Farm Management schema ownership` (2× useful, score=1.909664433)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Crop Code Catalog` and `Undefined Crop Code c32`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `create_app()` connect `DatasetVersion` to `FarmManagementService`, `test_agroclimatic_evaluation_api.py`, `InMemoryEvaluationRepository`, `farm_management/infrastructure/postgresql_repositories.py`, `PostgreSQLEvaluationRepository`, `Dataset`, `EnvironmentalInformationService`, `Project`, `test_environmental_information_api.py`, `Parcel`, `create_database`, `agroclimatic_evaluation/application/__init__.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `DomainValidationError`, `Dataset`, `DatasetVersion`, `SpatialExtent`, `CoverageMeasurement`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `AgroclimaticEvaluationService` connect `agroclimatic_evaluation/application/__init__.py` to `test_agroclimatic_evaluation_api.py`, `workflow.py`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `agroclimatic_evaluation/interfaces/http.py`, `DatasetVersion`, `DomainValidationError`, `EvaluationRepository`, `Evaluation`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `EnvironmentalInformationService` (e.g. with `CreateDataset` and `CreateDatasetVersion`) actually correct?**
  _`EnvironmentalInformationService` has 26 INFERRED edges - model-reasoned connections that need verification._