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

Runtime paths are deployment configuration and must resolve independently of the
process current working directory. B5 standardizes the provider-neutral
container topology:

| Path | Access | Lifetime | Owner |
| --- | --- | --- | --- |
| `/opt/via/CropSuiteLite` | read-only | image | VIA image |
| `/mnt/via/sources` | read-only | external | deployment/data |
| `/etc/via` | read-only | external | deployment/config |
| `/var/lib/via/workspace` | read-write | disposable | worker/container |
| `/var/lib/via/artifacts` | read-write | durable | deployment storage |

Dynamic environmental source datasets are supplied externally and are immutable
to VIA. The 39 environmental rasters remain outside the image under
`/mnt/via/sources`; they are not moved into CropSuiteLite or persisted as
artifacts. Existing input bindings continue to carry exact source references;
production bindings should use stable container paths below `/mnt/via/sources/...`
where those references point to mounted datasets. The existing evaluation-time
source SHA-256 verification remains authoritative. Two static, versioned `data/`
assets are intentionally included in the image: the tracked Huaura scope boundary
`data/huaura/boundary/huaura_province.geojson` at
`/opt/via/data/huaura/boundary/huaura_province.geojson`, and
`CropSuiteLite/data/usda_texture_classification.dat` at
`/opt/via/CropSuiteLite/data/usda_texture_classification.dat`. No environmental
raster, including `worldclim_prec` or `worldclim_temp`, is included. B5 does not
add mount-wide hashing or startup dataset scans.

Deployment configuration is supplied read-only at `/etc/via`. The required
bindings file has canonical path `/etc/via/input-bindings.json`, exposed by the
image as the structural default for `VIA_CROPSUITE_INPUT_BINDINGS`. The actual
file is not baked into the image, so a worker without the deployment mount still
fails when it attempts to load the required bindings. Optional
`VIA_CROPSUITE_SOURCE_CONFIG` identifies a runtime configuration file, while
`VIA_CROPSUITE_CATALOG` identifies a directory containing CropSuite `.inf`
catalog files. Either may be supplied read-only below `/etc/via` when a
deployment uses them.

`VIA_CROPSUITE_WORKSPACE=/var/lib/via/workspace` is disposable process state.
Per-evaluation request files, generated engine inputs, logs, bridge output, and
temporary scientific output live there and may disappear when a worker/container
is replaced. Finalized scientific artifacts are published into
`VIA_ARTIFACTS_ROOT=/var/lib/via/artifacts` with opaque relative storage
references plus their persisted SHA-256/size metadata. Persisted artifact
references therefore must not depend on workspace files remaining after an
evaluation completes.

The filesystem artifact implementation can prove that its root exists and is
writable; it cannot prove storage durability. Production deployment must mount
storage at `/var/lib/via/artifacts` whose lifecycle survives container
replacement. B5 deliberately selects no cloud storage product and adds no
Docker `VOLUME` instruction. B6 wires these paths in a production-like Compose
smoke. B7 owns provider-specific persistent storage selection.

Scientific execution rejects writable workspace/artifact layouts that are equal
to or nested inside the immutable CropSuiteLite tree, and rejects durable
artifact storage that is equal to or nested inside the disposable workspace.
These checks resolve paths without requiring them to exist during pure settings
parsing. The adapter's existing workspace-vs-engine guard remains in place.

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

## B6 production-like Docker Compose smoke

The root `compose.production-smoke.yaml` is the provider-neutral local/CI runtime
smoke for the B1-B5 contracts. It is deliberately not an internet-ready
production manifest: it publishes the API only for the smoke, uses fixed
CI-only PostgreSQL credentials, contains no TLS/ingress/provider integration,
and selects no managed database or persistent-storage product. B7 translates
the same runtime contract into provider-specific deployment resources.

The smoke starts exactly four services with release ordering encoded by Compose
dependency conditions:

```text
db (PostGIS healthy)
        |
        v
migrate (via-migrate upgrade, exit 0)
        |
        +----------------+
        |                |
        v                v
api (via-api)       worker (via-worker run)
```

