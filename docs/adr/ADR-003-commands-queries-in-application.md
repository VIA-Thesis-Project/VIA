# ADR-003: Commands and queries in Application

## Status

Recommended — pending confirmation

## Context

An earlier structure placed Commands, Queries, and command/query service interfaces in Domain. The architecture review treats these messages as use-case intent and coordination rather than domain rules.

## Decision

Place Commands, Queries, and their application services under Application. Keep invariants in Domain. Confirm whether the applicable academic convention requires the earlier folder placement before making the convention definitive.

## Consequences

Application clearly owns orchestration and Domain remains independent of transport and external services. If academic requirements choose another location, the dependency rule still prohibits Domain from depending on HTTP, ORM, queue clients, or CropSuiteLite.

## Current implementation status

No backend command/query structure exists. The recommendation is documented but not implemented.

## Source

Sections 6 and 8 and ADR 03 in section 20 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx).
