# Graph Report - poc_via_cslite  (2026-09-12)

## Corpus Check
- 41 files · ~84,327 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1068 nodes · 1865 edges · 134 communities (54 shown, 42 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 137 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FarmManagementService
- run_cropsuitelite.py
- NexGenPreProcessing
- Huaura Dataset Preprocessing Configuration
- check_files.py
- DomainValidationError
- postgresql_repositories.py
- Crop Membership Functions
- multicrop.py
- crop_suitability_main.py
- downscaling.py
- DownloadCMIP6Data
- InMemoryParcelRepository
- climate_suitability_main_xarray.py
- CropSuiteLite
- Settings
- climate_suitability_main.py
- test_environmental_coverage.py
- test_farm_management_postgresql.py
- crop_rotation.py
- Project
- VIA architecture guardrails
- Farm Management minimum vertical slice
- CropSuite.py
- Architecture and Backend for CropSuiteLite Huaura v2
- Huaura Environmental Correction
- climate_suitability_main.py
- test_architecture.py
- Farm Management schema ownership
- Bounded-context layered structure
- CropSuiteAdapter
- EnvironmentalCoverageTest
- Farm Management minimum vertical slice
- Application commands and queries
- Farm Management minimum vertical slice
- Backend foundation architecture verification query
- PrecipitationCoastTest
- PrecipitationUnitsTest
- Python and FastAPI backend decision
- Huaura Environmental Correction
- env.py
- ParcelGeometry
- Proposed Bounded Contexts
- Post GIS service
- FarmManagementService
- Farm Management minimum vertical slice
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
- agroclimatic_evaluation/application/__init__.py
- agroclimatic_evaluation/domain/__init__.py
- agroclimatic_evaluation/infrastructure/__init__.py
- agroclimatic_evaluation/__init__.py
- agroclimatic_evaluation/interfaces/__init__.py
- decision_support/application/__init__.py
- decision_support/domain/__init__.py
- decision_support/infrastructure/__init__.py
- decision_support/__init__.py
- decision_support/interfaces/__init__.py
- environmental_information/application/__init__.py
- environmental_information/domain/__init__.py
- environmental_information/infrastructure/__init__.py
- environmental_information/__init__.py
- environmental_information/interfaces/__init__.py
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
- test_architecture.py
- Documentation Deployment Workflow
- Suitability and Limiting-Factor Outputs
- Nodata Coverage Conservation
- Membership Functions Diagram
- Modified Membership Functions Diagram
- CropSuiteLite Conda Environment
- Logical and deployment boundary separation
- via-backend

## God Nodes (most connected - your core abstractions)
1. `Parcel` - 38 edges
2. `FarmManagementService` - 34 edges
3. `Project` - 28 edges
4. `create_router()` - 21 edges
5. `climsuit_new()` - 20 edges
6. `DomainValidationError` - 20 edges
7. `ParcelGeometry` - 20 edges
8. `CropSensitivity` - 19 edges
9. `process_day_climsuit_xarray()` - 19 edges
10. `ParcelVersion` - 17 edges

## Surprising Connections (you probably didn't know these)
- `PostgreSQL/PostGIS durable persistence workflow` --semantically_similar_to--> `Farm Management persistence`  [INFERRED] [semantically similar]
  graphify-out/memory/query_20260912_070850_44f16014_continue_the_farm_management_durable_persistence_i.md → docs/architecture/farm-management-persistence.md
- `ParcelRepository stale-write conflict handling` --semantically_similar_to--> `Revision concurrency`  [INFERRED] [semantically similar]
  graphify-out/memory/query_20260912_060606_5f4afb72_optimistic_stale_write_handling_introduced_in_the.md → docs/architecture/farm-management-persistence.md
- `Inward dependency direction` --semantically_similar_to--> `Domain dependency rule`  [INFERRED] [semantically similar]
  docs/architecture/backend-structure.md → AGENTS.md
- `Cross-context public contracts` --semantically_similar_to--> `Bounded-context ownership`  [INFERRED] [semantically similar]
  docs/architecture/backend-structure.md → AGENTS.md
- `Nodata Preservation` --semantically_similar_to--> `Zero Versus Nodata`  [INFERRED] [semantically similar]
  CropSuiteLite/docs/huaura_environment_correction.md → docs/implementation/poc-preservation.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Bounded-context layered architecture** — docs_architecture_backend_structure_bounded_context_layering, docs_architecture_backend_structure_domain_layer, docs_architecture_backend_structure_application_layer, docs_architecture_backend_structure_infrastructure_layer, docs_architecture_backend_structure_interfaces_layer [EXTRACTED 1.00]
- **Scientific isolation and execution boundary** — agents_icropsuitabilityengine, docs_architecture_cropsuite_integration_cropsuiteadapter, agents_recoverable_background_worker, docs_architecture_overview_recoverable_job_mechanism [EXTRACTED 1.00]
- **Atlas Adaptation Evidence Pipeline** — cropsuitelite_docs_atlas_solutions_supporting_material_manual_source_validation, cropsuitelite_docs_atlas_solutions_atlas_solution_example_response_functions_yaml, cropsuitelite_docs_atlas_solutions_atlas_solution_example_improved_crop_varieties [INFERRED 0.85]
- **Huaura Environmental Bundle Data Flow** — data_huaura_readme_huaura_environmental_bundle, data_huaura_huaura_config_environmental_dataset_directory_map, cropsuitelite_yaml_configurations_crop_suite_datasets_huaura_0041667_huaura_processed_0041667_outputs, cropsuitelite_yaml_configurations_general_config_huaura_huaura_simulation_inputs [INFERRED 0.85]
- **Reproducible Multicrop Execution** — docs_adr_adr_005_background_worker_background_worker, docs_adr_adr_006_scientific_traceability_scientific_traceability, docs_adr_adr_008_sequential_crop_execution_sequential_crop_execution, docs_adr_adr_009_multicrop_evaluation_multicrop_evaluation, docs_architecture_evaluation_flow_target_evaluation_flow [INFERRED 0.85]
- **Adaptation Solution Configuration Framework** — cropsuitelite_yaml_configurations_response_functions_adaptation_response_catalog, cropsuitelite_yaml_configurations_general_config_huaura_solution_framework_integration, cropsuitelite_yaml_configurations_general_config_solutions_solution_framework_integration [INFERRED 0.95]
- **CropSuiteLite Climate Data Pipeline** — cropsuitelite_docs_getting_started_download_cmp6_nex_gddp_cmip6, cropsuitelite_docs_getting_started_from_climatedata_tocrsdatatype_input_data_preprocessing, cropsuitelite_docs_getting_started_from_climatedata_tocrsdatatype_climatological_daily_rasters, cropsuitelite_docs_getting_started_running_cropsuite_cropsuitelite_execution [INFERRED 0.95]
- **Huaura CMIP6 Download Preprocess Simulation Pipeline** — cropsuitelite_yaml_configurations_download_cmip6_huaura_huaura_cmip6_download_configuration, cropsuitelite_yaml_configurations_crop_suite_datasets_huaura_0041667_huaura_high_resolution_preprocessing_configuration, cropsuitelite_yaml_configurations_general_config_huaura_huaura_simulation_configuration [INFERRED 0.95]
- **Scientific Engine Boundary** — docs_adr_adr_004_cropsuite_port_adapter_cropsuite_port_and_adapter, docs_architecture_cropsuite_integration_icropsuitabilityengine, docs_architecture_cropsuite_integration_cropsuiteadapter, docs_implementation_poc_preservation_cropsuitelite_poc_preservation_contract [INFERRED 0.95]
- **Farm Management durable persistence contract** — docs_adr_adr_011_postgresql_postgis_farm_persistence_persistence_technology_stack, docs_adr_adr_011_postgresql_postgis_farm_persistence_farm_management_schema_ownership, docs_adr_adr_011_postgresql_postgis_farm_persistence_postgis_geometry_storage, docs_adr_adr_011_postgresql_postgis_farm_persistence_optimistic_revision_transaction [EXTRACTED 1.00]
- **Farm Management vertical slice flow** — docs_architecture_farm_management_slice_project_and_parcel_http_resources, docs_architecture_farm_management_slice_application_commands_and_queries, docs_architecture_farm_management_slice_project_parcel_and_parcelversion_domain_model, docs_architecture_farm_management_slice_repository_abstractions, docs_architecture_farm_management_slice_in_memory_and_durable_adapters [EXTRACTED 1.00]
- **VIA seven-increment delivery sequence** — docs_implementation_roadmap_modeling_increment, docs_implementation_roadmap_modular_foundation_increment, docs_implementation_roadmap_parcel_and_environmental_coverage_increment, docs_implementation_roadmap_result_querying_increment, docs_implementation_roadmap_on_demand_execution_increment, docs_implementation_roadmap_public_deployment_increment, docs_implementation_roadmap_explanation_and_comparison_increment [EXTRACTED 1.00]

## Communities (134 total, 42 thin omitted)

### Community 0 - "FarmManagementService"
Cohesion: 0.07
Nodes (57): APIRouter, CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject (+49 more)

### Community 1 - "run_cropsuitelite.py"
Cohesion: 0.07
Nodes (27): change_otherst_parameters(), change_st1_parameter(), create_crop_parameters(), create_crop_suite_configuration_file(), find_solution_type(), main(), modify_extent(), modify_general_files() (+19 more)

### Community 2 - "NexGenPreProcessing"
Cohesion: 0.08
Nodes (20): create_climatology_from_nexgen(), main(), mask_single_layer(), resample_soilgrids_data(), BaseProcessor, compute_averaged_temp(), NexGen, NexGenPreProcessing (+12 more)

### Community 3 - "Huaura Dataset Preprocessing Configuration"
Cohesion: 0.05
Nodes (43): Africa Processing Profile, Soil DEM and Land-Sea Layer Plan, Africa Climate Preprocessing Plan, Dataset Preprocessing Configuration, ACCESS-ESM1-5 SSP126 Climate Processing, Huaura 0.041667 Degree Processing Profile, Huaura High-Resolution Preprocessing Configuration, Huaura Processed 0.041667 Outputs (+35 more)

### Community 4 - "check_files.py"
Cohesion: 0.09
Nodes (40): calculate_area(), check_all_inputs(), check_climate_data(), check_soil(), check_within_one(), get_geotiff_datatype(), get_geotiff_extent(), get_geotiff_resolution() (+32 more)

### Community 5 - "DomainValidationError"
Cohesion: 0.11
Nodes (28): DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+20 more)

