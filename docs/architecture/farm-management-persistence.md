# Farm Management persistence

Farm Management uses the accepted technology in
[`ADR-011`](../adr/ADR-011-postgresql-postgis-farm-persistence.md). Its durable
adapter is optional at composition time; the in-memory adapter remains available
for unit and API tests.

## Ownership and schema

The bounded context owns PostgreSQL schema `farm_management`:

| Table | Purpose |
|---|---|
| `projects` | Project identity, name, and creation time. |
| `parcels` | Parcel identity, owning project, stable metadata, and current version. |
| `parcel_versions` | Immutable geometry snapshot and timestamp for each version. |

`parcel_versions` has a composite primary key on `(parcel_id, number)`. Geometry
is stored as two-dimensional PostGIS `MULTIPOLYGON` with SRID 4326 and a GiST
index. A separate geometry-kind field preserves whether the accepted GeoJSON was
a Polygon or MultiPolygon. No ORM record crosses the Infrastructure boundary.

## Revision concurrency

The repository conditionally changes `parcels.current_version` from
`expected_version` to the next number and inserts that immutable version in one
transaction. A stale writer updates no row and receives the existing application
conflict response. The composite primary key independently rejects duplicate
version storage. Earlier rows are never updated.

## Local database and migrations

Copy `backend/.env.example` to `backend/.env`, replace the local password, and
load those variables in the shell. Then run from `backend/`:

```powershell
docker compose up -d postgis
python -m alembic upgrade head
python -m pytest -m integration
```

`VIA_DATABASE_URL` selects PostgreSQL automatically when
`VIA_FARM_MANAGEMENT_REPOSITORY` is omitted. With neither setting, the application
uses process-local memory. Integration tests additionally require
`VIA_TEST_DATABASE_URL`; by default, its database name must end in `_test`.
Dedicated, disposable externally managed PostgreSQL test databases whose names
cannot follow that convention require the explicit test-only opt-in
`VIA_ALLOW_EXTERNAL_TEST_DATABASE=1`. The guard runs before Alembic or table
cleanup, does not affect `VIA_DATABASE_URL`, and is not provider-specific. Never
point destructive integration tests at a database containing development or
production data. Alembic remains the source of truth for creating VIA's schemas.

The first migration enables PostGIS when permitted, creates only the Farm
Management schema and tables, and leaves the shared extension installed during a
downgrade.

## Open decisions

Backups, recovery objectives, managed-database provider, connection-pool sizing,
and production credential delivery remain deployment decisions. Persistence for
other bounded contexts requires their own ownership decision and migrations.
