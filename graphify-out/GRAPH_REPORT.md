# Graph Report - poc_via_cslite  (2026-09-17)

## Corpus Check
- 312 files · ~155,269 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2917 nodes · 7163 edges · 205 communities (122 shown, 31 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 873 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6528614b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- farm_management/application/service.py
- run_cropsuitelite.py
- NexGenPreProcessing
- Huaura Dataset Preprocessing Configuration
- check_files.py
- DomainValidationError
- farm_management/infrastructure/postgresql_repositories.py
- Crop Membership Functions
- multicrop.py
- decision_support/application/service.py
- CropSuite.py
- DownloadCMIP6Data
- PostgreSQLEvaluationRepository
- climate_suitability_main_xarray.py
- CropSuiteLite
- test_migration_host.py
- climate_suitability_main.py
- InMemoryEvaluationRepository
- CoverageMeasurement
- decision_support/domain/models.py
- test_farm_management_postgresql.py
- VIA architecture guardrails
- Farm Management persistence
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- Architecture and Backend for CropSuiteLite Huaura v2
- Huaura Environmental Correction
- FilesystemScientificArtifactStore
- test_architecture.py
- Farm Management schema ownership
- Bounded-context layered structure
- Python and FastAPI backend decision
- IEnvironmentalInputIntegrityVerifier
- Farm Management minimum vertical slice
- Application commands and queries
- via_backend/worker.py
- VIA architecture implementation roadmap
- Evaluation
- EnvironmentalInputSnapshot
- EnvironmentalInputManifest
- Q: PostgreSQL Farm Management repositories
- agroclimatic_evaluation/interfaces/http.py
- ADR-012: PostgreSQL/PostGIS persistence for Environmental Information
- PostGIS service
- execution.py
- test_agroclimatic_evaluation_queries.py
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
- data_tools.py
- agroclimatic_evaluation/application/service.py
- agroclimatic_evaluation/__init__.py
- DatasetRepository
- Parcel
- ComparableCrop
- test_environmental_information_postgresql.py
- decision_support/__init__.py
- decision_support/interfaces/__init__.py
- EnvironmentalInformationService
- test_api_host.py
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
- ViabilityPolicySnapshot
- Huaura scientific fixture recovery audit
- DomainValidationError
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
- agroclimatic_evaluation/infrastructure/__init__.py
- test_agroclimatic_evaluation_domain.py
- test_decision_support.py
- Production deployment runtime contract
- GetPublishedDatasetVersion
- Settings
- EvaluationStatus
- read_crop_parameterizations_files
- FarmManagementService
- .from_geojson
- test_agroclimatic_evaluation_api.py
- cropsuite_adapter.py
- Agroclimatic Evaluation request, worker, recovery, and read slice
- Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation
- Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors
- test_production_compose_contract.py
- crop_suitability_main.py
- SpatialExtent
- cropsuite_comparison_adapter.py
- Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment.
- test_environmental_coverage.py
- PolicyReference
- config.py
- DomainValidationError
- Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract
- AgroclimaticEvaluationService
- test_decision_support_postgresql.py
- env.py
- test_environmental_information_api.py
- verify_runtime
- agroclimatic_evaluation/application/__init__.py
- test_farm_management_api.py
- benchmark_production_runtime.sh
- app.py
- migrate.py
- test_container_image_contract.py
- test_digitalocean_deployment_contract.py
- deploy_digitalocean.sh
- verify_production_compose.sh
- nc_tools.py
- process_precday_interp
- test_resource_benchmark_contract.py
- ._resolve_environmental_inputs
- backup_postgres.sh

## God Nodes (most connected - your core abstractions)
1. `Evaluation` - 90 edges
2. `DomainValidationError` - 56 edges
3. `PostgreSQLEvaluationRepository` - 50 edges
4. `EvaluationStatus` - 49 edges
5. `EnvironmentalInformationService` - 49 edges
6. `DatasetVersion` - 45 edges
7. `InMemoryEvaluationRepository` - 44 edges
8. `AgroclimaticEvaluationService` - 42 edges
9. `PolicyReference` - 39 edges
10. `EnvironmentalInputManifest` - 38 edges

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

## Communities (205 total, 31 thin omitted)

### Community 0 - "farm_management/application/service.py"
Cohesion: 0.10
Nodes (42): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., GetParcel, GetProject, ListParcels (+34 more)

### Community 1 - "run_cropsuitelite.py"
Cohesion: 0.06
Nodes (33): change_otherst_parameters(), change_st1_parameter(), create_crop_parameters(), create_crop_suite_configuration_file(), find_solution_type(), main(), modify_extent(), modify_general_files() (+25 more)

### Community 2 - "NexGenPreProcessing"
Cohesion: 0.07
Nodes (23): create_climatology_from_nexgen(), main(), mask_single_layer(), resample_soilgrids_data(), BaseProcessor, compute_averaged_temp(), NexGen, NexGenPreProcessing (+15 more)

### Community 3 - "Huaura Dataset Preprocessing Configuration"
Cohesion: 0.05
Nodes (43): Africa Processing Profile, Soil DEM and Land-Sea Layer Plan, Africa Climate Preprocessing Plan, Dataset Preprocessing Configuration, ACCESS-ESM1-5 SSP126 Climate Processing, Huaura 0.041667 Degree Processing Profile, Huaura High-Resolution Preprocessing Configuration, Huaura Processed 0.041667 Outputs (+35 more)

### Community 4 - "check_files.py"
Cohesion: 0.10
Nodes (36): calculate_area(), check_all_inputs(), check_climate_data(), check_soil(), check_within_one(), get_geotiff_datatype(), get_geotiff_extent(), get_geotiff_resolution() (+28 more)

### Community 5 - "DomainValidationError"
Cohesion: 0.12
Nodes (27): DomainValidationError, ValueError, Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring() (+19 more)

### Community 6 - "farm_management/infrastructure/postgresql_repositories.py"
Cohesion: 0.15
Nodes (20): Base, DeclarativeBase, SQLAlchemy metadata owned by Farm Management Infrastructure., Declarative base for Farm Management persistence records., Farm Management infrastructure layer., ParcelRecord, ParcelVersionRecord, ProjectRecord (+12 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.10
Nodes (22): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+14 more)

### Community 9 - "decision_support/application/service.py"
Cohesion: 0.09
Nodes (28): Decision Support application layer., IDecisionPolicy, IDefaultViabilityPolicyProvider, IDefaultViabilityPolicyStore, Protocol, Application ports for deterministic Decision Support policies., Evaluate comparable evidence without changing its scientific values., Provide the current VIA default viability policy without owning its storage. (+20 more)

### Community 10 - "CropSuite.py"
Cohesion: 0.14
Nodes (26): # NOTE: self.extent is modified here to align with grid, Interpolates or retrieves downscaled climate data (precipitation and…, extract_domain_from_global_3draster(), extract_domain_from_global_raster(), get_cpu_ram(), get_resolution_array(), get_shape_of_raster(), interpolate_nanmask() (+18 more)

### Community 11 - "DownloadCMIP6Data"
Cohesion: 0.09
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+9 more)

