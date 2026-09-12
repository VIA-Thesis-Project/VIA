---
type: "query"
date: "2026-09-12T20:17:50.370434+00:00"
question: "postgis transform crs geography coverage"
contributor: "graphify"
outcome: "useful"
source_nodes: ["PostGISCoverageCalculator", "SpatialCoveragePort", "DatasetVersion"]
---

# Q: postgis transform crs geography coverage

## Answer

Expanded from the original verification query via graph vocabulary: postgis, transform, crs, geography, coverage. PostGISCoverageCalculator implements SpatialCoveragePort, compares in the DatasetVersion native CRS, and measures transformed EPSG:4326 geography areas. The graph also links the real EPSG:3857 integration test.

## Outcome

- Signal: useful

## Source Nodes

- PostGISCoverageCalculator
- SpatialCoveragePort
- DatasetVersion