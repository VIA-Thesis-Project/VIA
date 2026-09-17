# Production deployment runtime contract

B1 defines the provider-neutral runtime contract for VIA before container image
work. It does not select a hosting provider or build a Docker image.

## Process topology

```text
PostgreSQL/PostGIS
      |
  +---+---+
  |       |
 API    Worker
          |
     CropSuiteLite
```

The API and worker are separate OS/container processes. A later deployment may
run both process types from one image only if that image contains the complete
VIA and scientific runtime.

The production API application factory is
`via_backend.app:create_production_app`. The `via_backend.app` module is a
side-effect-free composition module: importing it does not instantiate a
FastAPI application. The production factory resolves environment settings,
requires PostgreSQL persistence for all three currently persisted bounded
contexts, and then delegates to the shared application composition root. The
development-compatible `via_backend.main:app` remains available and may still
use in-memory repositories when `VIA_DATABASE_URL` is absent.

## Process responsibilities

The API process serves HTTP, uses PostgreSQL persistence in production, and does
not execute CropSuiteLite. It does not apply Alembic migrations during startup.

The worker process uses PostgreSQL polling to discover queued evaluations,
executes CropSuiteLite through the existing Infrastructure adapters, and
preserves durable scientific artifacts. `via-worker run` is the scientific
worker process. SIGINT and SIGTERM request cooperative shutdown: the worker stops
claiming new evaluations between items and allows an already-running synchronous
scientific call to finish. `via-worker active` and `via-worker recover` remain
separate, explicit operator commands; they are not automatic recovery behavior.

## Production process commands

The same OCI image serves the API, worker, and one-shot release migration roles,
with exactly one process role per container:

```text
API process:        via-api
Worker process:     via-worker run
Release migration: via-migrate upgrade
Operator commands: via-worker active
                   via-worker recover ...
```

The image default is the exec-form command `CMD ["via-api"]`. A worker
deployment overrides the image command with `via-worker run`. A release job
overrides it with `via-migrate upgrade`. No shell wrapper, Supervisor, systemd,
or combined launcher sits between the container runtime and the selected
process, so SIGINT/SIGTERM are delivered directly to API or worker processes.

`via-api` starts one Uvicorn process using factory semantics against
`via_backend.app:create_production_app`. It binds `0.0.0.0` by default on port
`8000`; `VIA_API_HOST` and `VIA_API_PORT` override those values. Production
persistence is validated before Uvicorn serves requests. Reload mode is not
enabled.

`via-backend` remains the development/local compatibility command and continues
to serve `via_backend.main:app` on its existing development defaults. It is not
the production process command.

Database migration is a separate one-shot release operation:

```text
via-migrate upgrade
```

`via-migrate upgrade` validates the production persistence contract and invokes
Alembic programmatically with target `head`. It accepts no arbitrary revision,
downgrade, revision-generation, or autogenerate operation. Neither `via-api` nor
`via-worker run` applies migrations during startup.

## Database and migration contract

`VIA_DATABASE_URL` is the database contract shared by the production API,
worker, and Alembic release operation. API startup and worker startup never run
migrations automatically.

For each release, `via-migrate upgrade` is run before processes that require the
new schema are deployed or restarted. The command requires the same production
PostgreSQL persistence configuration as the application, applies `alembic
upgrade head`, and exits after Alembic reaches head. Running it again when the
database is already at head is safe and leaves the schema unchanged. Migration
failures and invalid configuration propagate as a non-zero process exit; B4 does
not add application-level retries, locks, leader election, or automatic rollback.

Release orchestration is provider-neutral and conceptually ordered as:

```text
build/release image
       |
       v
via-migrate upgrade
       |
    success
       |
       +------> deploy/restart API
       |
       +------> deploy/restart worker
```

The migration role is responsible only for schema evolution. Deployment
orchestration is responsible for ensuring that the intended release migration
job runs before application processes depend on the new schema.

## Filesystem contract

Runtime paths are deployment configuration and must be absolute or otherwise
resolved independently of the process current working directory. The execution
workspace and durable artifacts root have different lifecycle requirements.