### Community 12 - "PostgreSQLEvaluationRepository"
Cohesion: 0.15
Nodes (49): PostgreSQLEvaluationRepository, SessionFactory, Durable adapter for immutable Evaluation aggregates., clean_evaluations(), _common_support(), _comparable_crops(), database(), _database_url() (+41 more)

### Community 13 - "climate_suitability_main_xarray.py"
Cohesion: 0.10
Nodes (31): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+23 more)

### Community 14 - "CropSuiteLite"
Cohesion: 0.12
Nodes (12): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Calculates climate suitability based on temperature and precipitation.…, Combines climate suitability with soil/terrain data to calculate final crop…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Calculates grid tiling based on available RAM to prevent memory overflow.… (+4 more)

### Community 15 - "test_migration_host.py"
Cohesion: 0.19
Nodes (19): main(), Run the explicit release migration CLI., _configure_valid_production(), CaptureFixture, MonkeyPatch, parametrize, Path, Focused tests for the explicit VIA release migration host. (+11 more)

### Community 16 - "climate_suitability_main.py"
Cohesion: 0.11
Nodes (26): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+18 more)

### Community 17 - "InMemoryEvaluationRepository"
Cohesion: 0.05
Nodes (87): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationExecutionService, Execute requested crops and summarize them through Application-owned ports., CropSuitabilityResult, One checked per-crop outcome from the scientific boundary. (+79 more)