`migrate`, `api`, and `worker` all resolve `${VIA_IMAGE:-via:b6}`. The API does
not override the image command, so the image default `via-api` remains the API
contract. The migration role overrides the command with the exec-form
`["via-migrate", "upgrade"]` and is a one-shot release operation. The worker
overrides it with `["via-worker", "run"]`. Compose waits for PostGIS TCP health,
then for migration completion, before starting API and worker; no sleep-based
release ordering, application-startup migration, restart loop, or provider
orchestrator is involved.

The B6 worker receives the B5 filesystem contract as actual deployment wiring:

| Worker path | B6 wiring | Semantics |
| --- | --- | --- |
| `/opt/via/CropSuiteLite` | image content | read-only engine |
| `/mnt/via/sources` | `deploy/smoke/sources` bind mount | read-only deployment data target |
| `/etc/via` | `deploy/smoke/config` bind mount | read-only deployment configuration |
| `/var/lib/via/workspace` | container tmpfs | disposable scientific workspace |
| `/var/lib/via/artifacts` | Compose named volume | durable across worker recreation |

The smoke bindings fixture exists only because worker startup validates the
configured bindings schema before it polls PostgreSQL. The smoke queues no
evaluation and provides no synthetic scientific dataset; the source mount is an
empty tracked deployment target. Consequently the worker remains idle and does
not execute CropSuiteLite or validate a source fingerprint during B6.

## B6.1 resource benchmark

B6.1 sizes the first VIA deployment for an expected audience of fewer than five
users. HTTP request concurrency is therefore not the initial capacity driver;
the dominant operational question is the RAM, CPU, and temporary-disk peak of a
single real scientific worker execution. Provider and tier selection remain B7
decisions made only after valid measurements exist.

`scripts/benchmark_production_runtime.sh` reuses
`compose.production-smoke.yaml` and the same image/process topology. The small
`compose.benchmark.yaml` override changes only the worker's external scientific
configuration/source mounts. The harness first starts PostGIS, the release
migration, and API, registers the fixture's Dataset and DatasetVersion metadata
through the existing HTTP API, generates exact `input-bindings.json` identities
from the returned UUIDs plus fixture-supplied source SHA-256 values, and only
then starts the normal asynchronous worker. Source SHA-256 verification,
`EnvironmentalInputManifest`, artifact persistence, and CropSuite execution are
not bypassed.

The fixture is deliberately external to the repository. Set
`VIA_BENCHMARK_FIXTURE` to a JSON document containing a parcel snapshot,
requested crops, environmental Dataset/DatasetVersion metadata, exact expected
CropSuite source SHA-256 values, and a `repeatable` flag. Set
`VIA_BENCHMARK_SOURCE_DIR` to the corresponding legitimate source tree, which is
mounted read-only at `/mnt/via/sources`. Optional additional worker
configuration can be supplied with `VIA_BENCHMARK_CONFIG_DIR`,
`VIA_BENCHMARK_SOURCE_CONFIG`, and `VIA_BENCHMARK_CATALOG`. Three runs are
allowed only when the fixture explicitly declares that sequential repetition is
safe; otherwise the harness runs exactly one evaluation.

The repository currently does not contain the Huaura scientific source tree
required by the existing CropSuite configurations. In particular,
`CropSuiteLite/data/huaura` is absent, so the referenced Huaura mask, climate,
soil, DEM, and land/sea inputs are unavailable in this checkout. The tracked B6
smoke binding is startup-only and is explicitly rejected by the benchmark
harness. B6.1 must therefore stop before scientific execution on a machine that
does not provide a legitimate external fixture and its matching source files;
no raster or benchmark value is synthesized to fill that gap.

After a configurable settle period, the harness samples the idle db/API/worker
stack for 45 seconds by default. During each evaluation it samples at a target
interval of approximately one second until a terminal status. Memory is Docker's
reported current `MemUsage` for each container, with total stack memory computed
as the per-sample sum. CPU is Docker `CPUPerc`; 100% is approximately one fully
utilized host core, so values can exceed 100% on multicore hosts. CPU percentages
and elapsed time from a GitHub runner must not be treated as equivalent to a
particular future VPS CPU model.

