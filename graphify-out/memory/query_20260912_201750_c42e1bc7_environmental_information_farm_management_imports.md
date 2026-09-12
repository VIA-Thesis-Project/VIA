---
type: "query"
date: "2026-09-12T20:17:50.775944+00:00"
question: "environmental information farm management imports dependency violations"
contributor: "graphify"
outcome: "useful"
source_nodes: ["EnvironmentalInformationService", "CoverageGeometry", "ParcelGeometry"]
---

# Q: environmental information farm management imports dependency violations

## Answer

Expanded from the original verification query via graph vocabulary: environmental, information, farm, management, imports, dependency, violations. Graphify shows Environmental Information coverage nodes within their own Domain, Application, Infrastructure, and Interfaces communities; composition occurs in main.py. A directed path check found no path from CoverageGeometry to ParcelGeometry, and repository architecture tests plus source scans found no cross-context import.

## Outcome

- Signal: useful

## Source Nodes

- EnvironmentalInformationService
- CoverageGeometry
- ParcelGeometry