### Community 18 - "CoverageMeasurement"
Cohesion: 0.16
Nodes (21): CheckDatasetVersionCoverage, CoverageClassification, CoverageMeasurement, StrEnum, Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port., _multi_polygon(), _polygon() (+13 more)

### Community 19 - "decision_support/domain/models.py"
Cohesion: 0.12
Nodes (25): DomainValidationError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Decision Support domain layer., CommonSupportEvidence, CommonSupportStatus, CropViabilityAssessment (+17 more)

### Community 20 - "test_farm_management_postgresql.py"
Cohesion: 0.21
Nodes (22): PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., clean_farm_management(), database(), _database_url(), _parcel(), _polygon() (+14 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management persistence"
Cohesion: 0.12
Nodes (20): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, Optimistic parcel revision transaction, ParcelVersionConflictError, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations (+12 more)

### Community 23 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.12
Nodes (40): EvaluationConflictError, Raised when an evaluation identity already exists., Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records., CropOutcomeRecord, EvaluationCommonSupportRecord (+32 more)

### Community 24 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.20
Nodes (10): Common-Support Ranking, ADR-002 Layered Bounded Contexts, ADR-003 Commands and Queries in Application, ADR-005 Background Worker, ADR-007 Initial Deployment, ADR-009 Multicrop Evaluation, Architecture and Backend for CropSuiteLite Huaura v2, Celery (+2 more)

### Community 25 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 26 - "FilesystemScientificArtifactStore"
Cohesion: 0.09
Nodes (48): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., _file_identity(), FilesystemScientificArtifactStore, _is_within(), PublishedScientificArtifact, Path, RuntimeError (+40 more)

### Community 27 - "test_architecture.py"
Cohesion: 0.15
Nodes (16): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+8 more)

### Community 28 - "Farm Management schema ownership"
Cohesion: 0.20
Nodes (10): Farm Management schema ownership, Projects, parcels, and parcel_versions tables, farm_management schema and owned tables, Optional durable repository adapter, Project, Parcel, and ParcelVersion domain model, Result querying increment, Bounded-context ownership and Farm Management repositories, Farm Management ownership query (+2 more)

### Community 29 - "Bounded-context layered structure"
Cohesion: 0.28
Nodes (9): Bounded-context ownership, Anti-corruption layer, Application layer, Bounded-context layered structure, Domain layer, Illustrative Evaluation module structure, Infrastructure layer, Interfaces layer (+1 more)

### Community 30 - "Python and FastAPI backend decision"
Cohesion: 0.22
Nodes (14): Multicrop Parcel Evaluation, run_evaluation Service, ADR-004 CropSuiteLite Port and Adapter, ADR-008 Sequential Crop Execution, Background worker execution, CropSuiteLite isolation boundary, FastAPI, Python (+6 more)

### Community 32 - "Farm Management minimum vertical slice"
Cohesion: 0.13
Nodes (13): ADR-011: PostgreSQL/PostGIS persistence for Farm Management, Consequences, Context, Decision, Status, Architectural alignment, Slice exclusions and authorization dependency, Explicit exclusions and provisional choices (+5 more)

### Community 33 - "Application commands and queries"
Cohesion: 0.29
Nodes (8): Application commands and queries, FastAPI composition root, In-memory and durable Infrastructure adapters, Project and parcel HTTP resources, Farm Management repository abstractions, Transport-to-domain path, ProjectRepository, ParcelRepository, and in-memory adapters, Repository ports and in-memory adapters query

