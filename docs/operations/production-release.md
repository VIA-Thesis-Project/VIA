# VIA production release, migration, and rollback runbook

Real-provider staging validation is documented separately in
[`staging-validation.md`](staging-validation.md). Complete that evidence before
using this production release procedure for the hybrid target.

ADR-016 makes the hybrid managed topology the production target: Cloud Run API,
Cloud Run migration job, Supabase PostgreSQL/PostGIS, DigitalOcean scientific
worker, and Cloudflare R2 sources/artifacts. The existing B7 single-Droplet
procedure is retained later in this document as the rollback/legacy topology.
This runbook does not authorize a deployment by itself. Run only reviewed,
immutable releases and never paste secrets into shell history or logs.

## Target hybrid release inputs

Record before changing any runtime:

- release git SHA and green verification run;
- immutable `VIA_IMAGE=ghcr.io/<owner>/<repo>@sha256:<digest>`;
- previous Cloud Run API revision/image and previous worker image digest;
- current Alembic revision and expected single head;
- pre-cutover PostgreSQL logical backup plus checksum;
- reviewed API, worker, and migration configuration versions;
- reviewed `input-bindings.json` version/hash;
- R2 source/artifact bucket names and credential references (never secret values);
- exact frontend HTTPS origin and target Cloud Run service URL.

Never deploy `latest` or a mutable branch tag.

## Supabase and R2 preparation

Create the Supabase project through normal provider administration. Enable and
verify PostGIS before moving application traffic. Using the reviewed migration
connection, the database capability check is conceptually:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
SELECT PostGIS_Version();
```

For an existing VIA database, take a consistent logical backup before cutover.
Restore that backup into the target database using the approved PostgreSQL
restore workflow, then run `via-migrate upgrade`. Do not make the application
create Supabase resources or extensions during normal startup. Validate the
single Alembic head and representative geometry/PostGIS queries before allowing
API or worker traffic.

Use separate externally managed database URLs:

```text
VIA_API_DATABASE_URL       -> transaction-pooling endpoint for Cloud Run
VIA_WORKER_DATABASE_URL    -> reachable session/direct endpoint for the Droplet
VIA_MIGRATION_DATABASE_URL -> direct migration endpoint when available
```

Connection URLs may contain provider-required SSL parameters. Do not copy real
URLs into Git, logs, issue text, or tracked env files.

Create separate R2 buckets or clearly separated prefixes for authoritative
scientific sources and finalized artifacts. Upload sources under stable
`object_key` values and prepare the reviewed binding manifest with logical
dataset/version identity, relative path, SHA-256, size, and media type. Verify
the uploaded bytes against the expected SHA-256 before cutover. The R2 URL is
physical storage metadata, not scientific identity.

The worker's local `/srv/via/cache/sources` and workspace are disposable. Do
not seed scientific identity from those directories and do not treat them as a
backup of R2.

## Target hybrid deployment procedure

1. Build/test the exact commit and publish one immutable image SHA/digest. Keep
   the same reviewed image for API, worker, and migration unless a later ADR
   explicitly separates them.

2. Prepare Cloud Run API configuration from
   `deploy/cloudrun/api.env.example`. Supply `VIA_API_DATABASE_URL` and secrets
   through the cloud secret/config mechanism. Leave `VIA_API_PORT` unset so
   `via-api` consumes Cloud Run's `PORT`.

3. Provide the reviewed small binding manifest at
   `/etc/via/input-bindings.json` to the API as configuration. The crop catalog
   is already shipped in the image at
   `/opt/via/CropSuiteLite/plant_params/huaura_maize`. Do not mount raw R2
   rasters or `/mnt/via/sources` into Cloud Run. Normal knowledge serving also
   does not require the original knowledge PDFs.

4. Create/update the one-shot Cloud Run Job from the same immutable image with
   command `via-migrate upgrade` and the configuration in
   `deploy/cloudrun/migrate.env.example`. Execute the job and wait for exit 0.
   On any migration failure, abort the release before changing API or worker.

5. Update the Cloud Run API to the reviewed immutable digest and verify its
   `/health` endpoint plus one database-backed read. Confirm the effective
   frontend CORS origin and secure refresh-cookie settings.

6. On the DigitalOcean compute Droplet, copy
   `deploy/digitalocean/worker.env.example` to
   `/srv/via/config/worker.env`, fill externally managed Supabase/R2 secrets,
   install the reviewed `input-bindings.json` and CropSuite runtime config under
   `/srv/via/config`, and set the env file to mode `0600`.

7. Pull and start only the worker using the immutable image:

   ```bash
   export VIA_IMAGE='ghcr.io/<owner>/<repo>@sha256:<digest>'
   docker pull "$VIA_IMAGE"
   docker compose --env-file /srv/via/config/worker.env \
     -f /opt/via-deploy/compose.digitalocean.worker.yaml \
     up -d --no-deps --force-recreate worker
   docker compose --env-file /srv/via/config/worker.env \
     -f /opt/via-deploy/compose.digitalocean.worker.yaml ps
   ```

   The target compose publishes no host ports. Keep
   `VIA_WORKER_BATCH_SIZE=1` and `VIA_CROPSUITE_MAX_WORKERS=1` for initial
   production.

8. Keep Tailscale on the Droplet for administration only. Remove/reset any old
   Funnel exposure after Cloud Run HTTPS is validated; do not create a new
   public ingress path to the worker.

9. Run the production smoke against the Cloud Run HTTPS URL with a reviewed
   Huaura parcel. Confirm authentication, project/parcel persistence, evaluation
   completion, result/evidence/limitations, source fingerprints, and artifact
   retrieval semantics. A valid low/zero suitability remains a valid scientific
   result.

10. Inspect Cloud Run, Supabase, worker, and R2 operational signals. Specifically
    check connection exhaustion/timeouts, worker claim conflicts, failed source
    integrity checks, repeated R2 downloads, cache growth, OOM/swap pressure,
    and artifact publication failures. Do not log database URLs, R2 keys,
    access tokens, refresh cookies, or OpenAI keys.

The release order is therefore fixed:

```text
build/test -> publish immutable image -> migration job
                                   failure -> abort
                                   success -> Cloud Run API
                                            -> DO worker
                                            -> smoke
