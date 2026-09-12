---
type: "query"
date: "2026-09-12T07:29:04.553124+00:00"
question: "ParcelVersion persistence"
contributor: "graphify"
outcome: "useful"
source_nodes: ["ParcelVersion", "ParcelVersionRecord", "PostgreSQLParcelRepository", "Optimistic parcel revision transaction", "ParcelVersionConflictError"]
---

# Q: ParcelVersion persistence

## Answer

Expanded terms: parcelversion, parcel, version, persistence, conflict, stale. ParcelVersion history is mapped by ParcelVersionRecord; PostgreSQLParcelRepository.save performs the optimistic single-append transaction and raises ParcelVersionConflictError through the conflict path.

## Outcome

- Signal: useful

## Source Nodes

- ParcelVersion
- ParcelVersionRecord
- PostgreSQLParcelRepository
- Optimistic parcel revision transaction
- ParcelVersionConflictError