### Community 34 - "via_backend/worker.py"
Cohesion: 0.07
Nodes (32): WorkerRunSummary, main(), make_shutdown_handler(), _parser(), _positive_integer(), _print_active_evaluations(), ArgumentParser, Logger (+24 more)

### Community 35 - "VIA architecture implementation roadmap"
Cohesion: 0.13
Nodes (16): Domain dependency rule, Layered modular monolith, Inward dependency direction, Architecture source and PoC preservation, Cross-stage architecture gates, Explanation and comparison increment, Modeling increment, Modular foundation increment (+8 more)

### Community 36 - "Evaluation"
Cohesion: 0.09
Nodes (13): Exception, CommonSupport, Validate deterministic scientific ranking semantics., Spatial support shared by the usable crop suitability rasters., validate_comparable_crops(), InvalidEvaluationTransitionError, RuntimeError, Raised when an Evaluation lifecycle transition is not allowed. (+5 more)

### Community 37 - "EnvironmentalInputSnapshot"
Cohesion: 0.21
Nodes (24): EnvironmentalInputSnapshot, Historical environmental input metadata captured for one evaluation input., ConfiguredEnvironmentalInputIntegrityVerifier, Verify manifests using deployment-configured exact dataset-version bindings., _binding(), _fingerprints(), _manifest(), parametrize (+16 more)

### Community 38 - "EnvironmentalInputManifest"
Cohesion: 0.18
Nodes (24): EnvironmentalInputManifest, Immutable set of exact environmental inputs resolved for an evaluation., parametrize, Focused domain tests for immutable environmental input manifests., _snapshot(), test_environmental_input_manifest_accepts_valid_inputs(), test_environmental_input_manifest_allows_same_version_for_distinct_input_keys(), test_environmental_input_manifest_rejects_duplicate_input_key() (+16 more)

### Community 40 - "Q: PostgreSQL Farm Management repositories"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: PostgreSQL Farm Management repositories, Source Nodes

### Community 41 - "agroclimatic_evaluation/interfaces/http.py"
Cohesion: 0.16
Nodes (20): CommonSupportResponse, ComparableCropResponse, CropEvidenceResponse, CropOutcomeResponse, EnvironmentalInputReferenceBody, EvaluationEvidenceResponse, EvaluationResponse, EvaluationResultResponse (+12 more)

### Community 42 - "ADR-012: PostgreSQL/PostGIS persistence for Environmental Information"
Cohesion: 0.12
Nodes (18): ADR-012: PostgreSQL/PostGIS persistence for Environmental Information, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation, Decision Support (+10 more)

### Community 43 - "PostGIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "execution.py"
Cohesion: 0.07
Nodes (40): _comparison_request(), datetime, Synchronous application orchestration for persisted evaluations., _to_common_support(), _to_comparable_crop(), CommonSupportResult, CropComparisonEngineError, CropComparisonExecutionError (+32 more)

### Community 45 - "test_agroclimatic_evaluation_queries.py"
Cohesion: 0.52
Nodes (6): _evaluation(), parametrize, Focused Application query tests for Agroclimatic Evaluation., _service(), test_finalized_public_contract_preserves_order_and_outcome_semantics(), test_public_contract_rejects_non_succeeded_evaluation()

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
Cohesion: 0.10
Nodes (20): DefaultViabilityPolicyConflictError, DefaultViabilityPolicyNotConfiguredError, LookupError, RuntimeError, Application errors for Decision Support policy configuration., Raised when VIA has no default viability policy configured., Raised when the default policy changed before an expected update., PolicyVersionConflictError (+12 more)

### Community 64 - "data_tools.py"
Cohesion: 0.15
Nodes (21): calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, create_cog_from_geotiff(), geotiff_to_smallest_datatype(), get_geotiff_extent(), ndarray (+13 more)

