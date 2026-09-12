# VIA backend architecture overview

## Purpose and scope

VIA is intended to let an authorized user register a parcel in Huaura, inspect geoenvironmental coverage, request an evaluation for one or more crops, and retrieve suitability results with reproducible evidence. CropSuiteLite performs the scientific calculation; the future backend will manage identity, parcels, requests, execution, persistence, and presentation.

This document separates the current scientific proof of concept from the target architecture and the initial backend foundation. The foundation provides application startup and a technical health endpoint; it does not claim that business APIs, authentication, a durable queue, or public deployment exist.

## Current PoC

The repository already contains a working CropSuiteLite-based flow:

- [`CropSuiteLite/evaluate.py`](../../CropSuiteLite/evaluate.py) exposes crop discovery and parcel evaluation from the CLI.
- [`CropSuiteLite/src/multicrop.py`](../../CropSuiteLite/src/multicrop.py) validates a single Polygon or MultiPolygon parcel in Huaura, snapshots it, evaluates selected crops sequentially in isolated subprocesses, summarizes outputs, and writes a local manifest.
- [`CropSuiteLite/tests/test_multicrop.py`](../../CropSuiteLite/tests/test_multicrop.py) verifies crop selection, spatial weighting, nodata semantics, independent failures, and common-support ranking.
- [`CropSuiteLite/docs/multicrop_evaluation.md`](../../CropSuiteLite/docs/multicrop_evaluation.md) documents the validated operating behavior and its limits.

The scientific PoC has no REST API, identity store, application database, recoverable job queue, cancellation, retry orchestration, quotas, or public frontend. The separate backend foundation currently exposes only a health endpoint. The PoC's local `evaluation.json` is evidence of an execution, not a substitute for those future capabilities.

## Target logical architecture

The accepted direction is a modular monolith organized by bounded contexts. Each context owns its model and exposes explicit collaboration contracts. Inside each context, dependencies follow the layers Domain, Application, Infrastructure, and Interfaces.

The initial backend implementation uses Python and FastAPI according to [`ADR-010`](../adr/ADR-010-python-fastapi-backend.md). This technology choice does not move CropSuiteLite into the HTTP layer or change the port-and-adapter and background-execution boundaries.

The proposed contexts are:

- Identity and Access
- Farm Management
- Environmental Information
- Agroclimatic Evaluation
- Decision Support

These boundaries are the current modeling hypothesis and must be refined through use cases. They are not permission to create one service or database per context.

The major logical components are the frontend, REST interfaces, application use cases, domain models, persistence and integration adapters, a recoverable job mechanism, a background worker, CropSuiteLite, and persistent scientific artifacts. CropSuiteLite remains an existing scientific engine behind the `ICropSuitabilityEngine` port and `CropSuiteAdapter`.

## Logical architecture versus deployment architecture

A bounded context is a model and ownership boundary. A process, container, or server is a deployment boundary. The first deployment may place the API, worker, and queue on one small VPS while keeping them logically separate. The worker may share application packages with the API and still run as another process. CropSuiteLite may keep its own Python environment, especially if the backend uses another language.

Components should be extracted into services only for observed needs such as independent scaling, resource isolation, failure isolation, or independent evolution. Kubernetes, a GPU server, and a separate HTTP API for each worker or data component are not current requirements.

## Decision classification

### Accepted direction

- Modular monolith organized by bounded contexts.
- Domain, Application, Infrastructure, and Interfaces inside each context.
- Python as the initial backend language and FastAPI as the HTTP/API framework.
- CropSuiteLite isolated behind a port and infrastructure adapter.
- Long-running calculations outside the HTTP request process.
- Snapshots, versions, checksums, and evidence sufficient to interpret historical evaluations.
- An initially small public deployment using one VPS and low-cost or free supporting services, subject to provider and capacity confirmation.

### Implemented in the PoC

- One parcel with multiple selected crops.
- Sequential crops with limited internal engine processes and isolated subprocesses.
- Independent per-crop results and failures.
- Parcel summaries and ranking on common valid support.
- Local snapshots and fingerprints for reproducibility checks.

### Recommended pending confirmation

- Place use-case Commands and Queries in Application. Confirm whether an academic convention requires another folder placement without allowing Domain to depend on HTTP, ORM, or external services.

### Open decisions

- Final bounded-context boundaries and whether later concepts such as Experiments require their own context.
- Definitive REST contracts, aggregate boundaries, persistence schema, event contracts, and state mapping.
- Minimum coverage required for recommendations; public scenarios and management options; validation scope for the remaining crop parameters.
- Queue/broker, reliable publication mechanism, retry and cancellation semantics.
- Cache/reuse identity, retention policy, object-storage timing, and any parcel processing margin required by the engine.
- VPS provider, measured capacity, worker concurrency, budget ceiling, publication duration, expected demand, backups, and recovery objectives.
- Scope, provider, quotas, evidence contract, and authorized corpus for optional explanations or RAG.

## Source

The design authority is [`docs/Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx). The Markdown documents preserve its decision states while making the architecture indexable; they do not replace or modify the DOCX.
