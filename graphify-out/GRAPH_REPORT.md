# Graph Report - poc_via_cslite  (2026-09-12)

## Corpus Check
- 238 files · ~101,064 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1712 nodes · 3489 edges · 155 communities (84 shown, 30 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 313 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `84267d92`
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
- crop_suitability_main.py
- data_tools.py
- DownloadCMIP6Data
- Parcel
- climate_suitability_main_xarray.py
- CropSuiteLite
- main.py
- climate_suitability_main.py
- read_plant_params.py
- _service
- cropsuite_adapter.py
- test_farm_management_postgresql.py
- VIA architecture guardrails
- Farm Management persistence
- nc_tools.py
- Architecture and Backend for CropSuiteLite Huaura v2
- Huaura Environmental Correction
- DatasetVersion
- test_architecture.py
- Farm Management schema ownership
- Bounded-context layered structure
- CropSuiteAdapter
- test_environmental_coverage.py
- ADR-011: PostgreSQL/PostGIS persistence for Farm Management
- Application commands and queries
- Farm Management minimum vertical slice
- Inward dependency direction
- write_to_netcdf
- Evaluation
- test_environmental_information_postgresql.py
- VIA architecture implementation roadmap
- Q: PostgreSQL Farm Management repositories
- test_farm_management_domain.py
- ADR-012: PostgreSQL/PostGIS persistence for Environmental Information
- PostGIS service
- SpatialExtent
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
- agroclimatic_evaluation/interfaces/http.py
- DomainValidationError
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- agroclimatic_evaluation/__init__.py
- DomainValidationError
- decision_support/application/__init__.py
- decision_support/domain/__init__.py
- decision_support/infrastructure/__init__.py
- decision_support/__init__.py
- decision_support/interfaces/__init__.py
- EnvironmentalInformationService
- SpatialResolution
- Dataset
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
- DatasetRepository
- Project
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
- ADR-013: PostgreSQL/PostGIS persistence for Agroclimatic Evaluation
- CropSuite.py
- test_agroclimatic_evaluation_domain.py
- env.py
- Python and FastAPI backend decision

## God Nodes (most connected - your core abstractions)
1. `EnvironmentalInformationService` - 43 edges
2. `DatasetVersion` - 43 edges
3. `Parcel` - 38 edges
4. `Dataset` - 34 edges
5. `FarmManagementService` - 34 edges
6. `Evaluation` - 31 edges
7. `DomainValidationError` - 30 edges
8. `Project` - 28 edges
9. `create_app()` - 27 edges
10. `AgroclimaticEvaluationService` - 23 edges

## Surprising Connections (you probably didn't know these)
- `PostgreSQL/PostGIS durable persistence workflow` --semantically_similar_to--> `Farm Management persistence`  [INFERRED] [semantically similar]
  graphify-out/memory/query_20260912_070850_44f16014_continue_the_farm_management_durable_persistence_i.md → docs/architecture/farm-management-persistence.md
- `ParcelRepository stale-write conflict handling` --semantically_similar_to--> `Revision concurrency`  [INFERRED] [semantically similar]
  graphify-out/memory/query_20260912_060606_5f4afb72_optimistic_stale_write_handling_introduced_in_the.md → docs/architecture/farm-management-persistence.md
- `Recoverable job mechanism` --semantically_similar_to--> `Recoverable background worker flow`  [INFERRED] [semantically similar]
  docs/architecture/overview.md → AGENTS.md
- `ADR-001 Modular Monolith` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-001-modular-monolith.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md
- `PostgreSQL/PostGIS durable persistence workflow` --semantically_similar_to--> `Durable Farm Management persistence`  [INFERRED] [semantically similar]
  graphify-out/memory/query_20260912_070850_44f16014_continue_the_farm_management_durable_persistence_i.md → docs/adr/ADR-011-postgresql-postgis-farm-persistence.md

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

## Communities (155 total, 30 thin omitted)

### Community 0 - "FarmManagementService"
Cohesion: 0.06
Nodes (59): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+51 more)

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
Cohesion: 0.17
Nodes (20): DomainValidationError, ValueError, Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring() (+12 more)

