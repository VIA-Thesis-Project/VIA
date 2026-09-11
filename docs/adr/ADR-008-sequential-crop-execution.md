# ADR-008: Sequential crop execution

## Status

Implemented in PoC

## Context

CropSuiteLite can create internal processes and uses configuration, temporary directories, and outputs that require isolation. Running many crops or evaluations concurrently can multiply CPU, memory, time, and storage use.

## Decision

Execute selected crops sequentially for one evaluation, in an isolated subprocess and work directory per crop. Limit the engine's internal process count with the existing `max_workers` control. Start the future deployment with one heavy evaluation at a time until measurements justify another limit.

## Consequences

Isolation prevents output and configuration collisions and lets a later crop continue after another fails. Runtime and storage grow with crop count because each crop currently prepares and retains its own derived climate data. Compatible reuse and caching remain future decisions and must never bypass manifest checks.

## Current implementation status

Implemented by [`CropSuiteLite/src/multicrop.py`](../../CropSuiteLite/src/multicrop.py) and exposed by [`CropSuiteLite/evaluate.py`](../../CropSuiteLite/evaluate.py). Future queue concurrency, shared preparation, cache identity, and retention are pending.

## Source

Sections 11, 12, 20, and 22 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx), [`CropSuiteLite/src/multicrop.py`](../../CropSuiteLite/src/multicrop.py), and [`CropSuiteLite/tests/test_multicrop.py`](../../CropSuiteLite/tests/test_multicrop.py).
