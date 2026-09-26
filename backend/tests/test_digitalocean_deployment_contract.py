from __future__ import annotations

import re
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
COMPOSE_PATH = REPOSITORY_ROOT / "compose.digitalocean.yaml"


def _read(relative_path: str) -> str:
    return (REPOSITORY_ROOT / relative_path).read_text(encoding="utf-8")


def _service_block(compose: str, service: str, next_service: str | None) -> str:
    start = compose.index(f"  {service}:\n")
    if next_service is None:
        end = compose.index("\nvolumes:\n", start)
    else:
        end = compose.index(f"\n  {next_service}:\n", start)
    return compose[start:end]


def test_digitalocean_compose_preserves_runtime_and_durability_contracts() -> None:
    compose = COMPOSE_PATH.read_text(encoding="utf-8")
    db = _service_block(compose, "db", "migrate")
    migrate = _service_block(compose, "migrate", "api")
    api = _service_block(compose, "api", "worker")
    worker = _service_block(compose, "worker", None)

    assert "postgis/postgis:16-3.5" in db
    assert "ports:" not in db
    assert "via_postgres_data:/var/lib/postgresql/data" in db

    via_image = "image: ${VIA_IMAGE:?VIA_IMAGE is required}"
    assert migrate.count(via_image) == 1
    assert api.count(via_image) == 1
    assert worker.count(via_image) == 1
    assert "${VIA_IMAGE:-" not in compose
    assert ":latest" not in compose.casefold()

    assert 'command: ["via-migrate", "upgrade"]' in migrate
    assert 'command: ["via-api"]' in api
    assert 'command: ["via-worker", "run"]' in worker
    assert "restart: unless-stopped" in worker
    assert "ports:" not in worker
    assert '"127.0.0.1:${VIA_API_HOST_PORT:-8000}:8000"' in api
    assert "VIA_CORS_ALLOWED_ORIGINS: ${VIA_CORS_ALLOWED_ORIGINS:?" in api
    for setting in (
        "VIA_AUTH_ACCESS_TOKEN_TTL_SECONDS",
        "VIA_AUTH_REFRESH_TOKEN_TTL_SECONDS",
        "VIA_AUTH_REFRESH_COOKIE_NAME",
        "VIA_AUTH_REFRESH_COOKIE_SECURE",
        "VIA_AUTH_REFRESH_COOKIE_SAMESITE",
        "VIA_RATE_LOGIN_PER_MINUTE",
        "VIA_RATE_REFRESH_PER_MINUTE",
        "VIA_RATE_DATASET_COVERAGE_PER_MINUTE",
        "VIA_RATE_KNOWLEDGE_PER_USER_PER_MINUTE",
        "VIA_RATE_RECOMMENDATIONS_PER_USER_PER_MINUTE",
    ):
        assert f"{setting}: ${{{setting}:-" in api
    assert (
        "VIA_HUAURA_AOI_BOUNDARY_PATH: "
        "/opt/via/data/huaura/boundary/huaura_province.geojson"
    ) in api
    assert (
        "VIA_HUAURA_AOI_METADATA_PATH: /opt/via/data/huaura/boundary/metadata.json"
        in api
    )
    assert "VIA_CROPSUITE_SOURCE_CONFIG: ${VIA_CROPSUITE_SOURCE_CONFIG:-}" in worker
    assert "VIA_CROPSUITE_CATALOG: ${VIA_CROPSUITE_CATALOG:-}" in worker
    assert "VIA_CROPSUITE_MAX_WORKERS: ${VIA_CROPSUITE_MAX_WORKERS:-1}" in worker

    assert "/srv/via/config:/etc/via:ro" in worker
    assert "/srv/via/sources:/mnt/via/sources:ro" in worker
    assert "/srv/via/artifacts:/var/lib/via/artifacts:rw" in worker
    assert "/var/lib/via/workspace:mode=1777" in worker

    assert "compose.production-smoke.yaml" not in compose
    assert "deploy/smoke" not in compose
    assert re.search(r"(?<!/opt/via/)data/huaura", compose, re.IGNORECASE) is None


def test_deployment_script_enforces_release_order_without_destructive_cleanup() -> None:
    script = _read("scripts/deploy_digitalocean.sh")

    pull = script.index('docker pull "${VIA_IMAGE}"')
    database = script.index('"${compose[@]}" up -d db')
    migrate = script.index('"${compose[@]}" run --rm --no-deps migrate')
    applications = script.index('"${compose[@]}" up -d --no-deps api worker')
    health = script.index("wait_for_health api 60")

    assert pull < database < migrate < applications < health
    assert "set -Eeuo pipefail" in script
    assert "down -v" not in script
    assert "rm -rf" not in script
    assert "latest is not accepted" in script
    assert "/srv/via/sources" in script
    assert "/srv/via/artifacts" in script
    assert "/srv/via/backups" in script


