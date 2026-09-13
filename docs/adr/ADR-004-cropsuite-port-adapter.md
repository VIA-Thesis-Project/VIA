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

The Application port and Infrastructure adapter are implemented in Agroclimatic
Evaluation. `CropSuiteAdapter` launches an explicitly configured scientific
Python interpreter in an isolated process; that process imports and invokes the
blocking [`run_evaluation(...)`](../../CropSuiteLite/src/multicrop.py) capability
for one crop. The existing CropSuiteLite capability then retains its own isolated
subprocess call to
[`scripts/run_evaluation_engine.py`](../../CropSuiteLite/scripts/run_evaluation_engine.py).

This keeps CropSuiteLite scientific dependencies outside the VIA backend Python
environment. The adapter is not connected to HTTP or a worker, and
result/evidence persistence remains deferred.

## Source

Sections 8, 11, 12, and 20 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx), plus the current PoC files cited above.
