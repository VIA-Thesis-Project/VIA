# ADR-005: Background worker for long calculations

## Status

Accepted

## Context

CropSuiteLite calculations are blocking and resource-intensive. Keeping an HTTP request open would tie API availability to scientific execution and would not survive process or network interruption reliably.

## Decision

Persist the evaluation, return an identifier, and execute scientific work in a separate PostgreSQL-polling worker outside the HTTP process. Queue discovery is read-only: `list_queued_ids()` returns candidates in `created_at, id` order. The authoritative claim is the optimistic status compare-and-swap `QUEUED -> PREPARING`; concurrent workers may discover the same row, but only one can claim it and the loser treats the conflict as benign contention.

Scientific calls run outside database transactions. A scientific/integration failure that the Application service durably records transitions the evaluation to `FAILED`; the worker counts it and continues. An unexpected failure that cannot be durably represented as `FAILED` escapes the worker process so the process supervisor can restart it. There is no automatic evaluation retry, automatic requeue, or replay of partial scientific work.

Graceful process shutdown is cooperative. SIGINT and SIGTERM set a process-local stop event. The worker checks it between evaluations, so it does not claim new work after shutdown is requested; an already-running synchronous CropSuiteLite call is allowed to finish. A hard process/container kill can still leave `PREPARING`, `RUNNING`, or `SUMMARIZING` state behind.

Operators can list those exact active states with `via-worker active`. Active age is informational only: `active` does not mean `orphaned`, and elapsed time alone is not used to classify or recover work. After independently confirming that the owning process is gone, an operator may run `via-worker recover <id> --expected-status preparing|running|summarizing --reason <text>`. Recovery fails the evaluation only when the persisted state still matches the operator-observed expected state.

## Consequences

The current claim model needs no lease, heartbeat, worker identifier, distributed queue, or long-lived transaction. Worker liveness belongs to the process/container supervisor. API `GET /health` remains API-process readiness only and does not claim to report worker liveness.

There is intentionally no automatic orphan detection because no durable heartbeat or status-change timestamp exists. Recovery is explicit and status-aware. Existing crop outcomes are retained when an active evaluation is recovered to `FAILED`; missing outcomes are not fabricated.

`EvaluationStatus.CANCELLED` remains part of the domain vocabulary, but A7 does not define active scientific cancellation. SIGTERM does not map to `CANCELLED`, and the worker does not terminate an in-flight CropSuiteLite process.

## Current implementation status

The backend has a separate `via-worker run` process, PostgreSQL-backed queue discovery and CAS claiming, explicit active listing and recovery commands, persisted per-crop outcomes, cooperative SIGINT/SIGTERM shutdown, and fail-fast systemic error handling. There is no automatic retry, lease/heartbeat, distributed queue, automatic orphan recovery, or active cancellation workflow.

## Source

Sections 12, 16, 18, and 20 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx) and [`CropSuiteLite/src/multicrop.py`](../../CropSuiteLite/src/multicrop.py).
