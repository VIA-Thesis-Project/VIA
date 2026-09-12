# Graph Report - poc_via_cslite  (2026-09-11)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 726 nodes · 1092 edges · 106 communities (26 shown, 43 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d55b7221`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CropSuite.py
- climate_suitability_main.py
- check_files.py
- NexGenPreProcessing
- Huaura Dataset Preprocessing Configuration
- run_cropsuitelite.py
- climate_suitability_main_xarray.py
- Crop Membership Functions
- multicrop.py
- DownloadCMIP6Data
- CropSensitivity
- health.py
- VIA architecture guardrails
- Huaura Environmental Correction
- Architecture and Backend for CropSuiteLite Huaura v2
- process_precday_interp
- CropSuiteAdapter
- Python and FastAPI backend decision
- Target logical architecture
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
- farm_management/application/__init__.py
- farm_management/domain/__init__.py
- farm_management/infrastructure/__init__.py
- farm_management/__init__.py
- farm_management/interfaces/__init__.py
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
- Path
- Documentation Deployment Workflow
- Suitability and Limiting-Factor Outputs
- Nodata Coverage Conservation
- Membership Functions Diagram
- Modified Membership Functions Diagram
- CropSuiteLite Conda Environment
- Logical and deployment boundary separation
- via-backend

## God Nodes (most connected - your core abstractions)
1. `climsuit_new()` - 20 edges
2. `CropSensitivity` - 19 edges
3. `process_day_climsuit_xarray()` - 19 edges
4. `CropSuiteLite` - 16 edges
5. `NexGenPreProcessing` - 15 edges
6. `load_specified_lines()` - 15 edges
7. `cropsuitability()` - 14 edges
8. `run_evaluation()` - 14 edges
9. `check_all_inputs()` - 13 edges
10. `Architecture and Backend for CropSuiteLite Huaura v2` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Nodata Preservation` --semantically_similar_to--> `Zero Versus Nodata`  [INFERRED] [semantically similar]
  CropSuiteLite/docs/huaura_environment_correction.md → docs/implementation/poc-preservation.md
- `ADR-002 Layered Bounded Contexts` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-002-layered-bounded-contexts.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md
- `ADR-005 Background Worker` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-005-background-worker.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md
- `ADR-006 Scientific Traceability` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-006-scientific-traceability.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md
- `Inward dependency direction` --semantically_similar_to--> `Domain dependency rule`  [INFERRED] [semantically similar]
  docs/architecture/backend-structure.md → AGENTS.md

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

## Communities (106 total, 43 thin omitted)

### Community 0 - "CropSuite.py"
Cohesion: 0.06
Nodes (72): # NOTE: self.extent is modified here to align with grid, Calculates climate suitability based on temperature and precipitation.…, Combines climate suitability with soil/terrain data to calculate final crop…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Interpolates or retrieves downscaled climate data (precipitation and…, calculate_suitabilities(), compute_combinations(), crop_rotation() (+64 more)

### Community 1 - "climate_suitability_main.py"
Cohesion: 0.06
Nodes (41): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+33 more)

### Community 2 - "check_files.py"
Cohesion: 0.07
Nodes (50): calculate_area(), check_all_inputs(), check_climate_data(), check_soil(), check_within_one(), get_geotiff_datatype(), get_geotiff_extent(), get_geotiff_resolution() (+42 more)

### Community 3 - "NexGenPreProcessing"
Cohesion: 0.08
Nodes (20): create_climatology_from_nexgen(), main(), mask_single_layer(), resample_soilgrids_data(), BaseProcessor, compute_averaged_temp(), NexGen, NexGenPreProcessing (+12 more)

### Community 4 - "Huaura Dataset Preprocessing Configuration"
Cohesion: 0.05
Nodes (43): Africa Processing Profile, Soil DEM and Land-Sea Layer Plan, Africa Climate Preprocessing Plan, Dataset Preprocessing Configuration, ACCESS-ESM1-5 SSP126 Climate Processing, Huaura 0.041667 Degree Processing Profile, Huaura High-Resolution Preprocessing Configuration, Huaura Processed 0.041667 Outputs (+35 more)

### Community 5 - "run_cropsuitelite.py"
Cohesion: 0.08
Nodes (28): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Merges tiled outputs into a single raster for the entire region. Parameters…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Calculates grid tiling based on available RAM to prevent memory overflow.…, change_otherst_parameters(), change_st1_parameter(), create_crop_parameters() (+20 more)

### Community 6 - "climate_suitability_main_xarray.py"
Cohesion: 0.10
Nodes (31): Calculates climate suitability for multiple plants based on the CropSuite…, Finds the optimal combination of days to maximize the sum of suitability values…, Reads temperature, precipitation, and failure suitability arrays from GeoTIFF…, climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start() (+23 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.10
Nodes (22): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+14 more)

### Community 9 - "DownloadCMIP6Data"
Cohesion: 0.10
Nodes (18): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+10 more)

### Community 10 - "CropSensitivity"
Cohesion: 0.11
Nodes (12): change_otherst_parameters(), change_st1_parameter(), create_crop_parameters(), CropSensitivity, ndarray, A class to read, handle, and write crop sensitivity parameters from .inf files., Initializes the CropSensitivity class. Args: crop (str): The name of the crop…, Reads the crop configuration .inf file and parses the parameters. The method… (+4 more)

### Community 11 - "health.py"
Cohesion: 0.13
Nodes (15): Domain dependency rule, health(), Host-level health endpoint., Report that the API process is ready to receive requests., create_app(), FastAPI application composition root., Build the VIA API and register its technical interfaces., Initial backend foundation status (+7 more)

### Community 12 - "VIA architecture guardrails"
Cohesion: 0.21
Nodes (12): VIA architecture guardrails, Bounded-context ownership, Scientific rule preservation, Anti-corruption layer, Application layer, Bounded-context layered structure, Domain layer, Illustrative Evaluation module structure (+4 more)

### Community 13 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 14 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.20
Nodes (12): Common-Support Ranking, Multicrop Parcel Evaluation, ADR-003 Commands and Queries in Application, ADR-007 Initial Deployment, ADR-008 Sequential Crop Execution, ADR-009 Multicrop Evaluation, Architecture and Backend for CropSuiteLite Huaura v2, Celery (+4 more)

### Community 15 - "process_precday_interp"
Cohesion: 0.26
Nodes (4): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall.

### Community 16 - "CropSuiteAdapter"
Cohesion: 0.29
Nodes (10): ICropSuitabilityEngine application port, run_evaluation Service, ADR-004 CropSuiteLite Port and Adapter, ADR-006 Scientific Traceability, CropSuiteLite scientific isolation, CropSuiteAdapter, CropSuiteLite Integration Boundary, ICropSuitabilityEngine (+2 more)

### Community 17 - "Python and FastAPI backend decision"
Cohesion: 0.20
Nodes (10): Recoverable background worker flow, ADR-002 Layered Bounded Contexts, ADR-005 Background Worker, ADR-004 CropSuite Port and Adapter, Background scientific execution, FastAPI interface boundary, Layered modular monolith, Python and FastAPI backend decision (+2 more)

### Community 18 - "Target logical architecture"
Cohesion: 0.22
Nodes (9): Nodata semantics, ParcelSnapshot, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC, Architecture decision classification, Proposed VIA bounded contexts, Reproducible scientific evidence, Target logical architecture (+1 more)

### Community 19 - "test_architecture.py"
Cohesion: 0.33
Nodes (4): _imported_modules(), Lightweight dependency checks for the modular-monolith foundation., test_domain_packages_do_not_import_outward_layers(), Path

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

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **57 isolated node(s):** `Answer`, `Outcome`, `Source Nodes`, `via-backend`, `Huaura Precipitation Validation` (+52 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 316 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Crop Code Catalog` and `Undefined Crop Code c32`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `BaseProcessor` connect `NexGenPreProcessing` to `climate_suitability_main_xarray.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `CropSensitivity` connect `CropSensitivity` to `run_cropsuitelite.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `CropSensitivity` (e.g. with `change_otherst_parameters()` and `change_st1_parameter()`) actually correct?**
  _`CropSensitivity` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Answer`, `Outcome`, `Source Nodes` to the rest of the system?**
  _57 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CropSuite.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05510388437217705 - nodes in this community are weakly interconnected._
- **Should `climate_suitability_main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05792349726775956 - nodes in this community are weakly interconnected._