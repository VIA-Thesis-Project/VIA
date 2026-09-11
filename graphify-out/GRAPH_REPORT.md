# Graph Report - poc_via_cslite  (2026-09-11)

## Corpus Check
- 54 files · ~77,010 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 603 nodes · 1006 edges · 64 communities (19 shown, 10 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 66 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Crop Suitability Engine
- CropSuite Execution Controller
- Dataset Preprocessing
- Environmental Coverage Tests
- Huaura Data Configuration
- Input Validation
- VIA Architecture and Multicrop
- Multicrop Evaluation
- CropSuite Documentation
- Climate Suitability NumPy
- Climate Suitability Xarray
- Climate Data Downloads
- Membership and Solutions
- Precipitation Coast Tests
- Precipitation Unit Contract
- Python Dependencies
- SoilGrid Downloads
- Graphify Tooling
- Atlas Branding
- Remote Raster Cropping
- Layered Backend Structure
- Bounded Context Sources
- Initial Deployment Stack
- Documentation Deployment
- Suitability Outputs
- Nodata Conservation
- Membership Diagram
- Modified Membership Diagram
- Python Environment

## God Nodes (most connected - your core abstractions)
1. `climsuit_new()` - 20 edges
2. `CropSensitivity` - 19 edges
3. `process_day_climsuit_xarray()` - 19 edges
4. `CropSuiteLite` - 16 edges
5. `NexGenPreProcessing` - 15 edges
6. `load_specified_lines()` - 15 edges
7. `run_evaluation()` - 15 edges
8. `cropsuitability()` - 14 edges
9. `check_all_inputs()` - 13 edges
10. `Architecture and Backend for CropSuiteLite Huaura v2` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Nodata Preservation` --semantically_similar_to--> `Zero Versus Nodata`  [INFERRED] [semantically similar]
  CropSuiteLite/docs/huaura_environment_correction.md → docs/implementation/poc-preservation.md
- `ADR-001 Modular Monolith` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-001-modular-monolith.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md
- `ADR-002 Layered Bounded Contexts` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-002-layered-bounded-contexts.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md
- `ADR-003 Commands and Queries in Application` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-003-commands-queries-in-application.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md
- `ADR-005 Background Worker` --references--> `Architecture and Backend for CropSuiteLite Huaura v2`  [INFERRED]
  docs/adr/ADR-005-background-worker.md → graphify-out/converted/Arquitectura_y_backend_CropSuiteLite_Huaura_v2_0e904345.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Layered Modular Architecture Alignment** — docs_adr_adr_001_modular_monolith_modular_monolith, docs_adr_adr_002_layered_bounded_contexts_layered_bounded_contexts, docs_architecture_backend_structure_intended_backend_structure, docs_architecture_overview_target_logical_architecture [INFERRED 0.85]
- **Scientific Engine Boundary** — docs_adr_adr_004_cropsuite_port_adapter_cropsuite_port_and_adapter, docs_architecture_cropsuite_integration_icropsuitabilityengine, docs_architecture_cropsuite_integration_cropsuiteadapter, docs_implementation_poc_preservation_cropsuitelite_poc_preservation_contract [INFERRED 0.95]
- **Reproducible Multicrop Execution** — docs_adr_adr_005_background_worker_background_worker, docs_adr_adr_006_scientific_traceability_scientific_traceability, docs_adr_adr_008_sequential_crop_execution_sequential_crop_execution, docs_adr_adr_009_multicrop_evaluation_multicrop_evaluation, docs_architecture_evaluation_flow_target_evaluation_flow [INFERRED 0.85]
- **CropSuiteLite Climate Data Pipeline** — cropsuitelite_docs_getting_started_download_cmp6_nex_gddp_cmip6, cropsuitelite_docs_getting_started_from_climatedata_tocrsdatatype_input_data_preprocessing, cropsuitelite_docs_getting_started_from_climatedata_tocrsdatatype_climatological_daily_rasters, cropsuitelite_docs_getting_started_running_cropsuite_cropsuitelite_execution [INFERRED 0.95]
- **Atlas Adaptation Evidence Pipeline** — cropsuitelite_docs_atlas_solutions_supporting_material_manual_source_validation, cropsuitelite_docs_atlas_solutions_atlas_solution_example_response_functions_yaml, cropsuitelite_docs_atlas_solutions_atlas_solution_example_improved_crop_varieties [INFERRED 0.85]
- **Huaura CMIP6 Download Preprocess Simulation Pipeline** — cropsuitelite_yaml_configurations_download_cmip6_huaura_huaura_cmip6_download_configuration, cropsuitelite_yaml_configurations_crop_suite_datasets_huaura_0041667_huaura_high_resolution_preprocessing_configuration, cropsuitelite_yaml_configurations_general_config_huaura_huaura_simulation_configuration [INFERRED 0.95]
- **Huaura Environmental Bundle Data Flow** — data_huaura_readme_huaura_environmental_bundle, data_huaura_huaura_config_environmental_dataset_directory_map, cropsuitelite_yaml_configurations_crop_suite_datasets_huaura_0041667_huaura_processed_0041667_outputs, cropsuitelite_yaml_configurations_general_config_huaura_huaura_simulation_inputs [INFERRED 0.85]
- **Adaptation Solution Configuration Framework** — cropsuitelite_yaml_configurations_response_functions_adaptation_response_catalog, cropsuitelite_yaml_configurations_general_config_huaura_solution_framework_integration, cropsuitelite_yaml_configurations_general_config_solutions_solution_framework_integration [INFERRED 0.95]

## Communities (64 total, 10 thin omitted)

### Community 0 - "Crop Suitability Engine"
Cohesion: 0.06
Nodes (60): # NOTE: self.extent is modified here to align with grid, Calculates climate suitability based on temperature and precipitation.…, Combines climate suitability with soil/terrain data to calculate final crop…, Interpolates or retrieves downscaled climate data (precipitation and…, aggregate_soil_raster_lst(), calcification_map(), cropsuitability(), get_soil_data() (+52 more)

### Community 1 - "CropSuite Execution Controller"
Cohesion: 0.06
Nodes (42): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Calculates grid tiling based on available RAM to prevent memory overflow.…, change_otherst_parameters(), change_st1_parameter() (+34 more)

### Community 2 - "Dataset Preprocessing"
Cohesion: 0.08
Nodes (20): create_climatology_from_nexgen(), main(), mask_single_layer(), resample_soilgrids_data(), BaseProcessor, compute_averaged_temp(), NexGen, NexGenPreProcessing (+12 more)

### Community 3 - "Environmental Coverage Tests"
Cohesion: 0.08
Nodes (25): process_day_climsuit_memopt(), process_day_concfut(), Processes climate suitability data for a specific day and saves the results to…, calculate_slope(), process_tempday_interp(), get_formula(), get_id_list_start(), get_plant_param_interp_forms_dict() (+17 more)

### Community 4 - "Huaura Data Configuration"
Cohesion: 0.05
Nodes (43): Africa Processing Profile, Soil DEM and Land-Sea Layer Plan, Africa Climate Preprocessing Plan, Dataset Preprocessing Configuration, ACCESS-ESM1-5 SSP126 Climate Processing, Huaura 0.041667 Degree Processing Profile, Huaura High-Resolution Preprocessing Configuration, Huaura Processed 0.041667 Outputs (+35 more)

### Community 5 - "Input Validation"
Cohesion: 0.09
Nodes (38): calculate_area(), check_all_inputs(), check_climate_data(), check_soil(), check_within_one(), get_geotiff_datatype(), get_geotiff_extent(), get_geotiff_resolution() (+30 more)

### Community 6 - "VIA Architecture and Multicrop"
Cohesion: 0.08
Nodes (38): VIA Architecture Guardrails, Huaura Environmental Correction, Nodata Preservation, Common-Support Ranking, Multicrop Parcel Evaluation, run_evaluation Service, ADR-001 Modular Monolith, ADR-002 Layered Bounded Contexts (+30 more)

### Community 7 - "Multicrop Evaluation"
Cohesion: 0.12
Nodes (24): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+16 more)

### Community 8 - "CropSuite Documentation"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 9 - "Climate Suitability NumPy"
Cohesion: 0.10
Nodes (29): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+21 more)

### Community 10 - "Climate Suitability Xarray"
Cohesion: 0.11
Nodes (28): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+20 more)

### Community 11 - "Climate Data Downloads"
Cohesion: 0.10
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations., Initialize the downloader. Parameters ---------- url_root : str Base URL… (+9 more)

### Community 12 - "Membership and Solutions"
Cohesion: 0.11
Nodes (12): change_otherst_parameters(), change_st1_parameter(), create_crop_parameters(), CropSensitivity, ndarray, A class to read, handle, and write crop sensitivity parameters from .inf files., Initializes the CropSensitivity class. Args: crop (str): The name of the crop…, Reads the crop configuration .inf file and parses the parameters. The method… (+4 more)

### Community 13 - "Precipitation Coast Tests"
Cohesion: 0.26
Nodes (4): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall.

### Community 14 - "Precipitation Unit Contract"
Cohesion: 0.33
Nodes (6): Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding

### Community 15 - "Python Dependencies"
Cohesion: 0.50
Nodes (4): CropSuiteLite Python Dependency Manifest, Geospatial Processing Stack, Runtime and Utility Stack, Scientific Computing Stack

### Community 16 - "SoilGrid Downloads"
Cohesion: 0.83
Nodes (3): crop_reproject(), get_vrt(), main()

### Community 17 - "Graphify Tooling"
Cohesion: 0.67
Nodes (3): Graphify, Honest Audit Trail, Knowledge Graph Pipeline

### Community 18 - "Atlas Branding"
Cohesion: 0.67
Nodes (3): Atlas A Logo, Atlas Branding, Stylized Green Letter A

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **45 isolated node(s):** `Membership Functions Diagram`, `Modified Membership Functions Diagram`, `79-Entry Crop Catalog`, `Intended Backend Structure`, `Domain Application Infrastructure Interfaces` (+40 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 224 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Crop Code Catalog` and `Undefined Crop Code c32`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `main()` connect `CropSuite Execution Controller` to `Multicrop Evaluation`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `CropSuiteLite` connect `CropSuite Execution Controller` to `Crop Suitability Engine`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `BaseProcessor` connect `Dataset Preprocessing` to `Climate Suitability Xarray`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `CropSensitivity` (e.g. with `change_otherst_parameters()` and `change_st1_parameter()`) actually correct?**
  _`CropSensitivity` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Path` (e.g. with `main()` and `main()`) actually correct?**
  _`Path` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Membership Functions Diagram`, `Modified Membership Functions Diagram`, `79-Entry Crop Catalog` to the rest of the system?**
  _45 weakly-connected nodes found - possible documentation gaps or missing edges._