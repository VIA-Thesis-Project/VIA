# ADR-015: PostgreSQL polling for Agroclimatic Evaluation worker dispatch

## Status

Accepted.

## Context

ADR-005 requires long-running scientific calculations to execute outside the
HTTP process. Agroclimatic Evaluation now persists evaluations as `queued` and
provides `AgroclimaticEvaluationExecutionService`, which already owns lifecycle
claiming, sequential crop execution, per-crop outcome persistence, and fatal
failure handling.

A background worker needs a durable mechanism to discover pending work without
duplicating those Application semantics. The project does not currently require
an external message broker.

## Decision

Use the Agroclimatic Evaluation `evaluations` table as the current durable work
source.

A separate worker process polls evaluations whose status is `queued`, ordered by
`created_at` ascending and evaluation id as a deterministic tie-breaker. Polling
uses a bounded batch size.

The database is not locked while scientific execution runs. Multiple worker
processes may discover the same queued evaluation. The existing optimistic
`queued -> preparing` save remains the authoritative claim; a losing worker
treats the resulting conflict as benign and continues.

Add an index on `(status, created_at, id)` to support queued work discovery.

The worker delegates execution to `AgroclimaticEvaluationExecutionService`; it
does not duplicate lifecycle, crop iteration, result persistence, or scientific
failure semantics.

Worker/process death may leave an evaluation in `preparing`, `running`, or
`summarizing`. Recovery is explicit and fail-only: an operator-confirmed orphan
may be transitioned to `failed` using optimistic expected-status persistence.
Recovery does not retry, requeue, or fabricate missing crop outcomes.

## Consequences

PostgreSQL is both the durable evaluation store and the initial work-discovery
mechanism, avoiding a broker for the current scale.

There is no heartbeat, lease, automatic stale detection, automatic takeover,
retry policy, or cancellation mechanism. Those remain future decisions.

Polling contention can cause more than one worker to observe the same queued
row, but only one may claim it successfully.

Scientific execution remains sequential and no database transaction spans the
blocking CropSuiteLite call.