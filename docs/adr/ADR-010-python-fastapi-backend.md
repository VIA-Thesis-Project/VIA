# ADR-010: Python and FastAPI for the initial backend

## Status

Accepted

## Context

The modular backend foundation needs a concrete implementation language and HTTP framework. The repository already uses Python for CropSuiteLite, and the initial VIA backend foundation has been established as a small Python package with typed modules, automated tests, and a FastAPI composition root. Selecting the same language can keep the initial project toolchain compact, but it does not make CropSuiteLite part of the backend's Domain or HTTP interface.

## Decision

Use Python as the initial VIA backend implementation language and FastAPI as its HTTP/API framework. Continue to organize the backend as a layered modular monolith. CropSuiteLite remains behind an application port implemented by an infrastructure adapter, and REST interfaces must not import or invoke it directly. Long scientific calculations must execute outside the HTTP request process.

## Consequences

The initial API, composition root, bounded-context packages, and tests can share one Python project and dependency workflow. FastAPI is limited to the interface and application-host concerns; it does not belong in Domain. Future persistence, messaging, worker, and scientific-adapter choices remain separate decisions. Replacing Python or FastAPI later would require a new ADR and must preserve the accepted context, dependency, scientific-isolation, and background-execution rules.

## Current implementation status

[`backend/`](../../backend) contains the Python package, FastAPI startup, technical health endpoint, bounded-context layer skeleton, and architecture tests. Business endpoints, persistence, authentication, worker execution, `ICropSuitabilityEngine`, and `CropSuiteAdapter` are not implemented.

## Source

This decision resolves the language/framework question recorded in [`overview.md`](../architecture/overview.md) and [`backend-structure.md`](../architecture/backend-structure.md). It preserves [`ADR-001`](ADR-001-modular-monolith.md), [`ADR-002`](ADR-002-layered-bounded-contexts.md), [`ADR-004`](ADR-004-cropsuite-port-adapter.md), and [`ADR-005`](ADR-005-background-worker.md).
