# Agroclimatic Evaluation request and synchronous execution slice

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

The current REST surface is:

- `POST /evaluations` — persist a request and return `201 Created`;
- `GET /evaluations/{evaluation_id}` — return one request or `404`;
- `GET /evaluations` — return requests in deterministic creation order.

`201` is used instead of the future illustrative `202` because no execution is
scheduled in this slice. Invalid domain input returns `422`; a persistence identity
conflict maps to `409`.

## Deliberately deferred

This slice does not implement Farm or Environmental Information adapters,
authorization, coverage selection, `EnvironmentalInputManifest`, dataset-version
selection, outbox or broker publication, worker execution, HTTP-triggered
CropSuiteLite execution, retries, recovery, cancellation, final scientific-run
or evidence persistence, recommendations, or LLM/RAG. The separate scientific
engine boundary is documented in
[`cropsuite-integration.md`](cropsuite-integration.md).

Persistence follows
[ADR-014](../adr/ADR-014-postgresql-postgis-agroclimatic-evaluation-persistence.md).