### Community 65 - "agroclimatic_evaluation/application/service.py"
Cohesion: 0.13
Nodes (27): FinalizedCommonSupport, FinalizedCommonSupportStatus, FinalizedComparableCrop, FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedEvaluationResult, FinalizedEvaluationResultReader, FinalizedScientificTrace (+19 more)

### Community 67 - "DatasetRepository"
Cohesion: 0.13
Nodes (11): CoverageComputation, Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort, datetime, DatasetRepository, DatasetVersionRepository, Protocol (+3 more)

### Community 68 - "Parcel"
Cohesion: 0.07
Nodes (26): ParcelVersionConflictError, RuntimeError, Domain errors raised by Farm Management invariants., Raised when persisted parcel history changed before a revision was saved., Farm Management domain layer., Parcel, Project, Farm Management domain model. (+18 more)

### Community 69 - "ComparableCrop"
Cohesion: 0.24
Nodes (16): ComparableCrop, One crop ranked on the exact common valid spatial support., _comparable_support(), _manifest(), parametrize, Domain tests for durable comparable crop results., _reference(), _snapshot() (+8 more)

### Community 70 - "test_environmental_information_postgresql.py"
Cohesion: 0.12
Nodes (28): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., Read and validate the test-only database settings before any DB operation., require_test_database_url(), UnsafeTestDatabaseError, validate_test_database_url() (+20 more)

### Community 73 - "EnvironmentalInformationService"
Cohesion: 0.07
Nodes (58): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Stable contracts deliberately published to other bounded contexts., GetDataset, GetDatasetVersion, ListDatasets (+50 more)

### Community 74 - "test_api_host.py"
Cohesion: 0.14
Nodes (19): ApiServerSettings, main(), Production HTTP process host for VIA., Provider-neutral Uvicorn bind settings for the production API process., Load API bind settings from the process environment., Validate production configuration and run one Uvicorn API process., _clear_api_environment(), _configure_production_persistence() (+11 more)

### Community 75 - "DatasetVersion"
Cohesion: 0.07
Nodes (35): DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., Dataset, DatasetVersion, Stable logical identity for a geoenvironmental dataset., Immutable reproducibility metadata for one dataset release., Positive horizontal and vertical source-cell resolution. (+27 more)

### Community 77 - "Q: ParcelVersion persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ParcelVersion persistence, Source Nodes

### Community 93 - "Q: Domain-to-Infrastructure dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Domain-to-Infrastructure dependency violations, Source Nodes

### Community 135 - "ViabilityPolicySnapshot"
Cohesion: 0.11
Nodes (22): EvaluateConfiguredDecisionSupport, StrEnum, How the viability policy configuration is selected for one execution., Select either VIA's current default policy or an explicit custom snapshot., Evaluate Decision Support using a selected viability-policy configuration., ViabilityPolicySelection, ViabilityPolicySelectionMode, ConfiguredDecisionSupportResult (+14 more)

### Community 136 - "Huaura scientific fixture recovery audit"
Cohesion: 0.08
Nodes (25): Benchmark compatibility, Boundary and reference mask, Climate, Current identity manifest, DEM, Executive status, Historical alternatives / abandoned paths, Huaura scientific fixture recovery audit (+17 more)

### Community 137 - "DomainValidationError"
Cohesion: 0.08
Nodes (40): _to_outcome(), CommonSupportStatus, StrEnum, Evaluation-level scientific common-support result., _is_finite_number(), datetime, Immutable environmental input snapshots owned by Agroclimatic Evaluation., _validate_aware_datetime() (+32 more)

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

### Community 150 - "agroclimatic_evaluation/infrastructure/__init__.py"
Cohesion: 0.13
Nodes (18): EnvironmentalInputIntegrityError, Raised when resolved environmental provenance does not match scientific inputs., Agroclimatic Evaluation infrastructure layer., CropSuiteEnvironmentalInputBinding, load_configured_environmental_input_integrity_verifier(), load_cropsuite_environmental_input_bindings(), _parse_uuid(), Any (+10 more)

