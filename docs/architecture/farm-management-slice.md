# Farm Management minimum vertical slice

## Scope

The first Farm Management increment implements a transport-to-domain path for projects and parcels. It supports:

- creating, listing, and retrieving agricultural projects;
- creating, listing, and retrieving parcels within a project;
- accepting GeoJSON `Polygon` and `MultiPolygon` parcel geometry; and
- appending immutable parcel geometry versions while retaining earlier versions.

The HTTP resources delegate to Application commands and queries. Application coordinates the `Project` and `Parcel` domain model through repository abstractions. Infrastructure supplies both process-local in-memory adapters and the durable PostgreSQL/PostGIS adapters described in [`farm-management-persistence.md`](farm-management-persistence.md). The FastAPI composition root selects and wires an implementation from environment settings.

## HTTP resources

| Method | Resource | Purpose |
|---|---|---|
| `POST` | `/projects` | Create a project. |
| `GET` | `/projects` | List projects. |
| `GET` | `/projects/{project_id}` | Retrieve a project. |
| `POST` | `/projects/{project_id}/parcels` | Create a parcel with geometry version 1. |
| `GET` | `/projects/{project_id}/parcels` | List a project's parcels. |
| `GET` | `/projects/{project_id}/parcels/{parcel_id}` | Retrieve a parcel and its geometry history. |
| `POST` | `/projects/{project_id}/parcels/{parcel_id}/versions` | Append a geometry version. |

## Invariants in this increment

- Project and parcel names are trimmed, non-empty, and at most 120 characters.
- A parcel belongs to exactly one project and begins with geometry version 1.
- Geometry versions are contiguous, ordered, and immutable.
- Geometry is a non-empty GeoJSON Polygon or MultiPolygon with closed rings, finite two-dimensional positions, and valid longitude/latitude ranges.
- A parcel cannot be retrieved or revised through a different project resource.

These checks are structural. This increment does not claim full GIS topology validation, Huaura coverage validation, or environmental-data availability.

## Explicit exclusions and provisional choices

This slice does not implement authentication or authorization, delete/rename operations, environmental coverage, evaluation requests, background workers, `ICropSuitabilityEngine`, or `CropSuiteAdapter`. It neither imports nor invokes CropSuiteLite.

The in-memory repositories remain replaceable Infrastructure adapters for development and tests and lose data when the process restarts. The durable adapter resolves Farm Management's persistence technology, schema, and optimistic-concurrency mechanism in [`ADR-011`](../adr/ADR-011-postgresql-postgis-farm-persistence.md); it does not settle aggregate or persistence choices for other contexts. Authorization must be added through the Identity and Access public collaboration before these resources are exposed as a protected production API.

## Architectural alignment

The implementation follows accepted [`ADR-001`](../adr/ADR-001-modular-monolith.md) and [`ADR-002`](../adr/ADR-002-layered-bounded-contexts.md). Commands and queries are placed in Application in line with the still-recommended, pending-confirmation [`ADR-003`](../adr/ADR-003-commands-queries-in-application.md); this increment does not change that ADR's status.
