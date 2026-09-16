# Graph Report - poc_via_cslite  (2026-09-16)

## Corpus Check
- 281 files · ~125,135 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2403 nodes · 5719 edges · 187 communities (113 shown, 27 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 680 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9e80b7e0`
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
- workflow.py
- data_tools.py
- DownloadCMIP6Data
- main.py
- climate_suitability_main_xarray.py
- CropSuiteLite
- cropsuite_adapter.py
- climate_suitability_main.py
- write_to_netcdf
- CoverageMeasurement
- decision_support/domain/models.py
- test_farm_management_postgresql.py
- VIA architecture guardrails
- Farm Management persistence
- CropSuiteAdapter
- Architecture and Backend for CropSuiteLite Huaura v2
- Huaura Environmental Correction
- scientific_artifact_store.py
- test_architecture.py
- Farm Management schema ownership
- Bounded-context layered structure
- CropSuiteAdapter
- CropSuite.py
- ADR-011: PostgreSQL/PostGIS persistence for Farm Management
- Application commands and queries
- Farm Management minimum vertical slice
- Python and FastAPI backend decision
- InMemoryEvaluationRepository
- AgroclimaticEvaluationExecutionService
- Project
- VIA architecture implementation roadmap
- Q: PostgreSQL Farm Management repositories
- agroclimatic_evaluation/interfaces/http.py
- ADR-012: PostgreSQL/PostGIS persistence for Environmental Information
- PostGIS service
- environmental_information/interfaces/http.py
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
- test_environmental_information_api.py
- DomainValidationError
- test_environmental_information_coverage_postgresql.py
- agroclimatic_evaluation/__init__.py
- DomainValidationError
- decision_support/application/service.py
- test_agroclimatic_evaluation_api.py
- FarmManagementService
- decision_support/__init__.py
- decision_support/interfaces/__init__.py
- EnvironmentalInformationService
- test_decision_support.py
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
- test_farm_management_api.py
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
- test_agroclimatic_evaluation_domain.py
- CropComparisonExecutionError
- CropSuiteComparisonAdapter
- Evaluation
- health.py
- execution.py
- agroclimatic_evaluation/application/__init__.py
- nc_tools.py
- ComparableCrop
- test_environmental_information_postgresql.py
- Settings
- read_plant_params.py
- Agroclimatic Evaluation request, worker, recovery, and read slice
- Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation
- Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors
- test_agroclimatic_evaluation_postgresql.py
- crop_suitability_main.py
- FilesystemScientificArtifactStore
- via_backend/worker.py
- CropComparisonRequest
- Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment.
- CropSuitabilityResult
- ViabilityPolicySnapshot
- cropsuite_comparison_adapter.py
- test_environmental_coverage.py
- Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract
- agroclimatic_evaluation/infrastructure/__init__.py
- test_decision_support_postgresql.py
- config.py
- ScientificArtifactStore

## God Nodes (most connected - your core abstractions)
1. `Evaluation` - 75 edges
2. `DomainValidationError` - 44 edges
3. `EnvironmentalInformationService` - 43 edges
4. `DatasetVersion` - 43 edges
5. `AgroclimaticEvaluationService` - 40 edges
6. `EvaluationStatus` - 40 edges
7. `Parcel` - 38 edges
8. `InMemoryEvaluationRepository` - 36 edges
9. `CropOutcome` - 35 edges
10. `Dataset` - 34 edges

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

## Communities (187 total, 27 thin omitted)

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

### Community 9 - "workflow.py"
Cohesion: 0.11
Nodes (22): Decision Support application layer., IDefaultViabilityPolicyProvider, Application ports for deterministic Decision Support policies., Provide the current VIA default viability policy without owning its storage., EvaluateConfiguredDecisionSupport, EvaluateDecisionSupport, StrEnum, Decision Support application query messages. (+14 more)

### Community 10 - "data_tools.py"
Cohesion: 0.14
Nodes (26): Combines climate suitability with soil/terrain data to calculate final crop…, Interpolates or retrieves downscaled climate data (precipitation and…, extract_domain_from_global_3draster(), extract_domain_from_global_raster(), get_cpu_ram(), get_resolution_array(), get_shape_of_raster(), interpolate_nanmask() (+18 more)

### Community 11 - "DownloadCMIP6Data"
Cohesion: 0.09
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+9 more)

### Community 12 - "main.py"
Cohesion: 0.09
Nodes (26): InvalidSpatialInputError, CoverageComputation, Protocol, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute. (+18 more)

### Community 13 - "climate_suitability_main_xarray.py"
Cohesion: 0.10
Nodes (31): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+23 more)

### Community 14 - "CropSuiteLite"
Cohesion: 0.13
Nodes (11): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Calculates climate suitability based on temperature and precipitation.…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Calculates grid tiling based on available RAM to prevent memory overflow.…, Private subprocess entry point; each invocation has its own working directory. (+3 more)

### Community 15 - "cropsuite_adapter.py"
Cohesion: 0.16
Nodes (33): InvalidEngineOutputError, Application-owned boundary for one crop suitability evaluation., Raised when the engine report does not satisfy the expected PoC contract., Current PoC parcel summary for the crop-suitability output., Portable grid identity needed to verify comparable scientific rasters., Scientific artifact roles understood by VIA., Durable opaque reference to one verified scientific artifact., An engine-reported failure, distinct from no coverage and a zero score. (+25 more)

### Community 16 - "climate_suitability_main.py"
Cohesion: 0.09
Nodes (31): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+23 more)

### Community 17 - "write_to_netcdf"
Cohesion: 0.26
Nodes (5): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, write_to_netcdf(), PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall.

### Community 18 - "CoverageMeasurement"
Cohesion: 0.16
Nodes (21): CheckDatasetVersionCoverage, CoverageClassification, CoverageMeasurement, StrEnum, Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port., _multi_polygon(), _polygon() (+13 more)

### Community 19 - "decision_support/domain/models.py"
Cohesion: 0.12
Nodes (27): DomainValidationError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Decision Support domain layer., CommonSupportEvidence, CropViabilityAssessment, DecisionEvidence (+19 more)

### Community 20 - "test_farm_management_postgresql.py"
Cohesion: 0.21
Nodes (22): PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel() (+14 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management persistence"
Cohesion: 0.15
Nodes (15): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations, Farm Management persistence, PostGIS geometry storage contract (+7 more)

### Community 23 - "CropSuiteAdapter"
Cohesion: 0.19
Nodes (29): CropExecutionStatus, Scientific outcomes reported independently of Evaluation lifecycle state., CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability., _adapter(), _geometry(), Any, parametrize (+21 more)

### Community 24 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.18
Nodes (11): Common-Support Ranking, ADR-002 Layered Bounded Contexts, ADR-003 Commands and Queries in Application, ADR-005 Background Worker, ADR-007 Initial Deployment, ADR-008 Sequential Crop Execution, ADR-009 Multicrop Evaluation, Architecture and Backend for CropSuiteLite Huaura v2 (+3 more)

### Community 25 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 26 - "scientific_artifact_store.py"
Cohesion: 0.15
Nodes (17): _file_identity(), _is_within(), PublishedScientificArtifact, Path, RuntimeError, Durable filesystem storage for scientific artifacts., Base error for durable scientific artifact storage failures., Raised when an immutable artifact reference already has different content. (+9 more)

### Community 27 - "test_architecture.py"
Cohesion: 0.15
Nodes (14): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+6 more)

### Community 28 - "Farm Management schema ownership"
Cohesion: 0.20
Nodes (10): Farm Management schema ownership, Projects, parcels, and parcel_versions tables, farm_management schema and owned tables, Optional durable repository adapter, Project, Parcel, and ParcelVersion domain model, Result querying increment, Bounded-context ownership and Farm Management repositories, Farm Management ownership query (+2 more)

### Community 29 - "Bounded-context layered structure"
Cohesion: 0.28
Nodes (9): Bounded-context ownership, Anti-corruption layer, Application layer, Bounded-context layered structure, Domain layer, Illustrative Evaluation module structure, Infrastructure layer, Interfaces layer (+1 more)

### Community 30 - "CropSuiteAdapter"
Cohesion: 0.46
Nodes (8): Multicrop Parcel Evaluation, run_evaluation Service, ADR-004 CropSuiteLite Port and Adapter, CropSuiteLite isolation boundary, CropSuiteAdapter, CropSuiteLite Integration Boundary, ICropSuitabilityEngine, On-demand execution increment

### Community 31 - "CropSuite.py"
Cohesion: 0.15
Nodes (20): # NOTE: self.extent is modified here to align with grid, calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):… (+12 more)

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

### Community 36 - "InMemoryEvaluationRepository"
Cohesion: 0.11
Nodes (38): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Mark an operator-confirmed active orphan as failed without retrying it., AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application., InMemoryEvaluationRepository, UUID (+30 more)

### Community 37 - "AgroclimaticEvaluationExecutionService"
Cohesion: 0.19
Nodes (25): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, Execute requested crops and summarize them through Application-owned ports., _artifact(), _evaluation(), _execute(), FakeComparisonEngine (+17 more)

### Community 38 - "Project"
Cohesion: 0.13
Nodes (10): Project, An agricultural project that groups parcels., ParcelRepository, ProjectRepository, Protocol, UUID, Repository abstractions for Farm Management aggregates., _project_from_record() (+2 more)

### Community 39 - "VIA architecture implementation roadmap"
Cohesion: 0.33
Nodes (7): Architecture source and PoC preservation, Cross-stage architecture gates, Explanation and comparison increment, Modeling increment, Parcel and environmental coverage increment, Public deployment increment, VIA architecture implementation roadmap

### Community 40 - "Q: PostgreSQL Farm Management repositories"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: PostgreSQL Farm Management repositories, Source Nodes

### Community 41 - "agroclimatic_evaluation/interfaces/http.py"
Cohesion: 0.17
Nodes (21): EvaluationStatus, StrEnum, Architecture-approved lifecycle vocabulary., CommonSupportResponse, ComparableCropResponse, CropEvidenceResponse, CropOutcomeResponse, EvaluationEvidenceResponse (+13 more)

### Community 42 - "ADR-012: PostgreSQL/PostGIS persistence for Environmental Information"
Cohesion: 0.12
Nodes (18): ADR-012: PostgreSQL/PostGIS persistence for Environmental Information, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation, Decision Support (+10 more)

### Community 43 - "PostGIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "environmental_information/interfaces/http.py"
Cohesion: 0.22
Nodes (13): CheckCoverageBody, CoverageGeometryBody, CreateDatasetBody, CreateDatasetVersionBody, DatasetResponse, DatasetVersionCoverageResponse, DatasetVersionResponse, BaseModel (+5 more)

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

### Community 63 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 64 - "DomainValidationError"
Cohesion: 0.07
Nodes (38): CommonSupport, Evaluation-level scientific common-support result., Validate deterministic scientific ranking semantics., Spatial support shared by the usable crop suitability rasters., validate_comparable_crops(), DomainValidationError, InvalidEvaluationTransitionError, RuntimeError (+30 more)

### Community 65 - "test_environmental_information_coverage_postgresql.py"
Cohesion: 0.27
Nodes (14): clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine, fixture, parametrize (+6 more)

### Community 67 - "DomainValidationError"
Cohesion: 0.15
Nodes (19): _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing, MultiPolygonCoordinates, PolygonCoordinates (+11 more)

### Community 68 - "decision_support/application/service.py"
Cohesion: 0.10
Nodes (24): FinalizedCommonSupport, FinalizedEvaluationResult, FinalizedEvaluationResultReader, GetFinalizedEvaluationResult, Protocol, Stable contracts deliberately published to other bounded contexts., Public local interface for a future Decision Support consumer., IDecisionPolicy (+16 more)

### Community 69 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.11
Nodes (38): ParcelSnapshotInput, Transport-neutral parcel state supplied by an authorized caller., GetEvaluation, create_router(), get_evaluation(), get_evaluation_evidence(), get_evaluation_result(), list_evaluations() (+30 more)

### Community 70 - "FarmManagementService"
Cohesion: 0.17
Nodes (11): ParcelResult, ParcelVersionResult, ProjectResult, Transport-neutral results returned by Farm Management use cases., FarmManagementService, InvalidCommandError, datetime, UUID (+3 more)

### Community 73 - "EnvironmentalInformationService"
Cohesion: 0.08
Nodes (45): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., GetDataset, GetDatasetVersion, ListDatasets, ListDatasetVersions (+37 more)

### Community 74 - "test_decision_support.py"
Cohesion: 0.12
Nodes (42): FinalizedCommonSupportStatus, FinalizedComparableCrop, ComparableCropEvidence, A provider-produced crop mean and rank over common valid support., _common_support(), _decision_evidence(), _DefaultPolicyProvider, _domain_common_support() (+34 more)

### Community 75 - "DatasetVersion"
Cohesion: 0.09
Nodes (34): DatasetVersionConflictError, RuntimeError, Domain errors raised by Environmental Information invariants., Raised when a dataset version identifier has already been registered., Environmental Information domain layer., DatasetVersion, Environmental Information domain model., Immutable reproducibility metadata for one dataset release. (+26 more)

### Community 77 - "Q: ParcelVersion persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ParcelVersion persistence, Source Nodes

### Community 93 - "Q: Domain-to-Infrastructure dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Domain-to-Infrastructure dependency violations, Source Nodes

### Community 135 - "Dataset"
Cohesion: 0.12
Nodes (11): Dataset, Stable logical identity for a geoenvironmental dataset., DatasetRepository, DatasetVersionRepository, Protocol, UUID, DatasetRecord, _dataset_from_record() (+3 more)

### Community 136 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 137 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.11
Nodes (39): EvaluationConflictError, Raised when an evaluation identity already exists., CropOutcome, One durable result associated with an Evaluation and requested crop., Durable scientific evidence referenced without exposing filesystem paths., ScientificArtifact, Base, DeclarativeBase (+31 more)

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

### Community 150 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.36
Nodes (9): _evaluation(), _polygon(), parametrize, Focused domain tests for immutable evaluation requests., _snapshot(), test_empty_or_duplicate_requested_crops_are_rejected(), test_parcel_snapshot_is_deeply_immutable_and_detached_from_input(), test_polygon_and_multipolygon_snapshot_geometry_are_supported() (+1 more)

### Community 151 - "CropComparisonExecutionError"
Cohesion: 0.24
Nodes (8): CropComparisonEngineError, CropComparisonExecutionError, RuntimeError, Base error for the scientific crop-comparison boundary., Raised when scientific common-support comparison cannot execute., _is_within(), Path, ComparisonRunner

### Community 152 - "CropSuiteComparisonAdapter"
Cohesion: 0.30
Nodes (17): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., _artifact(), Any, Path, _report(), _request(), _snapshot() (+9 more)

### Community 154 - "Evaluation"
Cohesion: 0.08
Nodes (18): Exception, Evaluation, An immutable multicrop evaluation and its scientific outcomes., EvaluationRepository, Protocol, UUID, _evaluation(), _outcome() (+10 more)

### Community 155 - "health.py"
Cohesion: 0.40
Nodes (4): health(), Host-level health endpoint., Report that the API process is ready to receive requests., get

### Community 157 - "execution.py"
Cohesion: 0.16
Nodes (17): _comparison_request(), Synchronous application orchestration for persisted evaluations., _to_common_support(), _to_comparable_crop(), _to_outcome(), CommonSupportStatus, StrEnum, CropOutcomeStatus (+9 more)

### Community 158 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.07
Nodes (51): Commands expressing Agroclimatic Evaluation use-case intent., RequestEvaluation, Agroclimatic Evaluation application layer., FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedScientificTrace, FinalizedSuitabilitySummary, StrEnum (+43 more)

### Community 159 - "nc_tools.py"
Cohesion: 0.22
Nodes (12): create_cog_from_geotiff(), geotiff_to_smallest_datatype(), Convert image to COG., merge_outputs_no_overlap(), get_netcdf_extent(), merge_netcdf_files(), downscaled_files: list of netcdf files overlap: In Degree extent: [North, Left,…, Get the spatial extent (min and max) of the latitude and longitude in a NetCDF… (+4 more)

### Community 160 - "ComparableCrop"
Cohesion: 0.25
Nodes (15): ComparableCrop, One crop ranked on the exact common valid spatial support., _comparable_support(), _outcome(), parametrize, Domain tests for durable comparable crop results., _snapshot(), _summarizing() (+7 more)

### Community 161 - "test_environmental_information_postgresql.py"
Cohesion: 0.18
Nodes (17): Base, DeclarativeBase, SQLAlchemy metadata owned by Environmental Information Infrastructure., Declarative base for Environmental Information persistence records., Database records for Environmental Information; not domain entities., clean_environmental_information(), database(), _database_url() (+9 more)

### Community 162 - "Settings"
Cohesion: 0.17
Nodes (13): Settings needed by the current backend composition root., Settings, MonkeyPatch, parametrize, Tests for environment-driven application composition settings., test_database_url_selects_postgresql_by_default(), test_environmental_postgresql_selection_requires_database_url(), test_evaluation_postgresql_selection_requires_database_url() (+5 more)

### Community 163 - "read_plant_params.py"
Cohesion: 0.15
Nodes (10): get_formula(), get_id_list_start(), get_plant_param_interp_forms_dict(), print_crop_param_output(), print_sections(), Prints the keys of a given dictionary as a list of sections or items. Args:…, Given two arrays of numerical values x_vals and y_vals representing data…, Prints the number of crop parameterizations found and the keys of a given… (+2 more)

### Community 164 - "Agroclimatic Evaluation request, worker, recovery, and read slice"
Cohesion: 0.15
Nodes (11): ADR-015: PostgreSQL polling for Agroclimatic Evaluation worker dispatch, Consequences, Context, Decision, Status, Agroclimatic Evaluation request, worker, recovery, and read slice, Current lifecycle and execution, Deliberately deferred (+3 more)

### Community 165 - "Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation, Source Nodes

### Community 166 - "Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors, Source Nodes

### Community 167 - "test_agroclimatic_evaluation_postgresql.py"
Cohesion: 0.11
Nodes (42): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., Read and validate the test-only database settings before any DB operation., require_test_database_url(), UnsafeTestDatabaseError, validate_test_database_url() (+34 more)

### Community 170 - "crop_suitability_main.py"
Cohesion: 0.13
Nodes (23): aggregate_soil_raster_lst(), calcification_map(), cropsuitability(), get_soil_data(), get_suitability_val_dict(), get_texture_class(), get_valid_dtype(), getTable() (+15 more)

### Community 171 - "FilesystemScientificArtifactStore"
Cohesion: 0.30
Nodes (14): FilesystemScientificArtifactStore, Filesystem-backed immutable artifact store., parametrize, Path, test_publish_creates_durable_artifact_with_opaque_reference(), test_publish_is_idempotent_for_identical_content(), test_publish_rejects_content_that_does_not_match_expected_checksum(), test_publish_rejects_different_content_for_existing_reference() (+6 more)

### Community 172 - "via_backend/worker.py"
Cohesion: 0.13
Nodes (18): ArgumentParser, create_database(), Engine, SessionFactory, Host-level SQLAlchemy engine and session construction., Create the shared engine and short-lived session factory., Shared technical infrastructure used by the application composition root., create_worker() (+10 more)

### Community 174 - "CropComparisonRequest"
Cohesion: 0.17
Nodes (10): CommonSupportResult, CropComparisonRequest, CropComparisonResult, ICropComparisonEngine, Compare crop suitability only on identical valid spatial support., Scientific support shared by all usable crop suitability rasters., Checked multicrop comparison returned by the scientific boundary., Compare durable crop outputs using the authoritative scientific engine. (+2 more)

### Community 175 - "Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment., Source Nodes

### Community 176 - "CropSuitabilityResult"
Cohesion: 0.13
Nodes (12): CropSuitabilityRequest, CropSuitabilityResult, ICropSuitabilityEngine, Protocol, Evaluate one crop without exposing engine process or filesystem details., Transport-neutral input for evaluating one crop against an exact snapshot., One checked per-crop outcome from the scientific boundary., Exception (+4 more)

### Community 177 - "ViabilityPolicySnapshot"
Cohesion: 0.09
Nodes (24): IViabilityPolicyRepository, Protocol, Store and restore immutable viability-policy versions., PolicyVersionConflictError, RuntimeError, Raised when one immutable policy reference is bound to different thresholds., PolicyReference, Stable identity of the deterministic policy selected for an evaluation. (+16 more)

### Community 178 - "cropsuite_comparison_adapter.py"
Cohesion: 0.26
Nodes (19): CommonSupportStatus, ComparableCropResult, InvalidComparisonOutputError, StrEnum, Scientific common-support outcome across evaluated crops., One crop summarized on the exact common spatial support., Raised when scientific comparison returns an invalid contract., _fraction() (+11 more)

### Community 180 - "test_environmental_coverage.py"
Cohesion: 0.18
Nodes (8): calculate_slope(), process_tempday_interp(), covered_gradient(), Spatial operations that preserve missing coverage instead of creating zeros., Central differences inside coverage, one-sided at its boundary. An axis with no…, Temporarily nearest-fill gaps, resample, then restore the coverage mask., resample_valid(), EnvironmentalCoverageTest

### Community 181 - "Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract, Source Nodes

### Community 182 - "agroclimatic_evaluation/infrastructure/__init__.py"
Cohesion: 0.25
Nodes (6): CropComparisonInput, One durable crop suitability raster offered to scientific comparison., Agroclimatic Evaluation infrastructure layer., scientific, Opt-in smoke test for the real CropSuiteLite comparison boundary., test_real_cropsuite_comparison_adapter_smoke()

### Community 183 - "test_decision_support_postgresql.py"
Cohesion: 0.34
Nodes (13): clean_policy_versions(), database(), _database_url(), Engine, fixture, SessionFactory, PostgreSQL integration tests for Decision Support policy persistence., _snapshot() (+5 more)

### Community 184 - "config.py"
Cohesion: 0.21
Nodes (9): _environment_float(), _environment_integer(), _optional_path(), Path, Environment-backed configuration for the VIA application host., Settings for the PostgreSQL polling worker process., WorkerSettings, test_worker_run_requires_durable_artifact_root() (+1 more)

### Community 185 - "ScientificArtifactStore"
Cohesion: 0.19
Nodes (10): CropSuitabilityEngineError, CropSuitabilityExecutionError, Base error for failures to invoke or understand the engine boundary., Raised when the existing engine service cannot produce a report., _is_within(), Path, Protocol, Publish immutable scientific files behind opaque logical references. (+2 more)

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **181 isolated node(s):** `via-backend`, `Status`, `Context`, `Decision`, `Consequences` (+176 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 838 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `test_environmental_information_coverage_postgresql.py`, `DomainValidationError`, `Dataset`, `DatasetVersion`, `main.py`, `environmental_information/interfaces/http.py`, `CoverageMeasurement`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `create_app()` connect `main.py` to `farm_management/application/service.py`, `Settings`, `InMemoryEvaluationRepository`, `test_agroclimatic_evaluation_api.py`, `FarmManagementService`, `Dataset`, `Parcel`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `EnvironmentalInformationService`, `DatasetVersion`, `Project`, `via_backend/worker.py`, `test_farm_management_api.py`, `test_farm_management_postgresql.py`, `agroclimatic_evaluation/application/__init__.py`, `test_environmental_information_api.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `FarmManagementService` connect `FarmManagementService` to `farm_management/application/service.py`, `DomainValidationError`, `Project`, `Parcel`, `main.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `EnvironmentalInformationService` (e.g. with `CreateDataset` and `CreateDatasetVersion`) actually correct?**
  _`EnvironmentalInformationService` has 26 INFERRED edges - model-reasoned connections that need verification._