```

## Target hybrid rollback

Prefer component rollback before topology rollback.

1. Stop further rollout and preserve migration/API/worker logs plus the exact
   failing image/config references.
2. If migration failed, leave API and worker on their previous images. Do not
   run an automatic Alembic downgrade.
3. If the new API or worker image fails after a successful additive migration,
   redeploy the previous immutable API revision/image and previous worker digest
   while leaving the database at the newer compatible revision when possible.
4. If only worker configuration/R2 access fails, stop the target worker, restore
   its previous reviewed env/config, and recreate the worker. R2 remains the
   authority; deleting the local cache is safe when investigating corruption.
5. If a full return to B7 is required, enter a maintenance window and restore a
   validated Supabase backup/export into the B7 PostgreSQL instance before
   reopening writes. Never run old local PostgreSQL and Supabase as independent
   writable authorities. Then use the legacy B7 procedure below with the
   previous immutable image.

After any rollback, repeat health/authenticated reads and one controlled
evaluation read/smoke against the active topology.

## Benchmark and concurrency gate

The credential-free repository benchmark remains
`scripts/benchmark_production_runtime.sh`. Run the same real fixture twice with
identical host/image/config except for:

```bash
VIA_BENCHMARK_CROPSUITE_MAX_WORKERS=1 ./scripts/benchmark_production_runtime.sh
VIA_BENCHMARK_CROPSUITE_MAX_WORKERS=2 ./scripts/benchmark_production_runtime.sh
```

Record both JSON results. For the live R2 target, additionally record a cold
source-cache run (delete only `/srv/via/cache/sources` contents before the run)
and an otherwise identical warm-cache run. Capture cache file/byte counts and
provider request/transfer telemetry. These measurements are opt-in because the
normal suite never requires real Supabase/R2/GCP credentials.

Do not increase production concurrency from this experiment alone. Multiple VIA
worker consumers require a separate claim/recovery design covering atomic claim
(`FOR UPDATE SKIP LOCKED` or equivalent), duplicate-execution prevention,
orphan recovery, retries, idempotency, and heartbeat/lease semantics.

## B7 single-Droplet rollback/legacy procedure

The remainder of this document is the retained B7 operator procedure. Its
public edge is intentionally different from the target architecture:

The intended edge remains:

```text
Internet
   -> HTTPS (Tailscale certificate)
