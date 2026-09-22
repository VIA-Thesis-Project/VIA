# Graph Report - poc_via_cslite  (2026-09-22)

## Corpus Check
- 397 files · ~209,084 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4284 nodes · 11051 edges · 260 communities (169 shown, 32 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 1442 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `38125f01`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FarmManagementService
- CropSensitivity
- NexGenPreProcessing
- Huaura Dataset Preprocessing Configuration
- check_files.py
- ParcelGeometry
- Parcel
- Crop Membership Functions
- multicrop.py
- decision_support/domain/models.py
- crop_suitability_main.py
- DownloadCMIP6Data
- PostgreSQLEvaluationRepository
- climate_suitability_main_xarray.py
- CropSuiteLite
- test_migration_host.py
- climate_suitability_main.py
- test_cropsuite_adapter.py
- CoverageMeasurement
- decision_support/application/service.py
- test_farm_management_postgresql.py
- VIA architecture guardrails
- Farm Management persistence
- knowledge_services.py
- Architecture and Backend for CropSuiteLite Huaura v2
- Huaura Environmental Correction
- EmbeddingIndex
- test_architecture.py
- Farm Management schema ownership
- Bounded-context layered structure
- Python and FastAPI backend decision
- AgroclimaticEvaluationExecutionService
- Farm Management minimum vertical slice
- Application commands and queries
- cropsuite_adapter.py
- VIA architecture implementation roadmap
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- test_agronomic_knowledge.py
- ConfiguredEnvironmentalInputIntegrityVerifier
- Q: PostgreSQL Farm Management repositories
- agroclimatic_evaluation/interfaces/http.py
- ADR-012: PostgreSQL/PostGIS persistence for Environmental Information
- PostGIS service
- GetPublishedDatasetVersion
- agroclimatic_evaluation/infrastructure/__init__.py
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
- Probar la API de VIA con Postman
- __main__.py
- Atlas A Logo
- read_remote_chunk
- decision_support/infrastructure/postgresql_repositories.py
- DomainValidationError
- EnvironmentalInputManifest
- agroclimatic_evaluation/__init__.py
- Dataset
- legacy_ownership_admin.py
- test_agronomic_knowledge_postgresql.py
- RetrievedKnowledge
- decision_support/__init__.py
- test_agronomic_knowledge_http.py
- EnvironmentalInformationService
- test_api_host.py
- DatasetVersion
- environmental_information/__init__.py
- Q: ParcelVersion persistence
- farm_management/__init__.py
- identity_access/application/service.py
- User
- PostgreSQLUserRepository
- identity_access/__init__.py
- app.py
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
- scientific_input_integrity.py
- Huaura scientific fixture recovery audit
- Project
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
- FilesystemScientificArtifactStore
- test_agroclimatic_evaluation_domain.py
- AuthSession
- Production deployment runtime contract
- test_frontend_openapi.py
- Settings
- knowledge_models.py
- CropSuite.py
- test_decision_support.py
- .from_geojson
- test_agroclimatic_evaluation_api.py
- test_evaluation_capabilities_api.py
- Agroclimatic Evaluation request, worker, recovery, and read slice
- Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation
- Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors
- CropSuiteComparisonAdapter
- SpatialExtent
- CropSuitabilityResult
- Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment.
- env.py
- PolicyReference
- config.py
- DomainValidationError
- Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract
- agroclimatic_evaluation/application/__init__.py
- test_decision_support_postgresql.py
- test_ia4_quota.py
- test_environmental_information_api.py
- verify_runtime
- decision_support/infrastructure/__init__.py
- test_farm_management_api.py
- benchmark_production_runtime.sh
- test_authentication.py
- InMemoryEvaluationRepository
- test_container_image_contract.py
- test_digitalocean_deployment_contract.py
- deploy_digitalocean.sh
- verify_production_compose.sh
- Frontend integration flows
- downscaling.py
- test_resource_benchmark_contract.py
- database_test_support.py
- backup_postgres.sh
- Evaluation
- via_backend/worker.py
- test_cors.py
- Scientific result semantics
- generate_frontend_openapi.py
- test_limiting_factor_domain.py
- health.py
- cropsuite_comparison_adapter.py
- Frontend API reference
- read_models.py
- Asynchronous evaluations
- nc_tools.py
- Frontend development setup
- resources/__init__.py
- Sample data
- knowledge/__init__.py
- Error handling
- VIA frontend handoff
- README.md
- check_get
- known-gaps.md
- create_database
- ViabilityPolicySnapshot
- test_identity_access.py
- test_ia5_release_security.py
- test_environmental_information_postgresql.py
- smoke_production_api.py
- QuotaExceededError
- test_production_compose_contract.py
- decision_support/interfaces/http.py
- run_cropsuitelite.py
- WaterRegime
- UUID
- aoi.py
- ParcelSnapshot
- test_ia5_huaura_aoi.py
- Scripts de VIA
- agroclimatic_evaluation/application/public.py
- Navegación
- test_ia5_release_artifacts.py
- Route and security matrix
- WorkerSettings
- migrate.py
- Contribuir a VIA
- factor_display_label
- knowledge.py
- [Unreleased]
- AuthorizedParcelSnapshotProvider
- ScientificArtifactRole

## God Nodes (most connected - your core abstractions)
1. `Evaluation` - 107 edges
2. `create_app()` - 74 edges
3. `DomainValidationError` - 70 edges
4. `Settings` - 66 edges
5. `WaterRegime` - 65 edges
6. `PostgreSQLEvaluationRepository` - 64 edges
7. `AgroclimaticEvaluationService` - 53 edges
8. `EvaluationStatus` - 52 edges
9. `InMemoryEvaluationRepository` - 52 edges
10. `EnvironmentalInformationService` - 49 edges

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

## Communities (260 total, 32 thin omitted)

### Community 0 - "FarmManagementService"
Cohesion: 0.06
Nodes (69): CreateParcel, CreateProject, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, Farm Management application layer., ParcelAreaOfInterestValidator, Protocol, Application ports owned by Farm Management. (+61 more)

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

### Community 5 - "ParcelGeometry"
Cohesion: 0.08
Nodes (35): DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position() (+27 more)

### Community 6 - "Parcel"
Cohesion: 0.11
Nodes (28): ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved., Parcel, A named parcel whose geometry changes only by appending versions., Base, DeclarativeBase, SQLAlchemy metadata owned by Farm Management Infrastructure. (+20 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.10
Nodes (22): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+14 more)

### Community 9 - "decision_support/domain/models.py"
Cohesion: 0.09
Nodes (32): DomainValidationError, PolicyVersionConflictError, RuntimeError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Raised when one immutable policy reference is bound to different thresholds., Decision Support domain layer. (+24 more)

### Community 10 - "crop_suitability_main.py"
Cohesion: 0.09
Nodes (39): Combines climate suitability with soil/terrain data to calculate final crop…, aggregate_soil_raster_lst(), calcification_map(), cropsuitability(), get_soil_data(), get_suitability_val_dict(), get_texture_class(), get_valid_dtype() (+31 more)

### Community 11 - "DownloadCMIP6Data"
Cohesion: 0.09
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+9 more)