Temporary disk is the peak `du -sb` size of evaluation-prefixed entries below
`/var/lib/via/workspace`. Final artifact bytes are measured only below
`/var/lib/via/artifacts/evaluations/<evaluation_id>`, excluding unrelated
artifacts. Database growth is
`pg_database_size(current_database())` after terminal state minus the value
immediately before submission. Elapsed time uses a monotonic clock. The JSON
also records `uname -m`, `nproc`, host RAM, Docker version, image ID, and git SHA.

Generated `benchmark-results.json` is ignored by git. It contains idle metrics,
individual evaluation samples, min/median/max aggregates when three sequential
runs are valid, and +30%/+50% RAM headroom calculations from the observed
container-stack peak. Those values are environment-specific and do not include
all host reserve needs such as Linux, Docker, filesystem cache, SSH/monitoring,
or operational variance, so B6.1 does not automatically declare a provider or
tier safe.

`.github/workflows/b6-resource-benchmark.yml` is manual-only and uses a
`self-hosted` Linux runner labelled `via-benchmark`, where the legitimate source
tree can already exist without being uploaded to GitHub. It builds the same VIA
image and may upload only the generated JSON. The normal B2-B6 gate never runs
the scientific benchmark, and scientific source data is not published as an
Actions artifact.

`scripts/verify_production_compose.sh` is the runtime gate. It validates the
Compose model, starts the topology, verifies PostGIS health and successful
one-shot migration, dynamically proves the database revision equals the single
Alembic head, and calls both `/health` and the database-backed `GET /projects`
endpoint. It also checks that migration, API, and worker containers resolved to
the same image, that engine/config/source locations are non-writable, and that
the worker remains alive over multiple normal polling intervals without a fatal
traceback.

The same gate writes one marker to artifacts and one to workspace, force
recreates only the worker without rerunning dependencies, then proves the named
artifact volume retained its marker while the tmpfs workspace did not. Finally
it stops API and worker through normal Docker Compose stop semantics and always
runs `down -v --remove-orphans` through its cleanup trap. This exercises the B5
durability boundary and A7 cooperative shutdown behavior without changing
either contract.

## B7 DigitalOcean single-Droplet deployment definition

B7.1 maps the provider-neutral B1-B6 runtime contract onto one DigitalOcean
Basic Droplet running Ubuntu 24.04 LTS. It is a deployment definition only: no
Droplet, firewall rule, registry package, or other DigitalOcean resource has
been created by this repository change.

The initial capacity target is 1 vCPU, 2 GiB RAM, and 50 GiB SSD for an expected
audience of fewer than five people. The deployment runs one VIA worker and keeps
the VIA evaluation queue sequential at the worker level with
`VIA_WORKER_BATCH_SIZE=1`. The same initial single-Droplet profile sets
`VIA_CROPSUITE_MAX_WORKERS=1`, so the scientific runtime also uses one worker on
the 1 vCPU host. No scientific parameters or workload are reduced to fit that
capacity. A resize to a 4 GiB Basic Droplet requires no VIA application
architecture change.

| B1-B6 contract | DigitalOcean implementation |
| --- | --- |
| OCI image | GHCR image tagged by the validated git SHA; digest preferred for deployment |
| host | One Ubuntu 24.04 Basic Droplet |
| API | `api` service in `compose.digitalocean.yaml` |
| worker | one `worker` service running `via-worker run` |
| migration | one-shot `migrate` service running `via-migrate upgrade` |
| PostgreSQL/PostGIS | local `postgis/postgis:16-3.5` service with named volume `via_postgres_data` |
| `/mnt/via/sources` | `/srv/via/sources` bind-mounted read-only |
| `/var/lib/via/artifacts` | `/srv/via/artifacts` bind-mounted read-write |
| `/var/lib/via/workspace` | disposable tmpfs with no persistent bind mount |
| `/etc/via` | `/srv/via/config` bind-mounted read-only |

