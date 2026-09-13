# ADR-014: PostgreSQL/PostGIS persistence for Agroclimatic Evaluation

## Status

Accepted

## Context

Agroclimatic Evaluation needs a durable request aggregate before asynchronous
scientific execution is introduced. Historical evaluations must keep the exact
parcel state they accepted even when Farm Management later appends another
`ParcelVersion`. Context ownership forbids Evaluation from reading Farm
Management ORM records or enforcing its history through cross-schema foreign
keys.

## Decision

Use the existing PostgreSQL/PostGIS, SQLAlchemy, GeoAlchemy2, psycopg, and Alembic
stack. Agroclimatic Evaluation owns schema `agroclimatic_evaluation` and tables
`evaluations`, `evaluation_crops`, and `crop_outcomes`.

Store the owned `ParcelSnapshot` directly with the evaluation: historical
`project_id` and `parcel_id`, positive parcel version, geometry, CRS, and capture
time. The identifiers have no foreign keys to Farm Management. Store geometry as
PostGIS `MULTIPOLYGON` with SRID 4326 and preserve the accepted public geometry
kind separately so Polygon and MultiPolygon round trips remain exact.

Store requested crops as ordered child rows. Position and crop uniqueness
constraints preserve deterministic order and reject duplicates at the database
boundary. The internal foreign key to `evaluations` is within the same bounded
context.

The domain implements explicit synchronous-execution transitions
`queued -> preparing -> running -> summarizing -> succeeded` and fatal active
transitions to `failed`. Repository saves use the expected prior status so only
one caller can claim a queued evaluation. A minimal failure reason is stored only
for overall orchestration failure.

Store one normalized outcome for each completed requested crop, keyed by
`(evaluation_id, crop_id)` and linked only to the same-context requested-crop
row. Preserve the current reliable suitability summary, scientific failure
message, and execution trace fields. Do not store engine workspaces, commands,
Python paths, internal CropSuiteLite paths, or invented versions.

Each lifecycle transition and per-crop outcome is committed in a short
transaction. Never keep the blocking scientific call inside a database
transaction. Worker dispatch, retry/recovery, cancellation, and the final
evidence/artifact model remain deferred.

## Consequences

Historical requests remain interpretable without joining current Farm
Management state. Snapshot geometry is intentionally duplicated at the bounded-
context boundary. A future authorized adapter may construct the transport-neutral
snapshot input from a Farm Management public contract, but the Evaluation
application and HTTP controller will not access Farm repositories directly.

Database constraints protect snapshot version, geometry kind and CRS, lifecycle
vocabulary, crop position, requested-crop uniqueness, one outcome per crop, and
basic outcome payload consistency. The current optimistic status check prevents
two callers from both claiming `queued`; recovery of an already-active
evaluation remains the responsibility of the future worker increment.

## Source

This decision applies [ADR-001](ADR-001-modular-monolith.md),
[ADR-002](ADR-002-layered-bounded-contexts.md), and
[ADR-006](ADR-006-scientific-traceability.md), plus the target
[evaluation flow](../architecture/evaluation-flow.md).