### Community 12 - "PostgreSQLEvaluationRepository"
Cohesion: 0.09
Nodes (82): Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records., CropLimitationEvidenceRecord, CropLimitingFactorRecord, CropOutcomeRecord, EvaluationCommonSupportRecord (+74 more)

### Community 13 - "climate_suitability_main_xarray.py"
Cohesion: 0.09
Nodes (33): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+25 more)

### Community 14 - "CropSuiteLite"
Cohesion: 0.13
Nodes (11): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Calculates climate suitability based on temperature and precipitation.…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Calculates grid tiling based on available RAM to prevent memory overflow.…, Private subprocess entry point; each invocation has its own working directory. (+3 more)

### Community 15 - "test_migration_host.py"
Cohesion: 0.19
Nodes (19): main(), Run the explicit release migration CLI., _configure_valid_production(), CaptureFixture, MonkeyPatch, parametrize, Path, Focused tests for the explicit VIA release migration host. (+11 more)

### Community 16 - "climate_suitability_main.py"
Cohesion: 0.07
Nodes (39): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+31 more)

### Community 17 - "test_cropsuite_adapter.py"
Cohesion: 0.11
Nodes (64): CropExecutionStatus, CropSuitabilityRequest, LimitationEvidenceAvailability, Scientific outcomes reported independently of Evaluation lifecycle state., Transport-neutral input for evaluating one crop against an exact snapshot., Availability of deterministic SAME-RUN limiting-factor evidence., CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability. (+56 more)

### Community 18 - "CoverageMeasurement"
Cohesion: 0.14
Nodes (23): CheckDatasetVersionCoverage, CoverageClassification, CoverageCompatibilityFailure, CoverageMeasurement, StrEnum, Structural metadata prevented a meaningful spatial measurement., Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port. (+15 more)

### Community 19 - "decision_support/application/service.py"
Cohesion: 0.09
Nodes (33): GetFinalizedEvaluationResult, Decision Support application layer., IDecisionPolicy, IDefaultViabilityPolicyProvider, Application ports for deterministic Decision Support policies., Evaluate comparable evidence without changing its scientific values., Provide the current VIA default viability policy without owning its storage., EvaluateConfiguredDecisionSupport (+25 more)

### Community 20 - "test_farm_management_postgresql.py"
Cohesion: 0.26
Nodes (21): clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel(), _polygon(), _project(), datetime (+13 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management persistence"
Cohesion: 0.12
Nodes (20): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, Optimistic parcel revision transaction, ParcelVersionConflictError, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations (+12 more)

### Community 23 - "knowledge_services.py"
Cohesion: 0.09
Nodes (37): EvidenceItem, RecommendationFactor, build_lexical_retrieval_query(), build_retrieval_query(), build_semantic_retrieval_query(), _choose_boundary(), _contiguous_section_spans(), _cosine_similarity() (+29 more)

### Community 24 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.20
Nodes (10): Common-Support Ranking, ADR-002 Layered Bounded Contexts, ADR-003 Commands and Queries in Application, ADR-005 Background Worker, ADR-007 Initial Deployment, ADR-009 Multicrop Evaluation, Architecture and Backend for CropSuiteLite Huaura v2, Celery (+2 more)

### Community 25 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 26 - "EmbeddingIndex"
Cohesion: 0.07
Nodes (19): CorpusSource, EmbeddingIndex, IngestionReport, IngestionSourceResult, KnowledgeChunk, IEmbeddingProvider, IKnowledgeChunker, IKnowledgeCorpusRepository (+11 more)

### Community 27 - "test_architecture.py"
Cohesion: 0.14
Nodes (18): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+10 more)

### Community 28 - "Farm Management schema ownership"
Cohesion: 0.20
Nodes (10): Farm Management schema ownership, Projects, parcels, and parcel_versions tables, farm_management schema and owned tables, Optional durable repository adapter, Project, Parcel, and ParcelVersion domain model, Result querying increment, Bounded-context ownership and Farm Management repositories, Farm Management ownership query (+2 more)

### Community 29 - "Bounded-context layered structure"
Cohesion: 0.28
Nodes (9): Bounded-context ownership, Anti-corruption layer, Application layer, Bounded-context layered structure, Domain layer, Illustrative Evaluation module structure, Infrastructure layer, Interfaces layer (+1 more)

### Community 30 - "Python and FastAPI backend decision"
Cohesion: 0.22
Nodes (14): Multicrop Parcel Evaluation, run_evaluation Service, ADR-004 CropSuiteLite Port and Adapter, ADR-008 Sequential Crop Execution, Background worker execution, CropSuiteLite isolation boundary, FastAPI, Python (+6 more)

### Community 31 - "AgroclimaticEvaluationExecutionService"
Cohesion: 0.20
Nodes (36): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, Execute requested crops and summarize them through Application-owned ports., _artifact(), _environmental_information_for(), _evaluation(), _execute() (+28 more)

