# VIA hybrid staging validation

This runbook validates ADR-016 against real staging infrastructure without
changing the application architecture. It is intentionally separate from the
production release procedure: every resource created here must be disposable or
explicitly identified as staging.

The target route is:

```text
Cloud Run API
    -> Supabase PostgreSQL/PostGIS
    -> DigitalOcean VIA Worker
    -> Cloudflare R2 Scientific Sources
    -> local SHA-256 cache
    -> CropSuiteLite
    -> Cloudflare R2 Scientific Artifacts
    -> Supabase result state
    -> Cloud Run API
```

Keep one VIA worker consumer, `VIA_WORKER_BATCH_SIZE=1`, and
`VIA_CROPSUITE_MAX_WORKERS=1` for the first end-to-end validation. The
`max_workers=2` experiment changes only CropSuiteLite internal parallelism and
does not authorize multiple queue consumers.

## 1. Credential-safe local preflight

On Windows:

```powershell
.\scripts\staging_preflight.ps1
.\scripts\staging_preflight.ps1 -Json
```

The script reports only whether tools and credential environment variables are
present. It never prints credential values.

Record the exact Git SHA before doing provider work:

```powershell
git rev-parse HEAD
git status --short
git diff --check
```

Run the repository verification before publishing an image:

```powershell
Set-Location backend
.\.venv\Scripts\pytest.exe
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\pyright.exe -p pyproject.toml
.\.venv\Scripts\lint-imports.exe
```

## 2. Minimum authentication actions

Do not paste tokens into tracked files or shell commands that will be committed.
Use provider login flows or local untracked secret files.

Google Cloud:

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project "$GCP_PROJECT_ID"
gcloud auth list
```

If `gcloud` is not installed locally, the same deployment commands may be run
from Google Cloud Shell after authenticating to the intended staging project.

Supabase: create or select a dedicated staging project in the Supabase dashboard.
Record its region and obtain three connection strings without committing them:

```text
VIA_API_DATABASE_URL       transaction pooler
VIA_WORKER_DATABASE_URL    reachable session/direct endpoint
VIA_MIGRATION_DATABASE_URL direct endpoint when available
```

Cloudflare R2:

```bash
npx wrangler login
npx wrangler whoami
npx wrangler r2 bucket create via-staging-sources
npx wrangler r2 bucket create via-staging-artifacts
```

Create an R2 S3 API credential scoped only to the staging buckets. Keep its key
ID and secret outside Git. The application uses the S3-compatible endpoint and
`region=auto`.

DigitalOcean: use the existing administrative SSH/Tailscale access to the
compute Droplet. If provider CLI access is required:

```bash
doctl auth init
doctl account get
```

GHCR, when the image is private:

```bash
printf '%s' "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USER" --password-stdin
```

## 3. Region record

Do not select a Cloud Run region from this repository. Before deployment record:

```text
GCP_PROJECT_ID=
GCP_REGION=
SUPABASE_REGION=
DIGITALOCEAN_DROPLET_REGION=
```

Choose a Cloud Run region only after the actual Supabase project and existing
Droplet regions are known. The staging report must include measured API->DB and
worker->DB latency rather than assuming geography is sufficient.

## 4. Supabase PostgreSQL/PostGIS validation

Use the migration/direct connection for administrative validation. Confirm the
current connection itself uses TLS:

```sql
SELECT ssl, version, cipher
FROM pg_stat_ssl
WHERE pid = pg_backend_pid();
```

Enable and verify PostGIS in staging:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
SELECT PostGIS_Version();
```

Before application traffic, run the migration job described below and then
verify:

```sql
SELECT version_num FROM alembic_version;
SELECT extname, extversion FROM pg_extension WHERE extname = 'postgis';
```

For a safe representative local database, use a custom-format logical backup:

```bash
pg_dump --format=custom --no-owner --no-acl "$SAFE_LOCAL_DATABASE_URL" -f via-staging.dump
pg_restore --clean --if-exists --no-owner --no-acl --dbname "$VIA_MIGRATION_DATABASE_URL" via-staging.dump
```

Restore only reviewed non-sensitive staging data. Run Alembic after restore.

Measure each connection class separately, for example:

```bash
psql "$VIA_API_DATABASE_URL" -c "SELECT clock_timestamp();"
psql "$VIA_WORKER_DATABASE_URL" -c "SELECT clock_timestamp();"
psql "$VIA_MIGRATION_DATABASE_URL" -c "SELECT clock_timestamp();"
```

For comparable latency, collect repeated client-side wall-clock timings from
Cloud Run and from the Droplet; do not compare a local laptop measurement with a
provider-to-provider path.

## 5. R2 source preparation and integrity

Upload only reviewed scientific staging inputs. Use stable object keys matching
the reviewed `input-bindings.json`. For each source record:

```text
object_key
relative_path
size_bytes
sha256
media_type
```

Compute the source identity before upload:

```bash
sha256sum path/to/source.tif
stat -c '%s' path/to/source.tif
```

Upload with Wrangler or another S3-compatible client, then download the object
to a temporary file and recompute both size and SHA-256. A provider HEAD alone
is not sufficient to prove byte identity.

Use separate buckets:

```text
via-staging-sources
via-staging-artifacts
```

The worker configuration comes from
`deploy/digitalocean/worker.env.example`. The source cache remains
`/srv/via/cache/sources`; R2 remains authoritative.

## 6. Immutable image and Cloud Run migration gate

Publish the exact tested Git SHA and record the immutable registry digest. Never
use `latest`.

Create or update the staging migration job with command:

```text
via-migrate upgrade
```

Example Cloud Run shape:

```bash
gcloud run jobs deploy via-staging-migrate \
  --region "$GCP_REGION" \
  --image "$VIA_IMAGE_DIGEST" \
  --command via-migrate \
  --args upgrade

gcloud run jobs execute via-staging-migrate \
  --region "$GCP_REGION" \
  --wait
```

Inject `VIA_MIGRATION_DATABASE_URL` through Secret Manager or the reviewed
provider secret mechanism. A non-zero migration execution aborts the rollout.
FastAPI startup must not run migrations.

## 7. Cloud Run API staging

Use `deploy/cloudrun/api.env.example` as the reviewed environment contract.
Cloud Run supplies `PORT`; leave `VIA_API_PORT` unset.

Deploy the same immutable digest used by the migration job. Mount the reviewed
small `input-bindings.json` at `/etc/via/input-bindings.json`. Do not mount
raw scientific rasters into Cloud Run.

After deployment validate:

```bash
curl --fail --show-error "$VIA_STAGING_API_URL/health"
curl --fail --show-error "$VIA_STAGING_API_URL/openapi.json" > /dev/null
```

Confirm the configured frontend staging origin, database-backed reads, Cloud Run
logs, and that no Tailscale Funnel URL is part of the public path.

## 8. DigitalOcean worker staging

Install the reviewed files:

```text
/opt/via-deploy/compose.digitalocean.worker.yaml
/srv/via/config/worker.env
/srv/via/config/input-bindings.json
/srv/via/config/huaura-runtime.ini
```

Keep `worker.env` mode `0600`.

```bash
export VIA_IMAGE='ghcr.io/<owner>/<repo>@sha256:<digest>'
docker pull "$VIA_IMAGE"
docker compose --env-file /srv/via/config/worker.env \
  -f /opt/via-deploy/compose.digitalocean.worker.yaml \
  up -d --no-deps --force-recreate worker
docker compose --env-file /srv/via/config/worker.env \
  -f /opt/via-deploy/compose.digitalocean.worker.yaml ps
```

The target compose publishes no ports. Tailscale is administrative only.

## 9. Cold and warm materializer validation

Cold run:

```bash
docker compose --env-file /srv/via/config/worker.env \
  -f /opt/via-deploy/compose.digitalocean.worker.yaml stop worker
find /srv/via/cache/sources -mindepth 1 -delete
docker compose --env-file /srv/via/config/worker.env \
  -f /opt/via-deploy/compose.digitalocean.worker.yaml start worker
```

Record the cache file count/bytes before the evaluation, execute one E2E smoke,
then record count/bytes, hashes, worker logs, provider R2 request/transfer
telemetry, and evaluation timestamps.

Warm run: execute the same crop/regime and scientific dataset versions again
without deleting `/srv/via/cache/sources`. Confirm:

- the cache object SHA-256 values are unchanged;
- no source object is unnecessarily downloaded again;
- the worker still passes local filesystem paths to CropSuiteLite;
- the evaluation succeeds and produces artifacts in the staging artifact bucket.

The application materializer already verifies source size and SHA-256 before
atomically committing to the local cache. Provider transfer telemetry is the
authoritative measurement for R2 bytes when available.

## 10. Real end-to-end smoke

Use the existing smoke script against Cloud Run:

```bash
export VIA_SMOKE_API_URL="$VIA_STAGING_API_URL"
export VIA_SMOKE_EMAIL='<dedicated-staging-user>'
export VIA_SMOKE_PASSWORD='<set outside Git>'
export VIA_SMOKE_PARCEL_GEOJSON='/path/to/reviewed-huaura-parcel.geojson'
python3 scripts/smoke_production_api.py
```

The staging topology is validated only when at least one evaluation reaches
`succeeded` through Cloud Run -> Supabase -> DigitalOcean worker -> R2 sources
-> local materialization -> CropSuiteLite -> R2 artifacts -> Supabase -> Cloud
Run API.

Retain the evaluation ID and verify state transitions, timestamps, source
fingerprints, evidence/limitations, artifacts, and final result.

## 11. Benchmark record

Keep the credential-free Linux benchmark as the controlled compute baseline:

```bash
VIA_BENCHMARK_RUNS=3 \
VIA_BENCHMARK_CROPSUITE_MAX_WORKERS=1 \
./scripts/benchmark_production_runtime.sh

VIA_BENCHMARK_RUNS=3 \
VIA_BENCHMARK_CROPSUITE_MAX_WORKERS=2 \
./scripts/benchmark_production_runtime.sh
```

For staging, execute at least one cold and one warm E2E evaluation with
`VIA_CROPSUITE_MAX_WORKERS=1`. Capture on the Droplet:

```bash
docker stats --no-stream
du -sb /srv/via/cache/sources
docker logs --since 15m via-worker-worker-1
```

If repeated runs are practical, use three cold and three warm runs and report
min/median/max total duration. Only test `max_workers=2` after the
`max_workers=1` E2E path is stable; keep exactly one VIA worker consumer.

Required staging report fields:

```text
git_sha
image_digest
cloud_run_region
supabase_region
droplet_region
dataset_versions
input_sha256
crop_count
total_seconds
cpu_average / cpu_peak
ram_average / ram_peak
source_bytes_downloaded
artifact_bytes_uploaded
cache_hits / cache_misses
api_to_db_latency
worker_to_db_latency
```

Record `materialization_seconds`, `cropsuite_seconds`,
`artifact_upload_seconds`, `db_claim_latency`, and `db_update_latency` only
when the current logs/telemetry expose them reliably. Mark unavailable metrics
as unavailable rather than deriving them from unrelated timings.

## 12. Rollback

Application rollback uses immutable images:

```text
Cloud Run API: SHA N -> previous revision / SHA N-1
DigitalOcean worker: SHA N -> previous image digest / SHA N-1
```

Do not run an automatic destructive database downgrade. After an additive
migration, prefer rolling application components back while keeping the newer
compatible schema.

The B7 single-Droplet topology remains the topology rollback path documented in
`production-release.md`. Only one PostgreSQL authority may accept writes at a
time.

## 13. Cost and evidence rules

Record provider resources actually created. Do not state that a service costs
zero merely because it has a free tier:

- DigitalOcean Droplets are normally billable while provisioned.
- Supabase may be within a free plan when eligible, with plan quotas.
- Cloud Run requires an enabled Google Cloud project/billing relationship and
  may charge beyond its free allowance.
- R2 has plan allowances and may charge for storage/operations beyond them.

The final staging report must separate observed measurements from unavailable
metrics and prepared configuration from infrastructure that was actually
created.

Do not implement multi-consumer claiming, `FOR UPDATE SKIP LOCKED`,
lease/heartbeat, distributed retries, remote COG/GDAL VSI, Redis, RabbitMQ,
Celery, CropSuiteLite as a service, or additional OCI image splitting as part of
this validation.
