---
type: "query"
date: "2026-09-12T20:39:46.290499+00:00"
question: "Confirm backend package and layer structure, Domain/Application/Infrastructure/Interfaces boundaries, current dependency rules, and verification configuration"
contributor: "graphify"
outcome: "useful"
source_nodes: ["Domain dependency rule", "Application layer", "Infrastructure-only persistence mapping", "Interfaces layer", "Bounded-context layered structure"]
---

# Q: Confirm backend package and layer structure, Domain/Application/Infrastructure/Interfaces boundaries, current dependency rules, and verification configuration

## Answer

Expanded from original query via graph vocab: [backend, package, structure, domain, application, infrastructure, interfaces, architecture, dependency, contracts, verification, configuration]. The graph identifies five bounded contexts with Domain, Application, Infrastructure, and Interfaces layers. Domain is the innermost layer; Application coordinates use cases through Domain contracts; Infrastructure implements inward-facing ports; Interfaces delegates to Application. Reliable verification contracts are Domain must not depend on Infrastructure, Domain must not depend on Interfaces, and Application must not depend on concrete Infrastructure. Selected sources: AGENTS.md, docs/architecture/backend-structure.md, docs/adr/ADR-010-python-fastapi-backend.md, backend/tests/test_architecture.py, backend/pyproject.toml, backend/.importlinter, and backend/scripts/verify.ps1.

## Outcome

- Signal: useful

## Source Nodes

- Domain dependency rule
- Application layer
- Infrastructure-only persistence mapping
- Interfaces layer
- Bounded-context layered structure