### Community 32 - "Farm Management minimum vertical slice"
Cohesion: 0.13
Nodes (13): ADR-011: PostgreSQL/PostGIS persistence for Farm Management, Consequences, Context, Decision, Status, Architectural alignment, Slice exclusions and authorization dependency, Explicit exclusions and provisional choices (+5 more)

### Community 33 - "Application commands and queries"
Cohesion: 0.29
Nodes (8): Application commands and queries, FastAPI composition root, In-memory and durable Infrastructure adapters, Project and parcel HTTP resources, Farm Management repository abstractions, Transport-to-domain path, ProjectRepository, ParcelRepository, and in-memory adapters, Repository ports and in-memory adapters query

### Community 34 - "cropsuite_adapter.py"
Cohesion: 0.09
Nodes (56): CropLimitationEvidence, CropSuitabilityEngineError, CropSuitabilityExecutionError, IEnvironmentalInputIntegrityVerifier, InvalidEngineOutputError, LimitingFactorEvidence, Application-owned boundary for one crop suitability evaluation., Transport-neutral aggregate for one limiting-factor code. (+48 more)

### Community 35 - "VIA architecture implementation roadmap"
Cohesion: 0.13
Nodes (16): Domain dependency rule, Layered modular monolith, Inward dependency direction, Architecture source and PoC preservation, Cross-stage architecture gates, Explanation and comparison increment, Modeling increment, Modular foundation increment (+8 more)

### Community 36 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.07
Nodes (72): _comparison_request(), Synchronous application orchestration for persisted evaluations., _to_outcome(), CropComparisonInput, One durable crop suitability raster offered to scientific comparison., CommonSupportStatus, StrEnum, Evaluation-level scientific common-support result. (+64 more)

### Community 37 - "test_agronomic_knowledge.py"
Cohesion: 0.10
Nodes (32): ExtractedDocument, ExtractedPage, LexicalSearchHit, RetrievalStatus, VectorSearchCandidate, configured_embedding_index(), DeterministicKnowledgeChunker, Page-aware deterministic chunker using recoverable headings and overlap. (+24 more)

### Community 38 - "ConfiguredEnvironmentalInputIntegrityVerifier"
Cohesion: 0.23
Nodes (22): ConfiguredEnvironmentalInputIntegrityVerifier, Verify manifests using deployment-configured exact dataset-version bindings., _binding(), _fingerprints(), _manifest(), parametrize, Path, ScientificSourceFingerprint (+14 more)

### Community 40 - "Q: PostgreSQL Farm Management repositories"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: PostgreSQL Farm Management repositories, Source Nodes

### Community 41 - "agroclimatic_evaluation/interfaces/http.py"
Cohesion: 0.13
Nodes (29): EvaluationResultAvailability, StrEnum, Whether persisted outcomes are pending, partial, or final., EvaluationStatus, StrEnum, Architecture-approved lifecycle vocabulary., CommonSupportResponse, ComparableCropResponse (+21 more)

### Community 42 - "ADR-012: PostgreSQL/PostGIS persistence for Environmental Information"
Cohesion: 0.12
Nodes (18): ADR-012: PostgreSQL/PostGIS persistence for Environmental Information, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation, Decision Support (+10 more)

### Community 43 - "PostGIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "GetPublishedDatasetVersion"
Cohesion: 0.17
Nodes (21): GetPublishedDatasetVersion, PublishedDatasetVersion, PublishedDatasetVersionReader, Protocol, Stable contracts deliberately published to other bounded contexts., Public cross-context reader for exact immutable dataset versions., FakeEnvironmentalInformation, _published() (+13 more)

### Community 45 - "agroclimatic_evaluation/infrastructure/__init__.py"
Cohesion: 0.20
Nodes (10): CropCatalogEntry, ScientificallyBoundDatasetVersion, FilesystemCropCapabilityCatalog, FilesystemScientificInputBindingCatalog, Path, Read scientific capability metadata without importing the CropSuite engine., Adapter over the exact deployment-selected CropSuite parameter directory., Expose only public dataset identities from deployment bindings. (+2 more)

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

### Community 56 - "Probar la API de VIA con Postman"
Cohesion: 0.09
Nodes (22): 10. Limitaciones, 11. Decision Support: knowledge retrieval, 12. Decision Support: recommendation, 1. Health, 2. Login, 3. Requests autenticadas, 4. Usuario autenticado, 5. Projects y Parcels (+14 more)

### Community 59 - "Atlas A Logo"
Cohesion: 0.67
Nodes (3): Atlas A Logo, Atlas Branding, Stylized Green Letter A

### Community 63 - "decision_support/infrastructure/postgresql_repositories.py"
Cohesion: 0.08
Nodes (40): KnowledgeDocument, KnowledgeDocumentStatus, StrEnum, RecommendationRun, RecommendationStatus, StoredChunk, Base, DeclarativeBase (+32 more)

### Community 64 - "DomainValidationError"
Cohesion: 0.06
Nodes (47): _to_common_support(), _to_comparable_crop(), CommonSupport, ComparableCrop, normalize_common_support_measurements(), One crop ranked on the exact common valid spatial support., Normalize impossible boundary overshoots caused only by float noise., Validate deterministic scientific ranking semantics. (+39 more)

### Community 65 - "EnvironmentalInputManifest"
Cohesion: 0.18
Nodes (24): EnvironmentalInputManifest, Immutable set of exact environmental inputs resolved for an evaluation., parametrize, Focused domain tests for immutable environmental input manifests., _snapshot(), test_environmental_input_manifest_accepts_valid_inputs(), test_environmental_input_manifest_allows_same_version_for_distinct_input_keys(), test_environmental_input_manifest_rejects_duplicate_input_key() (+16 more)

### Community 67 - "Dataset"
Cohesion: 0.11
Nodes (12): Dataset, Stable logical identity for a geoenvironmental dataset., DatasetRepository, DatasetVersionRepository, Protocol, UUID, DatasetRecord, _dataset_from_record() (+4 more)

