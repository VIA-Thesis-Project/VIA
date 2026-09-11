# ADR-002: Layered bounded contexts

## Status

Accepted

## Context

Each context must protect its model from transport, persistence, messaging, and scientific-engine details.

## Decision

Structure every bounded context with Domain, Application, Infrastructure, and Interfaces responsibilities. Dependencies point inward: Interfaces delegates to Application; Application coordinates Domain through internal contracts; Infrastructure implements ports and repository abstractions. Domain does not depend on Infrastructure or HTTP.

## Consequences

Persistence and external technologies can change without becoming domain concepts. Folder names alone are insufficient; dependency checks and composition must enforce the direction. Some duplication at boundaries is acceptable to avoid leaking internal models.

## Current implementation status

The target backend layers have not been created. [`backend-structure.md`](../architecture/backend-structure.md) is guidance only.

## Source

Sections 6 through 10 and 20 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx).
