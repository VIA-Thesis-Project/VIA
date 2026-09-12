---
type: "query"
date: "2026-09-12T07:08:50.987445+00:00"
question: "Continue the Farm Management durable persistence increment from the current repository state"
contributor: "graphify"
outcome: "useful"
source_nodes: ["ParcelRepository", "ParcelVersion", "ParcelVersionConflictError", "InMemoryParcelRepository", "Domain dependency rule", "Application layer"]
---

# Q: Continue the Farm Management durable persistence increment from the current repository state

## Answer

Expanded from original query via graph vocab: [farm, management, repository, adapter, parcel, version, geometry, stale, conflict, domain, application, infrastructure]. The graph confirms inward repository ports, immutable ParcelVersion history, and ParcelVersionConflictError stale-write semantics; PostgreSQL work must remain in Infrastructure and composition.

## Outcome

- Signal: useful

## Source Nodes

- ParcelRepository
- ParcelVersion
- ParcelVersionConflictError
- InMemoryParcelRepository
- Domain dependency rule
- Application layer