### Community 68 - "legacy_ownership_admin.py"
Cohesion: 0.08
Nodes (29): _build_parser(), LegacyOwnershipAssignment, LegacyOwnershipError, LegacyOwnershipReport, main(), PostgreSQLLegacyOwnershipStore, ArgumentParser, Engine (+21 more)

### Community 69 - "test_agronomic_knowledge_postgresql.py"
Cohesion: 0.32
Nodes (13): _chunk(), clean_knowledge_tables(), database(), _index(), Engine, fixture, SessionFactory, PostgreSQL integration coverage for agronomic knowledge RAG persistence. (+5 more)

### Community 70 - "RetrievedKnowledge"
Cohesion: 0.11
Nodes (18): RecommendationContext, RecommendationGeneration, RetrievedKnowledge, IDocumentTextExtractor, IKnowledgeRetriever, IRecommendationGenerator, IRecommendationRepository, IStoredChunkReader (+10 more)

### Community 72 - "test_agronomic_knowledge_http.py"
Cohesion: 0.24
Nodes (13): _client(), _FailingFinalizedReader, _Owned, Exception, TestClient, HTTP contract tests for agronomic knowledge and recommendations., _Service, test_get_knowledge_retrieves_evidence_without_generation() (+5 more)

### Community 73 - "EnvironmentalInformationService"
Cohesion: 0.06
Nodes (63): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort, GetDataset (+55 more)

### Community 74 - "test_api_host.py"
Cohesion: 0.14
Nodes (19): ApiServerSettings, main(), Production HTTP process host for VIA., Provider-neutral Uvicorn bind settings for the production API process., Load API bind settings from the process environment., Validate production configuration and run one Uvicorn API process., _clear_api_environment(), _configure_production_persistence() (+11 more)

### Community 75 - "DatasetVersion"
Cohesion: 0.07
Nodes (38): InvalidSpatialInputError, CoverageComputation, RuntimeError, ValueError, Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, DatasetVersionConflictError (+30 more)

### Community 77 - "Q: ParcelVersion persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ParcelVersion persistence, Source Nodes

### Community 79 - "identity_access/application/service.py"
Cohesion: 0.10
Nodes (26): AuthenticationError, IdentityUserNotFoundError, LookupError, RuntimeError, Application-level Identity Access failures., Raised when an administrative user reference cannot be resolved., Raised when supplied authentication material is not valid., Identity Access application layer. (+18 more)

### Community 80 - "User"
Cohesion: 0.08
Nodes (26): IdentityValidationError, ValueError, Identity Access domain errors., Raised when an Identity Access domain object is invalid., Identity Access domain., normalize_email(), datetime, Identity Access domain models. (+18 more)

### Community 81 - "PostgreSQLUserRepository"
Cohesion: 0.21
Nodes (19): PostgreSQLUserRepository, SessionFactory, clean_identity_access(), database(), datetime, Engine, fixture, SessionFactory (+11 more)

### Community 83 - "app.py"
Cohesion: 0.05
Nodes (54): create_app(), _FarmAuthorizedParcelSnapshotProvider, FastAPI, UUID, Side-effect-free FastAPI application composition., Composition adapter from Farm's public DTO to Evaluation's owned snapshot., Build the VIA API and register its technical interfaces., Deliberately small public contract exported by Identity Access. (+46 more)

### Community 93 - "Q: Domain-to-Infrastructure dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Domain-to-Infrastructure dependency violations, Source Nodes

### Community 135 - "scientific_input_integrity.py"
Cohesion: 0.14
Nodes (17): EnvironmentalInputIntegrityError, Raised when resolved environmental provenance does not match scientific inputs., CropSuiteEnvironmentalInputBinding, load_configured_environmental_input_integrity_verifier(), load_cropsuite_environmental_input_bindings(), _parse_uuid(), Any, Path (+9 more)

### Community 136 - "Huaura scientific fixture recovery audit"
Cohesion: 0.08
Nodes (25): Benchmark compatibility, Boundary and reference mask, Climate, Current identity manifest, DEM, Executive status, Historical alternatives / abandoned paths, Huaura scientific fixture recovery audit (+17 more)

### Community 137 - "Project"
Cohesion: 0.08
Nodes (14): Project, An agricultural project that groups parcels., ParcelRepository, ProjectRepository, Protocol, UUID, Repository abstractions for Farm Management aggregates., PostgreSQLProjectRepository (+6 more)

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

### Community 150 - "FilesystemScientificArtifactStore"
Cohesion: 0.11
Nodes (34): _file_identity(), FilesystemScientificArtifactStore, _is_within(), PublishedScientificArtifact, Path, Protocol, RuntimeError, Durable filesystem storage for scientific artifacts. (+26 more)

### Community 151 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.19
Nodes (20): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+12 more)

### Community 152 - "AuthSession"
Cohesion: 0.09
Nodes (26): IdentityConflictError, RuntimeError, Raised when identity persistence would violate an existing identity., AuthSession, Base, DeclarativeBase, SQLAlchemy metadata owned by Identity Access Infrastructure., Declarative base for Identity Access persistence records. (+18 more)

### Community 154 - "Production deployment runtime contract"
Cohesion: 0.10
Nodes (19): B2 reproducible Linux container image, B6.1 resource benchmark, B6 production-like Docker Compose smoke, B7 DigitalOcean single-Droplet deployment definition, Database and migration contract, Environment contract, Filesystem contract, Process responsibilities (+11 more)

### Community 155 - "test_frontend_openapi.py"
Cohesion: 0.30
Nodes (13): _Engine, Any, OpenAPI contracts consumed by the frontend handoff., _schema(), _Sessions, test_all_live_functional_routes_publish_bearer_security(), test_committed_openapi_matches_live_non_production_schema(), test_decision_support_responses_publish_real_schemas() (+5 more)