| Resource | Access | Requirement | Persistence / placement |
| --- | --- | --- | --- |
| CropSuiteLite engine root | Read-only | Required by worker | Persistent with deployed code/image |
| Scientific source datasets | Read-only | Required by scientific execution | Deployment-provided inputs |
| Scientific input bindings | Read-only | Required | Deployment configuration |
| Source config/catalog | Read-only | Optional under current configuration | Deployment configuration |
| CropSuite execution workspace | Writable | Required by scientific execution | Temporary/disposable and outside the CropSuiteLite engine tree |
| Scientific artifacts root | Writable | Required by scientific execution | Durable; must survive worker/container replacement |

The execution workspace is disposable process state and is not durable evidence.
`VIA_ARTIFACTS_ROOT` stores durable scientific evidence. Any artifact reference
persisted in PostgreSQL is unsafe if it points to a filesystem that disappears
whenever a worker or container is replaced, so production must mount or provide
artifact storage with the required lifetime.

Scientific source datasets, input bindings, and any configured source
config/catalog are immutable runtime inputs from the worker's perspective.
CropSuiteLite's engine/source tree is also immutable. `VIA_CROPSUITE_WORKSPACE`
must remain outside `VIA_CROPSUITE_ROOT`, matching the existing adapter guard.

## Environment contract

The production API server uses `VIA_API_HOST` (default `0.0.0.0`) and
`VIA_API_PORT` (default `8000`). Production persistence requires a non-empty
`VIA_DATABASE_URL`. When the repository selectors are absent,
`Settings.from_env()` selects PostgreSQL for all three persisted contexts from
that database URL. If `VIA_FARM_MANAGEMENT_REPOSITORY`,
`VIA_ENVIRONMENTAL_INFORMATION_REPOSITORY`, or
`VIA_AGROCLIMATIC_EVALUATION_REPOSITORY` is set explicitly, production requires
each selected value to be `postgresql`.

The worker additionally uses `VIA_WORKER_POLL_INTERVAL_SECONDS`,
`VIA_WORKER_BATCH_SIZE`, `VIA_CROPSUITE_ROOT`, `VIA_CROPSUITE_PYTHON`,
`VIA_CROPSUITE_WORKSPACE`, `VIA_ARTIFACTS_ROOT`,
`VIA_CROPSUITE_INPUT_BINDINGS`, optional `VIA_CROPSUITE_SOURCE_CONFIG` and
`VIA_CROPSUITE_CATALOG`, and `VIA_CROPSUITE_MAX_WORKERS`.

`VIA_POSTGRES_DB`, `VIA_POSTGRES_USER`, `VIA_POSTGRES_PASSWORD`, and
`VIA_POSTGRES_PORT` configure the repository's local PostGIS Compose service.
They are not the API/worker database contract. `VIA_TEST_DATABASE_URL` and
`VIA_ALLOW_EXTERNAL_TEST_DATABASE` are integration-test controls only and are
not production runtime variables.

`VIA_ALEMBIC_CONFIG` is a structural path used only by the release migration
host. The standard OCI image sets it to `/opt/via/backend/alembic.ini`, so normal
container deployments do not need to override it. Source development can omit
the variable because `via_backend.migrate` resolves `backend/alembic.ini`
relative to its source module rather than the process current working directory.
If the variable is explicitly set, it must be non-empty and reference an
existing file. The path contains no credentials; `VIA_DATABASE_URL` remains the
single database URL consumed by Alembic through `migrations/env.py`.

See `backend/.env.example` for local development and
`backend/.env.production.example` for portable production path examples.

## B2 reproducible Linux container image

The root [`Dockerfile`](../../Dockerfile) packages the VIA backend and
CropSuiteLite into one provider-neutral Linux image based on
`python:3.11-slim-bookworm`. Both VIA and CropSuiteLite use the same interpreter,
`/usr/local/bin/python`. B2 installs one explicitly justified Debian runtime
package:

```text
libexpat1
    Required at runtime by the Rasterio/GDAL wheel dependency chain.
    Discovered by the Linux container smoke, not guessed in advance.
```

