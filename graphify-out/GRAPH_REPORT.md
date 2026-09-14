# Graph Report - poc_via_cslite  (2026-09-14)

## Corpus Check
- 258 files · ~113,020 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2052 nodes · 4552 edges · 173 communities (99 shown, 31 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 497 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d2318a95`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FarmManagementService
- CropSensitivity
- NexGenPreProcessing
- Huaura Dataset Preprocessing Configuration
- check_files.py
- DomainValidationError
- Project
- Crop Membership Functions
- multicrop.py
- InMemoryEvaluationRepository
- CropSuite.py
- DownloadCMIP6Data
- agroclimatic_evaluation/application/__init__.py
- climate_suitability_main_xarray.py
- CropSuiteLite
- CropSuiteAdapter
- climate_suitability_main.py
- read_crop_parameterizations_files
- CoverageMeasurement
- environmental_information/interfaces/http.py
- test_farm_management_postgresql.py
- VIA architecture guardrails
- Farm Management persistence
- crop_rotation.py
- Architecture and Backend for CropSuiteLite Huaura v2
- Huaura Environmental Correction
- run_cropsuitelite.py
- test_architecture.py
- Farm Management schema ownership
- Bounded-context layered structure
- CropSuiteAdapter
- EnvironmentalCoverageTest
- ADR-011: PostgreSQL/PostGIS persistence for Farm Management
- Application commands and queries
- Farm Management minimum vertical slice
- Python and FastAPI backend decision
- process_precday_interp
- Evaluation
- via_backend/worker.py
- VIA architecture implementation roadmap
- Q: PostgreSQL Farm Management repositories
- EvaluationStatus
- ADR-012: PostgreSQL/PostGIS persistence for Environmental Information
- PostGIS service
- environmental_information/application/ports.py
- Optimistic parcel revision transaction
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
- AgroclimaticEvaluationExecutionService
- DomainValidationError
- agroclimatic_evaluation/infrastructure/__init__.py
- agroclimatic_evaluation/__init__.py
- DomainValidationError
- decision_support/application/__init__.py
- decision_support/domain/__init__.py
- decision_support/infrastructure/__init__.py
- decision_support/__init__.py
- decision_support/interfaces/__init__.py
- EnvironmentalInformationService
- cropsuite_adapter.py
- main.py
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
- DatasetVersion
- Parcel
- test_agroclimatic_evaluation_postgresql.py
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
- create_router
- test_agroclimatic_evaluation_domain.py
- test_environmental_information_api.py
- SpatialExtent
- health.py
- test_agroclimatic_evaluation_queries.py
- Settings
- test_agroclimatic_evaluation_execution.py
- CropOutcome
- test_farm_management_api.py
- test_agroclimatic_evaluation_api.py
- test_farm_management_domain.py
- Agroclimatic Evaluation request, worker, recovery, and read slice
- Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation
- Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors
- test_environmental_information_coverage_postgresql.py
- AgroclimaticEvaluationRecoveryService
- crop_suitability_main.py
- via_backend/infrastructure/database.py
- Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment.

## God Nodes (most connected - your core abstractions)
1. `Evaluation` - 65 edges
2. `EnvironmentalInformationService` - 43 edges
3. `DatasetVersion` - 43 edges
4. `EvaluationStatus` - 40 edges
5. `Parcel` - 38 edges
6. `AgroclimaticEvaluationService` - 37 edges
7. `InMemoryEvaluationRepository` - 35 edges
8. `CropOutcome` - 34 edges
9. `Dataset` - 34 edges
10. `FarmManagementService` - 34 edges

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

## Communities (173 total, 31 thin omitted)

### Community 0 - "FarmManagementService"
Cohesion: 0.08
Nodes (52): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+44 more)

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
Cohesion: 0.17
Nodes (20): DomainValidationError, ValueError, Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring() (+12 more)

### Community 6 - "Project"
Cohesion: 0.09
Nodes (28): Project, An agricultural project that groups parcels., Base, DeclarativeBase, SQLAlchemy metadata owned by Farm Management Infrastructure., Declarative base for Farm Management persistence records., Farm Management infrastructure layer., ParcelRecord (+20 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.10
Nodes (22): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+14 more)

### Community 9 - "InMemoryEvaluationRepository"
Cohesion: 0.14
Nodes (21): AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application., InMemoryEvaluationRepository, UUID, _engine_result(), _evaluation(), FakeEngine, datetime (+13 more)

### Community 10 - "CropSuite.py"
Cohesion: 0.10
Nodes (41): # NOTE: self.extent is modified here to align with grid, create_cog_from_geotiff(), extract_domain_from_global_3draster(), extract_domain_from_global_raster(), geotiff_to_smallest_datatype(), get_cpu_ram(), get_resolution_array(), get_shape_of_raster() (+33 more)

### Community 11 - "DownloadCMIP6Data"
Cohesion: 0.09
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+9 more)

### Community 12 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.11
Nodes (31): Agroclimatic Evaluation application layer., FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedEvaluationResult, FinalizedEvaluationResultReader, FinalizedScientificTrace, FinalizedSuitabilitySummary, GetFinalizedEvaluationResult (+23 more)

### Community 13 - "climate_suitability_main_xarray.py"
Cohesion: 0.10
Nodes (31): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+23 more)

### Community 14 - "CropSuiteLite"
Cohesion: 0.11
Nodes (13): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Calculates climate suitability based on temperature and precipitation.…, Combines climate suitability with soil/terrain data to calculate final crop…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Interpolates or retrieves downscaled climate data (precipitation and… (+5 more)

### Community 15 - "CropSuiteAdapter"
Cohesion: 0.09
Nodes (51): CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability., _file_identity(), FilesystemScientificArtifactStore, _is_within(), PublishedScientificArtifact, Path, RuntimeError (+43 more)

### Community 16 - "climate_suitability_main.py"
Cohesion: 0.09
Nodes (32): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+24 more)

### Community 17 - "read_crop_parameterizations_files"
Cohesion: 0.15
Nodes (12): get_formula(), get_id_list_start(), get_plant_param_interp_forms_dict(), print_crop_param_output(), print_sections(), Reads and parses crop parameterization files from a specified folder path.…, Prints the keys of a given dictionary as a list of sections or items. Args:…, Given two arrays of numerical values x_vals and y_vals representing data… (+4 more)

### Community 18 - "CoverageMeasurement"
Cohesion: 0.14
Nodes (23): CheckDatasetVersionCoverage, CoverageClassification, CoverageCompatibilityFailure, CoverageMeasurement, StrEnum, Structural metadata prevented a meaningful spatial measurement., Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port. (+15 more)

### Community 19 - "environmental_information/interfaces/http.py"
Cohesion: 0.15
Nodes (18): CoverageUnavailableError, RuntimeError, Raised when immutable environmental metadata already exists., Raised when no spatial coverage implementation is configured., ResourceConflictError, CheckCoverageBody, CoverageGeometryBody, CreateDatasetBody (+10 more)

### Community 20 - "test_farm_management_postgresql.py"
Cohesion: 0.28
Nodes (19): clean_farm_management(), database(), _database_url(), _parcel(), _polygon(), _project(), datetime, Engine (+11 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management persistence"
Cohesion: 0.15
Nodes (15): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations, Farm Management persistence, PostGIS geometry storage contract (+7 more)

### Community 23 - "crop_rotation.py"
Cohesion: 0.16
Nodes (17): calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):…, Read a GeoTIFF file with multiple bands into a NumPy array. Parameters: - fn… (+9 more)

### Community 24 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.18
Nodes (11): Common-Support Ranking, ADR-002 Layered Bounded Contexts, ADR-003 Commands and Queries in Application, ADR-005 Background Worker, ADR-007 Initial Deployment, ADR-008 Sequential Crop Execution, ADR-009 Multicrop Evaluation, Architecture and Backend for CropSuiteLite Huaura v2 (+3 more)

### Community 25 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 26 - "run_cropsuitelite.py"
Cohesion: 0.19
Nodes (15): change_otherst_parameters(), change_st1_parameter(), create_crop_parameters(), create_crop_suite_configuration_file(), find_solution_type(), main(), modify_extent(), modify_general_files() (+7 more)

### Community 27 - "test_architecture.py"
Cohesion: 0.18
Nodes (11): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_domain_packages_do_not_import_outward_layers(), test_environmental_information_does_not_import_other_contexts() (+3 more)

### Community 28 - "Farm Management schema ownership"
Cohesion: 0.20
Nodes (10): Farm Management schema ownership, Projects, parcels, and parcel_versions tables, farm_management schema and owned tables, Optional durable repository adapter, Project, Parcel, and ParcelVersion domain model, Result querying increment, Bounded-context ownership and Farm Management repositories, Farm Management ownership query (+2 more)

### Community 29 - "Bounded-context layered structure"
Cohesion: 0.28
Nodes (9): Bounded-context ownership, Anti-corruption layer, Application layer, Bounded-context layered structure, Domain layer, Illustrative Evaluation module structure, Infrastructure layer, Interfaces layer (+1 more)

### Community 30 - "CropSuiteAdapter"
Cohesion: 0.46
Nodes (8): Multicrop Parcel Evaluation, run_evaluation Service, ADR-004 CropSuiteLite Port and Adapter, CropSuiteLite isolation boundary, CropSuiteAdapter, CropSuiteLite Integration Boundary, ICropSuitabilityEngine, On-demand execution increment

### Community 31 - "EnvironmentalCoverageTest"
Cohesion: 0.19
Nodes (4): calculate_slope(), covered_gradient(), Central differences inside coverage, one-sided at its boundary. An axis with no…, EnvironmentalCoverageTest

### Community 32 - "ADR-011: PostgreSQL/PostGIS persistence for Farm Management"
Cohesion: 0.29
Nodes (5): ADR-011: PostgreSQL/PostGIS persistence for Farm Management, Consequences, Context, Decision, Status

### Community 33 - "Application commands and queries"
Cohesion: 0.29
Nodes (8): Application commands and queries, FastAPI composition root, In-memory and durable Infrastructure adapters, Project and parcel HTTP resources, Farm Management repository abstractions, Transport-to-domain path, ProjectRepository, ParcelRepository, and in-memory adapters, Repository ports and in-memory adapters query

### Community 34 - "Farm Management minimum vertical slice"
Cohesion: 0.25
Nodes (8): Architectural alignment, Slice exclusions and authorization dependency, Explicit exclusions and provisional choices, Farm Management minimum vertical slice, Parcel geometry invariants, HTTP resources, Invariants in this increment, Scope

### Community 35 - "Python and FastAPI backend decision"
Cohesion: 0.14
Nodes (14): Domain dependency rule, Background worker execution, FastAPI, Layered modular monolith, Python, Python and FastAPI backend decision, Inward dependency direction, Open backend modeling decisions (+6 more)

### Community 36 - "process_precday_interp"
Cohesion: 0.26
Nodes (4): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall.

### Community 37 - "Evaluation"
Cohesion: 0.07
Nodes (31): Synchronous application orchestration for persisted evaluations., _to_outcome(), Explicit fail-only recovery for abandoned evaluation executions., CropOutcomeResult, Transport-neutral Agroclimatic Evaluation results., EvaluationConflictError, InvalidEvaluationTransitionError, RuntimeError (+23 more)

### Community 38 - "via_backend/worker.py"
Cohesion: 0.16
Nodes (16): ArgumentParser, create_database(), Engine, SessionFactory, Create the shared engine and short-lived session factory., create_worker(), main(), _parser() (+8 more)

### Community 39 - "VIA architecture implementation roadmap"
Cohesion: 0.33
Nodes (7): Architecture source and PoC preservation, Cross-stage architecture gates, Explanation and comparison increment, Modeling increment, Parcel and environmental coverage increment, Public deployment increment, VIA architecture implementation roadmap

### Community 40 - "Q: PostgreSQL Farm Management repositories"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: PostgreSQL Farm Management repositories, Source Nodes

### Community 41 - "EvaluationStatus"
Cohesion: 0.16
Nodes (22): EvaluationResultAvailability, StrEnum, Whether persisted outcomes are pending, partial, or final., EvaluationStatus, StrEnum, Architecture-approved lifecycle vocabulary., CropEvidenceResponse, CropOutcomeResponse (+14 more)

### Community 42 - "ADR-012: PostgreSQL/PostGIS persistence for Environmental Information"
Cohesion: 0.12
Nodes (18): ADR-012: PostgreSQL/PostGIS persistence for Environmental Information, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation, Decision Support (+10 more)

### Community 43 - "PostGIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "environmental_information/application/ports.py"
Cohesion: 0.13
Nodes (13): InvalidSpatialInputError, CoverageComputation, Protocol, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute. (+5 more)

### Community 45 - "Optimistic parcel revision transaction"
Cohesion: 0.50
Nodes (5): Optimistic parcel revision transaction, ParcelVersionConflictError, Revision concurrency, Optimistic stale-write handling query, ParcelRepository stale-write conflict handling

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

### Community 63 - "AgroclimaticEvaluationExecutionService"
Cohesion: 0.09
Nodes (24): ExecuteEvaluation, Commands expressing Agroclimatic Evaluation use-case intent., Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, Exception, Execute requested crops sequentially through the Application-owned port., ICropSuitabilityEngine, Protocol (+16 more)

### Community 64 - "DomainValidationError"
Cohesion: 0.12
Nodes (24): DomainValidationError, ValueError, Raised when evaluation data violates a domain invariant., Immutable spatial grid identity for a scientific raster., Durable scientific evidence referenced without exposing filesystem paths., ScientificArtifact, ScientificArtifactGrid, _parse_multi_polygon() (+16 more)

### Community 65 - "agroclimatic_evaluation/infrastructure/__init__.py"
Cohesion: 0.16
Nodes (13): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online(), Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure. (+5 more)

### Community 67 - "DomainValidationError"
Cohesion: 0.16
Nodes (21): CoverageGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing, MultiPolygonCoordinates (+13 more)

### Community 73 - "EnvironmentalInformationService"
Cohesion: 0.09
Nodes (38): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., GetDataset, GetDatasetVersion, ListDatasets, ListDatasetVersions (+30 more)

### Community 74 - "cropsuite_adapter.py"
Cohesion: 0.08
Nodes (54): CropExecutionStatus, CropSuitabilityEngineError, CropSuitabilityExecutionError, CropSuitabilityRequest, CropSuitabilityResult, InvalidEngineOutputError, RuntimeError, StrEnum (+46 more)

### Community 75 - "main.py"
Cohesion: 0.09
Nodes (26): Base, DeclarativeBase, SQLAlchemy metadata owned by Environmental Information Infrastructure., Declarative base for Environmental Information persistence records., Environmental Information infrastructure layer., DatasetRecord, DatasetVersionRecord, Database records for Environmental Information; not domain entities. (+18 more)

### Community 77 - "Q: ParcelVersion persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ParcelVersion persistence, Source Nodes

### Community 93 - "Q: Domain-to-Infrastructure dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Domain-to-Infrastructure dependency violations, Source Nodes

### Community 135 - "DatasetVersion"
Cohesion: 0.09
Nodes (27): datetime, Environmental Information command and query coordination., DatasetVersionConflictError, RuntimeError, Domain errors raised by Environmental Information invariants., Raised when a dataset version identifier has already been registered., Environmental Information domain layer., Dataset (+19 more)

### Community 136 - "Parcel"
Cohesion: 0.07
Nodes (25): datetime, ParcelVersionConflictError, RuntimeError, Domain errors raised by Farm Management invariants., Raised when persisted parcel history changed before a revision was saved., Farm Management domain layer., Parcel, ParcelVersion (+17 more)

### Community 137 - "test_agroclimatic_evaluation_postgresql.py"
Cohesion: 0.25
Nodes (20): clean_evaluations(), database(), _database_url(), _evaluation(), _multipolygon(), _polygon(), Engine, fixture (+12 more)

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

### Community 150 - "create_router"
Cohesion: 0.21
Nodes (15): ParcelSnapshotInput, Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, GetEvaluation, create_router(), get_evaluation(), get_evaluation_evidence(), get_evaluation_result() (+7 more)

### Community 151 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.36
Nodes (9): _evaluation(), _polygon(), parametrize, Focused domain tests for immutable evaluation requests., _snapshot(), test_empty_or_duplicate_requested_crops_are_rejected(), test_parcel_snapshot_is_deeply_immutable_and_detached_from_input(), test_polygon_and_multipolygon_snapshot_geometry_are_supported() (+1 more)

### Community 152 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 154 - "SpatialExtent"
Cohesion: 0.23
Nodes (9): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, parametrize, Unit tests for Environmental Information invariants., test_dataset_version_is_immutable(), test_extent_must_be_ordered(), test_invalid_dataset_version_metadata_is_rejected(), test_resolution_must_be_finite_and_positive() (+1 more)

### Community 155 - "health.py"
Cohesion: 0.40
Nodes (4): health(), Host-level health endpoint., Report that the API process is ready to receive requests., get

### Community 157 - "test_agroclimatic_evaluation_queries.py"
Cohesion: 0.18
Nodes (11): _evaluation(), _outcome(), parametrize, UUID, Focused Application query tests for Agroclimatic Evaluation., Repository double that fails if a query touches a mutation/worker method., _ReadOnlySpyRepository, _service() (+3 more)

### Community 158 - "Settings"
Cohesion: 0.11
Nodes (22): _environment_float(), _environment_integer(), _optional_path(), Path, Environment-backed configuration for the VIA application host., Settings needed by the current backend composition root., Settings for the PostgreSQL polling worker process., Settings (+14 more)

### Community 159 - "test_agroclimatic_evaluation_execution.py"
Cohesion: 0.20
Nodes (20): The reliable parcel summary currently returned by the scientific boundary., SuitabilitySummary, _evaluation(), _execute(), FakeEngine, Exception, parametrize, Fast tests for synchronous Agroclimatic Evaluation orchestration. (+12 more)

### Community 160 - "CropOutcome"
Cohesion: 0.17
Nodes (16): CropOutcome, One durable result associated with an Evaluation and requested crop., Current reproducibility trace without engine-specific filesystem details., ScientificTrace, CropOutcomeRecord, _evaluation_query(), _load_outcomes(), _multipolygon_wkt() (+8 more)

### Community 161 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 162 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.20
Nodes (23): Agroclimatic Evaluation interface layer., _app_with(), _body(), _completed_outcomes(), _evaluation(), _outcome(), Any, FastAPI (+15 more)

### Community 163 - "test_farm_management_domain.py"
Cohesion: 0.40
Nodes (5): _polygon(), parametrize, Unit tests for Farm Management invariants., test_invalid_geometry_is_rejected(), test_revising_geometry_appends_an_immutable_version()

### Community 164 - "Agroclimatic Evaluation request, worker, recovery, and read slice"
Cohesion: 0.15
Nodes (11): ADR-015: PostgreSQL polling for Agroclimatic Evaluation worker dispatch, Consequences, Context, Decision, Status, Agroclimatic Evaluation request, worker, recovery, and read slice, Current lifecycle and execution, Deliberately deferred (+3 more)

### Community 165 - "Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation, Source Nodes

### Community 166 - "Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors, Source Nodes

### Community 167 - "test_environmental_information_coverage_postgresql.py"
Cohesion: 0.09
Nodes (41): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., Read and validate the test-only database settings before any DB operation., require_test_database_url(), UnsafeTestDatabaseError, validate_test_database_url() (+33 more)

### Community 169 - "AgroclimaticEvaluationRecoveryService"
Cohesion: 0.18
Nodes (16): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Mark an operator-confirmed active orphan as failed without retrying it., _evaluation_in_status(), _outcome(), Exception, parametrize (+8 more)

### Community 170 - "crop_suitability_main.py"
Cohesion: 0.13
Nodes (23): aggregate_soil_raster_lst(), calcification_map(), cropsuitability(), get_soil_data(), get_suitability_val_dict(), get_texture_class(), get_valid_dtype(), getTable() (+15 more)

### Community 175 - "Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment., Source Nodes

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **178 isolated node(s):** `via-backend`, `Status`, `Context`, `Decision`, `Consequences` (+173 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 757 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `Domain dependency rule` (5× useful, score=4.812582038)
- `Application layer` (4× useful, score=3.847146267)
- `EnvironmentalInformationService` (3× useful, score=2.907490214)
- `ParcelGeometry` (3× useful, score=2.899897691)
- `ParcelVersion` (3× useful, score=2.87577866)
- `InMemoryParcelRepository` (3× useful, score=2.874502774)
- `ParcelRepository` (3× useful, score=2.874502772)
- `Settings` (2× useful, score=1.998335383) _(code changed — re-verify)_
- `Farm Management schema ownership` (2× useful, score=1.958136354)
- `CoverageGeometry` (2× useful, score=1.942051663)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Crop Code Catalog` and `Undefined Crop Code c32`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `DomainValidationError`, `DatasetVersion`, `main.py`, `environmental_information/application/ports.py`, `CoverageMeasurement`, `environmental_information/interfaces/http.py`, `SpatialExtent`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `create_app()` connect `main.py` to `CropOutcome`, `FarmManagementService`, `test_agroclimatic_evaluation_api.py`, `test_farm_management_api.py`, `Project`, `DatasetVersion`, `Parcel`, `InMemoryEvaluationRepository`, `EnvironmentalInformationService`, `via_backend/worker.py`, `agroclimatic_evaluation/application/__init__.py`, `create_router`, `test_environmental_information_api.py`, `Settings`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `FarmManagementService` connect `FarmManagementService` to `Parcel`, `main.py`, `DomainValidationError`, `Project`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_availability()`) actually correct?**
  _`Evaluation` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `EnvironmentalInformationService` (e.g. with `CreateDataset` and `CreateDatasetVersion`) actually correct?**
  _`EnvironmentalInformationService` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `DatasetVersion` (e.g. with `SpatialCoveragePort` and `DatasetVersionResult`) actually correct?**
  _`DatasetVersion` has 12 INFERRED edges - model-reasoned connections that need verification._