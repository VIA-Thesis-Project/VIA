# ADR-012: PostgreSQL/PostGIS persistence for Environmental Information

## Status

Accepted

## Context

Environmental Information needs a durable catalog for stable datasets and
immutable dataset versions. Each version must retain source-grid metadata and an
extent suitable for future compatibility and coverage checks without importing
raster or NetCDF data into the transactional database.

The architecture requires context-owned persistence, exact input versions and
checksums for scientific traceability, and storage references that can move from
local persistent storage to object storage without changing Domain.

## Decision

Use PostgreSQL/PostGIS through the backend's existing SQLAlchemy, GeoAlchemy2,
psycopg, and Alembic stack. Environmental Information owns schema
environmental_information and tables datasets and dataset_versions. There are
no foreign keys to another bounded context.

Dataset is the stable logical identity and retains name, source, environmental
variable, unit, and creation time. DatasetVersion is immutable and retains its
own UUID, a provider-facing version identifier unique within its dataset, EPSG
CRS, two-axis spatial resolution and resolution unit, rectangular extent,
optional validity bounds and scenario, checksum, opaque storage reference, and
registration time.

Store each extent as a two-dimensional PostGIS POLYGON in the version's native
EPSG CRS, with a GiST index. The polygon is the rectangular catalog extent, not
a validity mask and not a coverage result. The geometry column permits different
SRIDs, while a database check ensures the recorded EPSG code matches the
geometry SRID. The first slice accepts EPSG identifiers only.

Keep engine and session-factory construction in host-level Infrastructure so
multiple contexts can share a pool without importing another context's
Infrastructure. Each context retains its own declarative metadata, records,
repositories, schema, and migration ownership.

## Consequences

Future coverage logic can use indexed extent prefilters and transform known
EPSG geometries, but it must still consider validity masks, periods, scenarios,
resolution, units, and compatibility. A bounding extent cannot establish usable
pixel coverage.

Checksums and storage references are intentionally opaque in Domain. This slice
does not choose a checksum algorithm, resolve references to filesystem paths or
object-store URLs, validate file contents, or load rasters/NetCDF. Infrastructure
may later translate the reference through a storage adapter.

Non-EPSG CRS definitions, exact validity-mask persistence, layer/file format
metadata, dataset retirement, and metadata correction workflows remain open.
Because versions have no update use case, corrections require a new version in
this increment.

## Source

This decision applies the Environmental Information ownership described in
[bounded-contexts.md](../architecture/bounded-contexts.md), the geoenvironmental
catalog requirements in the original architecture source, and scientific
traceability from [ADR-006](ADR-006-scientific-traceability.md).