`/srv/via/config`, `/srv/via/sources`, `/srv/via/artifacts`, and
`/srv/via/backups` are provider-host directories. Only validated final runtime
scientific sources belong in `/srv/via/sources`; raw Huaura caches, WISE or
Pelletier archives, raw SoilGrids downloads, historical CropSuite outputs,
virtual environments, repository metadata, and other development caches do not.
`scripts/sync_digitalocean_sources.ps1` requires the operator to name the local
source directory explicitly before copying it. It performs no automatic
discovery of a repository data directory. After upload it normalizes
`/srv/via/sources` and every source directory to mode `0755`, every source file
to mode `0644`, and fails if verification finds any different mode. Ownership
remains deployment-owned; these modes let runtime uid 999 traverse and read the
tree while Compose still mounts `/srv/via/sources:/mnt/via/sources:ro`.

PostgreSQL data lives in the Docker-managed `via_postgres_data` named volume and
therefore survives database-container recreation and VIA image changes. Final
scientific artifacts live directly under `/srv/via/artifacts`, so worker and
Compose recreation do not remove them. Worker workspace remains tmpfs at
`/var/lib/via/workspace`; no size cap is imposed before benchmark evidence
justifies one.

The authoritative release entry point is `scripts/deploy_digitalocean.sh`. It
requires an explicit GHCR digest or full 40-character git-SHA tag and rejects
`latest`. The release sequence is deliberately procedural rather than delegated
to Compose dependencies:

```text
docker pull exact VIA_IMAGE
        |
        v
start/check PostGIS health
        |
        v
via-migrate upgrade
        |
    exit 0 only
        |
        +--------> update/start API
        |
        +--------> update/start worker
        |
        v
verify API health + worker/image liveness
```

If migration exits non-zero, shell strict mode terminates the release before the
API or worker is recreated with the new image. Migration remains one-shot and is
never moved into API or worker startup. The script never runs `docker compose
down -v` and never deletes the database volume, artifacts, sources, or backups.
`scripts/deploy_digitalocean.ps1` is only a Windows SSH wrapper around that Linux
entry point; it contains no duplicate release logic or SSH password.

Production secrets are host-local. Copy
`deploy/digitalocean/runtime.env.example` to `/srv/via/config/runtime.env`, fill
the PostgreSQL values, and set mode `0600`. The PostgreSQL password is stored
once as `VIA_POSTGRES_PASSWORD`; Compose derives the application
`VIA_DATABASE_URL` from it for API, worker, and migration. The deployment script
requires a URL-unreserved password of at least 24 characters so no second
encoded password copy is needed. A long random hex secret satisfies that
constraint. `VIA_IMAGE` is supplied per release instead of being stored in the
runtime secret file. The Huaura runtime example sets
`VIA_CROPSUITE_SOURCE_CONFIG=/etc/via/huaura-runtime.ini` and
`VIA_CROPSUITE_CATALOG=/opt/via/CropSuiteLite/plant_params/huaura_maize`. The
external `huaura-runtime.ini` sets
`texture_classes=/opt/via/CropSuiteLite/data/usda_texture_classification.dat`;
that path does not belong in `runtime.env`. The initial 1 vCPU Droplet sets
`VIA_CROPSUITE_MAX_WORKERS=1`.

`.github/workflows/b7-publish-ghcr.yml` publishes to
`ghcr.io/<owner>/<repository>:<validated-git-sha>` only after the existing
`B2-B6 Container Gate` reports success for that exact commit. The workflow
checks out `workflow_run.head_sha`, uses the repository `GITHUB_TOKEN` with only
`contents: read` and `packages: write`, runs the provider contract checks, then
builds and pushes that SHA tag. It never publishes `latest`. Deployment should
prefer the resulting `@sha256:<digest>` reference when available.

For a private GHCR package, the Droplet needs a registry credential that can
only read packages. Authenticate Docker interactively or through a protected
operator mechanism using a GitHub credential with `read:packages`; do not put
that credential in Git, cloud-init, Compose, or `runtime.env`. `docker pull` in
the deployment script is also the effective registry-access check.