### Community 6 - "postgresql_repositories.py"
Cohesion: 0.11
Nodes (26): Base, create_database(), Engine, SessionFactory, SQLAlchemy database primitives owned by Farm Management Infrastructure., Declarative base for Farm Management persistence records., Create the engine and short-lived session factory used by repositories., Farm Management infrastructure layer. (+18 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.10
Nodes (22): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+14 more)

### Community 9 - "crop_suitability_main.py"
Cohesion: 0.10
Nodes (31): aggregate_soil_raster_lst(), calcification_map(), calculate_slope(), cropsuitability(), get_soil_data(), get_suitability_val_dict(), get_texture_class(), get_valid_dtype() (+23 more)

### Community 10 - "downscaling.py"
Cohesion: 0.16
Nodes (26): extract_domain_from_global_3draster(), extract_domain_from_global_raster(), get_cpu_ram(), get_resolution_array(), get_shape_of_raster(), load_specified_lines(), Extracts a specific domain from a global raster dataset. Parameters: -…, Extracts a specific domain from a global 3D raster dataset. Parameters: -… (+18 more)

### Community 11 - "DownloadCMIP6Data"
Cohesion: 0.10
Nodes (18): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+10 more)

### Community 12 - "InMemoryParcelRepository"
Cohesion: 0.13
Nodes (12): ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved., Parcel, A named parcel whose geometry changes only by appending versions., ParcelRepository, UUID, Repository abstractions for Farm Management aggregates. (+4 more)

