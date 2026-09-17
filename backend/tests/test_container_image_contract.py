"""Static invariants for the provider-neutral B2-B5 container image."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
HUAURA_BOUNDARY_SOURCE = "data/huaura/boundary/huaura_province.geojson"
HUAURA_BOUNDARY_DESTINATION = "/opt/via/data/huaura/boundary/huaura_province.geojson"
USDA_TEXTURE_SOURCE = "CropSuiteLite/data/usda_texture_classification.dat"
USDA_TEXTURE_DESTINATION = "/opt/via/CropSuiteLite/data/usda_texture_classification.dat"
USDA_TEXTURE_SHA256 = "e1397f6f47f26ad2f2bb42d1ac9c80c17473c50d856a4f9bd90778955b5eb46a"


def test_docker_context_excludes_local_scientific_and_development_state() -> None:
    ignored_lines = [
        line.strip()
        for line in (REPOSITORY_ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    ignored = set(ignored_lines)
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

    expected_data_rules = [
        "data/",
        "**/data/",
        "!data/",
        "data/*",
        "!data/huaura/",
        "data/huaura/*",
        "!data/huaura/boundary/",
        "data/huaura/boundary/*",
        f"!{HUAURA_BOUNDARY_SOURCE}",
        "!CropSuiteLite/data/",
        "CropSuiteLite/data/*",
        f"!{USDA_TEXTURE_SOURCE}",
    ]
    first_data_rule = ignored_lines.index("data/")
    actual_data_rules = ignored_lines[
        first_data_rule : first_data_rule + len(expected_data_rules)
    ]
    assert actual_data_rules == expected_data_rules
    assert {
        line for line in ignored_lines if line.startswith("!") and "data/" in line
    } == {
        "!data/",
        "!data/huaura/",
        "!data/huaura/boundary/",
        f"!{HUAURA_BOUNDARY_SOURCE}",
        "!CropSuiteLite/data/",
        f"!{USDA_TEXTURE_SOURCE}",
    }
    assert (REPOSITORY_ROOT / HUAURA_BOUNDARY_SOURCE).is_file()
    usda_texture = REPOSITORY_ROOT / USDA_TEXTURE_SOURCE
    assert usda_texture.is_file()
    assert hashlib.sha256(usda_texture.read_bytes()).hexdigest() == USDA_TEXTURE_SHA256
    assert not any(
        line.startswith("!CropSuiteLite/data/worldclim_") for line in ignored_lines
    )


def test_cropsuite_scientific_manifest_pins_rioxarray_only_in_scientific_runtime() -> None:
    requirements = (
        REPOSITORY_ROOT / "CropSuiteLite" / "requirements.txt"
    ).read_text(encoding="utf-8").splitlines()
    pyproject = tomllib.loads(
        (REPOSITORY_ROOT / "backend" / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert requirements.count("rioxarray==0.19.0") == 1
    assert not any(
        dependency.casefold().startswith("rioxarray")
        for dependency in pyproject["project"]["dependencies"]
    )


def test_container_runtime_gate_imports_real_cropsuite_with_same_interpreter() -> None:
    verifier = (
        REPOSITORY_ROOT / "backend" / "scripts" / "verify_container_runtime.py"
    ).read_text(encoding="utf-8")

    assert '"rioxarray",' in verifier
    assert 'CROPSUITE_IMPORT_SMOKE = "import rioxarray; import CropSuite"' in verifier
    assert '[sys.executable, "-c", CROPSUITE_IMPORT_SMOKE]' in verifier
    assert "cwd=engine_root" in verifier
    assert USDA_TEXTURE_DESTINATION in verifier
    assert "_require_read_only_file(" in verifier


def test_image_does_not_bake_deployment_secrets_or_bindings() -> None:
    dockerfile = (REPOSITORY_ROOT / "Dockerfile").read_text(encoding="utf-8")

    for forbidden_setting in (
        "VIA_DATABASE_URL",
        "VIA_CROPSUITE_SOURCE_CONFIG",
        "VIA_CROPSUITE_CATALOG",
        "VIA_POSTGRES_PASSWORD",
    ):
        assert forbidden_setting not in dockerfile
    copy_instructions = [
        line.strip()
        for line in dockerfile.splitlines()
        if line.lstrip().upper().startswith("COPY ")
    ]
    boundary_copy = f"COPY {HUAURA_BOUNDARY_SOURCE} {HUAURA_BOUNDARY_DESTINATION}"
    assert copy_instructions.count(boundary_copy) == 1

    copied_text = "\n".join(
        instruction for instruction in copy_instructions if instruction != boundary_copy
    ).casefold()
    for forbidden_copy in ("input-bindings.json", "data/", "downloads/", "/etc/via"):
        assert forbidden_copy not in copied_text
    assert "COPY . " not in dockerfile


def test_image_declares_b5_canonical_filesystem_contract() -> None:
    dockerfile = (REPOSITORY_ROOT / "Dockerfile").read_text(encoding="utf-8")
    instructions = [
        line.strip()
        for line in dockerfile.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]

    assert "VIA_CROPSUITE_ROOT=/opt/via/CropSuiteLite" in dockerfile
    assert "VIA_CROPSUITE_WORKSPACE=/var/lib/via/workspace" in dockerfile
    assert "VIA_ARTIFACTS_ROOT=/var/lib/via/artifacts" in dockerfile
    assert "VIA_CROPSUITE_INPUT_BINDINGS=/etc/via/input-bindings.json" in dockerfile
    assert "/mnt/via/sources" in dockerfile
    assert "/etc/via" in dockerfile
    assert not any(line.upper().startswith("VOLUME ") for line in instructions)


def test_image_defaults_to_exec_form_production_api_command() -> None:
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


def test_image_has_no_shell_process_multiplexer() -> None:
    dockerfile = (REPOSITORY_ROOT / "Dockerfile").read_text(encoding="utf-8").casefold()

    for forbidden in ("sh -c", "bash -c", "supervisor", "systemd"):
        assert forbidden not in dockerfile


def test_migration_cli_is_registered_and_container_has_structural_config_path() -> None:
    pyproject = tomllib.loads(
        (REPOSITORY_ROOT / "backend" / "pyproject.toml").read_text(encoding="utf-8")
    )
    dockerfile = (REPOSITORY_ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert pyproject["project"]["scripts"]["via-migrate"] == "via_backend.migrate:main"
    assert "VIA_ALEMBIC_CONFIG=/opt/via/backend/alembic.ini" in dockerfile


def test_api_and_worker_hosts_do_not_import_migration_execution() -> None:
    forbidden_modules = {"alembic", "via_backend.migrate"}
    host_paths = (
        REPOSITORY_ROOT / "backend" / "src" / "via_backend" / "api.py",
        REPOSITORY_ROOT / "backend" / "src" / "via_backend" / "app.py",
        REPOSITORY_ROOT / "backend" / "src" / "via_backend" / "worker.py",
    )

    for host_path in host_paths:
        tree = ast.parse(host_path.read_text(encoding="utf-8"), filename=str(host_path))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        assert forbidden_modules.isdisjoint(imported), host_path