### Community 151 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.19
Nodes (20): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+12 more)

### Community 152 - "test_decision_support.py"
Cohesion: 0.18
Nodes (24): ComparableCropEvidence, EvidenceAvailability, Whether deterministic policy evaluation has sufficient scientific evidence., A provider-produced crop mean and rank over common valid support., _decision_evidence(), _domain_common_support(), parametrize, Focused tests for the Decision Support bounded-context foundation. (+16 more)

### Community 154 - "Production deployment runtime contract"
Cohesion: 0.17
Nodes (11): B2 reproducible Linux container image, B6.1 resource benchmark, B6 production-like Docker Compose smoke, B7 DigitalOcean single-Droplet deployment definition, Database and migration contract, Environment contract, Filesystem contract, Process responsibilities (+3 more)

### Community 155 - "GetPublishedDatasetVersion"
Cohesion: 0.19
Nodes (19): GetPublishedDatasetVersion, PublishedDatasetVersion, PublishedDatasetVersionReader, Protocol, Public cross-context reader for exact immutable dataset versions., _published(), _dataset(), datetime (+11 more)

### Community 157 - "Settings"
Cohesion: 0.11
Nodes (27): Settings needed by the current backend composition root., Require the durable persistence contract used by the production API., Settings for the PostgreSQL polling worker process., Settings, WorkerSettings, MonkeyPatch, parametrize, Path (+19 more)

### Community 158 - "EvaluationStatus"
Cohesion: 0.08
Nodes (32): Commands expressing Agroclimatic Evaluation use-case intent., AgroclimaticEvaluationRecoveryService, Logger, Explicit fail-only recovery for abandoned evaluation executions., Mark an operator-confirmed active orphan as failed without retrying it., ActiveEvaluationResult, CropOutcomeResult, EvaluationResult (+24 more)

### Community 159 - "read_crop_parameterizations_files"
Cohesion: 0.15
Nodes (13): process_day_concfut(), get_formula(), get_id_list_start(), get_plant_param_interp_forms_dict(), print_crop_param_output(), print_sections(), Reads and parses crop parameterization files from a specified folder path.…, Prints the keys of a given dictionary as a list of sections or items. Args:… (+5 more)

### Community 160 - "FarmManagementService"
Cohesion: 0.17
Nodes (11): ParcelResult, ParcelVersionResult, ProjectResult, Transport-neutral results returned by Farm Management use cases., FarmManagementService, InvalidCommandError, datetime, UUID (+3 more)

### Community 161 - ".from_geojson"
Cohesion: 0.17
Nodes (18): _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing, MultiPolygonCoordinates, PolygonCoordinates (+10 more)

### Community 162 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.20
Nodes (28): _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any, FastAPI (+20 more)

### Community 163 - "cropsuite_adapter.py"
Cohesion: 0.08
Nodes (77): CropExecutionStatus, CropSuitabilityEngineError, CropSuitabilityExecutionError, InvalidEngineOutputError, Scientific outcomes reported independently of Evaluation lifecycle state., Base error for failures to invoke or understand the engine boundary., Raised when the existing engine service cannot produce a report., Raised when the engine report does not satisfy the expected PoC contract. (+69 more)

### Community 164 - "Agroclimatic Evaluation request, worker, recovery, and read slice"
Cohesion: 0.15
Nodes (11): ADR-015: PostgreSQL polling for Agroclimatic Evaluation worker dispatch, Consequences, Context, Decision, Status, Agroclimatic Evaluation request, worker, recovery, and read slice, Current lifecycle and execution, Deliberately deferred (+3 more)

### Community 165 - "Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation, Source Nodes

### Community 166 - "Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors, Source Nodes

### Community 167 - "test_production_compose_contract.py"
Cohesion: 0.36
Nodes (6): _mapping_keys(), Static invariants for the provider-neutral B6 production-like Compose smoke., _service_block(), test_b6_compose_encodes_release_ordering_and_runtime_mount_semantics(), test_b6_compose_has_exact_process_topology_and_same_image_contract(), test_b6_worker_bindings_fixture_is_valid_for_startup()