### Community 13 - "climate_suitability_main_xarray.py"
Cohesion: 0.14
Nodes (22): get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params(), get_prec_requirements(), get_suitability_val_dict_xarray(), get_suitable_values(), get_temp_for_sowing_duration() (+14 more)

### Community 14 - "CropSuiteLite"
Cohesion: 0.11
Nodes (13): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Calculates climate suitability based on temperature and precipitation.…, Combines climate suitability with soil/terrain data to calculate final crop…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Interpolates or retrieves downscaled climate data (precipitation and… (+5 more)

### Community 15 - "Settings"
Cohesion: 0.13
Nodes (18): Environment-backed configuration for the VIA application host., Settings needed by the current backend composition root., Settings, Tests for environment-driven application composition settings., test_database_url_selects_postgresql_by_default(), test_postgresql_selection_requires_database_url(), _polygon(), Any (+10 more)

### Community 16 - "climate_suitability_main.py"
Cohesion: 0.14
Nodes (20): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params(), get_prec_requirements() (+12 more)

### Community 17 - "test_environmental_coverage.py"
Cohesion: 0.16
Nodes (16): process_day_climsuit_memopt(), process_day_concfut(), Processes climate suitability data for a specific day and saves the results to…, get_formula(), get_id_list_start(), get_plant_param_interp_forms_dict(), print_crop_param_output(), print_sections() (+8 more)

### Community 18 - "test_farm_management_postgresql.py"
Cohesion: 0.28
Nodes (19): clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel(), _polygon(), _project(), datetime (+11 more)

### Community 19 - "crop_rotation.py"
Cohesion: 0.16
Nodes (17): calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):…, Read a GeoTIFF file with multiple bands into a NumPy array. Parameters: - fn… (+9 more)