Tailscale Funnel
   -> HTTP loopback only
127.0.0.1:8000
VIA API container
```

There is no Caddy/nginx/Traefik layer. PostgreSQL and the worker publish no host ports. Port 8000 must never bind to `0.0.0.0` or a public interface.

## Release inputs to record before changing anything

- release git SHA and green GitHub Actions run URL;
- immutable `VIA_IMAGE=ghcr.io/<owner>/<repo>@sha256:<64-hex-digest>`;
- previous immutable image digest for rollback;
- timestamped runtime configuration backup path;
- timestamped PostgreSQL dump and SHA-256 sidecar;
- expected Alembic head: `20260921_0017`;
- exact public Funnel URL and exact frontend origin;
- operator and change-window identifier.

Do not deploy `latest` or a mutable branch tag. The existing deployment script also permits a full 40-character git-SHA tag, but production release records should prefer the registry digest.

## Manual release procedure

The examples assume the repository is `/opt/via-deploy`; adjust only that reviewed path.

1. Confirm the `B2-B6 Container Gate`, provider contract, backend tests, static analysis, and GHCR publication workflow are green for the exact release SHA. Confirm the checkout HEAD matches it:

   ```bash
   cd /opt/via-deploy
   git rev-parse HEAD
   ```

2. Obtain the immutable digest from the successful GHCR workflow/package page and verify it locally without relying on a mutable tag:

   ```bash
   export VIA_IMAGE='ghcr.io/<owner>/<repo>@sha256:<digest>'
   docker pull "$VIA_IMAGE"
   docker image inspect "$VIA_IMAGE" --format '{{json .RepoDigests}}'
   ```

   Record both the new digest and the currently running API digest:

   ```bash
   docker inspect via-api-1 --format '{{.Image}}' || true
   ```

3. Back up the host runtime configuration without printing it, then create the logical database backup:

   ```bash
   release_stamp="$(date -u +%Y%m%dT%H%M%SZ)"
   sudo install -d -m 0700 /srv/via/backups/config
   sudo cp --preserve=mode,ownership,timestamps \
     /srv/via/config/runtime.env \
     "/srv/via/backups/config/runtime.env.${release_stamp}"
   sudo chmod 0600 "/srv/via/backups/config/runtime.env.${release_stamp}"
   sudo VIA_RUNTIME_ENV_FILE=/srv/via/config/runtime.env \
     /opt/via-deploy/scripts/backup_postgres.sh
   ```

4. Verify the immutable image contains the authoritative Huaura AOI asset and metadata, and that metadata identifies the expected CRS/source. This is read-only:

   ```bash
   docker run --rm --entrypoint python "$VIA_IMAGE" -c \
     "import json,pathlib; b=pathlib.Path('/opt/via/data/huaura/boundary/huaura_province.geojson'); m=pathlib.Path('/opt/via/data/huaura/boundary/metadata.json'); assert b.is_file() and m.is_file(); d=json.loads(m.read_text()); assert d['crs']=='EPSG:4326' and d['source']=='GADM 4.1'; print('Huaura AOI assets OK')"
   ```

5. Load the protected runtime environment only for Compose interpolation and verify permissions. Do not print it:

   ```bash
   test "$(stat -c '%a' /srv/via/config/runtime.env)" = 600
   set -a
   . /srv/via/config/runtime.env
   set +a
   export VIA_IMAGE
   compose=(docker compose --env-file /srv/via/config/runtime.env \
     -f /opt/via-deploy/compose.digitalocean.yaml)
   ```

6. Start/verify PostgreSQL, then run the one-shot migration. Migration must complete before API/worker recreation:

   ```bash
   "${compose[@]}" up -d db
   "${compose[@]}" run --rm migrate
   ```

   Stop here on any non-zero result. Do not recreate API/worker and do not attempt an automatic downgrade.

7. Recreate only API and worker with the reviewed digest:

   ```bash
   "${compose[@]}" up -d --no-deps --force-recreate api worker
   "${compose[@]}" ps
   ```

8. Verify loopback health from the Droplet:

   ```bash
   curl --fail --silent --show-error http://127.0.0.1:8000/health
   ```

9. Prove port 8000 is not publicly bound. The expected listener is `127.0.0.1:8000`, never `0.0.0.0:8000`, `[::]:8000`, or the public Droplet address:

   ```bash
   sudo ss -ltnp '( sport = :8000 )'
   docker compose --env-file /srv/via/config/runtime.env \
     -f /opt/via-deploy/compose.digitalocean.yaml port api 8000
   ```

10. If Tailscale is not installed, follow the current official Linux installation instructions from `https://tailscale.com/download/linux`, inspect the downloaded installer, then enroll the node with the approved tailnet identity. At minimum verify:

    ```bash
    tailscale version
    sudo tailscale up
    tailscale status
    ```

