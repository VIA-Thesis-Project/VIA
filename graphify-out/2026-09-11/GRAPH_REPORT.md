# Graph Report - poc_via_cslite  (2026-09-11)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 463 nodes · 855 edges · 49 communities (11 shown, 3 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 27 edges (avg confidence: 0.86)
- Token cost: 1,333 input · 552 output

## Graph Freshness
- Built from commit: `d2f12123`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Crop Climate Suitability
- Climate Suitability Parameters
- CropSuitLite Model Controller
- NextGen Data Preprocessing
- Input Data Validation
- Crop Evaluation and Metrics
- Xarray Climate Suitability
- Data Downloading Tools
- Crop Rotation and Raster IO
- Precipitation Resampling Tests
- Soilgrids Download and Reprojection
- Remote Data Chunk Handling
- Membership Functions Diagram
- Modified Membership Functions Diagram

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
10. `read_crop_parameterizations_files()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Calculates climate suitability for multiple plants based on the CropSuite…` --rationale_for--> `climate_suitability_xarray()`  [EXTRACTED]
  CropSuiteLite/src/climate_suitability_main.py → CropSuiteLite/src/climate_suitability_main_xarray.py
- `change_otherst_parameters()` --uses--> `CropSensitivity`  [INFERRED]
  CropSuiteLite/run_cropsuitelite.py → CropSuiteLite/solutions/membership_functions.py
- `change_st1_parameter()` --uses--> `CropSensitivity`  [INFERRED]
  CropSuiteLite/run_cropsuitelite.py → CropSuiteLite/solutions/membership_functions.py
- `climate_suitability_xarray()` --calls--> `BaseProcessor`  [EXTRACTED]
  CropSuiteLite/src/climate_suitability_main_xarray.py → CropSuiteLite/datasets/utils.py
- `cropsuitability()` --calls--> `get_id_list_start()`  [EXTRACTED]
  CropSuiteLite/src/crop_suitability_main.py → CropSuiteLite/src/check_files.py

## Import Cycles
- None detected.

## Communities (49 total, 3 thin omitted)

### Community 0 - "Crop Climate Suitability"
Cohesion: 0.06
Nodes (69): # NOTE: self.extent is modified here to align with grid, Calculates climate suitability based on temperature and precipitation.…, Combines climate suitability with soil/terrain data to calculate final crop…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Interpolates or retrieves downscaled climate data (precipitation and…, aggregate_soil_raster_lst(), calcification_map() (+61 more)

### Community 1 - "Climate Suitability Parameters"
Cohesion: 0.06
Nodes (44): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+36 more)

### Community 2 - "CropSuitLite Model Controller"
Cohesion: 0.05
Nodes (35): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Main controller for the CropSuiteLite crop suitability modeling framework. This…, Calculates grid tiling based on available RAM to prevent memory overflow.…, change_otherst_parameters(), change_st1_parameter(), create_crop_parameters(), create_crop_suite_configuration_file() (+27 more)

### Community 3 - "NextGen Data Preprocessing"
Cohesion: 0.08
Nodes (20): create_climatology_from_nexgen(), main(), mask_single_layer(), resample_soilgrids_data(), BaseProcessor, compute_averaged_temp(), NexGen, NexGenPreProcessing (+12 more)

### Community 4 - "Input Data Validation"
Cohesion: 0.09
Nodes (40): calculate_area(), check_all_inputs(), check_climate_data(), check_soil(), check_within_one(), get_geotiff_datatype(), get_geotiff_extent(), get_geotiff_resolution() (+32 more)

### Community 5 - "Crop Evaluation and Metrics"
Cohesion: 0.12
Nodes (24): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+16 more)

### Community 6 - "Xarray Climate Suitability"
Cohesion: 0.11
Nodes (28): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+20 more)

### Community 7 - "Data Downloading Tools"
Cohesion: 0.10
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations., Initialize the downloader. Parameters ---------- url_root : str Base URL… (+9 more)

### Community 8 - "Crop Rotation and Raster IO"
Cohesion: 0.16
Nodes (17): calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):…, Read a GeoTIFF file with multiple bands into a NumPy array. Parameters: - fn… (+9 more)

### Community 9 - "Precipitation Resampling Tests"
Cohesion: 0.16
Nodes (5): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall., PrecipitationUnitsTest

### Community 10 - "Soilgrids Download and Reprojection"
Cohesion: 0.83
Nodes (3): crop_reproject(), get_vrt(), main()

## Knowledge Gaps
- **2 isolated node(s):** `Membership Functions Diagram`, `Modified Membership Functions Diagram`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 172 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `CropSuitLite Model Controller` to `Crop Evaluation and Metrics`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `CropSuiteLite` connect `CropSuitLite Model Controller` to `Crop Climate Suitability`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Why does `BaseProcessor` connect `NextGen Data Preprocessing` to `Xarray Climate Suitability`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `CropSensitivity` (e.g. with `change_otherst_parameters()` and `change_st1_parameter()`) actually correct?**
  _`CropSensitivity` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Path` (e.g. with `main()` and `main()`) actually correct?**
  _`Path` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Membership Functions Diagram`, `Modified Membership Functions Diagram` to the rest of the system?**
  _2 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Crop Climate Suitability` be split into smaller, more focused modules?**
  _Cohesion score 0.056962025316455694 - nodes in this community are weakly interconnected._