`infra/digitalocean/cloud-init.yaml` prepares the Ubuntu host with Docker Engine,
Compose v2, unattended security updates, the `/srv/via` directories, and a
non-root `via-deploy` administrator. Password SSH authentication is disabled.
The bootstrap contains no private key; it copies the public key that the cloud
image/provider placed in root's `authorized_keys` into the deployment user's
account, then writes an SSH daemon override disabling direct root login only
after that key is present for `via-deploy`. A Droplet must therefore be created
with an operator SSH public key already supplied to DigitalOcean.

The host security boundary is SSH keys only, non-root routine administration,
no published PostgreSQL port, no worker port, and no tracked secrets. A
DigitalOcean Cloud Firewall should restrict SSH to the operator's known source
IP range. B7.1 does not invent that IP and does not mutate firewall rules. The
Compose API port is bound to `127.0.0.1` on the Droplet, so direct HTTP can be
used only for a controlled smoke through an SSH tunnel. External testers must
not send credentials over that plaintext boundary; a later B7.2/B8 edge/domain
step must provide HTTPS before external authenticated use. B7.1 therefore adds
no nginx, Caddy, or Traefik service.

`scripts/backup_postgres.sh` runs `pg_dump` inside the running PostGIS container
and writes timestamped custom-format dumps plus SHA-256 sidecars to
`/srv/via/backups/postgres`. Optional retention is applied only when the operator
sets `VIA_BACKUP_RETENTION_DAYS`. Same-host `pg_dump` protects against logical
mistakes and supports routine recovery, but it is not full disaster recovery.
DigitalOcean Droplet backups/snapshots protect the VM at the infrastructure
level, while an off-host database backup remains desirable before wider
production use. B7.1 adds no paid object-storage dependency.

DigitalOcean host monitoring should track at least memory, CPU, and disk
utilization during the initial 2 GiB trial. Do not add an arbitrary worker
memory limit. Resize the Droplet to 4 GiB if real evaluation workload causes an
OOM kill, sustained swap pressure, unsafe memory headroom, or a measured total
stack peak close to available host RAM. Those signals justify increasing host
capacity rather than changing scientific rules or reducing the workload.

`backend/tests/test_digitalocean_deployment_contract.py` statically enforces the
provider invariants: private DB/worker ports, one explicit `VIA_IMAGE` contract,
no `latest`, exact process commands, read-only source/config mounts, durable
artifact/database storage, disposable workspace, release ordering, no B6 smoke
fixture dependency, no raw Huaura path, no obvious committed credentials, and
same-commit GHCR publication gating.

The operator-facing release, Tailscale Funnel, smoke, legacy ownership,
migration-gate, and rollback procedure is maintained in
[`docs/operations/production-release.md`](../operations/production-release.md).
For the B7 rollback topology, HTTPS terminates at Funnel, which proxies only to
`127.0.0.1:8000`; no Caddy layer and no public port-8000 bind are introduced.

## B8 target hybrid managed deployment

ADR-016 defines the target production runtime while B7 remains available as a
rollback topology during cutover. The target separates the public/control plane
from scientific compute without changing the application boundaries or the
scientific identity model.

```text
[Frontend Hosting]
└── VIA SPA
      │ HTTPS
      ▼
[Google Cloud]
├── Cloud Run
│   └── VIA API
└── Cloud Run Job
    └── VIA Migration (via-migrate upgrade, one-shot)
          │
          ▼
[Supabase]
└── PostgreSQL/PostGIS
      ▲                 ▲
      │ API persistence │ worker claim/status/results
      │                 │
[DigitalOcean]
└── VIA Compute Droplet
    ├── Tailscale (administration only)
    └── Docker Engine / Compose
        └── VIA Worker
            └── CropSuiteLite
                 │
                 ▼
[Cloudflare]
└── R2
    ├── Scientific Sources
    └── Scientific Artifacts
```

This is a C4 Deployment/runtime view. `ScientificSourceMaterializer`, the R2
adapters, repositories, and other implementation components are deliberately
absent because they are not deployment containers. CropSuiteLite remains inside
the worker process/container and is not promoted to a service.

