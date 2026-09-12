---
type: "query"
date: "2026-09-12T06:06:06.757097+00:00"
question: "optimistic stale-write handling introduced in the current slice"
contributor: "graphify"
outcome: "useful"
source_nodes: ["ParcelVersionConflictError", "InMemoryParcelRepository", "test_stale_save_cannot_overwrite_persisted_geometry_history()"]
---

# Q: optimistic stale-write handling introduced in the current slice

## Answer

Expanded from original query via graph vocab: [stale, revision, conflict, parcel, version]. ParcelRepository.save carries expected_version; the in-memory adapter compares persisted history and raises ParcelVersionConflictError when a stale append attempts to overwrite the current history.

## Outcome

- Signal: useful

## Source Nodes

- ParcelVersionConflictError
- InMemoryParcelRepository
- test_stale_save_cannot_overwrite_persisted_geometry_history()