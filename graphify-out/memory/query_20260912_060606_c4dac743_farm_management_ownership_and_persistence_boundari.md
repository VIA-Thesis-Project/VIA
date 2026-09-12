---
type: "query"
date: "2026-09-12T06:06:06.749982+00:00"
question: "Farm Management ownership and persistence boundaries"
contributor: "graphify"
outcome: "useful"
source_nodes: ["Bounded-context ownership", "ProjectRepository", "ParcelRepository"]
---

# Q: Farm Management ownership and persistence boundaries

## Answer

Expanded from original query via graph vocab: [farm, management, ownership, boundary, repository]. Farm Management owns Project, Parcel, ParcelVersion, geometry, and repository abstractions; Infrastructure supplies adapters. Sources: bounded-contexts.md, backend-structure.md, domain/repositories.py.

## Outcome

- Signal: useful

## Source Nodes

- Bounded-context ownership
- ProjectRepository
- ParcelRepository