### Community 157 - "Settings"
Cohesion: 0.09
Nodes (37): create_production_app(), Build the production API after enforcing durable persistence settings., Require the durable persistence contract used by the production API., Settings needed by the current backend composition root., Settings, MonkeyPatch, parametrize, test_auth_cookie_samesite_environment_rejects_unknown_value() (+29 more)

### Community 158 - "knowledge_models.py"
Cohesion: 0.11
Nodes (22): EmbeddingBatch, EmbeddingVector, Provider-neutral models for agronomic knowledge retrieval and recommendations., RecommendationItem, StructuredRecommendation, KnowledgeProviderUnavailableError, RuntimeError, External provider required by the knowledge use case is unavailable. (+14 more)

### Community 159 - "CropSuite.py"
Cohesion: 0.09
Nodes (25): # NOTE: self.extent is modified here to align with grid, calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):… (+17 more)

### Community 160 - "test_decision_support.py"
Cohesion: 0.10
Nodes (46): FinalizedCommonSupport, FinalizedCommonSupportStatus, FinalizedComparableCrop, FinalizedEvaluationResult, Select either VIA's current default policy or an explicit custom snapshot., ViabilityPolicySelection, ComparableCropEvidence, A provider-produced crop mean and rank over common valid support. (+38 more)

### Community 161 - ".from_geojson"
Cohesion: 0.21
Nodes (16): _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing, MultiPolygonCoordinates, PolygonCoordinates (+8 more)

### Community 162 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.06
Nodes (67): CapabilityStatus, CropEvaluationCapability, EnvironmentalInputCapability, EvaluationCapabilities, EvaluationCapabilitiesService, EvaluationCapabilitiesUnavailableError, ICropCapabilityCatalog, IScientificInputBindingCatalog (+59 more)

### Community 163 - "test_evaluation_capabilities_api.py"
Cohesion: 0.37
Nodes (12): _bindings(), _catalog(), _client(), Path, TestClient, HTTP discovery of deployment-selected scientific capabilities., test_capabilities_do_not_expose_private_binding_details(), test_capabilities_publish_configured_crops_scenarios_and_bindings() (+4 more)

### Community 164 - "Agroclimatic Evaluation request, worker, recovery, and read slice"
Cohesion: 0.15
Nodes (11): ADR-015: PostgreSQL polling for Agroclimatic Evaluation worker dispatch, Consequences, Context, Decision, Status, Agroclimatic Evaluation request, worker, recovery, and read slice, Current lifecycle and execution, Deliberately deferred (+3 more)

### Community 165 - "Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation, Source Nodes

### Community 166 - "Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors, Source Nodes

### Community 170 - "CropSuiteComparisonAdapter"
Cohesion: 0.22
Nodes (22): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., create_worker(), Compose the production worker and fail fast on missing scientific settings., Path, test_create_worker_fails_fast_on_invalid_scientific_input_bindings(), _artifact(), Any (+14 more)

### Community 172 - "SpatialExtent"
Cohesion: 0.13
Nodes (23): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine (+15 more)

### Community 174 - "CropSuitabilityResult"
Cohesion: 0.13
Nodes (8): datetime, CropSuitabilityResult, ICropSuitabilityEngine, One checked per-crop outcome from the scientific boundary., Evaluate one crop without exposing engine process or filesystem details., Exception, Exception, __init__()

### Community 175 - "Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment., Source Nodes

### Community 176 - "env.py"
Cohesion: 0.47
Nodes (5): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online()

### Community 177 - "PolicyReference"
Cohesion: 0.09
Nodes (36): DefaultViabilityPolicyConflictError, DefaultViabilityPolicyNotConfiguredError, InvalidViabilityPolicyRevisionError, LookupError, RuntimeError, ValueError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist. (+28 more)

### Community 178 - "config.py"
Cohesion: 0.24
Nodes (10): _environment_boolean(), _environment_csv(), _environment_float(), _environment_integer(), _is_same_or_within(), _optional_path(), _optional_path_alias(), Path (+2 more)

### Community 180 - "DomainValidationError"
Cohesion: 0.11
Nodes (29): Application ports for Environmental Information spatial collaboration., CoverageGeometry, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing (+21 more)

### Community 181 - "Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract, Source Nodes

### Community 182 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.06
Nodes (60): EnvironmentalInputReferenceInput, ParcelReferenceInput, Commands expressing Agroclimatic Evaluation use-case intent., Minimum Farm Management reference supplied by an authenticated caller., RequestEvaluation, Agroclimatic Evaluation application layer., AuthorizedParcelSnapshotNotFoundError, LookupError (+52 more)

### Community 183 - "test_decision_support_postgresql.py"
Cohesion: 0.14
Nodes (33): PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., Read and validate the test-only database settings before any DB operation., require_test_database_url(), clean_policy_versions() (+25 more)

### Community 184 - "test_ia4_quota.py"
Cohesion: 0.20
Nodes (13): _context(), _Generator, MonkeyPatch, _recommendation(), _retrieved(), _Retriever, test_openai_responses_adapter_uses_strict_schema_and_no_tools(), test_recommendation_cache_key_changes_with_prompt_version() (+5 more)

### Community 185 - "test_environmental_information_api.py"
Cohesion: 0.27
Nodes (14): _dataset_body(), Any, Response, End-to-end API tests for Environmental Information., _request(), _test_app(), test_dataset_and_version_lifecycle(), scenario() (+6 more)

### Community 187 - "verify_runtime"
Cohesion: 0.36
Nodes (10): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_read_only_directory(), _require_read_only_file(), _require_writable_directory(), _run_cropsuite_import_smoke() (+2 more)

### Community 188 - "decision_support/infrastructure/__init__.py"
Cohesion: 0.18
Nodes (20): CorpusManifest, Decision Support infrastructure adapters., load_taxonomy(), _load_yaml_mapping(), ManifestValidationError, _optional_string(), _parse_source(), Any (+12 more)

### Community 189 - "test_farm_management_api.py"
Cohesion: 0.16
Nodes (19): Farm Management interface layer., _AllowAllAreaOfInterest, _polygon(), Any, Response, End-to-end API tests for the Farm Management vertical slice., _request(), _test_app() (+11 more)