def test_deployment_script_requires_stable_worker_liveness_across_poll_intervals() -> None:
    script = _read("scripts/deploy_digitalocean.sh")

    api_health = script.index("wait_for_health api 60")
    worker_check = script.index("verify_worker_liveness", api_health)

    assert api_health < worker_check
    assert "initial_restart_count" in script
    assert "{{.RestartCount}}" in script
    assert "for observation in 1 2 3" in script
    assert 'sleep "${worker_poll_interval}"' in script
    assert 'worker_poll_interval="${VIA_WORKER_POLL_INTERVAL_SECONDS:-5}"' in script
    assert 'if [ "${worker_running}" != "true" ]' in script
    assert 'if [ "${restart_count}" != "${initial_restart_count}" ]' in script
    assert 'logs --no-color worker' in script
    assert "Traceback (most recent call last):" in script


def test_provider_files_do_not_embed_secrets_or_raw_huaura_paths() -> None:
    provider_files = (
        "compose.digitalocean.yaml",
        "deploy/digitalocean/runtime.env.example",
        "scripts/deploy_digitalocean.sh",
        "scripts/backup_postgres.sh",
        "scripts/deploy_digitalocean.ps1",
        "scripts/sync_digitalocean_sources.ps1",
        "infra/digitalocean/cloud-init.yaml",
        ".github/workflows/b7-publish-ghcr.yml",
    )
    secret_pattern = re.compile(
        r"(-----BEGIN [A-Z ]*PRIVATE KEY-----|"
        r"github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]+|dop_v1_[A-Za-z0-9]+)"
    )
    raw_huaura_path = re.compile(r"(?<!/opt/via/)data/huaura", re.IGNORECASE)

    for relative_path in provider_files:
        text = _read(relative_path)
        assert secret_pattern.search(text) is None, relative_path
        assert raw_huaura_path.search(text) is None, relative_path
        assert "doctl " not in text.casefold(), relative_path

    runtime_example = _read("deploy/digitalocean/runtime.env.example")
    assert "VIA_POSTGRES_PASSWORD=REPLACE_ME" in runtime_example
    assert "frontend.example.com" not in runtime_example
    assert "VIA_CORS_ALLOWED_ORIGINS=REPLACE_WITH_FRONTEND_HTTPS_ORIGIN" in runtime_example
    assert "VIA_AUTH_REFRESH_COOKIE_SECURE=true" in runtime_example
    assert "VIA_AUTH_REFRESH_COOKIE_SAMESITE=lax" in runtime_example
    assert "VIA_CROPSUITE_SOURCE_CONFIG=/etc/via/huaura-runtime.ini" in runtime_example
    assert (
        "VIA_CROPSUITE_CATALOG=/opt/via/CropSuiteLite/plant_params/huaura_maize"
        in runtime_example
    )
    assert "VIA_CROPSUITE_MAX_WORKERS=1" in runtime_example
    assert "VIA_DATABASE_URL=" not in runtime_example
    assert "VIA_IMAGE=" not in runtime_example


def test_ghcr_publish_is_gated_by_successful_b2_b6_run_for_same_commit() -> None:
    workflow = _read(".github/workflows/b7-publish-ghcr.yml")

    assert "workflow_run:" in workflow
    assert "B2-B6 Container Gate" in workflow
    assert "github.event.workflow_run.conclusion == 'success'" in workflow
    assert "ref: ${{ github.event.workflow_run.head_sha }}" in workflow
    assert "RELEASE_SHA: ${{ github.event.workflow_run.head_sha }}" in workflow
    assert "packages: write" in workflow
    assert "GITHUB_TOKEN" in workflow
    assert 'docker push "$VIA_GHCR_IMAGE:$RELEASE_SHA"' in workflow
    assert ":latest" not in workflow.casefold()
    assert "doctl " not in workflow.casefold()
    assert "digitalocean_token" not in workflow.casefold()
    assert "api.digitalocean.com" not in workflow.casefold()


def test_docker_build_context_excludes_scientific_data() -> None:
    dockerignore = _read(".dockerignore")

    assert "data/" in dockerignore.splitlines()
    assert "**/data/" in dockerignore.splitlines()


def test_source_sync_normalizes_and_verifies_read_only_runtime_permissions() -> None:
    script = _read("scripts/sync_digitalocean_sources.ps1")

    assert "chmod 0755 '__REMOTE_PATH__'" in script
    assert "-mindepth 1 -type d -exec chmod 0755 {} +" in script
    assert "-type f -exec chmod 0644 {} +" in script
    assert "-type d ! -perm 0755 -print -quit" in script
    assert "-type f ! -perm 0644 -print -quit" in script
    assert "chmod 777" not in script
    assert "chown" not in script.casefold()