The selected scientific wheels must still prove their remaining Linux runtime
requirements during the real image build and smoke verification.

CropSuiteLite's source requirements are not rewritten. Repository inspection found
no `tkinter`, `from tkinter`, or `import tk` usage in the VIA scientific path
(`src.multicrop` and the engine code it launches). The `tk` line is therefore a
non-portable packaging artifact for this runtime and only that exact line is
excluded from the container installation. No other scientific dependency or
version is changed.

The build runs
[`backend/scripts/verify_container_runtime.py`](../../backend/scripts/verify_container_runtime.py)
as the final non-root `via` user and fails unless all of the following are true:

- the build is running on Linux with Python 3.11 or newer;
- `VIA_CROPSUITE_PYTHON` is the interpreter executing the verification;
- `via_backend` and the worker module import successfully;
- `via-api`, `via-backend`, `via-worker`, and `via-migrate` are installed on `PATH`;
- the scientific stack imports successfully, including rasterio, pyproj,
  shapely, cartopy, netCDF4, scipy, numba, xarray, rio-cogeo, dask,
  scikit-image, and related dependencies;
- `python -m pip check` succeeds;
- the expected CropSuiteLite entrypoint/source files exist and `src.multicrop`
  imports using the same scientific interpreter;
- the runtime UID is not root;
- `/opt/via/CropSuiteLite` is not writable by the runtime user; and
- `/var/lib/via/workspace` and `/var/lib/via/artifacts` are writable by that user.

B2 intentionally stopped before defining a VIA `CMD` or `ENTRYPOINT`. B3 adds
the exec-form default `CMD ["via-api"]` while retaining no `ENTRYPOINT` wrapper.
B4 adds `via-migrate upgrade` as an explicit command override while keeping the
default image role unchanged. Schema migration is never run by image startup.

Runtime processes use the non-root `via` user. `/opt/via/CropSuiteLite` and the
backend code remain image-owned read-only inputs. `/var/lib/via/workspace` is the
disposable CropSuite execution workspace and `/var/lib/via/artifacts` is the
writable artifact path; production still has to place the artifact path on
durable storage. `VIA_CROPSUITE_INPUT_BINDINGS`, scientific datasets, and any
optional source config/catalog remain deployment-provided read-only inputs and
are intentionally not baked into the image. `HOME=/tmp` and
`MPLCONFIGDIR=/tmp/matplotlib` keep Matplotlib's runtime cache/configuration in
temporary storage for the non-root process rather than in a persistent path.

Build from the repository root so both `backend/` and `CropSuiteLite/` are in
the Docker build context:

```text
docker build -t via:b4 .
docker run --rm via:b4 python /opt/via/backend/scripts/verify_container_runtime.py --require-linux
docker run --rm via:b4 python --version
docker run --rm via:b4 python -m pip check
docker run --rm via:b4 via-worker --help
docker run --rm -e VIA_DATABASE_URL=<postgresql-url> via:b4 via-migrate upgrade
```

B2-B4 do not choose a hosting provider, add scientific datasets to the image,
alter CropSuiteLite scientific requirements or behavior, change artifact-storage
semantics, or change worker lifecycle. B5 still owns durable artifact storage
mounting/configuration.

The existing Linux container workflow proves the B3 process contract and the B4
release migration contract.
It starts the image using its default command with a syntactically valid but
unreachable PostgreSQL URL, polls `/health`, then performs a normal
`docker stop --time 10`. The health endpoint is technical API-process readiness
and application composition only constructs the SQLAlchemy engine, so this smoke
does not require a live database connection. The same workflow verifies the
worker CLI through command override and asserts that `via-worker run` exits
non-zero when required scientific configuration is missing.

For B4, the workflow additionally starts a temporary `postgis/postgis:16-3.5`
database on an isolated Docker network, runs `via-migrate upgrade` from the VIA
image, verifies the database revision equals the single dynamically discovered
repository Alembic head, runs the migration command a second time, and verifies
head again. It also proves `via-migrate upgrade` fails before database access
when `VIA_DATABASE_URL` is absent. Temporary containers and networks are removed
through cleanup traps and useful database/migration logs are emitted on failure.