### Community 191 - "benchmark_production_runtime.sh"
Cohesion: 0.19
Nodes (16): artifact_bytes_for_evaluation(), COMPOSE_PROJECT_NAME, database_size_bytes(), fail(), monotonic_ns(), post_json(), record_stack_sample(), require_command() (+8 more)

### Community 192 - "test_authentication.py"
Cohesion: 0.10
Nodes (12): _Clock, _Harness, _http_client(), _PasswordHasher, datetime, TestClient, test_auth_openapi_exposes_bearer_only_for_me(), test_http_login_failures_do_not_reveal_account_existence() (+4 more)

### Community 193 - "InMemoryEvaluationRepository"
Cohesion: 0.11
Nodes (45): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application., InMemoryEvaluationRepository, _artifact(), _engine_result(), _evaluation() (+37 more)

### Community 195 - "test_digitalocean_deployment_contract.py"
Cohesion: 0.36
Nodes (9): _read(), _service_block(), test_deployment_script_enforces_release_order_without_destructive_cleanup(), test_deployment_script_requires_stable_worker_liveness_across_poll_intervals(), test_digitalocean_compose_preserves_runtime_and_durability_contracts(), test_docker_build_context_excludes_scientific_data(), test_ghcr_publish_is_gated_by_successful_b2_b6_run_for_same_commit(), test_provider_files_do_not_embed_secrets_or_raw_huaura_paths() (+1 more)

### Community 196 - "deploy_digitalocean.sh"
Cohesion: 0.57
Nodes (7): fail(), require_command(), require_directory(), deploy_digitalocean.sh script, verify_worker_liveness(), VIA_IMAGE, wait_for_health()

### Community 197 - "verify_production_compose.sh"
Cohesion: 0.60
Nodes (4): assert_running(), assert_worker_liveness(), container_id(), verify_production_compose.sh script

### Community 198 - "Frontend integration flows"
Cohesion: 0.20
Nodes (9): 1. Establish and restore the session, 2. Bootstrap the functional UI, 3. Create or select a parcel version, 4. Select environmental dataset versions, 5. Queue an evaluation, 6. Render results while work progresses, 7. Render scientific evidence and limitations, 8. Retrieve knowledge and recommendations (+1 more)

