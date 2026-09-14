# ADR-001: Modular monolith

## Status

Accepted

## Context

VIA needs explicit business boundaries and a deployable architecture suitable for a small thesis budget. Separate services would add operational and consistency costs before independent scaling or evolution has been demonstrated.

## Decision

Organize the backend as a modular monolith by bounded context. Keep context contracts and data ownership explicit even when modules share one codebase, process, or PostgreSQL instance. Extract a service later only for observed scaling, resource, failure-isolation, or independent-evolution needs.

## Consequences

The first backend can be deployed simply while retaining architectural boundaries. Modules must not write another context's tables or use its internal repositories. A bounded context is not automatically a server, and a worker process is not automatically another context.

## Current implementation status

The VIA backend is implemented as a layered modular monolith under
[`backend/`](../../backend). Delivered slices currently include Farm Management,
Environmental Information, and Agroclimatic Evaluation, with explicit
Application contracts and context-owned persistence.

The HTTP API and the background evaluation worker are separate process entry
points while remaining part of the same modular backend. PostgreSQL/PostGIS is
shared infrastructure, but module dependency and data-ownership boundaries are
enforced by architecture tests and Import Linter contracts.

Identity & Access and deterministic Decision Support are not yet complete.
Service extraction remains deferred until an observed scaling,
failure-isolation, resource, or independent-evolution need justifies it.

## Source

Sections 3 through 5 and 20 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx).
