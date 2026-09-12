# Graph Report - poc_via_cslite  (2026-09-12)

## Corpus Check
- 157 files · ~81,012 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 903 nodes · 1543 edges · 121 communities (43 shown, 41 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 93 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4a01febd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- crop_suitability_main.py
- climate_suitability_main.py
- check_files.py
- NexGenPreProcessing
- Huaura Dataset Preprocessing Configuration
- run_cropsuitelite.py
- climate_suitability_main_xarray.py
- Crop Membership Functions
- multicrop.py
- DownloadCMIP6Data
- downscaling.py
- FarmManagementService
- Bounded-context layered structure
- Huaura Environmental Correction
- Architecture and Backend for CropSuiteLite Huaura v2
- PrecipitationCoastTest
- CropSuiteAdapter
- Python and FastAPI backend decision
- VIA architecture guardrails
- test_architecture.py
- Proposed Bounded Contexts
- Q: Verify that the new VIA backend foundation is discoverable and consistent with the intended architecture.
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
- data_tools.py
- DomainValidationError
- InMemoryParcelRepository
- farm_management/__init__.py
- CropSuite.py
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
- test_farm_management_api.py
- Documentation Deployment Workflow
- Suitability and Limiting-Factor Outputs
- Nodata Coverage Conservation
- Membership Functions Diagram
- Modified Membership Functions Diagram
- CropSuiteLite Conda Environment
- Logical and deployment boundary separation
- via-backend
- CropSuiteLite
- Backend foundation architecture verification query
- Farm Management minimum vertical slice
- Huaura Precipitation Unit Contract
- read_crop_parameterizations_files
- models.py
- Project
- EnvironmentalCoverageTest
- Parcel
- process_day_climsuit_memopt
- interpolate_precipitation
- PrecipitationUnitsTest
- test_farm_management_domain.py
- find_max_sum_new
- _validate_name

## God Nodes (most connected - your core abstractions)
1. `FarmManagementService` - 34 edges
2. `Parcel` - 29 edges
3. `Project` - 21 edges
4. `create_router()` - 21 edges
5. `climsuit_new()` - 20 edges
6. `DomainValidationError` - 20 edges
7. `CropSensitivity` - 19 edges
8. `process_day_climsuit_xarray()` - 19 edges
9. `CropSuiteLite` - 16 edges
10. `NexGenPreProcessing` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Inward dependency direction` --semantically_similar_to--> `Domain dependency rule`  [INFERRED] [semantically similar]
  docs/architecture/backend-structure.md → AGENTS.md
- `Cross-context public contracts` --semantically_similar_to--> `Bounded-context ownership`  [INFERRED] [semantically similar]
  docs/architecture/backend-structure.md → AGENTS.md
- `Nodata Preservation` --semantically_similar_to--> `Zero Versus Nodata`  [INFERRED] [semantically similar]
  CropSuiteLite/docs/huaura_environment_correction.md → docs/implementation/poc-preservation.md
- `ADR-002 Layered Bounded Contexts` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-002-layered-bounded-contexts.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md
- `ADR-005 Background Worker` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-005-background-worker.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Bounded-context layered architecture** — docs_architecture_backend_structure_bounded_context_layering, docs_architecture_backend_structure_domain_layer, docs_architecture_backend_structure_application_layer, docs_architecture_backend_structure_infrastructure_layer, docs_architecture_backend_structure_interfaces_layer [EXTRACTED 1.00]
- **Scientific isolation and execution boundary** — agents_icropsuitabilityengine, docs_architecture_cropsuite_integration_cropsuiteadapter, agents_recoverable_background_worker, docs_adr_adr_010_python_fastapi_backend_scientific_isolation, docs_adr_adr_010_python_fastapi_backend_background_execution, docs_architecture_overview_recoverable_job_mechanism [EXTRACTED 1.00]
- **Atlas Adaptation Evidence Pipeline** — cropsuitelite_docs_atlas_solutions_supporting_material_manual_source_validation, cropsuitelite_docs_atlas_solutions_atlas_solution_example_response_functions_yaml, cropsuitelite_docs_atlas_solutions_atlas_solution_example_improved_crop_varieties [INFERRED 0.85]
- **Huaura Environmental Bundle Data Flow** — data_huaura_readme_huaura_environmental_bundle, data_huaura_huaura_config_environmental_dataset_directory_map, cropsuitelite_yaml_configurations_crop_suite_datasets_huaura_0041667_huaura_processed_0041667_outputs, cropsuitelite_yaml_configurations_general_config_huaura_huaura_simulation_inputs [INFERRED 0.85]
- **Reproducible Multicrop Execution** — docs_adr_adr_005_background_worker_background_worker, docs_adr_adr_006_scientific_traceability_scientific_traceability, docs_adr_adr_008_sequential_crop_execution_sequential_crop_execution, docs_adr_adr_009_multicrop_evaluation_multicrop_evaluation, docs_architecture_evaluation_flow_target_evaluation_flow [INFERRED 0.85]
- **Adaptation Solution Configuration Framework** — cropsuitelite_yaml_configurations_response_functions_adaptation_response_catalog, cropsuitelite_yaml_configurations_general_config_huaura_solution_framework_integration, cropsuitelite_yaml_configurations_general_config_solutions_solution_framework_integration [INFERRED 0.95]
- **CropSuiteLite Climate Data Pipeline** — cropsuitelite_docs_getting_started_download_cmp6_nex_gddp_cmip6, cropsuitelite_docs_getting_started_from_climatedata_tocrsdatatype_input_data_preprocessing, cropsuitelite_docs_getting_started_from_climatedata_tocrsdatatype_climatological_daily_rasters, cropsuitelite_docs_getting_started_running_cropsuite_cropsuitelite_execution [INFERRED 0.95]
- **Huaura CMIP6 Download Preprocess Simulation Pipeline** — cropsuitelite_yaml_configurations_download_cmip6_huaura_huaura_cmip6_download_configuration, cropsuitelite_yaml_configurations_crop_suite_datasets_huaura_0041667_huaura_high_resolution_preprocessing_configuration, cropsuitelite_yaml_configurations_general_config_huaura_huaura_simulation_configuration [INFERRED 0.95]
- **Scientific Engine Boundary** — docs_adr_adr_004_cropsuite_port_adapter_cropsuite_port_and_adapter, docs_architecture_cropsuite_integration_icropsuitabilityengine, docs_architecture_cropsuite_integration_cropsuiteadapter, docs_implementation_poc_preservation_cropsuitelite_poc_preservation_contract [INFERRED 0.95]

## Communities (121 total, 41 thin omitted)

### Community 0 - "crop_suitability_main.py"
Cohesion: 0.12
Nodes (25): get_id_list_start(), Get a list of keys from a dictionary that start with a specified prefix.…, aggregate_soil_raster_lst(), calcification_map(), cropsuitability(), get_soil_data(), get_suitability_val_dict(), get_texture_class() (+17 more)

### Community 1 - "climate_suitability_main.py"
Cohesion: 0.18
Nodes (16): climate_suitability(), climsuit_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params(), get_prec_requirements(), get_temp_for_sowing_duration(), lethal_params_threshold() (+8 more)

### Community 2 - "check_files.py"
Cohesion: 0.09
Nodes (38): calculate_area(), check_all_inputs(), check_climate_data(), check_soil(), check_within_one(), get_geotiff_datatype(), get_geotiff_extent(), get_geotiff_resolution() (+30 more)

### Community 3 - "NexGenPreProcessing"
Cohesion: 0.07
Nodes (23): create_climatology_from_nexgen(), main(), mask_single_layer(), resample_soilgrids_data(), BaseProcessor, compute_averaged_temp(), NexGen, NexGenPreProcessing (+15 more)

### Community 4 - "Huaura Dataset Preprocessing Configuration"
Cohesion: 0.05
Nodes (43): Africa Processing Profile, Soil DEM and Land-Sea Layer Plan, Africa Climate Preprocessing Plan, Dataset Preprocessing Configuration, ACCESS-ESM1-5 SSP126 Climate Processing, Huaura 0.041667 Degree Processing Profile, Huaura High-Resolution Preprocessing Configuration, Huaura Processed 0.041667 Outputs (+35 more)

### Community 5 - "run_cropsuitelite.py"
Cohesion: 0.06
Nodes (33): change_otherst_parameters(), change_st1_parameter(), create_crop_parameters(), create_crop_suite_configuration_file(), find_solution_type(), main(), modify_extent(), modify_general_files() (+25 more)

### Community 6 - "climate_suitability_main_xarray.py"
Cohesion: 0.10
Nodes (31): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+23 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.10
Nodes (22): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+14 more)

### Community 9 - "DownloadCMIP6Data"
Cohesion: 0.10
Nodes (18): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+10 more)

### Community 10 - "downscaling.py"
Cohesion: 0.15
Nodes (23): calculate_slope(), extract_domain_from_global_raster(), get_cpu_ram(), load_specified_lines(), Extracts a specific domain from a global raster dataset. Parameters: -…, Get information about the CPU and available RAM. Returns: list: A list…, interpolate_precipitation_method(), interpolate_temperature_method() (+15 more)

### Community 11 - "FarmManagementService"
Cohesion: 0.07
Nodes (58): APIRouter, CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject (+50 more)

### Community 12 - "Bounded-context layered structure"
Cohesion: 0.28
Nodes (9): Bounded-context ownership, Anti-corruption layer, Application layer, Bounded-context layered structure, Domain layer, Illustrative Evaluation module structure, Infrastructure layer, Interfaces layer (+1 more)

### Community 13 - "Huaura Environmental Correction"
Cohesion: 0.29
Nodes (8): Huaura Environmental Correction, Nodata Preservation, CropSuiteLite PoC Preservation Contract, Zero Versus Nodata, Seven-Increment Delivery Sequence, VIA Architecture Implementation Roadmap, 79-Entry Crop Catalog, Huaura Multicrop PoC

### Community 14 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.18
Nodes (11): Common-Support Ranking, ADR-003 Commands and Queries in Application, ADR-006 Scientific Traceability, ADR-007 Initial Deployment, ADR-009 Multicrop Evaluation, Immutable ParcelSnapshot, Target Evaluation Flow, Architecture and Backend for CropSuiteLite Huaura v2 (+3 more)

### Community 16 - "CropSuiteAdapter"
Cohesion: 0.36
Nodes (9): ICropSuitabilityEngine application port, Multicrop Parcel Evaluation, run_evaluation Service, ADR-004 CropSuiteLite Port and Adapter, ADR-008 Sequential Crop Execution, CropSuiteLite scientific isolation, CropSuiteAdapter, CropSuiteLite Integration Boundary (+1 more)

### Community 17 - "Python and FastAPI backend decision"
Cohesion: 0.16
Nodes (14): Recoverable background worker flow, ADR-001 Modular Monolith, ADR-002 Layered Bounded Contexts, ADR-005 Background Worker, ADR-004 CropSuite Port and Adapter, Background scientific execution, FastAPI interface boundary, Layered modular monolith (+6 more)

### Community 18 - "VIA architecture guardrails"
Cohesion: 0.25
Nodes (8): VIA architecture guardrails, Nodata semantics, ParcelSnapshot, Scientific rule preservation, Current CropSuiteLite scientific PoC, Original architecture design authority, Reproducible scientific evidence, VIA backend purpose

### Community 19 - "test_architecture.py"
Cohesion: 0.31
Nodes (6): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_domain_packages_do_not_import_outward_layers()

### Community 20 - "Proposed Bounded Contexts"
Cohesion: 0.60
Nodes (6): Agroclimatic Evaluation, Decision Support, Environmental Information, Farm Management, Identity and Access, Proposed Bounded Contexts

### Community 21 - "Q: Verify that the new VIA backend foundation is discoverable and consistent with the intended architecture."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Verify that the new VIA backend foundation is discoverable and consistent with the intended architecture., Source Nodes

### Community 23 - "CropSuiteLite Python Dependency Manifest"
Cohesion: 0.50
Nodes (4): CropSuiteLite Python Dependency Manifest, Geospatial Processing Stack, Runtime and Utility Stack, Scientific Computing Stack

### Community 24 - "download_soilgrids_huaura.py"
Cohesion: 0.83
Nodes (3): crop_reproject(), get_vrt(), main()

### Community 25 - "Knowledge Graph Pipeline"
Cohesion: 0.67
Nodes (3): Graphify, Honest Audit Trail, Knowledge Graph Pipeline

### Community 27 - "Atlas A Logo"
Cohesion: 0.67
Nodes (3): Atlas A Logo, Atlas Branding, Stylized Green Letter A

### Community 46 - "data_tools.py"
Cohesion: 0.16
Nodes (19): calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, extract_domain_from_global_3draster(), get_geotiff_extent(), get_shape_of_raster(), ndarray (+11 more)

### Community 47 - "DomainValidationError"
Cohesion: 0.23
Nodes (16): DomainValidationError, ValueError, Raised when a Farm Management value violates a domain invariant., _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any (+8 more)

### Community 48 - "InMemoryParcelRepository"
Cohesion: 0.15
Nodes (9): ParcelVersionConflictError, RuntimeError, Domain errors raised by Farm Management invariants., Raised when persisted parcel history changed before a revision was saved., Farm Management infrastructure layer., InMemoryParcelRepository, UUID, In-memory Farm Management repository adapters. (+1 more)

### Community 50 - "CropSuite.py"
Cohesion: 0.24
Nodes (11): # NOTE: self.extent is modified here to align with grid, create_cog_from_geotiff(), geotiff_to_smallest_datatype(), Convert image to COG., merge_outputs_no_overlap(), merge_netcdf_files(), downscaled_files: list of netcdf files overlap: In Degree extent: [North, Left,…, Merge multiple NetCDF files based on latitude and longitude coordinates… (+3 more)

### Community 65 - "test_farm_management_api.py"
Cohesion: 0.25
Nodes (10): _polygon(), Any, End-to-end API tests for the Farm Management vertical slice., _request(), test_invalid_parcel_geometry_returns_validation_error(), scenario(), test_parcel_requires_an_existing_project(), test_project_and_versioned_parcel_lifecycle() (+2 more)

### Community 106 - "CropSuiteLite"
Cohesion: 0.13
Nodes (12): CropSuiteLite, Calculates climate suitability based on temperature and precipitation.…, Combines climate suitability with soil/terrain data to calculate final crop…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Calculates grid tiling based on available RAM to prevent memory overflow.…, Private subprocess entry point; each invocation has its own working directory. (+4 more)

### Community 107 - "Backend foundation architecture verification query"
Cohesion: 0.25
Nodes (8): Domain dependency rule, FastAPI application composition root., Initial backend foundation status, Inward dependency direction, Backend architecture consistency evidence, Backend foundation architecture verification query, Bounded-context package foundation, health() endpoint

### Community 108 - "Farm Management minimum vertical slice"
Cohesion: 0.29
Nodes (6): Architectural alignment, Explicit exclusions and provisional choices, Farm Management minimum vertical slice, HTTP resources, Invariants in this increment, Scope

### Community 109 - "Huaura Precipitation Unit Contract"
Cohesion: 0.33
Nodes (6): Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding

### Community 110 - "read_crop_parameterizations_files"
Cohesion: 0.18
Nodes (12): Loads crop parameterization files and interpolation formulas., get_formula(), get_id_list_start(), get_plant_param_interp_forms_dict(), print_crop_param_output(), print_sections(), Reads and parses crop parameterization files from a specified folder path.…, Prints the keys of a given dictionary as a list of sections or items. Args:… (+4 more)

### Community 111 - "models.py"
Cohesion: 0.19
Nodes (10): ParcelGeometry, An immutable, minimally validated Polygon or MultiPolygon geometry., Farm Management domain layer., ParcelVersion, datetime, Farm Management domain model., An immutable version of a parcel geometry., _geometry() (+2 more)

### Community 112 - "Project"
Cohesion: 0.22
Nodes (7): Project, An agricultural project that groups parcels., ProjectRepository, UUID, Repository abstractions for Farm Management aggregates., InMemoryProjectRepository, Process-local project storage for the first vertical slice.

### Community 113 - "EnvironmentalCoverageTest"
Cohesion: 0.21
Nodes (3): climate_coverage(), Require complete daily coverage; missing observations are not unsuitable days., EnvironmentalCoverageTest

### Community 114 - "Parcel"
Cohesion: 0.25
Nodes (6): ParcelVersionResult, Transport-neutral results returned by Farm Management use cases., Parcel, A named parcel whose geometry changes only by appending versions., ParcelRepository, Protocol

### Community 115 - "process_day_climsuit_memopt"
Cohesion: 0.25
Nodes (9): calculate_average_sunshine(), calculate_day_length(), get_suitability_val_dict(), process_day_climsuit_memopt(), process_day_concfut(), Calculates the suitability value based on a specified formula for a given plant…, Calculate the daylight duration in hours for a given latitude and day of the…, Calculate the average sunshine duration over a given range of days for each… (+1 more)

### Community 116 - "interpolate_precipitation"
Cohesion: 0.33
Nodes (6): Interpolates or retrieves downscaled climate data (precipitation and…, _create_interpolation_folders(), interpolate_precipitation(), interpolate_temperature(), domain: [y_max, x_min, y_min, x_max], domain: [y_max, x_min, y_min, x_max]

### Community 118 - "test_farm_management_domain.py"
Cohesion: 0.40
Nodes (5): _polygon(), Unit tests for Farm Management invariants., test_invalid_geometry_is_rejected(), test_revising_geometry_appends_an_immutable_version(), parametrize

### Community 119 - "find_max_sum_new"
Cohesion: 0.50
Nodes (4): process_index(), find_max_sum_new(), jit, Finds the optimal combination of days to maximize the sum of suitability values…

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **62 isolated node(s):** `via-backend`, `Scope`, `HTTP resources`, `Invariants in this increment`, `Explicit exclusions and provisional choices` (+57 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 375 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **41 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Crop Code Catalog` and `Undefined Crop Code c32`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `FastAPI application composition root.` connect `Backend foundation architecture verification query` to `FarmManagementService`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `Backend architecture consistency evidence` connect `Backend foundation architecture verification query` to `CropSuiteAdapter`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `FarmManagementService` (e.g. with `CreateParcel` and `CreateProject`) actually correct?**
  _`FarmManagementService` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Parcel` (e.g. with `ParcelResult` and `FarmManagementService`) actually correct?**
  _`Parcel` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `Project` (e.g. with `ProjectResult` and `FarmManagementService`) actually correct?**
  _`Project` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `via-backend`, `Scope`, `HTTP resources` to the rest of the system?**
  _62 weakly-connected nodes found - possible documentation gaps or missing edges._