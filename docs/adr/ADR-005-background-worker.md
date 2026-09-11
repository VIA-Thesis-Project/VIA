# ADR-005: Background worker for long calculations

## Status

Accepted

## Context

CropSuiteLite calculations are blocking and resource-intensive. Keeping an HTTP request open would tie API availability to scientific execution and would not survive process or network interruption reliably.

## Decision

Persist the evaluation, schedule it recoverably, return an identifier, and execute the scientific work in a background worker outside the HTTP process. Clients obtain progress and results through polling initially.

## Consequences

The system needs durable state, idempotent task handling, bounded concurrency, retry classification, and recovery after restart. An outbox or equivalent is proposed for reliable persistence-to-queue coordination. Celery and Redis are candidates in a Python implementation, not settled requirements.

## Current implementation status

The current CLI runs synchronously and has no durable queue, recovery, cancellation, or polling API. It does isolate each crop in a subprocess and records progress in a local manifest.

## Source

Sections 12, 16, 18, and 20 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx) and [`CropSuiteLite/src/multicrop.py`](../../CropSuiteLite/src/multicrop.py).
