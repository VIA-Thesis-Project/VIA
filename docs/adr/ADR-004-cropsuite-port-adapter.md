# ADR-004: CropSuiteLite port and adapter

## Status

Accepted

## Context

CropSuiteLite is a working scientific engine with engine-specific Python modules, configuration files, subprocess behavior, and file outputs. Allowing those details into controllers or Domain would couple the backend to the engine and weaken scientific preservation.

## Decision

Application depends on an `ICropSuitabilityEngine` port. Infrastructure provides `CropSuiteAdapter`, which translates verified requests to CropSuiteLite inputs and returns checked result references. Controllers and Domain never call or import CropSuiteLite directly.

## Consequences

The engine remains replaceable at the boundary and its scientific behavior can be preserved during backend work. The adapter owns paths, configuration translation, process invocation, and output verification. Integration tests are required around this boundary.

## Current implementation status

The port and adapter are not implemented. The adapter is expected to wrap the blocking capability in [`CropSuiteLite/src/multicrop.py`](../../CropSuiteLite/src/multicrop.py), currently exposed by [`CropSuiteLite/evaluate.py`](../../CropSuiteLite/evaluate.py).

## Source

Sections 8, 11, 12, and 20 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx), plus the current PoC files cited above.
