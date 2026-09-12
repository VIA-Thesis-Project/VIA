# ADR-013: Extent coverage and CRS comparison

## Status

Accepted

## Context

Environmental Information must answer whether a registered `DatasetVersion`
spatially covers a supplied parcel geometry before any raster values are loaded.
Dataset extents are retained in their native EPSG CRS, while current Farm
Management parcel geometry is represented in EPSG:4326. Coverage must not imply
pixel-level availability, and longitude/latitude degrees are not meaningful area
units.

## Decision

Keep the native-CRS extent selected by ADR-012; do not add a normalized extent
column. Accept parcel geometry through an Environmental Information public
boundary value containing GeoJSON Polygon or MultiPolygon coordinates and an
explicit EPSG CRS. Environmental Information does not import or persist Farm
Management types.

Use PostGIS to validate topology, transform the parcel into the dataset extent's
native CRS, and classify the extent relationship. `full` means the registered
extent covers the whole parcel, `partial` means the intersection has positive
area but does not cover the whole parcel, and `none` means the intersection has
zero area. `not_assessed` is reserved for structurally incompatible metadata and
is not the same as no coverage.

Measure parcel and intersection areas with `ST_Area` on WGS84 geography after
transforming the relevant geometry to EPSG:4326. Return square metres and derive
percentage as intersection area divided by parcel area, bounded to 0–100. Record
the comparison CRS, transformation description, and area method in the result.

Compatibility in this increment means that the registered extent is valid, its
recorded CRS matches its stored SRID, the dataset and parcel EPSG CRSs are known
to PostGIS and transformable, and registered resolution/extent invariants hold.
Validity period and scenario matching are deferred because the request has no
time or scenario context.

## Consequences

The coverage endpoint requires the PostgreSQL/PostGIS configuration; metadata
CRUD can continue to use in-memory repositories for isolated tests. The result
is transport-neutral and can later be consumed through an Agroclimatic
Evaluation port, but it is not the final `EnvironmentalInputManifest`.

Coverage is based only on the rectangular catalog extent. It does not inspect a
validity mask, nodata, pixels, variables, units beyond existing metadata
invariants, or storage contents. Transforming stored polygon vertices and using
geography area is appropriate for this first Huaura-oriented extent check, but
future large-area or high-precision requirements may require densification or a
reviewed local equal-area CRS policy.

No schema change or cross-context foreign key is introduced.