11. Configure Funnel only during the authorized deployment window. The current Tailscale CLI syntax is a persistent HTTPS reverse proxy to loopback:

    ```bash
    sudo tailscale funnel --bg http://127.0.0.1:8000
    sudo tailscale funnel status --json
    ```

    Funnel requires MagicDNS, HTTPS certificates, and an approved `funnel` node attribute. Its public TLS ports are restricted by Tailscale. To remove all Funnel exposure during rollback/incident response:

    ```bash
    sudo tailscale funnel reset
    ```

    Do not activate Funnel while merely preparing or reviewing this release.

12. Verify HTTPS health at the exact `https://<node>.<tailnet>.ts.net/health` URL returned by Funnel:

    ```bash
    curl --fail --silent --show-error 'https://<node>.<tailnet>.ts.net/health'
    ```

13. Set `VIA_CORS_ALLOWED_ORIGINS` to the exact HTTPS frontend origin, without path or wildcard, and recreate API if the value changed. For same-site deployments keep the secure `__Secure-via_refresh` cookie with `SameSite=lax`. For a genuinely cross-site frontend use `SameSite=none` only with `Secure=true`, exact credentialed CORS, and browser requests using `credentials: "include"`.

14. Run login and `/me` checks through HTTPS with the dedicated smoke account. Never echo the password, access token, `Set-Cookie`, or cookie jar.

15. Run the Project/Parcel/Evaluation smoke described below with a reviewed geometry completely inside Huaura.

16. Confirm the evaluation reaches `succeeded` and inspect result, evidence, and limitations. This is the scientific E2E gate; do not weaken scientific parameters, units, masks, interpolation, scoring, or no-data semantics to make it pass.

17. Run Decision Support smoke when its source/config/OpenAI provider is enabled. Cache reuse is the normal call; do not use `force_regenerate` for routine smoke.

18. Review API/worker/database logs and host monitoring for tracebacks, repeated restarts, OOM/swap pressure, disk exhaustion, migration errors, 401/403/429 anomalies, and provider failures. Logs must not contain secrets, full tokens, refresh cookies, database URLs, or OpenAI keys.

The existing `scripts/deploy_digitalocean.sh "$VIA_IMAGE"` implements the pull -> DB -> migrate -> API/worker -> local health sequence. The numbered procedure remains the operator checklist around it, including backups, Funnel, external HTTPS, authenticated/scientific smoke, and log review.

## Production smoke command

The smoke is intentionally mutating: it creates durable Project, Parcel, and Evaluation records and prints their non-secret IDs for later audit. Use a dedicated active USER account and a reviewed GeoJSON Polygon/MultiPolygon inside the Huaura AOI.

```bash
export VIA_SMOKE_API_URL='https://<node>.<tailnet>.ts.net'
export VIA_SMOKE_EMAIL='smoke-user@example.org'
export VIA_SMOKE_PARCEL_GEOJSON='/srv/via/config/smoke-parcel.geojson'
python3 /opt/via-deploy/scripts/smoke_production_api.py
```

The script prompts for the password with hidden input. `VIA_SMOKE_PASSWORD` is supported for a protected non-interactive runner, but an environment variable can be visible to privileged process inspection and must never be persisted in `runtime.env`, shell history, CI logs, or repository files. The script is fail-fast, withholds tokens/cookies, polls to a terminal state, reads result/evidence/limitations, and runs Decision Support when available. Use `--decision-support required` only when provider/config readiness is a release requirement. Do not run this script against production during code review.

## Tailscale and trusted-proxy decision

The API currently keys IP-based login/refresh limits from `request.client.host`. It does not trust `X-Forwarded-For` automatically because no verified trusted-proxy allowlist and header-normalization policy has been implemented. This avoids spoofed client IPs.

