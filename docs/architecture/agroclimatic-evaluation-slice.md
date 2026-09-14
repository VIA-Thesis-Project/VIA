# Agroclimatic Evaluation request, worker, recovery, and read slice

## Ownership

Agroclimatic Evaluation owns the durable `Evaluation` aggregate, its immutable
`ParcelSnapshot`, ordered requested crop identifiers, lifecycle status, creation
time, minimal per-crop outcomes, scientific trace fields, and any orchestration
failure reason. Farm Management continues to own `Project`, `Parcel`, and
`ParcelVersion`; Environmental Information continues to own `Dataset` and
`DatasetVersion`.

The creation use case receives explicit transport-neutral snapshot data. It does
not import another context's domain model, repository, ORM record, table, or
session. A later composition adapter may obtain an authorized parcel description
through a public Farm Management contract.

## ParcelSnapshot

The snapshot contains historical `project_id` and `parcel_id` traceability
identifiers, the exact positive parcel version, a deeply immutable GeoJSON Polygon
or MultiPolygon, `EPSG:4326`, and the timezone-aware capture time. It is copied
into the Evaluation-owned schema so later Farm changes cannot reinterpret an old
request. Cross-context foreign keys are intentionally absent because identifiers
record provenance; they do not transfer ownership to Evaluation.

PostgreSQL stores the geometry as `MULTIPOLYGON(4326)` and retains the original
Polygon/MultiPolygon kind for public round trips, following the established Farm
Management geometry convention without sharing its ORM mapping.

## Current lifecycle and execution

The domain vocabulary is `queued`, `preparing`, `running`, `summarizing`,
`succeeded`, `failed`, and `cancelled`, as proposed by the target architecture.
New evaluations start `queued`. The synchronous Application executor implements
`queued -> preparing -> running -> summarizing -> succeeded` plus fatal
transitions from active states to `failed`. Explicit domain methods protect these
transitions; arbitrary status assignment is not used by the orchestrator.

Execution depends only on the Evaluation repository contract and
`ICropSuitabilityEngine`. Requested crops execute sequentially in their persisted
order. Each returned per-crop outcome is committed before the next crop starts,
and lifecycle transitions are committed outside the long-running scientific
call. The `(evaluation_id, crop_id)` key prevents duplicate outcomes in the
current no-retry model.

Per-crop `failed` is a reported scientific outcome, so it is persisted and later
crops continue. `no_coverage` is distinct from failure and from a valid
`succeeded` score of zero. Overall `succeeded` records completed orchestration and
may contain any mixture of these three per-crop outcomes. Overall `failed` is
reserved for a boundary or orchestration exception that prevents completion.

A separate `via-worker run` process now polls PostgreSQL for a bounded set of
`queued` evaluation IDs ordered by `created_at ASC, id ASC`. Evaluation remains
the durable work source; there is no generic job table or broker. Discovery holds
no transaction during science. Multiple worker processes may discover the same
ID, but the executor's optimistic `queued -> preparing` save permits one claim;
the loser treats `ResourceConflictError` as benign and continues. One worker
process handles evaluations sequentially.

The worker's `run_once()` is finite and testable. The long-running host repeats
it, sleeping after a non-full batch, and uses standard logging. A persisted
orchestration failure does not stop later work. A failure that was not persisted
as `failed` escapes instead of being silently swallowed as ordinary work.

The current versioned REST surface is:

- `POST /api/v1/evaluations` persists a request and returns `201 Created`;
- `GET /api/v1/evaluations` returns requests in deterministic creation order;
- `GET /api/v1/evaluations/{evaluation_id}` returns polling status and persisted counts;
- `GET /api/v1/evaluations/{evaluation_id}/result` returns currently persisted ordered outcomes;
- `GET /api/v1/evaluations/{evaluation_id}/evidence` returns the safe current evidence subset.

The status resource reports `requested_crop_count`, `completed_crop_count`, and
lifecycle `status`; it does not invent a numeric percentage. Result availability
is `pending`, `partial`, `final`, or `failed`. Only overall `succeeded`
is final. Overall failure is public as a safe boolean/availability state while
persisted orchestration and crop diagnostic messages remain internal.

## Read contracts and current evidence

The read use cases are immutable `GetEvaluation`, `GetEvaluationResult`, and
`GetEvaluationEvidence` queries over the existing aggregate repository. No
separate read store or schema is introduced. They do not claim work, mutate
lifecycle state, invoke the scientific engine, or control the worker.

The HTTP evidence resource exposes the currently reliable persisted fields:
`engine_identifier`, `started_at`, `finished_at`, `elapsed_seconds`,
`execution_mode`, `parcel_sha256`, `parameter_sha256`,
`configuration_sha256`, and `source_files_unchanged`. It omits the opaque
`execution_reference` because it may encode an internal execution location, and
it omits raw failure diagnostics.

The Application `public.py` module deliberately publishes
`FinalizedEvaluationResult`, its immutable nested values, and
`FinalizedEvaluationResultReader` for future local cross-context use. The
reader returns a contract only for overall `succeeded` evaluations. It exposes
no Evaluation aggregate, repository, ORM mapping, table, CropSuite adapter, or
CropSuiteLite type.

Decision Support behavior is still absent. Independent per-crop means are not
ranked because they do not prove the common valid spatial support required by
ADR-009. No common coverage is reconstructed from independent coverage fractions.


## Deliberately deferred

This slice also provides explicit fail-only orphan recovery. An operator-confirmed
evaluation in `preparing`, `running`, or `summarizing` can be transitioned to
`failed` with a required reason and optimistic expected-status save. Existing
outcomes are preserved; missing outcomes are not fabricated; no retry or requeue
occurs. `queued`, terminal states, and stale concurrent recovery commands are
rejected.

A crashed or interrupted worker may leave an active evaluation until an operator
recovers it. There is deliberately no heartbeat, lease, automatic stale timeout,
takeover, retry, requeue, mid-CropSuite cancellation, or public recovery endpoint.
Blind time-based recovery would be unsafe because valid scientific runs may be
long.

This slice does not implement Farm or Environmental Information adapters,
authorization, coverage selection, `EnvironmentalInputManifest`, dataset-version
selection, outbox or broker publication, HTTP-triggered CropSuiteLite execution,
automatic retries, cancellation, final scientific-run or evidence persistence,
recommendations, or LLM/RAG. The separate scientific engine boundary is
documented in [`cropsuite-integration.md`](cropsuite-integration.md).

Persistence follows
[ADR-014](../adr/ADR-014-postgresql-postgis-agroclimatic-evaluation-persistence.md);
PostgreSQL polling and explicit recovery follow
[ADR-015](../adr/ADR-015-postgresql-polling-evaluation-worker.md).