The runtime responsibilities are:

| Deployment node | Runtime responsibility |
| --- | --- |
| Cloud Run / VIA API | HTTP/auth/business APIs, capability discovery, persisted knowledge serving |
| Cloud Run Job / VIA Migration | one-shot Alembic migration before runtime rollout |
| Supabase PostgreSQL/PostGIS | authoritative transactional persistence and worker queue state |
| DigitalOcean VIA Worker | polling/claiming and long scientific execution through `CropSuiteAdapter` |
| Cloudflare R2 Sources | authoritative scientific source objects |
| Cloudflare R2 Artifacts | authoritative finalized scientific artifacts |
| Droplet source cache/workspace | reconstructible/disposable local execution state |

### Database endpoints and pooling

API, worker, and migration have separate database variables because their
connection lifecycles differ:

- `VIA_API_DATABASE_URL` is intended for the Supabase Transaction Pooler
  endpoint on port 6543 used by serverless API instances. Production Cloud Run
  sets `VIA_API_DATABASE_TRANSACTION_POOLER=true`; the API then uses SQLAlchemy
  `NullPool` because Supavisor owns pooling and disables psycopg prepared
  statements with `prepare_threshold=None`. The API QueuePool size, overflow,
  timeout, and recycle settings apply only when transaction-pooler mode is off.
- `VIA_WORKER_DATABASE_URL` is intended for the session/direct endpoint that is
  reachable from the persistent Droplet. Worker defaults are pool size 2,
  overflow 0, timeout 30 seconds, recycle 300 seconds.
- `VIA_MIGRATION_DATABASE_URL` is used only by Alembic and should prefer the
  direct database endpoint when the deployment network supports it. Alembic
  keeps `NullPool` semantics.

Provider SSL/query parameters belong in the externally supplied connection URL;
VIA does not hard-code Supabase hostnames or credentials. PostGIS remains a
required database capability and must be validated before migration/cutover.

### Scientific source and artifact storage

The target worker uses `VIA_SCIENTIFIC_SOURCE_BACKEND=s3` and
`VIA_SCIENTIFIC_ARTIFACT_BACKEND=s3` against Cloudflare R2's S3-compatible API.
The persisted/reviewed binding manifest carries provider-neutral object keys,
relative paths, expected SHA-256, expected size, and media type. A provider URL
is never the scientific identity.

For sources, the execution path remains:

```text
R2 authoritative object
    -> local content-addressed cache (sha256/<hash>)
    -> SHA-256 + size verification
    -> materialized local logical path
    -> CropSuiteLite
```

Cache entries and workspace can be deleted and reconstructed. A cache hit is
verified before use; a failed or partial download is never committed as a valid
entry. The filesystem source/artifact implementations remain supported for
development, tests, and the B7 rollback topology.

### Cloud Run API filesystem contract

Cloud Run API does not mount `/mnt/via/sources` and does not need original
knowledge PDFs for normal serving. Knowledge serving uses the packaged
manifest/taxonomy plus the PostgreSQL corpus; source PDFs remain an explicit
`via-knowledge ingest` concern.

Capability discovery still needs two small/versioned configuration inputs:
`VIA_CROPSUITE_CATALOG` points to the catalog shipped in the immutable image,
and `VIA_CROPSUITE_INPUT_BINDINGS=/etc/via/input-bindings.json` points to the
same reviewed logical binding manifest used for scientific input availability.
Cloud Run must provide that small manifest as configuration (for example an
immutable reviewed config/secret volume); it must not mount the raw raster set.

Cloud Run injects `PORT`. `via-api` uses `VIA_API_PORT` when explicitly set,
otherwise `PORT`, otherwise 8000. The target Cloud Run configuration therefore
leaves `VIA_API_PORT` unset.

### DigitalOcean worker-only runtime