### Community 20 - "Project"
Cohesion: 0.18
Nodes (9): Project, An agricultural project that groups parcels., ProjectRepository, PostgreSQLProjectRepository, _project_from_record(), Durable adapter for the Project aggregate., InMemoryProjectRepository, Process-local project storage for the first vertical slice. (+1 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management minimum vertical slice"
Cohesion: 0.15
Nodes (15): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations, Farm Management persistence, PostGIS geometry storage contract (+7 more)

### Community 23 - "CropSuite.py"
Cohesion: 0.24
Nodes (11): # NOTE: self.extent is modified here to align with grid, create_cog_from_geotiff(), geotiff_to_smallest_datatype(), Convert image to COG., merge_outputs_no_overlap(), merge_netcdf_files(), downscaled_files: list of netcdf files overlap: In Degree extent: [North, Left,…, Merge multiple NetCDF files based on latitude and longitude coordinates… (+3 more)

### Community 24 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.14
Nodes (14): Common-Support Ranking, ADR-002 Layered Bounded Contexts, ADR-003 Commands and Queries in Application, ADR-005 Background Worker, ADR-006 Scientific Traceability, ADR-007 Initial Deployment, ADR-008 Sequential Crop Execution, ADR-009 Multicrop Evaluation (+6 more)

### Community 25 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 26 - "climate_suitability_main.py"
Cohesion: 0.17
Nodes (12): process_index(), find_max_sum_new(), jit, Calculates climate suitability for multiple plants based on the CropSuite…, Finds the optimal combination of days to maximize the sum of suitability values…, Reads temperature, precipitation, and failure suitability arrays from GeoTIFF…, climate_suitability_xarray(), compute_suitability() (+4 more)

### Community 27 - "test_architecture.py"
Cohesion: 0.25
Nodes (8): _imported_modules(), Lightweight dependency checks for the modular-monolith foundation., test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_domain_packages_do_not_import_outward_layers(), test_farm_management_does_not_import_other_contexts(), test_postgresql_adapters_satisfy_repository_method_contracts(), Path

### Community 28 - "Farm Management schema ownership"
Cohesion: 0.20
Nodes (10): Farm Management schema ownership, Projects, parcels, and parcel_versions tables, farm_management schema and owned tables, Optional durable repository adapter, Project, Parcel, and ParcelVersion domain model, Result querying increment, Bounded-context ownership and Farm Management repositories, Farm Management ownership query (+2 more)

### Community 29 - "Bounded-context layered structure"
Cohesion: 0.28
Nodes (9): Bounded-context ownership, Anti-corruption layer, Application layer, Bounded-context layered structure, Domain layer, Illustrative Evaluation module structure, Infrastructure layer, Interfaces layer (+1 more)

### Community 30 - "CropSuiteAdapter"
Cohesion: 0.46
Nodes (8): Multicrop Parcel Evaluation, run_evaluation Service, ADR-004 CropSuiteLite Port and Adapter, CropSuiteLite isolation boundary, CropSuiteAdapter, CropSuiteLite Integration Boundary, ICropSuitabilityEngine, On-demand execution increment

### Community 32 - "Farm Management minimum vertical slice"
Cohesion: 0.29
Nodes (5): ADR-011: PostgreSQL/PostGIS persistence for Farm Management, Consequences, Context, Decision, Status

### Community 33 - "Application commands and queries"
Cohesion: 0.29
Nodes (8): Application commands and queries, FastAPI composition root, In-memory and durable Infrastructure adapters, Project and parcel HTTP resources, Farm Management repository abstractions, Transport-to-domain path, ProjectRepository, ParcelRepository, and in-memory adapters, Repository ports and in-memory adapters query

### Community 34 - "Farm Management minimum vertical slice"
Cohesion: 0.25
Nodes (8): Architectural alignment, Slice exclusions and authorization dependency, Explicit exclusions and provisional choices, Farm Management minimum vertical slice, Parcel geometry invariants, HTTP resources, Invariants in this increment, Scope

### Community 35 - "Backend foundation architecture verification query"
Cohesion: 0.29
Nodes (7): Domain dependency rule, Inward dependency direction, Backend architecture consistency evidence, Backend foundation architecture verification query, Bounded-context package foundation, health() endpoint, Domain, Application, and Infrastructure dependency query

### Community 38 - "Python and FastAPI backend decision"
Cohesion: 0.29
Nodes (7): Background worker execution, FastAPI, Layered modular monolith, Python, Python and FastAPI backend decision, Open backend modeling decisions, Modular foundation increment

### Community 39 - "Huaura Environmental Correction"
Cohesion: 0.33
Nodes (7): Architecture source and PoC preservation, Cross-stage architecture gates, Explanation and comparison increment, Modeling increment, Parcel and environmental coverage increment, Public deployment increment, VIA architecture implementation roadmap

### Community 40 - "env.py"
Cohesion: 0.47
Nodes (5): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to tables owned by Farm Management., run_migrations_offline(), run_migrations_online()

### Community 41 - "ParcelGeometry"
Cohesion: 0.40
Nodes (5): _polygon(), parametrize, Unit tests for Farm Management invariants., test_invalid_geometry_is_rejected(), test_revising_geometry_appends_an_immutable_version()

### Community 42 - "Proposed Bounded Contexts"
Cohesion: 0.60
Nodes (6): Agroclimatic Evaluation, Decision Support, Environmental Information, Farm Management, Identity and Access, Proposed Bounded Contexts

### Community 43 - "Post GIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "FarmManagementService"
Cohesion: 0.40
Nodes (4): health(), Host-level health endpoint., Report that the API process is ready to receive requests., get

### Community 45 - "Farm Management minimum vertical slice"
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

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **103 isolated node(s):** `Consequences`, `Context`, `Decision`, `Status`, `Local database and migrations` (+98 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 434 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Crop Code Catalog` and `Undefined Crop Code c32`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `BaseProcessor` connect `NexGenPreProcessing` to `climate_suitability_main.py`, `climate_suitability_main_xarray.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `Parcel` (e.g. with `ParcelResult` and `FarmManagementService`) actually correct?**
  _`Parcel` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `FarmManagementService` (e.g. with `CreateParcel` and `CreateProject`) actually correct?**
  _`FarmManagementService` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `Project` (e.g. with `ProjectResult` and `FarmManagementService`) actually correct?**
  _`Project` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Consequences`, `Context`, `Decision` to the rest of the system?**
  _103 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FarmManagementService` be split into smaller, more focused modules?**
  _Cohesion score 0.0688088283024992 - nodes in this community are weakly interconnected._