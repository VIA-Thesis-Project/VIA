# ADR-011: PostgreSQL/PostGIS persistence for Farm Management

## Status

Accepted

## Context

The existing Farm Management vertical slice owns `Project`, `Parcel`, immutable
`ParcelVersion` history, and geometry, but its first Infrastructure adapters are
process-local. The next increment requires durable storage without exposing ORM,
database-session, or spatial-database concerns to Domain or Application.

## Decision

Use PostgreSQL with PostGIS, SQLAlchemy 2.x, GeoAlchemy2, psycopg 3, and Alembic
for Farm Management persistence. Farm Management owns the `farm_management`
schema and the `projects`, `parcels`, and `parcel_versions` tables. SQLAlchemy
records remain Infrastructure types and are mapped explicitly to existing domain
entities.

Store parcel snapshots in a PostGIS `MULTIPOLYGON` column with SRID 4326. Promote
Polygon input to a one-member MultiPolygon for storage and retain its public
geometry kind separately so API round trips preserve the existing Polygon versus
MultiPolygon contract.

Persist a revision by conditionally advancing `parcels.current_version` from the
caller's expected version and inserting the next immutable `parcel_versions` row
in the same transaction. A composite primary key on `(parcel_id, number)` is the
database backstop against duplicate version numbers. Database conflicts are
translated to the existing `ParcelVersionConflictError` contract.

## Consequences

Production composition can select durable repositories through environment
settings while isolated tests retain the in-memory adapters. A database role used
for the initial migration must be able to enable PostGIS, or PostGIS must already
be provisioned. The migration does not remove the shared PostGIS extension on
downgrade.

This decision does not choose persistence for other bounded contexts, authorize
cross-context table access, or change Farm Management domain behavior.