### Community 199 - "downscaling.py"
Cohesion: 0.12
Nodes (18): Interpolates or retrieves downscaled climate data (precipitation and…, extract_domain_from_global_3draster(), get_cpu_ram(), get_resolution_array(), Extracts a specific domain from a global 3D raster dataset. Parameters: -…, Get information about the CPU and available RAM. Returns: list: A list…, _create_interpolation_folders(), interpolate_precipitation() (+10 more)

### Community 201 - "database_test_support.py"
Cohesion: 0.22
Nodes (14): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., UnsafeTestDatabaseError, validate_test_database_url(), CaptureFixture, parametrize (+6 more)

### Community 205 - "Evaluation"
Cohesion: 0.06
Nodes (20): EnvironmentalInputResolutionError, Exception, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved., Logger, Logger, EvaluationConflictError, InvalidEvaluationTransitionError (+12 more)

### Community 206 - "via_backend/worker.py"
Cohesion: 0.07
Nodes (32): WorkerRunSummary, main(), make_shutdown_handler(), _parser(), _positive_integer(), _print_active_evaluations(), ArgumentParser, Logger (+24 more)

### Community 207 - "test_cors.py"
Cohesion: 0.39
Nodes (7): _client(), TestClient, Environment-configured development CORS behavior., test_allowed_origin_is_echoed(), test_allowed_preflight_supports_frontend_method_and_headers(), test_disallowed_origin_receives_no_cors_permission(), test_empty_configuration_preserves_no_cors_behavior()

### Community 208 - "Scientific result semantics"
Cohesion: 0.25
Nodes (7): Coverage and no-data, Cross-crop ranking, Limiting factors, Scientific result semantics, Scientific trace, Suitability scale, Water regimes

### Community 209 - "generate_frontend_openapi.py"
Cohesion: 0.47
Nodes (4): _Engine, main(), Generate the frontend OpenAPI snapshot without external service calls., _Sessions

### Community 210 - "test_limiting_factor_domain.py"
Cohesion: 0.33
Nodes (7): _factor(), LimitingFactorEvidence, parametrize, Focused domain invariants for deterministic limiting-factor evidence., test_available_limitation_evidence_accepts_traceable_factor(), test_limiting_factor_rejects_invalid_affected_cells(), test_limiting_factor_rejects_non_integer_raw_code()

### Community 211 - "health.py"
Cohesion: 0.40
Nodes (4): health(), Host-level health endpoint., Report that the API process is ready to receive requests., get

### Community 212 - "cropsuite_comparison_adapter.py"
Cohesion: 0.10
Nodes (35): CommonSupportResult, CommonSupportStatus, ComparableCropResult, CropComparisonEngineError, CropComparisonExecutionError, CropComparisonRequest, CropComparisonResult, ICropComparisonEngine (+27 more)

### Community 213 - "Frontend API reference"
Cohesion: 0.33
Nodes (5): Authentication and authorization, Capability discovery, Decision Support request shapes, Evaluation request, Frontend API reference

### Community 214 - "read_models.py"
Cohesion: 0.20
Nodes (13): _availability(), CommonSupportReadResult, ComparableCropReadResult, CropEvidenceResult, CropLimitationResult, LimitationEvidenceResult, LimitingFactorResult, PersistedCropOutcomeResult (+5 more)

### Community 216 - "Asynchronous evaluations"
Cohesion: 0.40
Nodes (4): Asynchronous evaluations, Lifecycle, Polling behavior, Result availability is separate from lifecycle

### Community 217 - "nc_tools.py"
Cohesion: 0.22
Nodes (12): create_cog_from_geotiff(), geotiff_to_smallest_datatype(), Convert image to COG., merge_outputs_no_overlap(), get_netcdf_extent(), merge_netcdf_files(), downscaled_files: list of netcdf files overlap: In Degree extent: [North, Left,…, Get the spatial extent (min and max) of the latitude and longitude in a NetCDF… (+4 more)

### Community 218 - "Frontend development setup"
Cohesion: 0.40
Nodes (4): Backend origin, Frontend development setup, OpenAPI, Smoke scripts

### Community 220 - "Sample data"
Cohesion: 0.40
Nodes (4): Evaluation request, Final result, Polling response, Sample data

### Community 223 - "Error handling"
Cohesion: 0.50
Nodes (3): Capabilities 503, Decision Support 503, Error handling

### Community 224 - "VIA frontend handoff"
Cohesion: 0.40
Nodes (4): Authentication bootstrap, Base URL and route prefixes, Frontend rules that should be treated as invariants, VIA frontend handoff

### Community 229 - "create_database"
Cohesion: 0.07
Nodes (34): PasswordPolicyError, ValueError, Raised when an administratively supplied password violates policy., datetime, Clock adapter for Identity Access., SystemClock, Argon2PasswordHasher, Hash passwords with Argon2id through pwdlib. (+26 more)

### Community 230 - "ViabilityPolicySnapshot"
Cohesion: 0.15
Nodes (6): Immutable identity and exact thresholds used for a policy execution., ViabilityPolicySnapshot, One immutable persisted viability-policy configuration., ViabilityPolicyVersionRecord, _snapshot_from_record(), _InMemoryViabilityPolicyRepository

### Community 231 - "test_identity_access.py"
Cohesion: 0.13
Nodes (22): Security primitive adapters for Identity Access., Generate URL-safe opaque tokens with 256 bits of entropy., Create the deterministic digest persisted for an opaque token., SecretsOpaqueTokenGenerator, Sha256TokenHasher, parametrize, _session(), test_argon2id_hashing_is_salted_and_verifiable() (+14 more)

### Community 232 - "test_ia5_release_security.py"
Cohesion: 0.21
Nodes (15): _decision_support_client(), _inside_geometry(), _login(), _Owned, Any, parametrize, TestClient, UUID (+7 more)

### Community 233 - "test_environmental_information_postgresql.py"
Cohesion: 0.27
Nodes (13): Shared technical infrastructure used by the application composition root., clean_environmental_information(), database(), _database_url(), _dataset(), Engine, fixture, SessionFactory (+5 more)

### Community 234 - "smoke_production_api.py"
Cohesion: 0.19
Nodes (16): ApiClient, _assert_safe_base_url(), _choose_capability(), _credentials(), _load_geometry(), main(), _parser(), Any (+8 more)

### Community 235 - "QuotaExceededError"
Cohesion: 0.20
Nodes (13): QuotaExceededError, Request burst protection shared by HTTP adapters; no worker dependency., SessionFactory, PostgreSQL quota transactions; skipped when VIA_TEST_DATABASE_URL is absent., test_evaluation_quota_is_owner_scoped_and_atomic(), test_recommendation_ledger_is_owner_scoped_durable_and_atomic(), test_simultaneous_evaluation_posts_admit_only_one(), attempt() (+5 more)

### Community 236 - "test_production_compose_contract.py"
Cohesion: 0.31
Nodes (6): _mapping_keys(), Static invariants for the provider-neutral B6 production-like Compose smoke., _service_block(), test_b6_compose_encodes_release_ordering_and_runtime_mount_semantics(), test_b6_compose_has_exact_process_topology_and_same_image_contract(), test_b6_worker_bindings_fixture_is_valid_for_startup()

### Community 237 - "decision_support/interfaces/http.py"
Cohesion: 0.22
Nodes (15): _build_context(), create_router(), authorize(), generate_recommendation(), get_knowledge(), list_recommendations(), throttle(), APIRouter (+7 more)

### Community 238 - "run_cropsuitelite.py"
Cohesion: 0.19
Nodes (15): change_otherst_parameters(), change_st1_parameter(), create_crop_parameters(), create_crop_suite_configuration_file(), find_solution_type(), main(), modify_extent(), modify_general_files() (+7 more)

### Community 239 - "WaterRegime"
Cohesion: 0.18
Nodes (11): Published water-regime values shared with consumer bounded contexts., WaterRegime, KnowledgeContextConflictError, KnowledgeContextUnavailableError, LookupError, Raised when the finalized scientific result cannot form a scenario context., Raised when an existing evaluation does not yet have finalized evidence., _Builder (+3 more)

### Community 241 - "aoi.py"
Cohesion: 0.24
Nodes (11): AreaOfInterestProvenance, HuauraAreaOfInterestValidator, _load_boundary(), _load_json(), _load_provenance(), Any, Path, Authoritative Huaura area-of-interest validation. (+3 more)

### Community 242 - "ParcelSnapshot"
Cohesion: 0.09
Nodes (21): ParcelSnapshot, The exact Farm Management parcel state accepted for an evaluation., _SnapshotProvider, _evaluation(), _outcome(), parametrize, Focused Application query tests for Agroclimatic Evaluation., _service() (+13 more)

### Community 243 - "test_ia5_huaura_aoi.py"
Cohesion: 0.27
Nodes (12): _authenticated_client(), _authoritative_boundary(), _geojson(), _inside_parcels(), Any, Path, TestClient, IA-5 public-release Huaura AOI enforcement. (+4 more)

### Community 244 - "Scripts de VIA"
Cohesion: 0.12
Nodes (15): `backup_postgres.sh`, Benchmark, `benchmark_production_runtime.sh`, `deploy_digitalocean.sh` / `deploy_digitalocean.ps1`, Descarga de datos, Diagnóstico y validación científica, Operación y despliegue, Preparación científica (+7 more)

### Community 245 - "agroclimatic_evaluation/application/public.py"
Cohesion: 0.10
Nodes (25): FinalizedCropLimitationEvidence, FinalizedCropOutcome, FinalizedCropOutcomeStatus, FinalizedEvaluationNotFoundError, FinalizedEvaluationNotReadyError, FinalizedEvaluationResultReader, FinalizedLimitationEvidenceAvailability, FinalizedLimitingFactorEvidence (+17 more)

### Community 246 - "Navegación"
Cohesion: 0.14
Nodes (13): `adr/`, `architecture/`, Documentación de VIA, `frontend/`, `implementation/`, Knowledge base, Knowledge graph para agentes, Motor científico (+5 more)

### Community 248 - "Route and security matrix"
Cohesion: 0.50
Nodes (3): Production-only surface, Route and security matrix, Status semantics

### Community 251 - "WorkerSettings"
Cohesion: 0.24
Nodes (11): Settings for the PostgreSQL polling worker process., WorkerSettings, parametrize, Path, _scientific_worker_settings(), test_worker_run_requires_durable_artifact_root(), test_worker_run_requires_scientific_input_bindings(), test_worker_run_requires_scientific_paths() (+3 more)

### Community 252 - "migrate.py"
Cohesion: 0.23
Nodes (11): _build_parser(), ArgumentParser, Path, One-shot production schema migration host for VIA releases., Return the repository-local Alembic config when running from source., Resolve the Alembic config without depending on the process cwd., Validate production persistence and migrate the schema to Alembic head., _require_production_postgresql() (+3 more)

### Community 253 - "Contribuir a VIA"
Cohesion: 0.17
Nodes (11): Arquitectura del backend, Cambios científicos, Commits, Contribuir a VIA, Docker y producción, Documentación, Flujo de trabajo, Migraciones de base de datos (+3 more)

### Community 254 - "factor_display_label"
Cohesion: 0.24
Nodes (6): factor_display_label(), Human-readable labels for stable agroclimatic factor codes., Return the Spanish display label while preserving raw labels as fallback., parametrize, test_factor_display_label_preserves_raw_label_for_unmapped_factor(), test_factor_display_label_uses_spanish_application_labels()

### Community 255 - "knowledge.py"
Cohesion: 0.27
Nodes (8): _DryRunRepository, main(), _parser(), ArgumentParser, Namespace, Administrative CLI for the VIA agronomic knowledge corpus., Fail loudly if a dry run ever tries to touch persistence., _run_ingest()

### Community 256 - "[Unreleased]"
Cohesion: 0.29
Nodes (6): Added, Changed, Changelog, Convención de versiones, Removed, [Unreleased]

### Community 257 - "AuthorizedParcelSnapshotProvider"
Cohesion: 0.40
Nodes (4): AuthorizedParcelSnapshotProvider, Protocol, UUID, Application-owned port for authoritative Farm parcel snapshots.

### Community 258 - "ScientificArtifactRole"
Cohesion: 0.67
Nodes (3): StrEnum, Scientific artifact roles understood by VIA., ScientificArtifactRole

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **317 isolated node(s):** `via-backend`, `backup_postgres.sh script`, `VIA_IMAGE`, `VIA_BENCHMARK_SOURCE_DIR`, `VIA_BENCHMARK_RUNTIME_CONFIG_DIR` (+312 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1375 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `Domain dependency rule` (6× useful, score=4.999685072)
- `Application layer` (4× useful, score=3.294315216)
- `EnvironmentalInformationService` (3× useful, score=2.489686793)
- `ParcelGeometry` (3× useful, score=2.483185308)
- `ParcelVersion` (3× useful, score=2.462532158) _(code changed — re-verify)_
- `InMemoryParcelRepository` (3× useful, score=2.461439615) _(code changed — re-verify)_
- `ParcelRepository` (3× useful, score=2.461439613) _(code changed — re-verify)_
- `EvaluationResult` (2× useful, score=1.716801747)
- `Settings` (2× useful, score=1.711176597) _(code changed — re-verify)_
- `Farm Management schema ownership` (2× useful, score=1.676754129)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Crop Code Catalog` and `Undefined Crop Code c32`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `create_app()` connect `app.py` to `FarmManagementService`, `Parcel`, `Project`, `PostgreSQLEvaluationRepository`, `AuthSession`, `EmbeddingIndex`, `test_frontend_openapi.py`, `Settings`, `knowledge_models.py`, `test_agroclimatic_evaluation_api.py`, `test_evaluation_capabilities_api.py`, `test_agronomic_knowledge.py`, `agroclimatic_evaluation/infrastructure/__init__.py`, `agroclimatic_evaluation/application/__init__.py`, `test_environmental_information_api.py`, `decision_support/infrastructure/__init__.py`, `decision_support/infrastructure/postgresql_repositories.py`, `test_authentication.py`, `InMemoryEvaluationRepository`, `Dataset`, `RetrievedKnowledge`, `EnvironmentalInformationService`, `DatasetVersion`, `identity_access/application/service.py`, `User`, `PostgreSQLUserRepository`, `test_cors.py`, `generate_frontend_openapi.py`, `create_database`, `test_identity_access.py`, `test_ia5_release_security.py`, `decision_support/interfaces/http.py`, `aoi.py`, `test_ia5_huaura_aoi.py`, `agroclimatic_evaluation/application/public.py`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `AgroclimaticEvaluationService` connect `agroclimatic_evaluation/application/__init__.py` to `test_decision_support.py`, `AuthorizedParcelSnapshotProvider`, `DomainValidationError`, `test_agroclimatic_evaluation_api.py`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `agroclimatic_evaluation/interfaces/http.py`, `Evaluation`, `WaterRegime`, `ParcelSnapshot`, `app.py`, `decision_support/application/service.py`, `agroclimatic_evaluation/application/public.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `Dataset`, `CropSuiteComparisonAdapter`, `DatasetVersion`, `GetPublishedDatasetVersion`, `SpatialExtent`, `via_backend/worker.py`, `CoverageMeasurement`, `app.py`, `DomainValidationError`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 37 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 37 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Settings`) actually correct?**
  _`create_app()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 27 INFERRED edges - model-reasoned connections that need verification._