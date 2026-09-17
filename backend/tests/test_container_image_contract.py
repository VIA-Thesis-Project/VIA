"""Static invariants for the provider-neutral B2/B3 container image."""

import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_docker_context_excludes_local_scientific_and_development_state() -> None:
    ignored = {
        line.strip()
        for line in (REPOSITORY_ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    required = {
        ".git/",
        ".codex/",
        "graphify-out/",
        "backend/graphify-out/",
        "**/.venv/",
        "**/__pycache__/",
        "**/.pytest_cache/",
        "**/.ruff_cache/",
        "data/",
        "**/data/",
        "downloads/",
        "**/downloads/",
        "results/",
        "**/results/",
        ".env",
        "**/.env",
        "a4_1_review.zip",
        "**/a4_1_review.zip",
    }
    assert required <= ignored


def test_image_does_not_bake_deployment_secrets_or_bindings() -> None:
    dockerfile = (REPOSITORY_ROOT / "Dockerfile").read_text(encoding="utf-8")

    for forbidden_setting in (
        "VIA_DATABASE_URL",
        "VIA_CROPSUITE_INPUT_BINDINGS",
        "VIA_CROPSUITE_SOURCE_CONFIG",
        "VIA_CROPSUITE_CATALOG",
        "VIA_POSTGRES_PASSWORD",
    ):
        assert forbidden_setting not in dockerfile
    assert "COPY . " not in dockerfile


def test_b3_image_defaults_to_exec_form_production_api_command() -> None:
    dockerfile = (REPOSITORY_ROOT / "Dockerfile").read_text(encoding="utf-8")
    instructions = [
        line.strip()
        for line in dockerfile.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    commands = [line[3:].strip() for line in instructions if line.upper().startswith("CMD ")]
    entrypoints = [line for line in instructions if line.upper().startswith("ENTRYPOINT ")]

    assert len(commands) == 1
    assert json.loads(commands[0]) == ["via-api"]
    assert entrypoints == []


def test_b3_image_has_no_shell_process_multiplexer() -> None:
    dockerfile = (REPOSITORY_ROOT / "Dockerfile").read_text(encoding="utf-8").casefold()

    for forbidden in ("sh -c", "bash -c", "supervisor", "systemd"):
        assert forbidden not in dockerfile
