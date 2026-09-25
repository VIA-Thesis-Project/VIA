from __future__ import annotations

from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TARGET_COMPOSE = REPOSITORY_ROOT / "compose.digitalocean.worker.yaml"


def _read(relative_path: str) -> str:
    return (REPOSITORY_ROOT / relative_path).read_text(encoding="utf-8")


def test_target_digitalocean_runtime_is_worker_only() -> None:
    compose = TARGET_COMPOSE.read_text(encoding="utf-8")

    assert '\n  worker:\n' in compose
    assert '\n  api:\n' not in compose
    assert '\n  db:\n' not in compose
    assert '\n  migrate:\n' not in compose
    assert 'command: ["via-worker", "run"]' in compose
    assert "ports:" not in compose
    assert "image: ${VIA_IMAGE:?VIA_IMAGE is required}" in compose
    assert ":latest" not in compose.casefold()

    assert "VIA_WORKER_DATABASE_URL: ${VIA_WORKER_DATABASE_URL:?" in compose
    assert "VIA_WORKER_BATCH_SIZE: ${VIA_WORKER_BATCH_SIZE:-1}" in compose
    assert "VIA_CROPSUITE_MAX_WORKERS: ${VIA_CROPSUITE_MAX_WORKERS:-1}" in compose

    assert "VIA_SCIENTIFIC_SOURCE_BACKEND: s3" in compose
    assert "VIA_SCIENTIFIC_SOURCE_CACHE_DIR: /var/lib/via/source-cache" in compose
    assert "VIA_SCIENTIFIC_SOURCE_BUCKET:" in compose
    assert "VIA_SCIENTIFIC_ARTIFACT_BACKEND: s3" in compose
    assert "VIA_SCIENTIFIC_ARTIFACT_BUCKET:" in compose

    assert "/srv/via/config:/etc/via:ro" in compose
    assert "/srv/via/cache/sources:/var/lib/via/source-cache:rw" in compose
    assert "/srv/via/cache/artifacts:/var/lib/via/artifacts:rw" in compose
    assert "/var/lib/via/workspace:mode=1777" in compose
    assert "/srv/via/sources:/mnt/via/sources" not in compose


def test_cloud_run_examples_separate_api_and_migration_database_endpoints() -> None:
    api = _read("deploy/cloudrun/api.env.example")
    migrate = _read("deploy/cloudrun/migrate.env.example")

    assert "VIA_API_DATABASE_URL=REPLACE_WITH_SUPABASE_TRANSACTION_POOLER_URL" in api
    assert "VIA_API_DATABASE_TRANSACTION_POOLER=true" in api
    assert "port 6543" in api
    assert "SQLAlchemy NullPool" in api
    assert "VIA_API_DATABASE_POOL_SIZE=5" in api
    assert "VIA_API_PORT=" not in api
    assert "VIA_KNOWLEDGE_SOURCE_DIR=" not in api
    assert "VIA_MIGRATION_DATABASE_URL=" not in api
    assert "VIA_CROPSUITE_INPUT_BINDINGS=/etc/via/input-bindings.json" in api
    assert (
        "VIA_CROPSUITE_CATALOG=/opt/via/CropSuiteLite/plant_params/huaura_maize"
        in api
    )

    assert (
        "VIA_MIGRATION_DATABASE_URL=REPLACE_WITH_SUPABASE_MIGRATION_DATABASE_URL"
        in migrate
    )
    assert "VIA_API_DATABASE_URL=" not in migrate
    assert "VIA_WORKER_DATABASE_URL=" not in migrate


def test_target_worker_example_keeps_sequential_defaults_and_no_real_secrets() -> None:
    worker = _read("deploy/digitalocean/worker.env.example")

    assert "VIA_WORKER_DATABASE_URL=REPLACE_WITH_SUPABASE_WORKER_DATABASE_URL" in worker
    assert "VIA_WORKER_BATCH_SIZE=1" in worker
    assert "VIA_CROPSUITE_MAX_WORKERS=1" in worker
    assert "VIA_CROPSUITE_INPUT_BINDINGS=/etc/via/input-bindings.json" in worker
    assert "VIA_SCIENTIFIC_SOURCE_BUCKET=REPLACE_WITH_R2_SOURCE_BUCKET" in worker
    assert "VIA_SCIENTIFIC_ARTIFACT_BUCKET=REPLACE_WITH_R2_ARTIFACT_BUCKET" in worker
    assert "REPLACE_WITH_" in worker
    assert "r2.cloudflarestorage.com" not in worker
    assert "supabase.co" not in worker


def test_single_droplet_compose_remains_available_as_rollback() -> None:
    rollback = _read("compose.digitalocean.yaml")

    assert "\n  db:\n" in rollback
    assert "\n  migrate:\n" in rollback
    assert "\n  api:\n" in rollback
    assert "\n  worker:\n" in rollback
