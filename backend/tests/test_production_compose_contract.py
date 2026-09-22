"""Static invariants for the provider-neutral B6 production-like Compose smoke."""

from __future__ import annotations

from pathlib import Path

from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    load_cropsuite_environmental_input_bindings,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
COMPOSE_PATH = REPOSITORY_ROOT / "compose.production-smoke.yaml"
SMOKE_SCRIPT_PATH = REPOSITORY_ROOT / "scripts" / "verify_production_compose.sh"


def _mapping_keys(text: str, section: str) -> set[str]:
    lines = text.splitlines()
    section_line = f"{section}:"
    start = lines.index(section_line) + 1
    keys: set[str] = set()
    for line in lines[start:]:
        if line and not line.startswith(" "):
            break
        if line.startswith("  ") and not line.startswith("    ") and line.rstrip().endswith(":"):
            keys.add(line.strip()[:-1])
    return keys


def _service_block(text: str, service: str) -> str:
    lines = text.splitlines()
    start = lines.index(f"  {service}:")
    block = [lines[start]]
    for line in lines[start + 1 :]:
        if line.startswith("  ") and not line.startswith("    ") and line.rstrip().endswith(":"):
            break
        if line and not line.startswith(" "):
            break
        block.append(line)
    return "\n".join(block)


def test_b6_compose_has_exact_process_topology_and_same_image_contract() -> None:
    compose = COMPOSE_PATH.read_text(encoding="utf-8")

    assert _mapping_keys(compose, "services") == {"db", "migrate", "api", "worker"}
    assert "image: postgis/postgis:16-3.5" in _service_block(compose, "db")

    for service in ("migrate", "api", "worker"):
        assert "image: ${VIA_IMAGE:-via:b6}" in _service_block(compose, service)

    assert 'command: ["via-migrate", "upgrade"]' in _service_block(compose, "migrate")
    assert "command:" not in _service_block(compose, "api")
    assert 'command: ["via-worker", "run"]' in _service_block(compose, "worker")


def test_b6_compose_encodes_release_ordering_and_runtime_mount_semantics() -> None:
    compose = COMPOSE_PATH.read_text(encoding="utf-8")
    database = _service_block(compose, "db")
    migrate = _service_block(compose, "migrate")
    api = _service_block(compose, "api")
    worker = _service_block(compose, "worker")

    assert "pg_isready -h 127.0.0.1" in database
    assert "ports:" not in database
    assert "condition: service_healthy" in migrate
    expected_runtime_dependencies = "\n".join(
        (
            "    depends_on:",
            "      db:",
            "        condition: service_healthy",
            "      migrate:",
            "        condition: service_completed_successfully",
        )
    )
    for service in (api, worker):
        assert expected_runtime_dependencies in service
    assert '"18000:8000"' in api
    assert "urllib.request" in api

    assert "./deploy/smoke/config:/etc/via:ro" in worker
    assert "./deploy/smoke/sources:/mnt/via/sources:ro" in worker
    assert "via_artifacts:/var/lib/via/artifacts" in worker
    assert "/var/lib/via/workspace:mode=1777" in worker
    assert "/var/lib/via/artifacts" not in api
    assert "/var/lib/via/workspace" not in api
    assert "restart:" not in compose


def test_b6_compose_remains_provider_neutral_and_uses_smoke_only_credentials() -> None:
    compose = COMPOSE_PATH.read_text(encoding="utf-8").casefold()

    assert "ci-only-password" in compose
    for provider_term in (
        "aws",
        "azure",
        "gcp",
        "google cloud",
        "supabase",
        "render.com",
        "railway.app",
    ):
        assert provider_term not in compose


def test_b6_worker_bindings_fixture_is_valid_for_startup() -> None:
    bindings_path = REPOSITORY_ROOT / "deploy" / "smoke" / "config" / "input-bindings.json"

    bindings = load_cropsuite_environmental_input_bindings(bindings_path)

    assert len(bindings) == 1
    assert bindings[0].storage_reference == "/mnt/via/sources"

def test_b6_smoke_requires_health_and_rejects_anonymous_projects_access() -> None:
    script = SMOKE_SCRIPT_PATH.read_text(encoding="utf-8")

    assert (
        'health_json="$(curl --fail --silent http://127.0.0.1:18000/health)"'
        in script
    )
    assert 'grep -q \'"status":"ok"\' <<<"${health_json}"' in script

    assert "--write-out '%{http_code}'" in script
    assert "http://127.0.0.1:18000/projects" in script
    assert 'test "${projects_status}" = "401"' in script

    assert (
        'projects_json="$(curl --fail --silent http://127.0.0.1:18000/projects)"'
        not in script
    )
    assert 'test "${projects_json}" = "[]"' not in script