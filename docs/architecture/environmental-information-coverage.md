# Environmental Information coverage and compatibility

## Capability

`POST /datasets/{dataset_id}/versions/{version_id}/coverage` checks one supplied
parcel-shaped geometry against one immutable `DatasetVersion`. The body contains
an explicit CRS and a GeoJSON Polygon or MultiPolygon. It is a query despite
using POST: arbitrary geometry is request input and neither the parcel nor the
dataset version is mutated or persisted.

The application contract is owned by Environmental Information. It contains
only geometry coordinates and CRS information; it does not import Farm
Management entities, repositories, ORM records, tables, or identifiers. A future
Agroclimatic Evaluation adapter may translate an authorized `ParcelVersion` or
`ParcelSnapshot` into this contract.

## Coverage semantics

- `full`: the registered rectangular dataset extent covers the complete parcel.
- `partial`: intersection area is positive but the extent does not cover the
  complete parcel.
- `none`: intersection area is zero.
- `not_assessed`: structural incompatibility prevented a meaningful comparison.

`none`, `partial`, nodata, and suitability zero are distinct. This increment
only compares the registered extent. Extent overlap does not prove that every
intersecting pixel contains valid scientific data.

## CRS and area policy

The dataset extent remains in its native EPSG CRS for traceability. The request
must state the parcel CRS explicitly; current Farm Management callers use
`EPSG:4326`. PostGIS confirms that both EPSG identifiers are registered, validates
the parcel topology, and transforms the parcel into the dataset CRS for
`ST_Covers` and `ST_Intersection`.

Areas are not calculated in longitude/latitude degrees. Parcel and intersection
geometries are transformed to EPSG:4326 and measured by PostGIS as WGS84
geography in square metres. Percentage is covered area divided by parcel area
and is bounded to 0–100. The response states the native comparison CRS, area
method, and transformations applied.

This approach transforms stored polygon vertices and is intended for the first
Huaura-scale rectangular-extent check. Larger regions or precision requirements
may require boundary densification or a reviewed local equal-area policy.

## Compatibility now

A version is structurally compatible when its existing positive-resolution and
ordered-extent invariants hold, the stored extent is a valid non-empty polygon,
its SRID matches the recorded EPSG CRS, and PostGIS can transform the relevant
CRSs. An untransformable dataset CRS returns `compatible: false` and
`coverage: not_assessed`; it is not reported as `none`. Invalid supplied geometry
or parcel CRS is a 422 request error.

The response includes dataset/version identity, compatibility, classification,
parcel and intersection areas, percentage, CRS/area interpretation fields,
warnings, and incompatibility reasons. Missing datasets or versions return 404.
Coverage requires the PostgreSQL/PostGIS application configuration; otherwise
the endpoint returns 503 while existing in-memory metadata CRUD remains usable.

## Deferred work

This increment does not inspect validity masks, nodata, pixels, raster/NetCDF
values, file formats, variables, precipitation units, periods, scenarios, or
CropSuiteLite inputs. It does not select among multiple versions, resample data,
run suitability calculations, or finalize `EnvironmentalInputManifest`.

Later Agroclimatic Evaluation work should consume this result through a
consumer-owned port, combine it with request period/scenario requirements, and
retain exact dataset versions/checksums and the immutable parcel snapshot under
ADR-006.
