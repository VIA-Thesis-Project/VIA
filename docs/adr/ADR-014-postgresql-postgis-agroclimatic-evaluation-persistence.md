# ADR-013: PostgreSQL/PostGIS persistence for Agroclimatic Evaluation

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
`evaluations` and `evaluation_crops`.

Store the owned `ParcelSnapshot` directly with the evaluation: historical
`project_id` and `parcel_id`, positive parcel version, geometry, CRS, and capture
time. The identifiers have no foreign keys to Farm Management. Store geometry as
PostGIS `MULTIPOLYGON` with SRID 4326 and preserve the accepted public geometry
kind separately so Polygon and MultiPolygon round trips remain exact.

Store requested crops as ordered child rows. Position and crop uniqueness
constraints preserve deterministic order and reject duplicates at the database
boundary. The internal foreign key to `evaluations` is within the same bounded
context.

The domain recognizes the proposed lifecycle vocabulary, but this increment can
only create `queued` evaluations. It adds no transition methods, worker dispatch,
scientific run, result, evidence, or cancellation behavior.

## Consequences

Historical requests remain interpretable without joining current Farm
Management state. Snapshot geometry is intentionally duplicated at the bounded-
context boundary. A future authorized adapter may construct the transport-neutral
snapshot input from a Farm Management public contract, but the Evaluation
application and HTTP controller will not access Farm repositories directly.

Database constraints protect snapshot version, geometry kind and CRS, lifecycle
vocabulary, crop position, and crop uniqueness. Future lifecycle transitions and
scientific traceability records require separate increments and must preserve the
immutable request fields decided here.

## Source

This decision applies [ADR-001](ADR-001-modular-monolith.md),
[ADR-002](ADR-002-layered-bounded-contexts.md), and
[ADR-006](ADR-006-scientific-traceability.md), plus the target
[evaluation flow](../architecture/evaluation-flow.md).