### Community 170 - "crop_suitability_main.py"
Cohesion: 0.12
Nodes (24): get_id_list_start(), Get a list of keys from a dictionary that start with a specified prefix.…, aggregate_soil_raster_lst(), calcification_map(), cropsuitability(), get_soil_data(), get_suitability_val_dict(), get_texture_class() (+16 more)

### Community 172 - "SpatialExtent"
Cohesion: 0.13
Nodes (23): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine (+15 more)

### Community 174 - "cropsuite_comparison_adapter.py"
Cohesion: 0.20
Nodes (22): CommonSupportStatus, ComparableCropResult, InvalidComparisonOutputError, StrEnum, Scientific common-support outcome across evaluated crops., One crop summarized on the exact common spatial support., Raised when scientific comparison returns an invalid contract., _fraction() (+14 more)

### Community 175 - "Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment., Source Nodes

### Community 176 - "test_environmental_coverage.py"
Cohesion: 0.15
Nodes (12): process_day_climsuit_memopt(), Processes climate suitability data for a specific day and saves the results to…, calculate_slope(), process_tempday_interp(), climate_coverage(), covered_gradient(), Spatial operations that preserve missing coverage instead of creating zeros., Require complete daily coverage; missing observations are not unsuitable days. (+4 more)

### Community 177 - "PolicyReference"
Cohesion: 0.14
Nodes (26): InvalidViabilityPolicyRevisionError, ValueError, Raised when a requested persisted policy version does not exist., Raised when a requested viability-policy revision is not a new version., ViabilityPolicyVersionNotFoundError, Application lifecycle for immutable Decision Support viability policies., Register one explicitly identified immutable viability-policy version., Create a new immutable version derived from an existing policy identity. (+18 more)

### Community 178 - "config.py"
Cohesion: 0.33
Nodes (7): _environment_float(), _environment_integer(), _is_same_or_within(), _optional_path(), Path, Environment-backed configuration for the VIA application host., _validate_scientific_path_topology()

### Community 180 - "DomainValidationError"
Cohesion: 0.08
Nodes (40): InvalidSpatialInputError, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, CoverageCompatibilityFailure (+32 more)

### Community 181 - "Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract, Source Nodes

### Community 182 - "AgroclimaticEvaluationService"
Cohesion: 0.12
Nodes (27): EnvironmentalInputReferenceInput, ParcelSnapshotInput, Transport-neutral parcel state supplied by an authorized caller., RequestEvaluation, GetEvaluation, GetEvaluationEvidence, GetEvaluationResult, ListEvaluations (+19 more)

### Community 183 - "test_decision_support_postgresql.py"
Cohesion: 0.17
Nodes (30): Decision Support infrastructure adapters., PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+22 more)

### Community 184 - "env.py"
Cohesion: 0.47
Nodes (5): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online()

### Community 185 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 187 - "verify_runtime"
Cohesion: 0.39
Nodes (8): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_read_only_directory(), _require_writable_directory(), _run_pip_check(), verify_runtime()

### Community 188 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.19
Nodes (16): Agroclimatic Evaluation application layer., _availability(), CommonSupportReadResult, ComparableCropReadResult, CropEvidenceResult, EvaluationEvidenceResult, EvaluationReadResult, EvaluationResultAvailability (+8 more)

### Community 189 - "test_farm_management_api.py"
Cohesion: 0.27
Nodes (11): _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app(), test_invalid_parcel_geometry_returns_validation_error(), scenario() (+3 more)

### Community 191 - "benchmark_production_runtime.sh"
Cohesion: 0.19
Nodes (16): artifact_bytes_for_evaluation(), COMPOSE_PROJECT_NAME, database_size_bytes(), fail(), monotonic_ns(), post_json(), record_stack_sample(), require_command() (+8 more)