`compose.digitalocean.worker.yaml` is the target Droplet topology. It has one
service, publishes no ports, mounts `/srv/via/config` read-only, stores the R2
source cache under `/srv/via/cache/sources`, and uses tmpfs for workspace. R2
artifacts are authoritative; `/srv/via/cache/artifacts` is only local adapter
scratch/cache state. Tailscale is for SSH/administration of the compute node;
Tailscale Funnel is not part of target API ingress.

The worker starts with `VIA_WORKER_BATCH_SIZE=1` and
`VIA_CROPSUITE_MAX_WORKERS=1`. These defaults are intentionally unchanged by the
infrastructure split.

### Release and CI/CD separation

CI/CD builds and tests one immutable OCI image and publishes a git-SHA tag or
digest. Runtime deployment then executes the same ordered release gate:

```text
build/test -> publish immutable image -> Cloud Run migration job
                                      -> failure: abort
                                      -> success: update Cloud Run API
                                                  update DO worker
                                                  run smoke
```

The CI/CD system is not part of the C4 runtime diagram. Migration remains a
one-shot release action and is never coupled to FastAPI or worker startup.

### Benchmark and future worker concurrency

`scripts/benchmark_production_runtime.sh` remains the reproducible scientific
resource benchmark. It records elapsed time, CPU, peak memory, workspace bytes,
artifact bytes, and database growth for a real external fixture. The benchmark
now accepts `VIA_BENCHMARK_CROPSUITE_MAX_WORKERS=1|2` and records that value in
the result, allowing two otherwise-identical runs to compare engine concurrency
without changing production defaults.

For the R2 target, perform a cold-cache run after deleting only the disposable
source cache, then repeat the identical evaluation without deleting it for the
warm-cache case. Record source-cache bytes/files before and after together with
R2 request/transfer telemetry available to the operator. These live-provider
measurements are opt-in and are not part of the credential-free normal test
suite.

Multiple VIA worker consumers remain deferred. The current PostgreSQL design
allows workers to discover the same queued evaluation and relies on the
optimistic `queued -> preparing` compare-and-save as the authoritative claim.
Before scaling to Worker 1/2/3, a separate decision must cover an atomic dequeue
strategy such as `FOR UPDATE SKIP LOCKED` (or equivalent), orphan recovery,
retry policy, idempotency, and any required heartbeat/lease. Benchmark evidence
must justify the additional compute first.

Remote COG/HTTP Range/GDAL VSI access, Redis, RabbitMQ, Celery, automatic worker
concurrency, and automatic multi-consumer scaling are outside B8.

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

`CropSuiteLite/requirements.txt` is the authoritative scientific manifest
installed into the image. It includes the required scientific runtime dependency
`rioxarray==0.19.0`. CropSuiteLite's remaining source requirements are not
rewritten. Repository inspection found no `tkinter`, `from tkinter`, or `import
tk` usage in the VIA scientific path (`src.multicrop` and the engine code it
launches). The `tk` line is therefore a non-portable packaging artifact for this
runtime and only that exact line is excluded from the container installation. No
other scientific dependency or version is changed.

The build runs
[`backend/scripts/verify_container_runtime.py`](../../backend/scripts/verify_container_runtime.py)
as the final non-root `via` user and fails unless all of the following are true:

- the build is running on Linux with Python 3.11 or newer;
- `VIA_CROPSUITE_PYTHON` is the interpreter executing the verification;
- `via_backend` and the worker module import successfully;
- `via-api`, `via-backend`, `via-worker`, and `via-migrate` are installed on `PATH`;
- the scientific stack imports successfully, including rasterio, pyproj,
  shapely, cartopy, netCDF4, scipy, numba, xarray, rioxarray, rio-cogeo, dask,
  scikit-image, and related dependencies;
- `python -m pip check` succeeds;
- the expected CropSuiteLite entrypoint/source files exist and `src.multicrop`
  imports using the same scientific interpreter;
- a subprocess using that same production interpreter and
  `/opt/via/CropSuiteLite` as its working directory successfully executes
  `import rioxarray; import CropSuite`, covering the real CropSuite entrypoint;
- the static Huaura boundary exists at
  `/opt/via/data/huaura/boundary/huaura_province.geojson`, is a regular file,
  and is not writable by the runtime user;
