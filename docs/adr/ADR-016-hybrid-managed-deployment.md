# ADR-016: Hybrid managed control plane and dedicated scientific worker

## Status

Accepted as the target production topology. The existing B7 single-Droplet
deployment remains a rollback path until cutover validation is complete.

## Context

The B7 deployment co-locates the HTTP API, PostgreSQL/PostGIS, Alembic job,
scientific worker, authoritative scientific sources, and generated artifacts on
one DigitalOcean Droplet. That shape is simple, but it couples public ingress,
database durability, scientific compute, and scientific object storage to one
host.

VIA must retain its existing reproducibility guarantees: source identity is the
logical dataset/version plus SHA-256, CropSuiteLite continues to receive local
filesystem paths, and long scientific execution stays outside the HTTP process.

## Decision

Adopt the following production target incrementally:

- VIA API runs as a Google Cloud Run service.
- Alembic runs as a one-shot Google Cloud Run Job using via-migrate upgrade.
- PostgreSQL/PostGIS runs in Supabase.
- VIA Worker and CropSuiteLite remain together on a DigitalOcean compute Droplet.
- authoritative scientific sources and scientific artifacts live in Cloudflare R2.
- the worker materializes exact R2 source objects into a reconstructible local
  content-addressed cache, verifies SHA-256, and passes local paths to CropSuiteLite.
- worker workspace and object caches are local/disposable; they are never the
  scientific authority.
- Tailscale is retained for Droplet administration only. Public API ingress no
  longer depends on Tailscale Funnel.

The physical object provider is not scientific identity. Provider-specific URLs
or temporary URLs must not replace persisted logical source/version/hash
identity.

API, worker, and migration may use different PostgreSQL endpoints. The API
should use the Supabase transaction pooler appropriate for serverless traffic;
the persistent worker should use a long-running session/direct endpoint
appropriate to Droplet connectivity; migrations should prefer the direct
database endpoint.

The same immutable OCI image may continue to serve API, worker, and migration
roles during this migration.

## Consequences

The public API no longer requires persistent scientific filesystem mounts.
Knowledge serving uses the packaged manifest/taxonomy and persisted PostgreSQL
corpus; external source PDFs remain an ingestion concern.

The worker still has one durable work source: PostgreSQL polling. Batch size and
CropSuiteLite worker count remain 1 initially. This ADR does not introduce
Redis, RabbitMQ, Celery, multiple consumers, direct remote COG access, or
automatic scientific concurrency.

compose.digitalocean.yaml remains the documented B7 rollback deployment.
compose.digitalocean.worker.yaml is the target worker-only Droplet runtime.

Future multiple-worker execution requires a separate decision covering atomic
claiming, orphan recovery, retry/idempotency, and lease/heartbeat behavior. The
current optimistic queued-to-preparing claim remains valid for the single-worker
target.