### Community 192 - "app.py"
Cohesion: 0.12
Nodes (17): create_app(), create_production_app(), FastAPI, Side-effect-free FastAPI application composition., Build the production API after enforcing durable persistence settings., Build the VIA API and register its technical interfaces., create_database(), Engine (+9 more)

### Community 193 - "migrate.py"
Cohesion: 0.23
Nodes (11): _build_parser(), ArgumentParser, Path, One-shot production schema migration host for VIA releases., Return the repository-local Alembic config when running from source., Resolve the Alembic config without depending on the process cwd., Validate production persistence and migrate the schema to Alembic head., _require_production_postgresql() (+3 more)

### Community 195 - "test_digitalocean_deployment_contract.py"
Cohesion: 0.39
Nodes (8): _read(), _service_block(), test_deployment_script_enforces_release_order_without_destructive_cleanup(), test_deployment_script_requires_stable_worker_liveness_across_poll_intervals(), test_digitalocean_compose_preserves_runtime_and_durability_contracts(), test_docker_build_context_excludes_scientific_data(), test_ghcr_publish_is_gated_by_successful_b2_b6_run_for_same_commit(), test_provider_files_do_not_embed_secrets_or_raw_huaura_paths()

### Community 196 - "deploy_digitalocean.sh"
Cohesion: 0.57
Nodes (7): fail(), require_command(), require_directory(), deploy_digitalocean.sh script, verify_worker_liveness(), VIA_IMAGE, wait_for_health()

### Community 197 - "verify_production_compose.sh"
Cohesion: 0.60
Nodes (4): assert_running(), assert_worker_liveness(), container_id(), verify_production_compose.sh script

### Community 198 - "nc_tools.py"
Cohesion: 0.43
Nodes (6): get_netcdf_extent(), downscaled_files: list of netcdf files overlap: In Degree extent: [North, Left,…, Get the spatial extent (min and max) of the latitude and longitude in a NetCDF…, read_area_from_netcdf_list(), read_ind_date_file(), sort_coordinatelist()

### Community 199 - "process_precday_interp"
Cohesion: 0.26
Nodes (4): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall.

### Community 201 - "._resolve_environmental_inputs"
Cohesion: 0.50
Nodes (3): EnvironmentalInputResolutionError, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved.

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **220 isolated node(s):** `via-backend`, `backup_postgres.sh script`, `VIA_IMAGE`, `VIA_BENCHMARK_SOURCE_DIR`, `VIA_BENCHMARK_RUNTIME_CONFIG_DIR` (+215 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 992 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
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
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `app.py`, `via_backend/worker.py`, `DatasetRepository`, `DatasetVersion`, `SpatialExtent`, `CoverageMeasurement`, `DomainValidationError`, `GetPublishedDatasetVersion`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `create_app()` connect `app.py` to `FarmManagementService`, `farm_management/application/service.py`, `test_agroclimatic_evaluation_api.py`, `Parcel`, `farm_management/infrastructure/postgresql_repositories.py`, `EnvironmentalInformationService`, `DatasetVersion`, `PostgreSQLEvaluationRepository`, `InMemoryEvaluationRepository`, `DomainValidationError`, `test_farm_management_postgresql.py`, `AgroclimaticEvaluationService`, `test_farm_management_api.py`, `test_environmental_information_api.py`, `Settings`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `AgroclimaticEvaluationService` connect `AgroclimaticEvaluationService` to `app.py`, `agroclimatic_evaluation/application/service.py`, `.from_geojson`, `test_agroclimatic_evaluation_api.py`, `Evaluation`, `DomainValidationError`, `agroclimatic_evaluation/interfaces/http.py`, `execution.py`, `test_agroclimatic_evaluation_queries.py`, `InMemoryEvaluationRepository`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `agroclimatic_evaluation/application/__init__.py`, `EvaluationStatus`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 34 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `PostgreSQLEvaluationRepository` (e.g. with `EvaluationConflictError` and `Evaluation`) actually correct?**
  _`PostgreSQLEvaluationRepository` has 9 INFERRED edges - model-reasoned connections that need verification._