- the static USDA texture classification exists at
  `/opt/via/CropSuiteLite/data/usda_texture_classification.dat`, is a regular
  file, is readable, and is not writable by the runtime user;
- the runtime UID is not root;
- `/opt/via/CropSuiteLite` is not writable by the runtime user; and
- `/etc/via` and `/mnt/via/sources` exist and are not writable by the runtime user; and
- `/var/lib/via/workspace` and `/var/lib/via/artifacts` are writable by that user.

B2 intentionally stopped before defining a VIA `CMD` or `ENTRYPOINT`. B3 adds
the exec-form default `CMD ["via-api"]` while retaining no `ENTRYPOINT` wrapper.
B4 adds `via-migrate upgrade` as an explicit command override while keeping the
default image role unchanged. Schema migration is never run by image startup.

Runtime processes use the non-root `via` user. `/opt/via/CropSuiteLite` and the
backend code remain image-owned read-only inputs. The image also contains empty,
non-writable mount targets at `/etc/via` and `/mnt/via/sources`.
`/var/lib/via/workspace` is the disposable CropSuite execution workspace and
`/var/lib/via/artifacts` is the writable artifact path; production must place
the artifact path on deployment-owned durable storage.
`VIA_CROPSUITE_INPUT_BINDINGS` defaults structurally to
`/etc/via/input-bindings.json`; the bindings file, the 39 dynamic environmental
rasters, and the source-config file remain deployment-provided read-only inputs.
The validated Huaura maize catalog is image-owned at
`/opt/via/CropSuiteLite/plant_params/huaura_maize`. The only permitted `data/`
assets in the image are the tracked static Huaura scope boundary at
`/opt/via/data/huaura/boundary/huaura_province.geojson` and the tracked static
USDA texture classification at
`/opt/via/CropSuiteLite/data/usda_texture_classification.dat`. `HOME=/tmp` and
`MPLCONFIGDIR=/tmp/matplotlib` keep Matplotlib's runtime cache/configuration in
temporary storage for the non-root process rather than in a persistent path.

Build from the repository root so both `backend/` and `CropSuiteLite/` are in
the Docker build context:

```text
docker build -t via:b6 .
docker run --rm via:b6 python /opt/via/backend/scripts/verify_container_runtime.py --require-linux
docker run --rm via:b6 python --version
docker run --rm via:b6 python -m pip check
docker run --rm via:b6 via-worker --help
docker run --rm -e VIA_DATABASE_URL=<postgresql-url> via:b6 via-migrate upgrade
```

B2-B6 do not choose a hosting provider, add dynamic environmental datasets to
the image, alter CropSuiteLite scientific requirements or behavior, change
artifact-storage identities/database semantics, or change worker lifecycle. The
versioned Huaura scope boundary is the single static `data/` exception required
by the existing scientific runtime. B5 defines the durability and mount
contract, while B6 exercises that contract locally and in CI and leaves
provider-specific storage to B7.

The Linux container workflow proves the B3 process contract, the B4 release
migration contract, and the B5 filesystem/mount contract.
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

For B5, the workflow also verifies that the intrinsic `/etc/via` and
`/mnt/via/sources` targets are non-writable by the default `via` user, then
mounts harmless host marker directories read-only at those locations and proves
the markers are readable while writes fail. A deployment-owned artifact bind
mount is prepared using the image's dynamically discovered UID/GID; one
container writes a unique marker and a replacement container reads the same
marker from the same mount. A separate pair of containers proves an unmounted
workspace marker disappears across container replacement. These Linux Docker
checks prove deployment behavior that unit tests cannot establish.

For B6, the same workflow keeps the B2-B5 gates first and then launches the
dedicated production-like Compose topology with the already-built `via:b6`
image. The Compose smoke adds release-ordering, real API-to-PostgreSQL access,
idle worker-to-PostgreSQL liveness, same-image role verification, named-volume
artifact persistence, tmpfs workspace disposal, read-only deployment mounts,
and normal Compose shutdown. No image is pushed and no external provider,
registry credential, application secret, or internet deployment is required.
