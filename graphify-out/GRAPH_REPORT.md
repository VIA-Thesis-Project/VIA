# Graph Report - poc_via_cslite  (2026-10-01)

## Corpus Check
- 419 files · ~231,380 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4596 nodes · 11897 edges · 265 communities (169 shown, 35 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 1553 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `171a166b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FarmManagementService
- run_cropsuitelite.py
- NexGenPreProcessing
- Huaura Dataset Preprocessing Configuration
- check_files.py
- ViabilityPolicySnapshot
- Parcel
- Crop Membership Functions
- multicrop.py
- decision_support/domain/models.py
- CropSuite.py
- Dataset
- PostgreSQLEvaluationRepository
- climate_suitability_main_xarray.py
- CropSuiteLite
- test_migration_host.py
- climate_suitability_main.py
- test_cropsuite_adapter.py
- CoverageMeasurement
- IDefaultViabilityPolicyProvider
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
- agroclimatic_evaluation/infrastructure/__init__.py
- VIA architecture implementation roadmap
- agroclimatic_evaluation/infrastructure/postgresql_repositories.py
- cropsuite_adapter.py
- cropsuite_comparison_adapter.py
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
- Project
- CropSuiteLite Python Dependency Manifest
- download_soilgrids_huaura.py
- Probar la API de VIA con Postman
- __main__.py
- Atlas A Logo
- read_remote_chunk
- decision_support/infrastructure/postgresql_repositories.py
- DomainValidationError
- test_decision_support.py
- agroclimatic_evaluation/__init__.py
- policy_http.py
- legacy_ownership_admin.py
- test_agroclimatic_evaluation_queries.py
- RetrievedKnowledge
- decision_support/__init__.py
- decision_support/interfaces/http.py
- EnvironmentalInformationService
- farm_management/infrastructure/postgresql_repositories.py
- DatasetVersion
- environmental_information/__init__.py
- Q: ParcelVersion persistence
- farm_management/__init__.py
- identity_access/interfaces/http.py
- User
- PostgreSQLUserRepository
- identity_access/__init__.py
- .execute_evaluation
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
- identity_access/infrastructure/postgresql_repositories.py
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
- scientific_artifact_store.py
- test_agroclimatic_evaluation_domain.py
- AuthSession
- VIA production release, migration, and rollback runbook
- test_frontend_openapi.py
- Settings
- knowledge.py
- read_crop_parameterizations_files
- EnvironmentalInputManifest
- test_environmental_information_postgresql.py
- test_agroclimatic_evaluation_api.py
- test_evaluation_capabilities_api.py
- Agroclimatic Evaluation request, worker, recovery, and read slice
- Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation
- Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors
- via_backend/worker.py
- test_environmental_information_coverage_postgresql.py
- test_api_host.py
- Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment.
- generate_frontend_openapi.py
- PolicyReference
- config.py
- DomainValidationError
- Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract
- test_decision_support_postgresql.py
- InMemoryEvaluationRepository
- crop_rotation.py
- verify_runtime
- knowledge_manifest.py
- create_database
- benchmark_production_runtime.sh
- test_authentication.py
- AgroclimaticEvaluationWorker
- test_container_image_contract.py
- test_digitalocean_deployment_contract.py
- deploy_digitalocean.sh
- verify_production_compose.sh
- Frontend integration flows
- process_precday_interp
- test_resource_benchmark_contract.py
- CropComparisonRequest
- backup_postgres.sh
- ScientificSourceMaterializer
- test_worker_host.py
- test_viability_policy_migration.py
- Scientific result semantics
- test_hybrid_deployment_contract.py
- test_limiting_factor_domain.py
- decision-support-viability-policy.md
- environmental_information/interfaces/http.py
- Frontend API reference
- scientific_input_integrity.py
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
- test_ia4_postgresql.py
- FilesystemScientificArtifactStore
- smoke_production_api.py
- test_agronomic_knowledge.py
- test_production_compose_contract.py
- test_auth_config.py
- app.py
- agroclimatic_evaluation/application/__init__.py
- Evaluation
- farm_management/infrastructure/__init__.py
- test_ia5_release_security.py
- test_ia5_huaura_aoi.py
- Scripts de VIA
- ParcelSnapshot
- Navegación
- test_ia5_release_artifacts.py
- Route and security matrix
- make_shutdown_handler
- test_r2_scientific_storage.py
- Contribuir a VIA
- Colección Postman de VIA
- factor_display_label
- [0.1.0] - 2026-09-22
- CropSuitabilityRequest
- VIA.postman_environment.json
- env.py
- test_cors.py
- test_parcel_metadata_migration.py
- .__init__
- save

## God Nodes (most connected - your core abstractions)
1. `Evaluation` - 108 edges
2. `create_app()` - 89 edges
3. `DomainValidationError` - 70 edges
4. `Settings` - 68 edges
5. `WaterRegime` - 65 edges
6. `PostgreSQLEvaluationRepository` - 63 edges
7. `ViabilityPolicySnapshot` - 62 edges
8. `PolicyReference` - 60 edges
9. `AgroclimaticEvaluationService` - 54 edges
10. `InMemoryEvaluationRepository` - 53 edges

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

## Communities (265 total, 35 thin omitted)

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
Cohesion: 0.08
Nodes (19): DefaultViabilityPolicyNotConfiguredError, EvaluationPolicyBindingConflictError, RuntimeError, Raised when an evaluation is already bound to a different policy., Raised when VIA has no default viability policy configured., PolicyVersionConflictError, RuntimeError, Raised when one immutable policy reference is bound to different thresholds. (+11 more)

### Community 6 - "Parcel"
Cohesion: 0.06
Nodes (44): Application ports owned by Farm Management., DomainValidationError, ParcelVersionConflictError, RuntimeError, ValueError, Domain errors raised by Farm Management invariants., Raised when a Farm Management value violates a domain invariant., Raised when persisted parcel history changed before a revision was saved. (+36 more)

### Community 7 - "Crop Membership Functions"
Cohesion: 0.06
Nodes (33): Datasets Module, datasets.download_data.DownloadCMIP6Data, datasets.download_data.ProcessTools, CropSuite Main Interface, CropSuite.CropSuiteLite, CropSuiteLite API Reference, solutions.membership_functions.CropSensitivity, Atlas Solutions (+25 more)

### Community 8 - "multicrop.py"
Cohesion: 0.08
Nodes (23): register(), main(), Public CLI for crop catalog discovery and selected-crop parcel evaluations., cell_areas(), compare_crops(), input_fingerprints(), list_crops(), load_geometry() (+15 more)

### Community 9 - "decision_support/domain/models.py"
Cohesion: 0.06
Nodes (51): IDecisionPolicy, Application ports for deterministic Decision Support policies., Evaluate comparable evidence without changing its scientific values., EvaluateDecisionSupport, Decision Support application query messages., Prepare evidence and apply one explicitly versioned policy when possible., DecisionSupportResult, DecisionSupportService (+43 more)

### Community 10 - "CropSuite.py"
Cohesion: 0.07
Nodes (59): # NOTE: self.extent is modified here to align with grid, Combines climate suitability with soil/terrain data to calculate final crop…, aggregate_soil_raster_lst(), calcification_map(), cropsuitability(), get_soil_data(), get_suitability_val_dict(), get_texture_class() (+51 more)

### Community 11 - "Dataset"
Cohesion: 0.06
Nodes (25): Dataset, Stable logical identity for a geoenvironmental dataset., DatasetRepository, DatasetVersionRepository, Protocol, UUID, Repository abstractions for Environmental Information aggregates., InMemoryDatasetRepository (+17 more)

### Community 12 - "PostgreSQLEvaluationRepository"
Cohesion: 0.06
Nodes (103): EnvironmentalInputReference, Caller-selected exact environmental dataset version., Base, DeclarativeBase, SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure., Declarative base for Agroclimatic Evaluation persistence records., CropLimitationEvidenceRecord, CropLimitingFactorRecord (+95 more)

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

### Community 17 - "test_cropsuite_adapter.py"
Cohesion: 0.11
Nodes (63): CropExecutionStatus, LimitationEvidenceAvailability, StrEnum, Scientific outcomes reported independently of Evaluation lifecycle state., Availability of deterministic SAME-RUN limiting-factor evidence., CropSuiteAdapter, Map a VIA snapshot to the preserved blocking CropSuiteLite capability., _adapter() (+55 more)

### Community 18 - "CoverageMeasurement"
Cohesion: 0.16
Nodes (21): CheckDatasetVersionCoverage, CoverageClassification, CoverageMeasurement, StrEnum, Extent-based relationship between a dataset version and a parcel., Successful, CRS-aware area measurement returned by a spatial port., _multi_polygon(), _polygon() (+13 more)

### Community 19 - "IDefaultViabilityPolicyProvider"
Cohesion: 0.29
Nodes (5): IDefaultViabilityPolicyProvider, IDefaultViabilityPolicyStore, Protocol, Provide the current VIA default viability policy without owning its storage., Read and change the current default viability-policy pointer.

### Community 20 - "test_farm_management_postgresql.py"
Cohesion: 0.20
Nodes (27): PostgreSQLParcelRepository, PostgreSQLProjectRepository, SessionFactory, Durable adapter for the Project aggregate., Durable adapter that appends immutable PostGIS geometry versions., clean_farm_management(), database(), _database_url() (+19 more)

### Community 21 - "VIA architecture guardrails"
Cohesion: 0.16
Nodes (15): VIA architecture guardrails, ICropSuitabilityEngine application port, Nodata semantics, ParcelSnapshot, Recoverable background worker flow, Scientific rule preservation, ADR-001 Modular Monolith, Current CropSuiteLite scientific PoC (+7 more)

### Community 22 - "Farm Management persistence"
Cohesion: 0.12
Nodes (20): Durable Farm Management persistence, Polygon and MultiPolygon round-trip preservation, Infrastructure-only persistence mapping, Optimistic parcel revision transaction, ParcelVersionConflictError, PostGIS MULTIPOLYGON SRID 4326 storage, PostgreSQL/PostGIS Farm Management persistence decision, Database configuration and Alembic migrations (+12 more)

### Community 23 - "knowledge_services.py"
Cohesion: 0.09
Nodes (38): EvidenceItem, StoredChunk, build_lexical_retrieval_query(), build_retrieval_query(), build_semantic_retrieval_query(), _choose_boundary(), _contiguous_section_spans(), _cosine_similarity() (+30 more)

### Community 24 - "Architecture and Backend for CropSuiteLite Huaura v2"
Cohesion: 0.20
Nodes (10): Common-Support Ranking, ADR-002 Layered Bounded Contexts, ADR-003 Commands and Queries in Application, ADR-005 Background Worker, ADR-007 Initial Deployment, ADR-009 Multicrop Evaluation, Architecture and Backend for CropSuiteLite Huaura v2, Celery (+2 more)

### Community 25 - "Huaura Environmental Correction"
Cohesion: 0.18
Nodes (12): Huaura Environmental Correction, Nodata Preservation, Huaura Precipitation Validation, process_precday_interp, compute_climate_suitability, Existing Output Cache Reuse, Huaura Precipitation Unit Contract, Tenths-of-mm Precipitation Encoding (+4 more)

### Community 26 - "knowledge_models.py"
Cohesion: 0.08
Nodes (27): CorpusManifest, CorpusSource, EmbeddingIndex, IngestionReport, IngestionSourceResult, KnowledgeChunk, KnowledgeDocument, KnowledgeDocumentStatus (+19 more)

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

### Community 34 - "agroclimatic_evaluation/infrastructure/__init__.py"
Cohesion: 0.08
Nodes (35): Agroclimatic Evaluation infrastructure layer., create_s3_compatible_client(), Any, Protocol, Small S3-compatible SDK boundary shared by scientific object stores., Subset of the boto3 S3 client used by VIA infrastructure adapters., Create the production S3-compatible client without leaking SDK types upward., S3CompatibleClient (+27 more)

### Community 35 - "VIA architecture implementation roadmap"
Cohesion: 0.13
Nodes (16): Domain dependency rule, Layered modular monolith, Inward dependency direction, Architecture source and PoC preservation, Cross-stage architecture gates, Explanation and comparison increment, Modeling increment, Modular foundation increment (+8 more)

### Community 36 - "agroclimatic_evaluation/infrastructure/postgresql_repositories.py"
Cohesion: 0.09
Nodes (55): Synchronous application orchestration for persisted evaluations., _to_outcome(), Agroclimatic Evaluation domain layer., CropLimitationEvidence, CropOutcome, LimitationEvidenceAvailability, LimitingFactorEvidence, StrEnum (+47 more)

### Community 37 - "cropsuite_adapter.py"
Cohesion: 0.09
Nodes (60): CropLimitationEvidence, CropSuitabilityEngineError, CropSuitabilityExecutionError, InvalidEngineOutputError, LimitingFactorEvidence, Application-owned boundary for one crop suitability evaluation., Transport-neutral aggregate for one limiting-factor code., Deterministic explanatory evidence returned by the scientific adapter. (+52 more)

### Community 38 - "cropsuite_comparison_adapter.py"
Cohesion: 0.11
Nodes (31): CommonSupportResult, CommonSupportStatus, ComparableCropResult, CropComparisonEngineError, CropComparisonExecutionError, CropComparisonResult, ICropComparisonEngine, InvalidComparisonOutputError (+23 more)

### Community 40 - "Q: PostgreSQL Farm Management repositories"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: PostgreSQL Farm Management repositories, Source Nodes

### Community 41 - "WaterRegime"
Cohesion: 0.08
Nodes (47): _comparison_request(), _availability(), CommonSupportReadResult, ComparableCropReadResult, CropEvidenceResult, CropLimitationResult, EvaluationResultAvailability, LimitationEvidenceResult (+39 more)

### Community 42 - "ADR-012: PostgreSQL/PostGIS persistence for Environmental Information"
Cohesion: 0.12
Nodes (18): ADR-012: PostgreSQL/PostGIS persistence for Environmental Information, Consequences, Context, Decision, Source, Status, Agroclimatic Evaluation, Decision Support (+10 more)

### Community 43 - "PostGIS service"
Cohesion: 0.40
Nodes (5): PostGIS PostgreSQL 16-3.5 image, PostGIS service, VIA PostGIS persistent data volume, VIA PostgreSQL environment configuration, PostgreSQL, PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic

### Community 44 - "GetPublishedDatasetVersion"
Cohesion: 0.37
Nodes (14): GetPublishedDatasetVersion, _dataset(), datetime, UUID, Public cross-context contract tests for Environmental Information., _service(), test_exact_dataset_and_version_returns_all_published_metadata(), test_missing_dataset_returns_none() (+6 more)

### Community 45 - "capabilities.py"
Cohesion: 0.07
Nodes (37): CapabilityStatus, CropCatalogEntry, CropEvaluationCapability, EnvironmentalInputCapability, EvaluationCapabilities, EvaluationCapabilitiesService, EvaluationCapabilitiesUnavailableError, ICropCapabilityCatalog (+29 more)

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

### Community 53 - "Project"
Cohesion: 0.07
Nodes (14): ParcelAreaOfInterestValidator, Protocol, Validate parcel geometry against the configured authoritative AOI., datetime, Project, An agricultural project that groups parcels., ParcelRepository, ProjectRepository (+6 more)

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
Nodes (40): RecommendationCitation, Base, DeclarativeBase, SQLAlchemy metadata owned by Decision Support Infrastructure., Declarative base for Decision Support persistence records., DefaultViabilityPolicyRecord, EmbeddingIndexRecord, EvaluationViabilityPolicyBindingRecord (+32 more)

### Community 64 - "DomainValidationError"
Cohesion: 0.06
Nodes (50): CommonSupport, ComparableCrop, normalize_common_support_measurements(), Evaluation-level scientific common-support result., One crop ranked on the exact common valid spatial support., Normalize impossible boundary overshoots caused only by float noise., Validate deterministic scientific ranking semantics., Spatial support shared by the usable crop suitability rasters. (+42 more)

### Community 65 - "test_decision_support.py"
Cohesion: 0.09
Nodes (51): FinalizedCommonSupportStatus, FinalizedComparableCrop, EvaluateConfiguredDecisionSupport, StrEnum, How the viability policy configuration is selected for one execution., Select either VIA's current default policy or an explicit custom snapshot., Evaluate Decision Support using a selected viability-policy configuration., ViabilityPolicySelection (+43 more)

### Community 67 - "policy_http.py"
Cohesion: 0.10
Nodes (27): OwnedEvaluationResolver, UUID, DefaultViabilityPolicyService, EvaluationPolicyBindingStore, Protocol, UUID, Application use cases for VIA's global viability policy., None means legacy policy not recorded; never substitute today's default. (+19 more)

### Community 68 - "legacy_ownership_admin.py"
Cohesion: 0.08
Nodes (29): _build_parser(), LegacyOwnershipAssignment, LegacyOwnershipError, LegacyOwnershipReport, main(), PostgreSQLLegacyOwnershipStore, ArgumentParser, Engine (+21 more)

### Community 69 - "test_agroclimatic_evaluation_queries.py"
Cohesion: 0.15
Nodes (12): _evaluation(), _outcome(), parametrize, UUID, Focused Application query tests for Agroclimatic Evaluation., Repository double that fails if a query touches a mutation/worker method., _ReadOnlySpyRepository, _service() (+4 more)

### Community 70 - "RetrievedKnowledge"
Cohesion: 0.08
Nodes (38): StrEnum, RecommendationContext, RecommendationGeneration, RecommendationRun, RecommendationStatus, RetrievalStatus, RetrievedKnowledge, StructuredRecommendation (+30 more)

### Community 72 - "decision_support/interfaces/http.py"
Cohesion: 0.05
Nodes (67): FinalizedEvaluationResultReader, Protocol, Public local interface for a future Decision Support consumer., Published water-regime values shared with consumer bounded contexts., WaterRegime, RecommendationFactor, KnowledgeContextConflictError, KnowledgeContextUnavailableError (+59 more)

### Community 73 - "EnvironmentalInformationService"
Cohesion: 0.07
Nodes (55): CreateDataset, CreateDatasetVersion, Commands expressing Environmental Information use-case intent., Environmental Information application layer., Protocol, Measure an external geometry against a registered dataset extent., SpatialCoveragePort, PublishedDatasetVersion (+47 more)

### Community 74 - "farm_management/infrastructure/postgresql_repositories.py"
Cohesion: 0.14
Nodes (17): Base, DeclarativeBase, SQLAlchemy metadata owned by Farm Management Infrastructure., Declarative base for Farm Management persistence records., ParcelRecord, ParcelVersionRecord, ProjectRecord, Database records for Farm Management; these are not domain entities. (+9 more)

### Community 75 - "DatasetVersion"
Cohesion: 0.08
Nodes (31): CoverageComputation, DatasetVersionConflictError, RuntimeError, Raised when a dataset version identifier has already been registered., DatasetVersion, Immutable reproducibility metadata for one dataset release., Base, DeclarativeBase (+23 more)

### Community 77 - "Q: ParcelVersion persistence"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: ParcelVersion persistence, Source Nodes

### Community 79 - "identity_access/interfaces/http.py"
Cohesion: 0.07
Nodes (47): AuthenticationError, IdentityUserNotFoundError, LookupError, RuntimeError, Application-level Identity Access failures., Raised when an administrative user reference cannot be resolved., Raised when supplied authentication material is not valid., Identity Access application layer. (+39 more)

### Community 80 - "User"
Cohesion: 0.11
Nodes (17): UUID, IdentityValidationError, ValueError, Raised when an Identity Access domain object is invalid., normalize_email(), datetime, StrEnum, Identity Access domain models. (+9 more)

### Community 81 - "PostgreSQLUserRepository"
Cohesion: 0.22
Nodes (18): PostgreSQLUserRepository, SessionFactory, clean_identity_access(), database(), datetime, Engine, fixture, SessionFactory (+10 more)

### Community 83 - ".execute_evaluation"
Cohesion: 0.22
Nodes (6): EnvironmentalInputResolutionError, Exception, RuntimeError, Raised when an exact caller-selected environmental version cannot be resolved., _to_common_support(), _to_comparable_crop()

### Community 93 - "Q: Domain-to-Infrastructure dependency violations"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Domain-to-Infrastructure dependency violations, Source Nodes

### Community 135 - "test_retrieval_and_recommendation_traces_persist_closed_citations"
Cohesion: 0.32
Nodes (13): _chunk(), clean_knowledge_tables(), database(), _index(), Engine, fixture, SessionFactory, PostgreSQL integration coverage for agronomic knowledge RAG persistence. (+5 more)

### Community 136 - "Huaura scientific fixture recovery audit"
Cohesion: 0.08
Nodes (25): Benchmark compatibility, Boundary and reference mask, Climate, Current identity manifest, DEM, Executive status, Historical alternatives / abandoned paths, Huaura scientific fixture recovery audit (+17 more)

### Community 137 - "identity_access/infrastructure/postgresql_repositories.py"
Cohesion: 0.14
Nodes (18): Base, DeclarativeBase, SQLAlchemy metadata owned by Identity Access Infrastructure., Declarative base for Identity Access persistence records., AuthSessionRecord, Database records for Identity Access; these are not domain entities., UserRecord, _auth_session_from_record() (+10 more)

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

### Community 150 - "scientific_artifact_store.py"
Cohesion: 0.09
Nodes (34): _file_identity(), _is_not_found_error(), _is_within(), PublishedScientificArtifact, Any, Exception, Path, PurePosixPath (+26 more)

### Community 151 - "test_agroclimatic_evaluation_domain.py"
Cohesion: 0.19
Nodes (20): _evaluation(), _manifest(), _polygon(), parametrize, ScientificSourceFingerprint, Focused domain tests for immutable evaluation requests., _reference(), _scientific_trace() (+12 more)

### Community 152 - "AuthSession"
Cohesion: 0.09
Nodes (19): IdentityConflictError, RuntimeError, Identity Access domain errors., Raised when identity persistence would violate an existing identity., Identity Access domain., AuthSession, IAuthSessionRepository, datetime (+11 more)

### Community 154 - "VIA production release, migration, and rollback runbook"
Cohesion: 0.04
Nodes (46): B2 reproducible Linux container image, B6.1 resource benchmark, B6 production-like Docker Compose smoke, B7 DigitalOcean single-Droplet deployment definition, B8 target hybrid managed deployment, Benchmark and future worker concurrency, Cloud Run API filesystem contract, Database and migration contract (+38 more)

### Community 155 - "test_frontend_openapi.py"
Cohesion: 0.28
Nodes (14): create_database(), _Engine, Any, OpenAPI contracts consumed by the frontend handoff., _schema(), _Sessions, test_all_live_functional_routes_publish_bearer_security(), test_committed_openapi_matches_live_non_production_schema() (+6 more)

### Community 157 - "Settings"
Cohesion: 0.08
Nodes (37): Require the durable persistence contract used by the production API., Settings needed by the current backend composition root., Settings, MonkeyPatch, parametrize, Path, Tests for environment-driven application composition settings., _scientific_worker_settings() (+29 more)

### Community 158 - "knowledge.py"
Cohesion: 0.09
Nodes (23): EmbeddingBatch, EmbeddingVector, RecommendationItem, MissingOpenAIAPIKeyError, OpenAIEmbeddingProvider, _parse_recommendation(), Any, OpenAI adapters for Decision Support knowledge operations. (+15 more)

### Community 159 - "read_crop_parameterizations_files"
Cohesion: 0.15
Nodes (12): get_formula(), get_id_list_start(), get_plant_param_interp_forms_dict(), print_crop_param_output(), print_sections(), Reads and parses crop parameterization files from a specified folder path.…, Prints the keys of a given dictionary as a list of sections or items. Args:…, Given two arrays of numerical values x_vals and y_vals representing data… (+4 more)

### Community 160 - "EnvironmentalInputManifest"
Cohesion: 0.15
Nodes (26): IEnvironmentalInputIntegrityVerifier, Verify resolved environmental provenance against scientific source fingerprints., EnvironmentalInputManifest, Immutable set of exact environmental inputs resolved for an evaluation., parametrize, Focused domain tests for immutable environmental input manifests., _snapshot(), test_environmental_input_manifest_accepts_valid_inputs() (+18 more)

### Community 161 - "test_environmental_information_postgresql.py"
Cohesion: 0.33
Nodes (12): clean_environmental_information(), database(), _database_url(), _dataset(), Engine, fixture, SessionFactory, PostgreSQL/PostGIS integration tests for Environmental Information. (+4 more)

### Community 162 - "test_agroclimatic_evaluation_api.py"
Cohesion: 0.06
Nodes (77): AsyncClient, _app_with(), _body(), _completed_outcomes(), _evaluation(), _evaluation_with_comparison(), _outcome(), Any (+69 more)

### Community 163 - "test_evaluation_capabilities_api.py"
Cohesion: 0.36
Nodes (13): _bindings(), _catalog(), _client(), Path, TestClient, HTTP discovery of deployment-selected scientific capabilities., test_capabilities_do_not_expose_private_binding_details(), test_capabilities_publish_configured_crops_scenarios_and_bindings() (+5 more)

### Community 164 - "Agroclimatic Evaluation request, worker, recovery, and read slice"
Cohesion: 0.15
Nodes (11): ADR-015: PostgreSQL polling for Agroclimatic Evaluation worker dispatch, Consequences, Context, Decision, Status, Agroclimatic Evaluation request, worker, recovery, and read slice, Current lifecycle and execution, Deliberately deferred (+3 more)

### Community 165 - "Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Locate VIA_TEST_DATABASE_URL safety, PostgreSQL integration tests, database URL validation, Alembic env, create_database, Settings, repositories, PostGIS, and schema creation, Source Nodes

### Community 166 - "Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors, Source Nodes

### Community 170 - "via_backend/worker.py"
Cohesion: 0.13
Nodes (23): Settings for the PostgreSQL polling worker process., WorkerSettings, ActiveEvaluationResult, _create_artifact_store(), create_worker(), _create_worker_database(), list_active_evaluations(), main() (+15 more)

### Community 172 - "test_environmental_information_coverage_postgresql.py"
Cohesion: 0.27
Nodes (14): clean_tables(), database(), _database_url(), _multi_polygon(), _polygon(), Engine, fixture, parametrize (+6 more)

### Community 174 - "test_api_host.py"
Cohesion: 0.14
Nodes (21): ApiServerSettings, main(), Production HTTP process host for VIA., Provider-neutral Uvicorn bind settings for the production API process., Load API bind settings from the process environment., Validate production configuration and run one Uvicorn API process., _clear_api_environment(), _configure_production_persistence() (+13 more)

### Community 175 - "Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment., Source Nodes

### Community 176 - "generate_frontend_openapi.py"
Cohesion: 0.47
Nodes (4): _Engine, main(), Generate the frontend OpenAPI snapshot without external service calls., _Sessions

### Community 177 - "PolicyReference"
Cohesion: 0.12
Nodes (28): InvalidViabilityPolicyRevisionError, LookupError, ValueError, Raised when a requested persisted policy version does not exist., Raised when a requested viability-policy revision is not a new version., ViabilityPolicyVersionNotFoundError, Decision Support application layer., Application lifecycle for immutable Decision Support viability policies. (+20 more)

### Community 178 - "config.py"
Cohesion: 0.16
Nodes (14): _environment_boolean(), _environment_csv(), _environment_float(), _environment_integer(), _is_same_or_within(), _optional_path(), _optional_path_alias(), _optional_scientific_storage_backend() (+6 more)

### Community 180 - "DomainValidationError"
Cohesion: 0.07
Nodes (49): InvalidSpatialInputError, RuntimeError, ValueError, Application ports for Environmental Information spatial collaboration., Raised when supplied parcel geometry is not topologically usable., Raised when the configured spatial implementation cannot execute., SpatialCoverageUnavailableError, CoverageCompatibilityFailure (+41 more)

### Community 181 - "Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Implement A4.1 Decision Support bounded context foundation using only the Agroclimatic Evaluation public Application contract, Source Nodes

### Community 183 - "test_decision_support_postgresql.py"
Cohesion: 0.15
Nodes (32): Decision Support infrastructure adapters., PostgreSQLDefaultViabilityPolicyStore, PostgreSQLViabilityPolicyRepository, SessionFactory, Persist and resolve the singleton VIA default-policy pointer., Durable adapter for immutable viability-policy versions., clean_policy_versions(), database() (+24 more)

### Community 184 - "InMemoryEvaluationRepository"
Cohesion: 0.13
Nodes (33): Fail one operator-confirmed orphaned active evaluation., RecoverEvaluation, AgroclimaticEvaluationRecoveryService, Mark an operator-confirmed active orphan as failed without retrying it., InMemoryEvaluationRepository, _evaluation(), _evaluation_in_status(), FakeEnvironmentalInformation (+25 more)

### Community 185 - "crop_rotation.py"
Cohesion: 0.18
Nodes (15): calculate_suitabilities(), compute_combinations(), crop_rotation(), njit, get_geotiff_extent(), ndarray, Get the spatial extent (bounding box) of a GeoTIFF file. Args: file_path (str):…, Read a GeoTIFF file with multiple bands into a NumPy array. Parameters: - fn… (+7 more)

### Community 187 - "verify_runtime"
Cohesion: 0.36
Nodes (10): main(), Path, Fail fast when the VIA container lacks its complete scientific runtime., Verify the interpreter used by the worker can import the complete runtime., _require_read_only_directory(), _require_read_only_file(), _require_writable_directory(), _run_cropsuite_import_smoke() (+2 more)

### Community 188 - "knowledge_manifest.py"
Cohesion: 0.20
Nodes (18): load_taxonomy(), _load_yaml_mapping(), ManifestValidationError, _optional_string(), _parse_source(), Any, Path, ValueError (+10 more)

### Community 189 - "create_database"
Cohesion: 0.12
Nodes (15): _configure_float_round_trip(), create_database(), Engine, SessionFactory, Host-level SQLAlchemy engine and session construction., Preserve PostgreSQL float8 values exactly across text-protocol round trips., Create the shared engine and short-lived session factory., Shared technical infrastructure used by the application composition root. (+7 more)

### Community 191 - "benchmark_production_runtime.sh"
Cohesion: 0.19
Nodes (16): artifact_bytes_for_evaluation(), COMPOSE_PROJECT_NAME, database_size_bytes(), fail(), monotonic_ns(), post_json(), record_stack_sample(), require_command() (+8 more)

### Community 192 - "test_authentication.py"
Cohesion: 0.09
Nodes (14): _Clock, _Harness, _http_client(), _PasswordHasher, datetime, TestClient, test_auth_openapi_exposes_bearer_only_for_me(), test_http_login_failures_do_not_reveal_account_existence() (+6 more)

### Community 193 - "AgroclimaticEvaluationWorker"
Cohesion: 0.20
Nodes (16): AgroclimaticEvaluationWorker, Discover queued IDs and delegate all execution semantics to Application., _artifact(), _engine_result(), _executor(), FakeComparisonEngine, FakeEngine, Exception (+8 more)

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

### Community 201 - "CropComparisonRequest"
Cohesion: 0.17
Nodes (12): CropComparisonInput, CropComparisonRequest, One durable crop suitability raster offered to scientific comparison., Compare crop suitability only on identical valid spatial support., StubComparisonEngine, test_comparison_engine_contract_is_runtime_checkable(), parametrize, Path (+4 more)

### Community 205 - "ScientificSourceMaterializer"
Cohesion: 0.32
Nodes (12): Materialize immutable source objects into a rebuildable local cache., ScientificSourceMaterializer, CountingStore, Path, Focused tests for provider-neutral scientific source materialization., _source(), test_cache_miss_downloads_and_cache_hit_avoids_redownload(), test_filesystem_store_reads_only_under_configured_root() (+4 more)

### Community 206 - "test_worker_host.py"
Cohesion: 0.14
Nodes (10): CaptureFixture, MonkeyPatch, Fast tests for the VIA worker process host and operator CLI., test_active_cli_emits_only_safe_stable_fields(), test_active_cli_rejects_non_positive_limit(), test_main_closes_runtime_when_systemic_worker_failure_escapes(), test_recover_cli_maps_only_active_expected_status(), test_recover_cli_requires_expected_status_and_reason() (+2 more)

### Community 208 - "Scientific result semantics"
Cohesion: 0.25
Nodes (7): Coverage and no-data, Cross-crop ranking, Limiting factors, Scientific result semantics, Scientific trace, Suitability scale, Water regimes

### Community 209 - "test_hybrid_deployment_contract.py"
Cohesion: 0.53
Nodes (4): _read(), test_cloud_run_examples_separate_api_and_migration_database_endpoints(), test_single_droplet_compose_remains_available_as_rollback(), test_target_worker_example_keeps_sequential_defaults_and_no_real_secrets()

### Community 210 - "test_limiting_factor_domain.py"
Cohesion: 0.33
Nodes (7): _factor(), LimitingFactorEvidence, parametrize, Focused domain invariants for deterministic limiting-factor evidence., test_available_limitation_evidence_accepts_traceable_factor(), test_limiting_factor_rejects_invalid_affected_cells(), test_limiting_factor_rejects_non_integer_raw_code()

### Community 212 - "environmental_information/interfaces/http.py"
Cohesion: 0.22
Nodes (13): CheckCoverageBody, CoverageGeometryBody, CreateDatasetBody, CreateDatasetVersionBody, DatasetResponse, DatasetVersionCoverageResponse, DatasetVersionResponse, BaseModel (+5 more)

### Community 213 - "Frontend API reference"
Cohesion: 0.33
Nodes (5): Authentication and authorization, Capability discovery, Decision Support request shapes, Evaluation request, Frontend API reference

### Community 214 - "scientific_input_integrity.py"
Cohesion: 0.09
Nodes (42): EnvironmentalInputIntegrityError, Raised when resolved environmental provenance does not match scientific inputs., ConfiguredEnvironmentalInputIntegrityVerifier, CropSuiteEnvironmentalInputBinding, load_configured_environmental_input_integrity_verifier(), load_cropsuite_environmental_input_bindings(), _parse_uuid(), Any (+34 more)

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
Cohesion: 0.08
Nodes (28): PasswordPolicyError, ValueError, Raised when an administratively supplied password violates policy., datetime, Clock adapter for Identity Access., SystemClock, _build_parser(), main() (+20 more)

### Community 231 - "test_identity_access.py"
Cohesion: 0.10
Nodes (24): Argon2PasswordHasher, Security primitive adapters for Identity Access., Hash passwords with Argon2id through pwdlib., Generate URL-safe opaque tokens with 256 bits of entropy., Create the deterministic digest persisted for an opaque token., SecretsOpaqueTokenGenerator, Sha256TokenHasher, parametrize (+16 more)

### Community 232 - "test_ia4_postgresql.py"
Cohesion: 0.24
Nodes (10): SessionFactory, PostgreSQL evaluation and generation ledger tests., test_multiple_active_evaluations_are_owner_scoped(), test_recommendation_ledger_records_multiple_attempts_per_owner(), test_simultaneous_evaluation_posts_are_both_admitted(), attempt(), _evaluation(), datetime (+2 more)

### Community 233 - "FilesystemScientificArtifactStore"
Cohesion: 0.28
Nodes (23): CropSuiteComparisonAdapter, Compare persisted CropSuiteLite rasters on common valid support., FilesystemScientificArtifactStore, Filesystem-backed immutable artifact store., _artifact(), Any, parametrize, Path (+15 more)

### Community 234 - "smoke_production_api.py"
Cohesion: 0.19
Nodes (16): ApiClient, _assert_safe_base_url(), _choose_capability(), _credentials(), _load_geometry(), main(), _parser(), Any (+8 more)

### Community 235 - "test_agronomic_knowledge.py"
Cohesion: 0.09
Nodes (31): ExtractedDocument, ExtractedPage, LexicalSearchHit, VectorSearchCandidate, configured_embedding_index(), DeterministicKnowledgeChunker, Page-aware deterministic chunker using recoverable headings and overlap., PyPdfDocumentTextExtractor (+23 more)

### Community 236 - "test_production_compose_contract.py"
Cohesion: 0.31
Nodes (6): _mapping_keys(), Static invariants for the provider-neutral B6 production-like Compose smoke., _service_block(), test_b6_compose_encodes_release_ordering_and_runtime_mount_semantics(), test_b6_compose_has_exact_process_topology_and_same_image_contract(), test_b6_worker_bindings_fixture_is_valid_for_startup()

### Community 237 - "test_auth_config.py"
Cohesion: 0.19
Nodes (12): MonkeyPatch, parametrize, test_auth_cookie_samesite_environment_rejects_unknown_value(), test_auth_cookie_secure_environment_must_be_boolean(), test_auth_settings_have_secure_defaults(), test_auth_settings_parse_environment_overrides(), test_auth_ttls_must_be_positive(), test_host_prefix_is_rejected_while_refresh_cookie_path_is_not_root() (+4 more)

### Community 238 - "app.py"
Cohesion: 0.08
Nodes (28): create_app(), create_production_app(), _FarmAuthorizedParcelSnapshotProvider, FastAPI, UUID, Side-effect-free FastAPI application composition., Composition adapter from Farm's public DTO to Evaluation's owned snapshot., Build the VIA API and register its technical interfaces. (+20 more)

### Community 239 - "agroclimatic_evaluation/application/__init__.py"
Cohesion: 0.05
Nodes (79): EnvironmentalInputReferenceInput, ParcelReferenceInput, Commands expressing Agroclimatic Evaluation use-case intent., Minimum Farm Management reference supplied by an authenticated caller., RequestEvaluation, Agroclimatic Evaluation application layer., AuthorizedParcelSnapshotNotFoundError, AuthorizedParcelSnapshotProvider (+71 more)

### Community 240 - "Evaluation"
Cohesion: 0.07
Nodes (16): datetime, EvaluationExecutor, Logger, Protocol, EvaluationConflictError, InvalidEvaluationTransitionError, RuntimeError, Raised when an Evaluation lifecycle transition is not allowed. (+8 more)

### Community 241 - "farm_management/infrastructure/__init__.py"
Cohesion: 0.22
Nodes (12): AreaOfInterestProvenance, HuauraAreaOfInterestValidator, _load_boundary(), _load_json(), _load_provenance(), Any, Path, Authoritative Huaura area-of-interest validation. (+4 more)

### Community 242 - "test_ia5_release_security.py"
Cohesion: 0.21
Nodes (15): _decision_support_client(), _inside_geometry(), _login(), _Owned, Any, parametrize, TestClient, UUID (+7 more)

### Community 243 - "test_ia5_huaura_aoi.py"
Cohesion: 0.27
Nodes (12): _authenticated_client(), _authoritative_boundary(), _geojson(), _inside_parcels(), Any, Path, TestClient, IA-5 public-release Huaura AOI enforcement. (+4 more)

### Community 244 - "Scripts de VIA"
Cohesion: 0.12
Nodes (16): `backup_postgres.sh`, Benchmark, `benchmark_production_runtime.sh`, `deploy_digitalocean.sh` / `deploy_digitalocean.ps1`, Descarga de datos, Diagnóstico y validación científica, Operación y despliegue, Preparación científica (+8 more)

### Community 245 - "ParcelSnapshot"
Cohesion: 0.07
Nodes (30): UUID, ParcelSnapshot, _parse_multi_polygon(), _parse_polygon(), _parse_position(), _parse_ring(), Any, LinearRing (+22 more)

### Community 246 - "Navegación"
Cohesion: 0.14
Nodes (13): `adr/`, `architecture/`, Documentación de VIA, `frontend/`, `implementation/`, Knowledge base, Knowledge graph para agentes, Motor científico (+5 more)

### Community 248 - "Route and security matrix"
Cohesion: 0.50
Nodes (3): Production-only surface, Route and security matrix, Status semantics

### Community 251 - "make_shutdown_handler"
Cohesion: 0.14
Nodes (12): WorkerRunSummary, make_shutdown_handler(), Logger, Poll until cooperative shutdown, waiting only after a non-full batch., Return a signal handler that only requests cooperative process shutdown., run_forever(), test_run_forever_does_not_poll_again_after_stop_is_requested(), run_once() (+4 more)

### Community 252 - "test_r2_scientific_storage.py"
Cohesion: 0.22
Nodes (12): FakeNotFound, FakeS3Client, Any, Exception, Path, Provider-mocked tests for Cloudflare R2 scientific storage adapters., test_r2_artifact_store_is_idempotent_for_same_remote_identity(), test_r2_artifact_store_publishes_metadata_and_resolves_verified_bytes() (+4 more)

### Community 253 - "Contribuir a VIA"
Cohesion: 0.17
Nodes (11): Arquitectura del backend, Cambios científicos, Commits, Contribuir a VIA, Docker y producción, Documentación, Flujo de trabajo, Migraciones de base de datos (+3 more)

### Community 254 - "Colección Postman de VIA"
Cohesion: 0.20
Nodes (9): Colección Postman de VIA, Endpoints incluidos, Environmental Inputs, Evaluaciones y polling, Flujo y variables automáticas, Importar y preparar, Notas de documentación, Producción, OpenAPI y CORS (+1 more)

### Community 255 - "factor_display_label"
Cohesion: 0.24
Nodes (6): factor_display_label(), Human-readable labels for stable agroclimatic factor codes., Return the Spanish display label while preserving raw labels as fallback., parametrize, test_factor_display_label_preserves_raw_label_for_unmapped_factor(), test_factor_display_label_uses_spanish_application_labels()

### Community 256 - "[0.1.0] - 2026-09-22"
Cohesion: 0.25
Nodes (7): [0.1.0] - 2026-09-22, Added, Changed, Changelog, Convención de versiones, Removed, [Unreleased]

### Community 257 - "CropSuitabilityRequest"
Cohesion: 0.24
Nodes (7): CropSuitabilityRequest, CropSuitabilityResult, ICropSuitabilityEngine, Protocol, One checked per-crop outcome from the scientific boundary., Evaluate one crop without exposing engine process or filesystem details., Transport-neutral input for evaluating one crop against an exact snapshot.

### Community 258 - "VIA.postman_environment.json"
Cohesion: 0.25
Nodes (7): id, name, _postman_exported_at, _postman_exported_using, _postman_variable_scope, $schema, values

### Community 259 - "env.py"
Cohesion: 0.47
Nodes (5): include_name(), Alembic environment for VIA database migrations., Limit autogeneration to bounded-context-owned schemas., run_migrations_offline(), run_migrations_online()

### Community 261 - "test_cors.py"
Cohesion: 0.39
Nodes (7): _client(), TestClient, Environment-configured development CORS behavior., test_allowed_origin_is_echoed(), test_allowed_preflight_supports_frontend_method_and_headers(), test_disallowed_origin_receives_no_cors_permission(), test_empty_configuration_preserves_no_cors_behavior()

## Ambiguous Edges - Review These
- `Crop Code Catalog` → `Undefined Crop Code c32`  [AMBIGUOUS]
  CropSuiteLite/yaml_configurations/response_functions.yaml · relation: references

## Knowledge Gaps
- **365 isolated node(s):** `via-backend`, `id`, `name`, `values`, `_postman_variable_scope` (+360 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1491 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `Domain dependency rule` (6× useful, score=4.551742829)
- `Production deployment runtime contract` (4× useful, score=3.994639857) _(code changed — re-verify)_
- `Application layer` (4× useful, score=2.999164036)
- `AgroclimaticEvaluationWorker` (3× useful, score=2.975861798)
- `Inward dependency direction` (3× useful, score=2.475418547)
- `EnvironmentalInformationService` (3× useful, score=2.266625566)
- `ParcelGeometry` (3× useful, score=2.260706575)
- `ParcelVersion` (3× useful, score=2.241903825) _(code changed — re-verify)_
- `InMemoryParcelRepository` (3× useful, score=2.240909168) _(code changed — re-verify)_
- `ParcelRepository` (3× useful, score=2.240909166) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Crop Code Catalog` and `Undefined Crop Code c32`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `create_app()` connect `app.py` to `FarmManagementService`, `ViabilityPolicySnapshot`, `Parcel`, `test_cors.py`, `decision_support/domain/models.py`, `identity_access/infrastructure/postgresql_repositories.py`, `Dataset`, `PostgreSQLEvaluationRepository`, `test_farm_management_postgresql.py`, `AuthSession`, `knowledge_models.py`, `test_frontend_openapi.py`, `Settings`, `knowledge.py`, `test_agroclimatic_evaluation_api.py`, `test_evaluation_capabilities_api.py`, `capabilities.py`, `generate_frontend_openapi.py`, `PolicyReference`, `Project`, `test_decision_support_postgresql.py`, `InMemoryEvaluationRepository`, `knowledge_manifest.py`, `create_database`, `decision_support/infrastructure/postgresql_repositories.py`, `test_authentication.py`, `policy_http.py`, `RetrievedKnowledge`, `decision_support/interfaces/http.py`, `EnvironmentalInformationService`, `DatasetVersion`, `identity_access/interfaces/http.py`, `PostgreSQLUserRepository`, `identity_admin.py`, `test_identity_access.py`, `test_agronomic_knowledge.py`, `agroclimatic_evaluation/application/__init__.py`, `farm_management/infrastructure/__init__.py`, `test_ia5_release_security.py`, `test_ia5_huaura_aoi.py`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `EnvironmentalInformationService` connect `EnvironmentalInformationService` to `via_backend/worker.py`, `DatasetVersion`, `GetPublishedDatasetVersion`, `Dataset`, `app.py`, `test_environmental_information_coverage_postgresql.py`, `CoverageMeasurement`, `DomainValidationError`, `environmental_information/interfaces/http.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `Evaluation` connect `Evaluation` to `DomainValidationError`, `EnvironmentalInputManifest`, `test_agroclimatic_evaluation_api.py`, `agroclimatic_evaluation/infrastructure/postgresql_repositories.py`, `test_agroclimatic_evaluation_queries.py`, `test_ia4_postgresql.py`, `WaterRegime`, `via_backend/worker.py`, `PostgreSQLEvaluationRepository`, `agroclimatic_evaluation/application/__init__.py`, `.execute_evaluation`, `ParcelSnapshot`, `test_agroclimatic_evaluation_domain.py`, `InMemoryEvaluationRepository`, `AgroclimaticEvaluationExecutionService`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Evaluation` (e.g. with `AgroclimaticEvaluationExecutionService` and `_comparison_request()`) actually correct?**
  _`Evaluation` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `recover_unpersisted_policy()`) actually correct?**
  _`create_app()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `DomainValidationError` (e.g. with `AgroclimaticEvaluationRecoveryService` and `AgroclimaticEvaluationService`) actually correct?**
  _`DomainValidationError` has 27 INFERRED edges - model-reasoned connections that need verification._