Consequence: behind Funnel, the backend may observe the proxy/loopback peer rather than the original internet client, so host-based limits can be shared by many users. The normalized-email login limiter and per-user functional limiters still separate subjects. Treat shared host buckets as a known operational limitation. Do not switch to forwarded headers until the exact proxy hop, header overwrite behavior, trusted source addresses, and framework proxy configuration are verified and tested. Tailscale's PROXY-protocol mode would also require an explicit compatible listener; it is not enabled by this runbook.

## Legacy ownership procedure

Legacy ownership is never inferred and never backfilled at startup or migration time. There is no "first admin" rule.

1. Read-only report of exact rows whose `owner_user_id IS NULL`:

   ```bash
   docker compose --env-file /srv/via/config/runtime.env \
     -f /opt/via-deploy/compose.digitalocean.yaml \
     run --rm --no-deps api via-legacy-ownership-admin report
   ```

2. Dry-run an explicit assignment (default because `--apply` is absent):

   ```bash
   docker compose --env-file /srv/via/config/runtime.env \
     -f /opt/via-deploy/compose.digitalocean.yaml \
     run --rm --no-deps api via-legacy-ownership-admin assign \
     --target-user-id '<user-uuid>' \
     --project-id '<project-uuid>' \
     --evaluation-id '<evaluation-uuid>'
   ```

3. After independently verifying the target user and every listed ID, repeat the exact command with `--apply` to perform the real transaction.

Only explicitly listed Project/Evaluation IDs with `owner_user_id IS NULL` are eligible. Existing ownership, missing resources, a missing target user, empty ID selection, or concurrent changes fail closed. Do not run this procedure against production during code review.

## Migration release gate

No migration after `20260921_0017` is required for IA-5. Do not create `0018` without a real schema requirement.

Static head check:

```bash
cd /opt/via-deploy/backend
alembic heads
# expected single head: 20260921_0017
```

On a disposable PostgreSQL/PostGIS test database only, when `VIA_TEST_DATABASE_URL` is set and passes the repository's test-database safety checks:

```bash
cd backend
VIA_DATABASE_URL="$VIA_TEST_DATABASE_URL" alembic current
VIA_DATABASE_URL="$VIA_TEST_DATABASE_URL" alembic downgrade 20260920_0016
VIA_DATABASE_URL="$VIA_TEST_DATABASE_URL" alembic upgrade 20260921_0017
VIA_DATABASE_URL="$VIA_TEST_DATABASE_URL" alembic current
pytest -q tests/test_ia4_postgresql.py \
  tests/test_farm_management_postgresql.py \
  tests/test_agroclimatic_evaluation_postgresql.py
```

Never point this gate at the production database. Record exact revisions, pass/fail/skip counts, and the sanitized database target class (local/container/approved external test), not its credential-bearing URL.

## Rollback procedure

Rollback inputs are the previously recorded image digest, the timestamped runtime config backup, and the pre-release database backup.

1. Stop the rollout and preserve API/worker/migration logs.
2. If configuration caused the failure, restore the reviewed backup without printing it and keep mode `0600`.
3. Set `VIA_IMAGE` to the previous immutable digest, pull it, and recreate API + worker only:

   ```bash
   export VIA_IMAGE='ghcr.io/<owner>/<repo>@sha256:<previous-digest>'
   docker pull "$VIA_IMAGE"
   compose=(docker compose --env-file /srv/via/config/runtime.env \
     -f /opt/via-deploy/compose.digitalocean.yaml)
   "${compose[@]}" up -d --no-deps --force-recreate api worker
   curl --fail --silent --show-error http://127.0.0.1:8000/health
   ```

4. Migration `20260921_0017` is additive. Prefer an application-only rollback and leave the database at 0017 when the previous application is compatible.
5. Do not downgrade to 0016 if `decision_support.recommendation_generation_attempts` may contain quota/ledger data. A downgrade drops that table and is destructive. Do not automate it. Consider downgrade only after an explicit incident decision, verified absence/export of relevant data, a tested restore path, and confirmation that the old application cannot operate with 0017.
6. Through HTTPS, repeat health, login, `/me`, owned Project/Parcel reads, and one controlled evaluation read/smoke. Re-check Funnel status, port binding, logs, and monitoring.

If public exposure itself is unsafe, run `sudo tailscale funnel reset` first, preserve loopback access for diagnosis, and do not open port 8000 as a workaround.