### Community 6 - "farm_management/infrastructure/postgresql_repositories.py"
Cohesion: 0.15
Nodes (21): Base, DeclarativeBase, SQLAlchemy metadata owned by Farm Management Infrastructure., Declarative base for Farm Management persistence records., Farm Management infrastructure layer., ParcelRecord, ParcelVersionRecord, ProjectRecord (+13 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.10
Nodes (22): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+14 more)

### Community 9 - "crop_suitability_main.py"
Cohesion: 0.13
Nodes (23): aggregate_soil_raster_lst(), calcification_map(), cropsuitability(), get_soil_data(), get_suitability_val_dict(), get_texture_class(), get_valid_dtype(), getTable() (+15 more)

### Community 10 - "data_tools.py"
Cohesion: 0.14
Nodes (26): Combines climate suitability with soil/terrain data to calculate final crop…, Interpolates or retrieves downscaled climate data (precipitation and…, extract_domain_from_global_3draster(), extract_domain_from_global_raster(), get_cpu_ram(), get_resolution_array(), get_shape_of_raster(), interpolate_nanmask() (+18 more)

### Community 11 - "DownloadCMIP6Data"
Cohesion: 0.09
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+9 more)

### Community 12 - "Parcel"
Cohesion: 0.10
Nodes (18): ParcelVersionConflictError, RuntimeError, Domain errors raised by Farm Management invariants., Raised when persisted parcel history changed before a revision was saved., Farm Management domain layer., Parcel, ParcelVersion, datetime (+10 more)

### Community 13 - "climate_suitability_main_xarray.py"
Cohesion: 0.10
Nodes (31): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+23 more)

### Community 14 - "CropSuiteLite"
Cohesion: 0.13
Nodes (11): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Calculates climate suitability based on temperature and precipitation.…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Calculates grid tiling based on available RAM to prevent memory overflow.…, Private subprocess entry point; each invocation has its own working directory. (+3 more)

### Community 15 - "main.py"
Cohesion: 0.06
Nodes (52): Environment-backed configuration for the VIA application host., Settings needed by the current backend composition root., Settings, health(), Host-level health endpoint., Report that the API process is ready to receive requests., create_app(), FastAPI application composition root. (+44 more)

### Community 16 - "climate_suitability_main.py"
Cohesion: 0.09
Nodes (31): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+23 more)

### Community 17 - "read_plant_params.py"
Cohesion: 0.15
Nodes (10): get_formula(), get_id_list_start(), get_plant_param_interp_forms_dict(), print_crop_param_output(), print_sections(), Prints the keys of a given dictionary as a list of sections or items. Args:…, Given two arrays of numerical values x_vals and y_vals representing data…, Prints the number of crop parameterizations found and the keys of a given… (+2 more)

### Community 18 - "_service"
Cohesion: 0.23
Nodes (15): _multi_polygon(), _polygon(), Any, parametrize, Fast tests for Environmental Information coverage orchestration., _service(), StubCoveragePort, test_application_distinguishes_coverage_classes() (+7 more)

### Community 19 - "cropsuite_adapter.py"
Cohesion: 0.07
Nodes (70): Agroclimatic Evaluation application layer., CropExecutionStatus, CropSuitabilityEngineError, CropSuitabilityExecutionError, CropSuitabilityRequest, CropSuitabilityResult, ICropSuitabilityEngine, InvalidEngineOutputError (+62 more)

