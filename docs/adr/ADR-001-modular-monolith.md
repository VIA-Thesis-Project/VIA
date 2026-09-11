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

The backend modular monolith does not exist. The repository contains the CropSuiteLite PoC that it will integrate.

## Source

Sections 3 through 5 and 20 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx).
