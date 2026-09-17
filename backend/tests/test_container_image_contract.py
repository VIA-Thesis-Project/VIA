"""Static invariants for the provider-neutral B2 container image."""

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


def test_b2_image_does_not_bake_deployment_secrets_or_b3_process_commands() -> None:
    dockerfile = (REPOSITORY_ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert "VIA_DATABASE_URL" not in dockerfile
    assert "VIA_CROPSUITE_INPUT_BINDINGS" not in dockerfile
    assert "COPY . " not in dockerfile

    instructions = [
        line.strip().split(maxsplit=1)[0].upper()
        for line in dockerfile.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert "CMD" not in instructions
    assert "ENTRYPOINT" not in instructions
