# Graph Report - poc_via_cslite  (2026-10-01)

## Corpus Check
- 423 files · ~233,269 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4644 nodes · 12079 edges · 270 communities (175 shown, 33 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 1603 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `24eb6aaf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FarmManagementService
- run_cropsuitelite.py
- NexGenPreProcessing
- Huaura Dataset Preprocessing Configuration
- check_files.py
- ViabilityPolicySnapshot
- ParcelGeometry
- Crop Membership Functions
- multicrop.py
- decision_support/domain/models.py
- CropSuite.py
- DownloadCMIP6Data
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- climate_suitability_main_xarray.py
- CropSuiteLite
- test_migration_host.py
- climate_suitability_main.py
- cropsuite_adapter.py
- CoverageMeasurement
- agroclimatic_evaluation/infrastructure/__init__.py
- test_farm_management_postgresql.py
- VIA architecture guardrails
- Farm Management persistence
- knowledge_services.py
- Architecture and Backend for CropSuiteLite Huaura v2
- Huaura Environmental Correction
- knowledge_models.py
- test_architecture.py
- Farm Management schema ownership
- Bounded-context layered structure
- Python and FastAPI backend decision
- AgroclimaticEvaluationExecutionService
- Farm Management minimum vertical slice
- Application commands and queries
- scientific_source_store.py
- VIA architecture implementation roadmap
- DomainValidationError
- DecisionSupportService
- agroclimatic_evaluation/application/ports.py
- Q: PostgreSQL Farm Management repositories
- WaterRegime
- ADR-012: PostgreSQL/PostGIS persistence for Environmental Information
- PostGIS service
- GetPublishedDatasetVersion
- capabilities.py
- Q: Verify that the new VIA backend foundation is discoverable and consistent with the intended architecture.
- Q: optimistic stale-write handling introduced in the current slice
- Q: repository ports and current in-memory adapters
- Q: Farm Management ownership and persistence boundaries
- Q: dependency direction involving Domain, Application and Infrastructure
- Q: Project, Parcel, ParcelVersion, ParcelGeometry
- Q: Continue the Farm Management durable persistence increment from the current repository state
- create_router
- CropSuiteLite Python Dependency Manifest
- download_soilgrids_huaura.py
- Probar la API de VIA con Postman
- __main__.py
- Atlas A Logo
- read_remote_chunk
- decision_support/infrastructure/postgresql_repositories.py
- Evaluation
- test_decision_support.py
- agroclimatic_evaluation/__init__.py
- policy_http.py
- legacy_ownership_admin.py
- EvaluationStatus
- RetrievedKnowledge
- decision_support/__init__.py
- test_agronomic_knowledge_http.py
- EnvironmentalInformationService
- farm_management/infrastructure/postgresql_repositories.py
- DatasetVersion
- environmental_information/__init__.py
- Q: ParcelVersion persistence
- farm_management/__init__.py
- identity_access/application/service.py
- User
- PostgreSQLUserRepository
- identity_access/__init__.py
- Parcel
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
- test_retrieval_and_recommendation_traces_persist_closed_citations
- Huaura scientific fixture recovery audit
- AuthSession
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
- IAuthSessionRepository
- VIA production release, migration, and rollback runbook
- test_frontend_openapi.py
- test_config.py
- identity_access/interfaces/http.py
- read_crop_parameterizations_files
- test_agroclimatic_environmental_inputs.py
- test_environmental_information_postgresql.py
- test_agroclimatic_evaluation_api.py
- test_evaluation_capabilities_api.py
- Agroclimatic Evaluation request, worker, recovery, and read slice
- Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation
- Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors
- Dataset
- SpatialExtent
- require_test_database_url
- Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment.
- generate_frontend_openapi.py
- PolicyReference
- config.py
- DomainValidationError
- Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract
- test_decision_support_postgresql.py
- test_agroclimatic_evaluation_worker.py
- crop_rotation.py
- verify_runtime
- decision_support/infrastructure/__init__.py
- create_database
- benchmark_production_runtime.sh
- test_authentication.py
- test_api_host.py
- test_container_image_contract.py
- test_digitalocean_deployment_contract.py
- deploy_digitalocean.sh
- verify_production_compose.sh
- Frontend integration flows
- process_precday_interp
- test_resource_benchmark_contract.py
- via_backend/worker.py
- backup_postgres.sh
- ScientificSourceMaterializer
- main
- test_viability_policy_migration.py
- Scientific result semantics
- test_hybrid_deployment_contract.py
- test_limiting_factor_domain.py
- decision-support-viability-policy.md
- _KnowledgeRepository
- Frontend API reference
- EnvironmentalInputSnapshot
- Asynchronous evaluations
- ADR-016: Hybrid managed control plane and dedicated scientific worker
- Frontend development setup
- resources/__init__.py
- Sample data
- knowledge/__init__.py
- Error handling
- VIA frontend handoff
- README.md
- check_get
- known-gaps.md
- identity_admin.py
- test_identity_access.py
- test_agronomic_knowledge.py
- AgroclimaticEvaluationRecoveryService
- smoke_production_api.py
- openai_knowledge.py
- test_production_compose_contract.py
- Settings
- app.py
- agroclimatic_evaluation/application/__init__.py
- _Service
- AreaOfInterestProvenance
- test_ia4_authorization.py
- test_ia5_huaura_aoi.py
- Scripts de VIA
- ParcelSnapshot
- Navegación
- test_ia5_release_artifacts.py
- Route and security matrix
- S3CompatibleClient
- RecommendationContextBuilder
- Contribuir a VIA
- Colección Postman de VIA
- InMemoryEvaluationRepository
- [0.1.0] - 2026-09-22
- EnvironmentalInputManifest
- VIA.postman_environment.json
- ParcelAreaOfInterestValidator
- test_cors.py
- test_parcel_metadata_migration.py
- create_router
- FixedWindowLimiter
- Q: Te parece bien la ui? tipos no hay dichos tecnicos qeu no se entiendan o información de más, etc. Qué te parece?
- env.py
- SystemClock
- decision_support/interfaces/__init__.py

## God Nodes (most connected - your core abstractions)
1. `Evaluation` - 108 edges
2. `create_app()` - 93 edges
3. `ViabilityPolicySnapshot` - 74 edges
4. `PolicyReference` - 71 edges
5. `DomainValidationError` - 70 edges
6. `Settings` - 69 edges
7. `WaterRegime` - 65 edges
8. `PostgreSQLEvaluationRepository` - 63 edges
9. `AgroclimaticEvaluationService` - 55 edges
10. `InMemoryEvaluationRepository` - 54 edges

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

## Communities (270 total, 33 thin omitted)

### Community 0 - "FarmManagementService"
Cohesion: 0.06
Nodes (70): CreateParcel, CreateProject, DeleteParcel, Commands expressing Farm Management use-case intent., ReviseParcelGeometry, UpdateParcelMetadata, Farm Management application layer., AuthorizedParcelGeometry (+62 more)

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
Nodes (40): calculate_area(), check_all_inputs(), check_climate_data(), check_soil(), check_within_one(), get_geotiff_datatype(), get_geotiff_extent(), get_geotiff_resolution() (+32 more)

### Community 5 - "ViabilityPolicySnapshot"
Cohesion: 0.06
Nodes (32): DefaultViabilityPolicyService, EvaluationPolicyBindingStore, Protocol, UUID, None means legacy policy not recorded; never substitute today's default., DefaultViabilityPolicyConflictError, DefaultViabilityPolicyNotConfiguredError, EvaluationPolicyBindingConflictError (+24 more)

### Community 6 - "ParcelGeometry"
Cohesion: 0.07
Nodes (40): Application ports owned by Farm Management., DomainValidationError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., ParcelGeometry, _parse_multi_polygon(), _parse_polygon() (+32 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.08
Nodes (22): main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry(), Isolated, selected-crop evaluations and area-weighted parcel comparisons. The… (+14 more)

### Community 9 - "decision_support/domain/models.py"
Cohesion: 0.10
Nodes (33): Decision Support evidence translation and policy coordination., _translate_common_support(), _translate_evidence(), DomainValidationError, ValueError, Domain errors raised by Decision Support invariants., Raised when decision evidence violates a domain invariant., Decision Support domain layer. (+25 more)

### Community 10 - "CropSuite.py"
Cohesion: 0.07
Nodes (59): # NOTE: self.extent is modified here to align with grid, Combines climate suitability with soil/terrain data to calculate final crop…, aggregate_soil_raster_lst(), calcification_map(), cropsuitability(), get_soil_data(), get_suitability_val_dict(), get_texture_class() (+51 more)

### Community 11 - "DownloadCMIP6Data"
Cohesion: 0.09
Nodes (17): DownloadCMIP6Data, get_individual_file(), main(), ProcessTools, Path, Save a dataset to a NetCDF file with appropriate encoding. Parameters…, Downloader for CMIP6 daily GCM data., List of all (gcm, ssp, var, year) combinations. (+9 more)

### Community 12 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.06
Nodes (121): EnvironmentalInputReference, Caller-selected exact environmental dataset version., EvaluationConflictError, RuntimeError, Raised when an evaluation identity already exists., Durable scientific evidence referenced without exposing filesystem paths., Opaque engine-reported scientific source identity and SHA-256., ScientificArtifact (+113 more)

### Community 13 - "climate_suitability_main_xarray.py"
Cohesion: 0.10
Nodes (31): climate_suitability_xarray(), compute_suitability(), process_index(), find_max_sum_new(), get_id_list_start(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration(), get_photoperiod_params() (+23 more)

### Community 14 - "CropSuiteLite"
Cohesion: 0.10
Nodes (16): CropSuiteLite, Loads crop parameterization files and interpolation formulas., Calculates climate suitability based on temperature and precipitation.…, Merges tiled outputs into a single raster for the entire region. Parameters…, Executes the full CropSuiteLite pipeline. Steps: 1. Downscale climate data. 2.…, Main controller for the CropSuiteLite crop suitability modeling framework. This…, Interpolates or retrieves downscaled climate data (precipitation and…, Calculates grid tiling based on available RAM to prevent memory overflow.… (+8 more)

### Community 15 - "test_migration_host.py"
Cohesion: 0.11
Nodes (30): _build_parser(), main(), ArgumentParser, Path, One-shot production schema migration host for VIA releases., Return the repository-local Alembic config when running from source., Resolve the Alembic config without depending on the process cwd., Validate production persistence and migrate the schema to Alembic head. (+22 more)

### Community 16 - "climate_suitability_main.py"
Cohesion: 0.07
Nodes (38): calculate_average_sunshine(), calculate_day_length(), climate_suitability(), climsuit_new(), process_index(), find_max_sum_new(), get_lethal_max_precipitation(), get_lethal_min_precipitation_duration() (+30 more)

### Community 17 - "cropsuite_adapter.py"
Cohesion: 0.06
Nodes (112): CropExecutionStatus, CropLimitationEvidence, CropSuitabilityExecutionError, InvalidEngineOutputError, LimitationEvidenceAvailability, LimitingFactorEvidence, StrEnum, Transport-neutral aggregate for one limiting-factor code. (+104 more)

### Community 18 - "CoverageMeasurement"
Cohesion: 0.18
Nodes (20): CheckDatasetVersionCoverage, CoverageCompatibilityFailure, CoverageMeasurement, Structural metadata prevented a meaningful spatial measurement., Successful, CRS-aware area measurement returned by a spatial port., _multi_polygon(), _polygon(), Any (+12 more)

### Community 19 - "agroclimatic_evaluation/infrastructure/__init__.py"
Cohesion: 0.10
Nodes (27): CropCatalogEntry, ScientificallyBoundDatasetVersion, FilesystemCropCapabilityCatalog, FilesystemScientificInputBindingCatalog, Path, Read scientific capability metadata without importing the CropSuite engine., Adapter over the exact deployment-selected CropSuite parameter directory., Expose only public dataset identities from deployment bindings. (+19 more)

### Community 20 - "test_farm_management_postgresql.py"
Cohesion: 0.26
Nodes (22): clean_farm_management(), database(), _database_url(), _multi_polygon(), _parcel(), _polygon(), _project(), datetime (+14 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management persistence"
Cohesion: 0.12
Nodes (20): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, Optimistic parcel revision transaction, ParcelVersionConflictError, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations (+12 more)

### Community 23 - "knowledge_services.py"
Cohesion: 0.10
Nodes (36): EvidenceItem, build_lexical_retrieval_query(), build_retrieval_query(), build_semantic_retrieval_query(), _choose_boundary(), _contiguous_section_spans(), _cosine_similarity(), _filter_low_value_lexical_hits() (+28 more)

### Community 24 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.20
Nodes (10): Common-Support Ranking, ADR-002 Layered Bounded Contexts, ADR-003 Commands and Queries in Application, ADR-005 Background Worker, ADR-007 Initial Deployment, ADR-009 Multicrop Evaluation, Architecture and Backend for CropSuiteLite Huaura v2, Celery (+2 more)

### Community 25 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 26 - "knowledge_models.py"
Cohesion: 0.05
Nodes (48): CorpusManifest, CorpusSource, EmbeddingIndex, ExtractedDocument, ExtractedPage, IngestionReport, IngestionSourceResult, KnowledgeChunk (+40 more)

### Community 27 - "test_architecture.py"
Cohesion: 0.13
Nodes (19): _imported_modules(), Path, Lightweight dependency checks for the modular-monolith foundation., test_agroclimatic_evaluation_does_not_import_other_contexts(), test_application_packages_do_not_import_outward_layers(), test_context_interfaces_do_not_import_infrastructure(), test_decision_support_application_uses_only_evaluation_public_contract(), test_decision_support_domain_does_not_depend_on_agroclimatic_evaluation() (+11 more)

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
Cohesion: 0.17
Nodes (37): ExecuteEvaluation, Request synchronous execution of one already-persisted evaluation., AgroclimaticEvaluationExecutionService, Execute requested crops and summarize them through Application-owned ports., _artifact(), _environmental_information_for(), _evaluation(), _execute() (+29 more)

### Community 32 - "Farm Management minimum vertical slice"
Cohesion: 0.13
Nodes (13): ADR-011: PostgreSQL/PostGIS persistence for Farm Management, Consequences, Context, Decision, Status, Architectural alignment, Slice exclusions and authorization dependency, Explicit exclusions and provisional choices (+5 more)

### Community 33 - "Application commands and queries"
Cohesion: 0.29
Nodes (8): Application commands and queries, FastAPI composition root, In-memory and durable Infrastructure adapters, Project and parcel HTTP resources, Farm Management repository abstractions, Transport-to-domain path, ProjectRepository, ParcelRepository, and in-memory adapters, Repository ports and in-memory adapters query

### Community 34 - "scientific_source_store.py"
Cohesion: 0.12
Nodes (24): _file_identity(), FilesystemScientificSourceStore, _fsync_file(), _is_within(), _matches_identity(), Path, Protocol, PurePosixPath (+16 more)

### Community 35 - "VIA architecture implementation roadmap"
Cohesion: 0.13
Nodes (16): Domain dependency rule, Layered modular monolith, Inward dependency direction, Architecture source and PoC preservation, Cross-stage architecture gates, Explanation and comparison increment, Modeling increment, Modular foundation increment (+8 more)

### Community 36 - "DomainValidationError"
Cohesion: 0.06
Nodes (67): Synchronous application orchestration for persisted evaluations., _to_common_support(), _to_comparable_crop(), _to_outcome(), CommonSupport, ComparableCrop, normalize_common_support_measurements(), Evaluation-level scientific common-support result. (+59 more)

### Community 37 - "DecisionSupportService"
Cohesion: 0.08
Nodes (30): IDecisionPolicy, IDefaultViabilityPolicyProvider, Evaluate comparable evidence without changing its scientific values., Provide the current VIA default viability policy without owning its storage., EvaluateConfiguredDecisionSupport, EvaluateDecisionSupport, StrEnum, Decision Support application query messages. (+22 more)

### Community 38 - "agroclimatic_evaluation/application/ports.py"
Cohesion: 0.06
Nodes (55): _comparison_request(), CommonSupportResult, CommonSupportStatus, ComparableCropResult, CropComparisonEngineError, CropComparisonExecutionError, CropComparisonInput, CropComparisonRequest (+47 more)

### Community 40 - "Q: PostgreSQL Farm Management repositories"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: PostgreSQL Farm Management repositories, Source Nodes

### Community 41 - "WaterRegime"
Cohesion: 0.10
Nodes (37): EvaluationResultAvailability, PersistedCropOutcomeResult, StrEnum, Whether persisted outcomes are pending, partial, or final., CommonSupportStatus, StrEnum, CropOutcomeStatus, LimitationEvidenceAvailability (+29 more)

### Community 42 - "ADR-012: PostgreSQL/PostGIS persistence for Environmental Information"
Cohesion: 0.12
Nodes (18): ADR-012: PostgreSQL/PostGIS persistence for Environmental Information, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation, Decision Support (+10 more)

### Community 43 - "PostGIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "GetPublishedDatasetVersion"
Cohesion: 0.20
Nodes (19): GetPublishedDatasetVersion, PublishedDatasetVersion, PublishedDatasetVersionReader, Protocol, Stable contracts deliberately published to other bounded contexts., Public cross-context reader for exact immutable dataset versions., _dataset(), datetime (+11 more)

### Community 45 - "capabilities.py"
Cohesion: 0.11
Nodes (23): CapabilityStatus, CropEvaluationCapability, EnvironmentalInputCapability, EvaluationCapabilities, EvaluationCapabilitiesService, EvaluationCapabilitiesUnavailableError, ICropCapabilityCatalog, IScientificInputBindingCatalog (+15 more)

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

### Community 53 - "create_router"
Cohesion: 0.10
Nodes (29): EnvironmentalInputReferenceInput, ParcelReferenceInput, Commands expressing Agroclimatic Evaluation use-case intent., Minimum Farm Management reference supplied by an authenticated caller., RequestEvaluation, create_router(), get_evaluation(), get_evaluation_evidence() (+21 more)

### Community 54 - "CropSuiteLite Python Dependency Manifest"
Cohesion: 0.50
Nodes (4): CropSuiteLite Python Dependency Manifest, Geospatial Processing Stack, Runtime and Utility Stack, Scientific Computing Stack

### Community 55 - "download_soilgrids_huaura.py"
Cohesion: 0.83
Nodes (3): crop_reproject(), get_vrt(), main()

### Community 56 - "Probar la API de VIA con Postman"
Cohesion: 0.08
Nodes (23): 10. Limitaciones, 11. Decision Support: knowledge retrieval, 12. Decision Support: recommendation, 1. Health, 2. Login, 3. Requests autenticadas, 4. Usuario autenticado, 5. Projects y Parcels (+15 more)

### Community 59 - "Atlas A Logo"
Cohesion: 0.67
Nodes (3): Atlas A Logo, Atlas Branding, Stylized Green Letter A

### Community 63 - "decision_support/infrastructure/postgresql_repositories.py"
Cohesion: 0.09
Nodes (41): RecommendationCitation, StoredChunk, _recommendation_citations(), Base, DeclarativeBase, SQLAlchemy metadata owned by Decision Support Infrastructure., Declarative base for Decision Support persistence records., DefaultViabilityPolicyRecord (+33 more)

### Community 64 - "Evaluation"
Cohesion: 0.08
Nodes (14): Logger, InvalidEvaluationTransitionError, Raised when an Evaluation lifecycle transition is not allowed., Evaluation, EvaluationScenarioResult, WaterRegime, Per-water-regime scientific comparison kept separate from other scenarios., An immutable multicrop evaluation and its scientific outcomes. (+6 more)

### Community 65 - "test_decision_support.py"
Cohesion: 0.11
Nodes (41): FinalizedCommonSupportStatus, FinalizedComparableCrop, FinalizedEvaluationResult, ComparableCropEvidence, A provider-produced crop mean and rank over common valid support., _common_support(), _decision_evidence(), _DefaultPolicyProvider (+33 more)

### Community 67 - "policy_http.py"
Cohesion: 0.19
Nodes (19): create_policy_router(), authorize(), get_evaluation_policy(), get_evaluation_viability(), get_policy(), get_user_policy(), update_policy(), update_user_policy() (+11 more)

### Community 68 - "legacy_ownership_admin.py"
Cohesion: 0.08
Nodes (29): _build_parser(), LegacyOwnershipAssignment, LegacyOwnershipError, LegacyOwnershipReport, main(), PostgreSQLLegacyOwnershipStore, ArgumentParser, Engine (+21 more)

### Community 69 - "EvaluationStatus"
Cohesion: 0.11
Nodes (20): Exception, Explicit fail-only recovery for abandoned evaluation executions., ActiveEvaluationResult, CropOutcomeResult, EvaluationResult, ParcelSnapshotResult, Transport-neutral Agroclimatic Evaluation results., InvalidCommandError (+12 more)

### Community 70 - "RetrievedKnowledge"
Cohesion: 0.09
Nodes (18): RecommendationContext, RecommendationGeneration, RecommendationRun, RetrievedKnowledge, IKnowledgeRetriever, IRecommendationGenerator, IRecommendationRepository, _embedding_index_id() (+10 more)

### Community 72 - "test_agronomic_knowledge_http.py"
Cohesion: 0.18
Nodes (17): Published water-regime values shared with consumer bounded contexts., WaterRegime, KnowledgeContextUnavailableError, LookupError, Raised when the finalized scientific result cannot form a scenario context., _Builder, _client(), _context() (+9 more)

### Community 73 - "EnvironmentalInformationService"
Cohesion: 0.06
Nodes (66): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort, GetDataset (+58 more)

### Community 74 - "farm_management/infrastructure/postgresql_repositories.py"
Cohesion: 0.10
Nodes (25): Base, DeclarativeBase, SQLAlchemy metadata owned by Farm Management Infrastructure., Declarative base for Farm Management persistence records., Farm Management infrastructure layer., ParcelRecord, ParcelVersionRecord, ProjectRecord (+17 more)

### Community 75 - "DatasetVersion"
Cohesion: 0.10
Nodes (27): CoverageComputation, DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., DatasetVersion, Immutable reproducibility metadata for one dataset release., Positive horizontal and vertical source-cell resolution., SpatialResolution (+19 more)

### Community 77 - "Q: ParcelVersion persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ParcelVersion persistence, Source Nodes

### Community 79 - "identity_access/application/service.py"
Cohesion: 0.09
Nodes (28): AuthenticationError, IdentityUserNotFoundError, LookupError, RuntimeError, Application-level Identity Access failures., Raised when an administrative user reference cannot be resolved., Raised when supplied authentication material is not valid., Identity Access application layer. (+20 more)

### Community 80 - "User"
Cohesion: 0.09
Nodes (25): IdentityConflictError, IdentityValidationError, RuntimeError, ValueError, Identity Access domain errors., Raised when an Identity Access domain object is invalid., Raised when identity persistence would violate an existing identity., Identity Access domain. (+17 more)

### Community 81 - "PostgreSQLUserRepository"
Cohesion: 0.22
Nodes (18): PostgreSQLUserRepository, SessionFactory, clean_identity_access(), database(), datetime, Engine, fixture, SessionFactory (+10 more)

### Community 83 - "Parcel"
Cohesion: 0.09
Nodes (17): ParcelVersionConflictError, RuntimeError, Raised when persisted parcel history changed before a revision was saved., Parcel, Project, An agricultural project that groups parcels., A named parcel whose geometry changes only by appending versions., ParcelRepository (+9 more)

### Community 93 - "Q: Domain-to-Infrastructure dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Domain-to-Infrastructure dependency violations, Source Nodes

### Community 135 - "test_retrieval_and_recommendation_traces_persist_closed_citations"
Cohesion: 0.32
Nodes (13): _chunk(), clean_knowledge_tables(), database(), _index(), Engine, fixture, SessionFactory, PostgreSQL integration coverage for agronomic knowledge RAG persistence. (+5 more)

### Community 136 - "Huaura scientific fixture recovery audit"
Cohesion: 0.08
Nodes (25): Benchmark compatibility, Boundary and reference mask, Climate, Current identity manifest, DEM, Executive status, Historical alternatives / abandoned paths, Huaura scientific fixture recovery audit (+17 more)

### Community 137 - "AuthSession"
Cohesion: 0.09
Nodes (25): AuthSession, StrEnum, Outcome of one atomic refresh-token rotation attempt., RefreshRotationStatus, Base, DeclarativeBase, Declarative base for Identity Access persistence records., Identity Access infrastructure adapters. (+17 more)

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
Cohesion: 0.06
Nodes (69): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., _file_identity(), FilesystemScientificArtifactStore, _is_not_found_error(), _is_within(), PublishedScientificArtifact, Any (+61 more)

### Community 151 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.15
Nodes (22): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+14 more)

### Community 152 - "IAuthSessionRepository"
Cohesion: 0.23
Nodes (3): IAuthSessionRepository, datetime, UUID

### Community 154 - "VIA production release, migration, and rollback runbook"
Cohesion: 0.04
Nodes (46): B2 reproducible Linux container image, B6.1 resource benchmark, B6 production-like Docker Compose smoke, B7 DigitalOcean single-Droplet deployment definition, B8 target hybrid managed deployment, Benchmark and future worker concurrency, Cloud Run API filesystem contract, Database and migration contract (+38 more)

### Community 155 - "test_frontend_openapi.py"
Cohesion: 0.30
Nodes (13): _Engine, Any, OpenAPI contracts consumed by the frontend handoff., _schema(), _Sessions, test_all_live_functional_routes_publish_bearer_security(), test_committed_openapi_matches_live_non_production_schema(), test_decision_support_responses_publish_real_schemas() (+5 more)

### Community 157 - "test_config.py"
Cohesion: 0.09
Nodes (31): create_production_app(), Build the production API after enforcing durable persistence settings., MonkeyPatch, parametrize, Path, Tests for environment-driven application composition settings., _scientific_worker_settings(), test_api_composition_passes_transaction_pooler_setting() (+23 more)

### Community 158 - "identity_access/interfaces/http.py"
Cohesion: 0.16
Nodes (19): _authentication_response(), AuthenticationResponse, _bearer_unauthorized(), resolve_principal(), login(), logout(), me(), refresh() (+11 more)

### Community 159 - "read_crop_parameterizations_files"
Cohesion: 0.15
Nodes (12): get_formula(), get_id_list_start(), get_plant_param_interp_forms_dict(), print_crop_param_output(), print_sections(), Reads and parses crop parameterization files from a specified folder path.…, Prints the keys of a given dictionary as a list of sections or items. Args:…, Given two arrays of numerical values x_vals and y_vals representing data… (+4 more)

### Community 160 - "test_agroclimatic_environmental_inputs.py"
Cohesion: 0.18
Nodes (22): parametrize, Focused domain tests for immutable environmental input manifests., _snapshot(), test_environmental_input_manifest_accepts_valid_inputs(), test_environmental_input_manifest_allows_same_version_for_distinct_input_keys(), test_environmental_input_manifest_rejects_duplicate_input_key(), test_environmental_input_manifest_rejects_empty_inputs(), test_environmental_input_manifest_rejects_input_registered_after_resolution() (+14 more)

### Community 161 - "test_environmental_information_postgresql.py"
Cohesion: 0.32
Nodes (12): create_database(), clean_environmental_information(), database(), _dataset(), Engine, fixture, SessionFactory, PostgreSQL/PostGIS integration tests for Environmental Information. (+4 more)

### Community 162 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.06
Nodes (78): AsyncClient, _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any (+70 more)

### Community 163 - "test_evaluation_capabilities_api.py"
Cohesion: 0.28
Nodes (16): _app(), principal(), _bindings(), _catalog(), _client(), FastAPI, Path, TestClient (+8 more)

### Community 164 - "Agroclimatic Evaluation request, worker, recovery, and read slice"
Cohesion: 0.15
Nodes (11): ADR-015: PostgreSQL polling for Agroclimatic Evaluation worker dispatch, Consequences, Context, Decision, Status, Agroclimatic Evaluation request, worker, recovery, and read slice, Current lifecycle and execution, Deliberately deferred (+3 more)

### Community 165 - "Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation, Source Nodes

### Community 166 - "Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors, Source Nodes

### Community 170 - "Dataset"
Cohesion: 0.11
Nodes (13): Environmental Information domain layer., Dataset, Stable logical identity for a geoenvironmental dataset., DatasetRepository, DatasetVersionRepository, Protocol, UUID, Repository abstractions for Environmental Information aggregates. (+5 more)

### Community 172 - "SpatialExtent"
Cohesion: 0.13
Nodes (23): A rectangular extent expressed in the dataset version's CRS., SpatialExtent, clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine (+15 more)

### Community 174 - "require_test_database_url"
Cohesion: 0.10
Nodes (29): ValueError, Safety guard shared by destructive PostgreSQL/PostGIS integration tests., Raised before destructive tests target a database that is not explicitly safe., Return a safe integration-test URL without ever including it in errors., Read and validate the test-only database settings before any DB operation., require_test_database_url(), UnsafeTestDatabaseError, validate_test_database_url() (+21 more)

### Community 175 - "Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment., Source Nodes

### Community 176 - "generate_frontend_openapi.py"
Cohesion: 0.47
Nodes (4): _Engine, main(), Generate the frontend OpenAPI snapshot without external service calls., _Sessions

### Community 177 - "PolicyReference"
Cohesion: 0.08
Nodes (42): Application use cases for VIA's global viability policy., InvalidViabilityPolicyRevisionError, LookupError, ValueError, Application errors for Decision Support policy configuration., Raised when a requested persisted policy version does not exist., Raised when a requested viability-policy revision is not a new version., ViabilityPolicyVersionNotFoundError (+34 more)

### Community 178 - "config.py"
Cohesion: 0.19
Nodes (13): _environment_boolean(), _environment_csv(), _environment_float(), _environment_integer(), _is_same_or_within(), _optional_path(), _optional_path_alias(), _optional_scientific_storage_backend() (+5 more)

### Community 180 - "DomainValidationError"
Cohesion: 0.09
Nodes (37): InvalidSpatialInputError, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, CoverageGeometry (+29 more)

### Community 181 - "Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract, Source Nodes

### Community 183 - "test_decision_support_postgresql.py"
Cohesion: 0.18
Nodes (34): One immutable persisted viability-policy configuration., ViabilityPolicyVersionRecord, PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+26 more)

### Community 184 - "test_agroclimatic_evaluation_worker.py"
Cohesion: 0.15
Nodes (27): AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application., _artifact(), _engine_result(), _evaluation(), _executor(), FakeComparisonEngine, FakeEngine (+19 more)

### Community 185 - "crop_rotation.py"
Cohesion: 0.18
Nodes (15): calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):…, Read a GeoTIFF file with multiple bands into a NumPy array. Parameters: - fn… (+7 more)

### Community 187 - "verify_runtime"
Cohesion: 0.36
Nodes (10): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_read_only_directory(), _require_read_only_file(), _require_writable_directory(), _run_cropsuite_import_smoke() (+2 more)

### Community 188 - "decision_support/infrastructure/__init__.py"
Cohesion: 0.18
Nodes (19): Decision Support infrastructure adapters., load_taxonomy(), _load_yaml_mapping(), ManifestValidationError, _optional_string(), _parse_source(), Any, Path (+11 more)

### Community 189 - "create_database"
Cohesion: 0.10
Nodes (17): SQLAlchemy metadata owned by Identity Access Infrastructure., _configure_float_round_trip(), create_database(), Engine, SessionFactory, Host-level SQLAlchemy engine and session construction., Preserve PostgreSQL float8 values exactly across text-protocol round trips., Create the shared engine and short-lived session factory. (+9 more)

### Community 191 - "benchmark_production_runtime.sh"
Cohesion: 0.19
Nodes (16): artifact_bytes_for_evaluation(), COMPOSE_PROJECT_NAME, database_size_bytes(), fail(), monotonic_ns(), post_json(), record_stack_sample(), require_command() (+8 more)

### Community 192 - "test_authentication.py"
Cohesion: 0.09
Nodes (14): _Clock, _Harness, _http_client(), _PasswordHasher, datetime, TestClient, test_auth_openapi_exposes_bearer_only_for_me(), test_http_login_failures_do_not_reveal_account_existence() (+6 more)

### Community 193 - "test_api_host.py"
Cohesion: 0.14
Nodes (21): ApiServerSettings, main(), Production HTTP process host for VIA., Provider-neutral Uvicorn bind settings for the production API process., Load API bind settings from the process environment., Validate production configuration and run one Uvicorn API process., _clear_api_environment(), _configure_production_persistence() (+13 more)

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

### Community 199 - "process_precday_interp"
Cohesion: 0.26
Nodes (4): process_precday_interp(), Resample mm/day without mixing missing coverage into coastal rainfall. Missing…, PrecipitationCoastTest, Missing source coverage must neither dilute rainfall nor gain rainfall.

### Community 201 - "via_backend/worker.py"
Cohesion: 0.11
Nodes (26): Settings for the PostgreSQL polling worker process., _require_worker_values(), WorkerSettings, create_s3_compatible_client(), Create the production S3-compatible client without leaking SDK types upward., _create_artifact_store(), _create_source_materializer(), create_worker() (+18 more)

### Community 205 - "ScientificSourceMaterializer"
Cohesion: 0.32
Nodes (12): Materialize immutable source objects into a rebuildable local cache., ScientificSourceMaterializer, CountingStore, Path, Focused tests for provider-neutral scientific source materialization., _source(), test_cache_miss_downloads_and_cache_hit_avoids_redownload(), test_filesystem_store_reads_only_under_configured_root() (+4 more)

### Community 206 - "main"
Cohesion: 0.08
Nodes (24): WorkerRunSummary, main(), make_shutdown_handler(), _print_active_evaluations(), Logger, Poll until cooperative shutdown, waiting only after a non-full batch., Return a signal handler that only requests cooperative process shutdown., run_forever() (+16 more)

### Community 208 - "Scientific result semantics"
Cohesion: 0.25
Nodes (7): Coverage and no-data, Cross-crop ranking, Limiting factors, Scientific result semantics, Scientific trace, Suitability scale, Water regimes

### Community 209 - "test_hybrid_deployment_contract.py"
Cohesion: 0.53
Nodes (4): _read(), test_cloud_run_examples_separate_api_and_migration_database_endpoints(), test_single_droplet_compose_remains_available_as_rollback(), test_target_worker_example_keeps_sequential_defaults_and_no_real_secrets()

### Community 210 - "test_limiting_factor_domain.py"
Cohesion: 0.33
Nodes (7): _factor(), LimitingFactorEvidence, parametrize, Focused domain invariants for deterministic limiting-factor evidence., test_available_limitation_evidence_accepts_traceable_factor(), test_limiting_factor_rejects_invalid_affected_cells(), test_limiting_factor_rejects_non_integer_raw_code()

### Community 212 - "_KnowledgeRepository"
Cohesion: 0.17
Nodes (15): KnowledgeDocument, LexicalSearchHit, StrEnum, RetrievalStatus, VectorSearchCandidate, configured_embedding_index(), HybridKnowledgeRetriever, Deterministic lexical + vector retrieval with reciprocal-rank fusion. (+7 more)

### Community 213 - "Frontend API reference"
Cohesion: 0.33
Nodes (5): Authentication and authorization, Capability discovery, Decision Support request shapes, Evaluation request, Frontend API reference

### Community 214 - "EnvironmentalInputSnapshot"
Cohesion: 0.20
Nodes (25): EnvironmentalInputSnapshot, Historical environmental input metadata captured for one evaluation input., ConfiguredEnvironmentalInputIntegrityVerifier, Verify manifests using deployment-configured exact dataset-version bindings., _binding(), _fingerprints(), _manifest(), parametrize (+17 more)

### Community 216 - "Asynchronous evaluations"
Cohesion: 0.40
Nodes (4): Asynchronous evaluations, Lifecycle, Polling behavior, Result availability is separate from lifecycle

### Community 217 - "ADR-016: Hybrid managed control plane and dedicated scientific worker"
Cohesion: 0.33
Nodes (5): ADR-016: Hybrid managed control plane and dedicated scientific worker, Consequences, Context, Decision, Status

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

### Community 229 - "identity_admin.py"
Cohesion: 0.11
Nodes (23): PasswordPolicyError, ValueError, Raised when an administratively supplied password violates policy., _build_parser(), main(), _prompt_password(), ArgumentParser, Administrative CLI for VIA identity users. (+15 more)

### Community 231 - "test_identity_access.py"
Cohesion: 0.10
Nodes (24): Argon2PasswordHasher, Security primitive adapters for Identity Access., Hash passwords with Argon2id through pwdlib., Generate URL-safe opaque tokens with 256 bits of entropy., Create the deterministic digest persisted for an opaque token., SecretsOpaqueTokenGenerator, Sha256TokenHasher, parametrize (+16 more)

### Community 232 - "test_agronomic_knowledge.py"
Cohesion: 0.12
Nodes (28): RecommendationFactor, RecommendationStatus, _context(), _Generator, _index(), datetime, MonkeyPatch, Focused tests for the Decision Support agronomic knowledge increment. (+20 more)

### Community 233 - "AgroclimaticEvaluationRecoveryService"
Cohesion: 0.16
Nodes (21): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Logger, Mark an operator-confirmed active orphan as failed without retrying it., _evaluation_in_status(), _manifest(), _outcome() (+13 more)

### Community 234 - "smoke_production_api.py"
Cohesion: 0.19
Nodes (16): ApiClient, _assert_safe_base_url(), _choose_capability(), _credentials(), _load_geometry(), main(), _parser(), Any (+8 more)

### Community 235 - "openai_knowledge.py"
Cohesion: 0.11
Nodes (20): EmbeddingBatch, EmbeddingVector, RecommendationItem, StructuredRecommendation, KnowledgeProviderUnavailableError, RuntimeError, External provider required by the knowledge use case is unavailable., MissingOpenAIAPIKeyError (+12 more)

### Community 236 - "test_production_compose_contract.py"
Cohesion: 0.31
Nodes (6): _mapping_keys(), Static invariants for the provider-neutral B6 production-like Compose smoke., _service_block(), test_b6_compose_encodes_release_ordering_and_runtime_mount_semantics(), test_b6_compose_has_exact_process_topology_and_same_image_contract(), test_b6_worker_bindings_fixture_is_valid_for_startup()

### Community 237 - "Settings"
Cohesion: 0.14
Nodes (19): Require the durable persistence contract used by the production API., Settings needed by the current backend composition root., Settings, Engine, _service_from_env(), MonkeyPatch, parametrize, test_auth_cookie_samesite_environment_rejects_unknown_value() (+11 more)

### Community 238 - "app.py"
Cohesion: 0.06
Nodes (29): create_app(), _FarmAuthorizedParcelSnapshotProvider, FastAPI, UUID, Side-effect-free FastAPI application composition., Composition adapter from Farm's public DTO to Evaluation's owned snapshot., Build the VIA API and register its technical interfaces., PostgreSQLEvaluationPolicyBindingStore (+21 more)

### Community 239 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.06
Nodes (59): factor_display_label(), Human-readable labels for stable agroclimatic factor codes., Return the Spanish display label while preserving raw labels as fallback., Agroclimatic Evaluation application layer., AuthorizedParcelSnapshotNotFoundError, AuthorizedParcelSnapshotProvider, LookupError, Raised when an owned, exact parcel version cannot be resolved. (+51 more)

### Community 240 - "_Service"
Cohesion: 0.18
Nodes (16): _Service, _decision_support_client(), _inside_geometry(), _login(), _Owned, Any, parametrize, TestClient (+8 more)

### Community 241 - "AreaOfInterestProvenance"
Cohesion: 0.29
Nodes (8): AreaOfInterestProvenance, _load_boundary(), _load_json(), _load_provenance(), Any, Path, Provenance declared next to the authoritative AOI asset., BaseGeometry

### Community 242 - "test_ia4_authorization.py"
Cohesion: 0.21
Nodes (13): _body(), _Owned, TestClient, UUID, IA-4 HTTP authorization, burst protection, and safe dataset DTOs., test_datasets_require_bearer_and_admin_for_writes_and_hide_paths(), test_decision_support_owner_role_and_rate_checks_precede_cost(), principal() (+5 more)

### Community 243 - "test_ia5_huaura_aoi.py"
Cohesion: 0.30
Nodes (11): _authenticated_client(), _authoritative_boundary(), _geojson(), _inside_parcels(), Any, Path, TestClient, IA-5 public-release Huaura AOI enforcement. (+3 more)

### Community 244 - "Scripts de VIA"
Cohesion: 0.12
Nodes (16): `backup_postgres.sh`, Benchmark, `benchmark_production_runtime.sh`, `deploy_digitalocean.sh` / `deploy_digitalocean.ps1`, Descarga de datos, Diagnóstico y validación científica, Operación y despliegue, Preparación científica (+8 more)

### Community 245 - "ParcelSnapshot"
Cohesion: 0.08
Nodes (33): UUID, ParcelSnapshot, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing (+25 more)

### Community 246 - "Navegación"
Cohesion: 0.14
Nodes (13): `adr/`, `architecture/`, Documentación de VIA, `frontend/`, `implementation/`, Knowledge base, Knowledge graph para agentes, Motor científico (+5 more)

### Community 248 - "Route and security matrix"
Cohesion: 0.50
Nodes (3): Production-only surface, Route and security matrix, Status semantics

### Community 251 - "S3CompatibleClient"
Cohesion: 0.20
Nodes (7): Any, Protocol, Small S3-compatible SDK boundary shared by scientific object stores., Subset of the boto3 S3 client used by VIA infrastructure adapters., S3CompatibleClient, R2ScientificSourceStore, Cloudflare R2 source store through its S3-compatible API.

### Community 252 - "RecommendationContextBuilder"
Cohesion: 0.15
Nodes (11): FinalizedEvaluationResultReader, OwnedEvaluationResolver, Protocol, UUID, Public local interface for a future Decision Support consumer., Translate finalized public scientific evidence into one scenario context., RecommendationContextBuilder, _FailingFinalizedReader (+3 more)

### Community 253 - "Contribuir a VIA"
Cohesion: 0.17
Nodes (11): Arquitectura del backend, Cambios científicos, Commits, Contribuir a VIA, Docker y producción, Documentación, Flujo de trabajo, Migraciones de base de datos (+3 more)

### Community 254 - "Colección Postman de VIA"
Cohesion: 0.20
Nodes (9): Colección Postman de VIA, Endpoints incluidos, Environmental Inputs, Evaluaciones y polling, Flujo y variables automáticas, Importar y preparar, Notas de documentación, Producción, OpenAPI y CORS (+1 more)

### Community 255 - "InMemoryEvaluationRepository"
Cohesion: 0.19
Nodes (6): InMemoryEvaluationRepository, UUID, _validate_limit(), parametrize, test_active_discovery_requires_positive_integer_limit(), test_queued_discovery_requires_positive_limit()

### Community 256 - "[0.1.0] - 2026-09-22"
Cohesion: 0.25
Nodes (7): [0.1.0] - 2026-09-22, Added, Changed, Changelog, Convención de versiones, Removed, [Unreleased]

### Community 257 - "EnvironmentalInputManifest"
Cohesion: 0.11
Nodes (15): EnvironmentalInputResolutionError, datetime, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved., CropSuitabilityRequest, CropSuitabilityResult, ICropSuitabilityEngine, IEnvironmentalInputIntegrityVerifier (+7 more)

### Community 258 - "VIA.postman_environment.json"
Cohesion: 0.25
Nodes (7): id, name, _postman_exported_at, _postman_exported_using, _postman_variable_scope, $schema, values

### Community 259 - "ParcelAreaOfInterestValidator"
Cohesion: 0.33
Nodes (4): ParcelAreaOfInterestValidator, Protocol, Validate parcel geometry against the configured authoritative AOI., datetime

### Community 261 - "test_cors.py"
Cohesion: 0.39
Nodes (7): _client(), TestClient, Environment-configured development CORS behavior., test_allowed_origin_is_echoed(), test_allowed_preflight_supports_frontend_method_and_headers(), test_disallowed_origin_receives_no_cors_permission(), test_empty_configuration_preserves_no_cors_behavior()

### Community 263 - "create_router"
Cohesion: 0.32
Nodes (12): _build_context(), create_router(), authorize(), generate_recommendation(), get_knowledge(), list_recommendations(), throttle(), APIRouter (+4 more)

### Community 264 - "FixedWindowLimiter"
Cohesion: 0.28
Nodes (5): FixedWindowLimiter, Exception, RateLimitExceededError, Request burst protection shared by HTTP adapters; no worker dependency., Atomic, process-local 60-second buckets with an injectable monotonic clock.

### Community 265 - "Q: Te parece bien la ui? tipos no hay dichos tecnicos qeu no se entiendan o información de más, etc. Qué te parece?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Te parece bien la ui? tipos no hay dichos tecnicos qeu no se entiendan o información de más, etc. Qué te parece?, Source Nodes

### Community 266 - "env.py"
Cohesion: 0.47
Nodes (5): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online()

### Community 267 - "SystemClock"
Cohesion: 0.50
Nodes (3): datetime, Clock adapter for Identity Access., SystemClock

### Community 268 - "decision_support/interfaces/__init__.py"
Cohesion: 0.50
Nodes (3): BaseModel, RecommendationRequest, Decision Support interface layer.

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **368 isolated node(s):** `via-backend`, `id`, `name`, `values`, `_postman_variable_scope` (+363 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1504 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `Domain dependency rule` (6× useful, score=3.865892034)
- `Application layer` (4× useful, score=2.54725383)
- `EnvironmentalInformationService` (3× useful, score=1.925093321)
- `ParcelGeometry` (3× useful, score=1.920066196)
- `ParcelVersion` (3× useful, score=1.904096621)
- `InMemoryParcelRepository` (3× useful, score=1.903251837)
- `ParcelRepository` (3× useful, score=1.903251836)
- `EvaluationResult` (2× useful, score=1.327477652)
- `Settings` (2× useful, score=1.323128133)
- `Farm Management schema ownership` (2× useful, score=1.296511747)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Crop Code Catalog` and `Undefined Crop Code c32`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `create_app()` connect `app.py` to `FarmManagementService`, `ViabilityPolicySnapshot`, `ParcelGeometry`, `create_router`, `FixedWindowLimiter`, `AuthSession`, `test_cors.py`, `SystemClock`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `agroclimatic_evaluation/infrastructure/__init__.py`, `test_frontend_openapi.py`, `test_config.py`, `test_agroclimatic_evaluation_api.py`, `test_evaluation_capabilities_api.py`, `DecisionSupportService`, `Dataset`, `capabilities.py`, `generate_frontend_openapi.py`, `PolicyReference`, `DomainValidationError`, `create_router`, `test_decision_support_postgresql.py`, `decision_support/infrastructure/__init__.py`, `create_database`, `decision_support/infrastructure/postgresql_repositories.py`, `test_authentication.py`, `policy_http.py`, `RetrievedKnowledge`, `EnvironmentalInformationService`, `farm_management/infrastructure/postgresql_repositories.py`, `DatasetVersion`, `identity_access/application/service.py`, `User`, `PostgreSQLUserRepository`, `Parcel`, `_KnowledgeRepository`, `test_identity_access.py`, `openai_knowledge.py`, `Settings`, `agroclimatic_evaluation/application/__init__.py`, `_Service`, `test_ia4_authorization.py`, `test_ia5_huaura_aoi.py`, `RecommendationContextBuilder`, `InMemoryEvaluationRepository`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `via_backend/worker.py`, `Dataset`, `DatasetVersion`, `GetPublishedDatasetVersion`, `SpatialExtent`, `app.py`, `CoverageMeasurement`, `DomainValidationError`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `FarmManagementService` connect `FarmManagementService` to `test_agroclimatic_evaluation_api.py`, `ParcelAreaOfInterestValidator`, `ParcelGeometry`, `app.py`, `Parcel`, `test_farm_management_postgresql.py`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `recover_unpersisted_policy()`) actually correct?**
  _`create_app()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `ViabilityPolicySnapshot` (e.g. with `DefaultViabilityPolicyService` and `EvaluationPolicyBindingStore`) actually correct?**
  _`ViabilityPolicySnapshot` has 23 INFERRED edges - model-reasoned connections that need verification._