"""Durable static invariants for the opt-in B6.1 resource benchmark."""

from __future__ import annotations

from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_SCRIPT = REPOSITORY_ROOT / "scripts" / "benchmark_production_runtime.sh"
BENCHMARK_COMPOSE = REPOSITORY_ROOT / "compose.benchmark.yaml"
BENCHMARK_WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "b6-resource-benchmark.yml"
CONTAINER_GATE = REPOSITORY_ROOT / ".github" / "workflows" / "b2-container-gate.yml"
GITIGNORE = REPOSITORY_ROOT / ".gitignore"


def test_benchmark_reuses_b6_topology_and_real_evaluation_endpoint() -> None:
    script = BENCHMARK_SCRIPT.read_text(encoding="utf-8")
    override = BENCHMARK_COMPOSE.read_text(encoding="utf-8")

    assert "compose.production-smoke.yaml" in script
    assert "compose.benchmark.yaml" in script
    assert "http://127.0.0.1:18000/api/v1/evaluations" in script
    assert "http://127.0.0.1:18000/datasets" in script
    assert "worker:" in override
    assert "VIA_BENCHMARK_SOURCE_DIR" in override
    assert "/mnt/via/sources:ro" in override


def test_benchmark_requires_external_science_and_keeps_integrity_bindings() -> None:
    script = BENCHMARK_SCRIPT.read_text(encoding="utf-8").lower()

    assert "source_sha256" in script
    assert "input-bindings.json" in script
    assert "smoke-only:bindings-loader-fixture" in script
    assert "the b6 startup-only bindings fixture cannot be used" in script
    assert "mock" not in script
    assert "stub" not in script
    assert "via_run_cropsuite_smoke" not in script


def test_benchmark_results_are_ignored_and_workflow_is_manual_only() -> None:
    workflow = BENCHMARK_WORKFLOW.read_text(encoding="utf-8")
    ignored = GITIGNORE.read_text(encoding="utf-8")

    assert "workflow_dispatch:" in workflow
    assert "pull_request:" not in workflow
    assert "push:" not in workflow
    assert "self-hosted" in workflow
    assert "benchmark-results.json" in ignored


def test_normal_b2_b6_gate_does_not_run_resource_benchmark() -> None:
    gate = CONTAINER_GATE.read_text(encoding="utf-8")

    assert "benchmark_production_runtime.sh" not in gate
    assert "b6-resource-benchmark.yml" not in gate

