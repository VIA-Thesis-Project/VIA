---
type: "query"
date: "2026-09-12T07:29:04.594726+00:00"
question: "Domain-to-Infrastructure dependency violations"
contributor: "graphify"
outcome: "useful"
source_nodes: ["Domain dependency rule", "Application layer", "Infrastructure-only persistence mapping"]
---

# Q: Domain-to-Infrastructure dependency violations

## Answer

Expanded terms: domain, application, infrastructure, dependency, import. The graph identifies the Domain dependency rule, Application layer, and Infrastructure-only persistence mapping. No prohibited Domain/Application database or outward-layer imports were found; this was also verified by the architecture test suite and explicit source scans.

## Outcome

- Signal: useful

## Source Nodes

- Domain dependency rule
- Application layer
- Infrastructure-only persistence mapping