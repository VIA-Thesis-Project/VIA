# VIA architecture implementation roadmap

This roadmap translates the architecture source into seven increments. It is planning documentation only; none of the backend stages is implemented by this change. Each increment must preserve CropSuiteLite behavior and the decision status in the ADRs.

## 1 Modeling

**Objective.** Validate the business language, use cases, events, rules, and ownership boundaries before fixing technical contracts.

**Deliverable.** Reviewed context map and use cases for parcel registration, coverage inspection, evaluation request, progress/result/evidence queries, and comparison.

**Entry assumptions.** The modular-monolith direction is accepted. The five contexts are a modeling hypothesis. The current PoC supplies known scientific and multicrop behavior.

**Acceptance criteria.** Context owners, public collaborations, invariants, commands, queries, and relevant events are explicit. Open questions are recorded without being converted into decisions. The academic convention for Command/Query placement is confirmed or remains visibly pending.

**Out of scope.** Backend code, schemas, endpoints, service provisioning, engine changes, new agronomic rules, and crop validation.

## 2 Modular foundation

**Objective.** Establish enforceable module and layer boundaries with initial configuration and persistence foundations.

**Deliverable.** Backend skeleton organized by bounded context and layer, composition root, dependency checks, context-owned migrations, and small public contracts needed by the first use cases.

**Entry assumptions.** Backend language/framework and academic conventions have been chosen. Initial aggregates and persistence ownership have been reviewed.

**Acceptance criteria.** Domain has no Infrastructure or HTTP dependency. Interfaces delegate to Application. Infrastructure implements internal ports. One context cannot modify another context's repositories or tables. No controller imports CropSuiteLite.

**Out of scope.** Scientific execution, broad CRUD, microservices, Kubernetes, production scaling, and speculative contexts.

## 3 Parcel and environmental coverage

**Objective.** Register authorized, versioned parcel geometry and describe compatible environmental coverage before calculation.

**Deliverable.** Project/parcel registration, immutable ParcelVersion behavior, authorization, GeoJSON validation, DatasetVersion catalog, and a coverage query through public context contracts.

**Entry assumptions.** Public GeoJSON CRS and size/complexity limits are confirmed. Huaura coverage data is cataloged with versions, checksums, units, resolution, extent, and masks.

**Acceptance criteria.** Polygon and MultiPolygon cases are handled according to the contract; unauthorized access is rejected; a geometry edit creates a new version; provincial containment and environmental coverage remain distinct; zero and nodata remain distinct; coverage and source resolution are explicit.

**Out of scope.** Running CropSuiteLite, suitability ranking, inventing missing environmental values, changing masks/interpolation, and implying sub-grid precision.

## 4 Result querying

**Objective.** Expose stored results from a compatible existing run before adding new on-demand execution.

**Deliverable.** Read models and query endpoints for evaluation metadata, parcel summary, per-crop results, coverage, and evidence references.

**Entry assumptions.** A versioned parcel, compatible scientific result, and explicit aggregation method are available. Public DTOs and authorization behavior are agreed.

**Acceptance criteria.** Queries do not mutate aggregates; DTOs do not expose ORM entities or internal paths; nodata, scale, coverage, and area-weighting method are visible; historical results remain tied to the original ParcelSnapshot.

**Out of scope.** Starting calculations, queue operation, cancellation, recommendations, and LLM explanations.

## 5 On-demand execution

**Objective.** Execute accepted evaluations recoverably outside the HTTP process through the CropSuiteLite boundary.

**Deliverable.** Persisted evaluation request, idempotent scheduling, worker, `ICropSuitabilityEngine`, `CropSuiteAdapter`, state transitions, retries for transient faults, verified artifacts, and reproducible evidence.

**Entry assumptions.** Queue/broker and reliability mechanism are chosen. The PoC preservation contract is approved. Resource measurements define initial concurrency. Final request and state-mapping contracts are agreed.

**Acceptance criteria.** HTTP returns without waiting for the engine; interrupted publication is recoverable; work directories are isolated; selected crops run sequentially with limited internal processes; one crop failure does not stop the others; expected outputs and compatibility are verified before success; source and artifact identities are persisted; relevant PoC and adapter tests pass.

**Out of scope.** Changing scientific rules, automatic shared caching without compatibility proof, unlimited concurrency, public hosting, and decision-support recommendations.

## 6 Public deployment

**Objective.** Make the frontend, API, persistence, queue, worker, and artifacts publicly operable within the reviewed budget.

**Deliverable.** Deployed system with HTTPS, secrets management, process supervision, resource limits, persistent storage, backups, monitoring/logging, quotas, and documented recovery procedures.

**Entry assumptions.** Uncached runtime, peak memory, CPU, output growth, and limited concurrency have been measured. Provider terms, budget, expected use, publication duration, and data-retention requirements are confirmed.

**Acceptance criteria.** Authorization is enforced server-side; database and broker are not unnecessarily public; restart and interrupted-job recovery are tested; a backup sample is restored; finished scientific results remain available independently of optional explanation services; actual cost and capacity are reviewed.

**Out of scope.** Kubernetes, GPU infrastructure, automatic service extraction, unsupported free-tier assumptions, and unbounded workloads.

## 7 Explanation and comparison

**Objective.** Present compatible comparisons and explanations grounded in authorized, structured scientific evidence.

**Deliverable.** Decision Support use cases for comparison and deterministic explanations, with an optional bounded LLM integration if justified.

**Entry assumptions.** Minimum coverage policy, comparison criteria, public scenarios/management options, evidence fields, quotas, and permitted claims are approved. Any LLM provider and authorized retrieval corpus are selected separately.

**Acceptance criteria.** Comparisons use compatible results and disclose common coverage; explanations cite factors, units, periods, versions, and missing evidence; the LLM does not recalculate scores; failure or budget exhaustion of an explanation service does not hide the scientific result; outputs do not claim profitability or unsupported agronomic causation.

**Out of scope.** Silent score adjustment, claims of field validation, market/water recommendations without sources, guaranteed benefits, and RAG without an authorized corpus and concrete retrieval need.

## Cross-stage gates

- Query Graphify and review relevant ADRs before architecture-impacting work.
- Preserve [`poc-preservation.md`](poc-preservation.md) constraints and the original architecture DOCX.
- Run relevant scientific regression tests when an adapter or integration boundary could affect engine inputs or outputs.
- Update Graphify after architecture-impacting changes.
- Treat new recommendations and provider choices as proposals until explicitly accepted.

## Source

The sequence comes from section 19 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx), elaborated with acceptance constraints from the other architecture sections and current PoC tests.