### Community 20 - "test_farm_management_postgresql.py"
Cohesion: 0.30
Nodes (18): clean_farm_management(), database(), _database_url(), _parcel(), _polygon(), _project(), datetime, Engine (+10 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management persistence"
Cohesion: 0.15
Nodes (15): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations, Farm Management persistence, PostGIS geometry storage contract (+7 more)

### Community 23 - "nc_tools.py"
Cohesion: 0.22
Nodes (12): create_cog_from_geotiff(), geotiff_to_smallest_datatype(), Convert image to COG., merge_outputs_no_overlap(), get_netcdf_extent(), merge_netcdf_files(), downscaled_files: list of netcdf files overlap: In Degree extent: [North, Left,…, Get the spatial extent (min and max) of the latitude and longitude in a NetCDF… (+4 more)

### Community 24 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.18
Nodes (11): Common-Support Ranking, ADR-002 Layered Bounded Contexts, ADR-003 Commands and Queries in Application, ADR-005 Background Worker, ADR-007 Initial Deployment, ADR-008 Sequential Crop Execution, ADR-009 Multicrop Evaluation, Architecture and Backend for CropSuiteLite Huaura v2 (+3 more)

### Community 25 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 26 - "DatasetVersion"
Cohesion: 0.15
Nodes (13): CoverageComputation, DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., DatasetVersion, Immutable reproducibility metadata for one dataset release., _version_record(), InMemoryDatasetVersionRepository (+5 more)

### Community 27 - "test_architecture.py"
Cohesion: 0.26
Nodes (9): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_domain_packages_do_not_import_outward_layers(), test_environmental_information_does_not_import_other_contexts() (+1 more)

### Community 28 - "Farm Management schema ownership"
Cohesion: 0.20
Nodes (10): Farm Management schema ownership, Projects, parcels, and parcel_versions tables, farm_management schema and owned tables, Optional durable repository adapter, Project, Parcel, and ParcelVersion domain model, Result querying increment, Bounded-context ownership and Farm Management repositories, Farm Management ownership query (+2 more)

### Community 29 - "Bounded-context layered structure"
Cohesion: 0.28
Nodes (9): Bounded-context ownership, Anti-corruption layer, Application layer, Bounded-context layered structure, Domain layer, Illustrative Evaluation module structure, Infrastructure layer, Interfaces layer (+1 more)

### Community 30 - "CropSuiteAdapter"
Cohesion: 0.46
Nodes (8): Multicrop Parcel Evaluation, run_evaluation Service, ADR-004 CropSuiteLite Port and Adapter, CropSuiteLite isolation boundary, CropSuiteAdapter, CropSuiteLite Integration Boundary, ICropSuitabilityEngine, On-demand execution increment

### Community 31 - "test_environmental_coverage.py"
Cohesion: 0.18
Nodes (8): calculate_slope(), process_tempday_interp(), covered_gradient(), Spatial operations that preserve missing coverage instead of creating zeros., Central differences inside coverage, one-sided at its boundary. An axis with no…, Temporarily nearest-fill gaps, resample, then restore the coverage mask., resample_valid(), EnvironmentalCoverageTest

### Community 32 - "ADR-011: PostgreSQL/PostGIS persistence for Farm Management"
Cohesion: 0.29
Nodes (5): ADR-011: PostgreSQL/PostGIS persistence for Farm Management, Consequences, Context, Decision, Status

### Community 33 - "Application commands and queries"
Cohesion: 0.29
Nodes (8): Application commands and queries, FastAPI composition root, In-memory and durable Infrastructure adapters, Project and parcel HTTP resources, Farm Management repository abstractions, Transport-to-domain path, ProjectRepository, ParcelRepository, and in-memory adapters, Repository ports and in-memory adapters query

### Community 34 - "Farm Management minimum vertical slice"
Cohesion: 0.25
Nodes (8): Architectural alignment, Slice exclusions and authorization dependency, Explicit exclusions and provisional choices, Farm Management minimum vertical slice, Parcel geometry invariants, HTTP resources, Invariants in this increment, Scope

### Community 35 - "Inward dependency direction"
Cohesion: 0.22
Nodes (9): Domain dependency rule, Layered modular monolith, Inward dependency direction, Modular foundation increment, Backend architecture consistency evidence, Backend foundation architecture verification query, Bounded-context package foundation, health() endpoint (+1 more)

### Community 36 - "write_to_netcdf"
Cohesion: 0.26
Nodes (5): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, write_to_netcdf(), PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall.

### Community 37 - "Evaluation"
Cohesion: 0.10
Nodes (21): Transport-neutral Agroclimatic Evaluation results., datetime, UUID, Agroclimatic Evaluation command and query coordination., Agroclimatic Evaluation domain layer., Evaluation, EvaluationStatus, StrEnum (+13 more)

### Community 38 - "test_environmental_information_postgresql.py"
Cohesion: 0.17
Nodes (18): create_database(), Engine, SessionFactory, Host-level SQLAlchemy engine and session construction., Create the shared engine and short-lived session factory., Shared technical infrastructure used by the application composition root., clean_environmental_information(), database() (+10 more)

### Community 39 - "VIA architecture implementation roadmap"
Cohesion: 0.33
Nodes (7): Architecture source and PoC preservation, Cross-stage architecture gates, Explanation and comparison increment, Modeling increment, Parcel and environmental coverage increment, Public deployment increment, VIA architecture implementation roadmap

### Community 40 - "Q: PostgreSQL Farm Management repositories"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: PostgreSQL Farm Management repositories, Source Nodes

### Community 41 - "test_farm_management_domain.py"
Cohesion: 0.40
Nodes (5): _polygon(), parametrize, Unit tests for Farm Management invariants., test_invalid_geometry_is_rejected(), test_revising_geometry_appends_an_immutable_version()

### Community 42 - "ADR-012: PostgreSQL/PostGIS persistence for Environmental Information"
Cohesion: 0.12
Nodes (18): ADR-012: PostgreSQL/PostGIS persistence for Environmental Information, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation, Decision Support (+10 more)

### Community 43 - "PostGIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "SpatialExtent"
Cohesion: 0.20
Nodes (16): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine (+8 more)

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

### Community 63 - "agroclimatic_evaluation/interfaces/http.py"
Cohesion: 0.08
Nodes (38): ParcelSnapshotInput, Commands expressing Agroclimatic Evaluation use-case intent., Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, GetEvaluation, ListEvaluations, Queries supported by Agroclimatic Evaluation., EvaluationResult (+30 more)

### Community 64 - "DomainValidationError"
Cohesion: 0.21
Nodes (18): DomainValidationError, ValueError, Raised when evaluation data violates a domain invariant., _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any (+10 more)

### Community 65 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.12
Nodes (21): EvaluationConflictError, RuntimeError, Domain errors for Agroclimatic Evaluation., Raised when an evaluation identity already exists., Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records. (+13 more)

### Community 67 - "DomainValidationError"
Cohesion: 0.08
Nodes (42): InvalidSpatialInputError, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, CoverageCompatibilityFailure (+34 more)

### Community 73 - "EnvironmentalInformationService"
Cohesion: 0.06
Nodes (65): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort, CheckDatasetVersionCoverage (+57 more)

### Community 74 - "SpatialResolution"
Cohesion: 0.29
Nodes (9): Positive horizontal and vertical source-cell resolution., SpatialResolution, parametrize, Unit tests for Environmental Information invariants., test_dataset_version_is_immutable(), test_extent_must_be_ordered(), test_invalid_dataset_version_metadata_is_rejected(), test_resolution_must_be_finite_and_positive() (+1 more)

### Community 75 - "Dataset"
Cohesion: 0.11
Nodes (19): Dataset, Stable logical identity for a geoenvironmental dataset., Base, DeclarativeBase, SQLAlchemy metadata owned by Environmental Information Infrastructure., Declarative base for Environmental Information persistence records., Environmental Information infrastructure layer., DatasetRecord (+11 more)

### Community 77 - "Q: ParcelVersion persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ParcelVersion persistence, Source Nodes

### Community 93 - "Q: Domain-to-Infrastructure dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Domain-to-Infrastructure dependency violations, Source Nodes

### Community 135 - "DatasetRepository"
Cohesion: 0.23
Nodes (5): DatasetRepository, DatasetVersionRepository, Protocol, UUID, Repository abstractions for Environmental Information aggregates.

### Community 136 - "Project"
Cohesion: 0.16
Nodes (8): Project, An agricultural project that groups parcels., PostgreSQLProjectRepository, _project_from_record(), SessionFactory, Durable adapter for the Project aggregate., InMemoryProjectRepository, Process-local project storage for the first vertical slice.

### Community 137 - "test_agroclimatic_evaluation_postgresql.py"
Cohesion: 0.28
Nodes (15): clean_evaluations(), database(), _database_url(), _evaluation(), _multipolygon(), _polygon(), Engine, fixture (+7 more)

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

### Community 149 - "ADR-013: PostgreSQL/PostGIS persistence for Agroclimatic Evaluation"
Cohesion: 0.12
Nodes (14): ADR-006 Scientific Traceability, ADR-013: PostgreSQL/PostGIS persistence for Agroclimatic Evaluation, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation request slice (+6 more)

### Community 150 - "CropSuite.py"
Cohesion: 0.15
Nodes (20): # NOTE: self.extent is modified here to align with grid, calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):… (+12 more)

### Community 151 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.33
Nodes (10): _evaluation(), _polygon(), parametrize, Focused domain tests for immutable evaluation requests., _snapshot(), test_empty_or_duplicate_requested_crops_are_rejected(), test_parcel_snapshot_is_deeply_immutable_and_detached_from_input(), test_polygon_and_multipolygon_snapshot_geometry_are_supported() (+2 more)

### Community 152 - "env.py"
Cohesion: 0.47
Nodes (5): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online()

### Community 154 - "Python and FastAPI backend decision"
Cohesion: 0.40
Nodes (5): Background worker execution, FastAPI, Python, Python and FastAPI backend decision, Open backend modeling decisions

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **164 isolated node(s):** `via-backend`, `Status`, `Context`, `Decision`, `Consequences` (+159 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 667 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `Domain dependency rule` (5× useful, score=4.934239422)
- `Application layer` (4× useful, score=3.944398375)
- `EnvironmentalInformationService` (3× useful, score=2.980988733)
- `ParcelGeometry` (3× useful, score=2.973204278)
- `ParcelVersion` (3× useful, score=2.948475542)
- `InMemoryParcelRepository` (3× useful, score=2.947167402)
- `ParcelRepository` (3× useful, score=2.947167401)
- `CoverageGeometry` (2× useful, score=1.991144837)
- `DatasetVersion` (2× useful, score=1.985416427)
- `Infrastructure-only persistence mapping` (2× useful, score=1.979290424)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Crop Code Catalog` and `Undefined Crop Code c32`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `DomainValidationError`, `DatasetRepository`, `SpatialResolution`, `Dataset`, `SpatialExtent`, `main.py`, `_service`, `DatasetVersion`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `create_app()` connect `main.py` to `FarmManagementService`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `DomainValidationError`, `Evaluation`, `farm_management/infrastructure/postgresql_repositories.py`, `test_environmental_information_postgresql.py`, `Project`, `EnvironmentalInformationService`, `Dataset`, `Parcel`, `DatasetVersion`, `agroclimatic_evaluation/interfaces/http.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `FarmManagementService` connect `FarmManagementService` to `Project`, `Parcel`, `DomainValidationError`, `main.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `EnvironmentalInformationService` (e.g. with `CreateDataset` and `CreateDatasetVersion`) actually correct?**
  _`EnvironmentalInformationService` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `DatasetVersion` (e.g. with `SpatialCoveragePort` and `DatasetVersionResult`) actually correct?**
  _`DatasetVersion` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Parcel` (e.g. with `ParcelResult` and `FarmManagementService`) actually correct?**
  _`Parcel` has 11 INFERRED edges - model-reasoned connections that need verification._