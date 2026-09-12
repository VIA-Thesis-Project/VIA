---
type: "query"
date: "2026-09-12T07:29:04.553212+00:00"
question: "PostgreSQL Farm Management repositories"
contributor: "graphify"
outcome: "useful"
source_nodes: ["PostgreSQLProjectRepository", "PostgreSQLParcelRepository", "ParcelVersionRecord", "Farm Management schema ownership"]
---

# Q: PostgreSQL Farm Management repositories

## Answer

Expanded terms: postgresql, postgis, farm, management, repository, adapter. The durable adapters are PostgreSQLProjectRepository and PostgreSQLParcelRepository; they map Project, Parcel, and ParcelVersion through Infrastructure ORM records and are documented by ADR-011.

## Outcome

- Signal: useful

## Source Nodes

- PostgreSQLProjectRepository
- PostgreSQLParcelRepository
- ParcelVersionRecord
- Farm Management schema ownership