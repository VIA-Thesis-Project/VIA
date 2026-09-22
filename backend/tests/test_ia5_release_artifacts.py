"""Static IA-5 gates for release documentation and production smoke safety."""

from __future__ import annotations

import re
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = REPOSITORY_ROOT / "docs" / "operations" / "production-release.md"
SMOKE = REPOSITORY_ROOT / "scripts" / "smoke_production_api.py"
MIGRATIONS = REPOSITORY_ROOT / "backend" / "migrations" / "versions"


def test_release_runbook_preserves_edge_migration_ownership_and_rollback_contracts() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")

    for required in (
        "Tailscale Funnel",
        "127.0.0.1:8000",
        "must never bind to `0.0.0.0`",
        "request.client.host",
        "does not trust `X-Forwarded-For`",
        "via-legacy-ownership-admin report",
        "Dry-run an explicit assignment",
        "--apply",
        "20260921_0017",
        "Prefer an application-only rollback",
        "Do not downgrade to 0016",
        "previous immutable digest",
    ):
        assert required in text


def test_production_smoke_is_secret_safe_and_covers_the_release_flow() -> None:
    source = SMOKE.read_text(encoding="utf-8")
    compile(source, str(SMOKE), "exec")

    for required in (
        "getpass.getpass",
        "VIA_SMOKE_PASSWORD",
        '"/health"',
        '"/api/v1/auth/login"',
        '"/api/v1/auth/me"',
        '"/api/v1/evaluation-capabilities"',
        '"/projects"',
        '"/api/v1/evaluations"',
        '"result", "evidence", "limitations"',
        "/knowledge?{query}",
        '"force_regenerate": False',
    ):
        assert required in source
    assert "print(login[\"access_token\"])" not in source
    assert "print(response_headers)" not in source


def test_expected_alembic_head_remains_0017_without_unnecessary_0018() -> None:
    revisions: set[str] = set()
    parents: set[str] = set()
    for migration in MIGRATIONS.glob("*.py"):
        source = migration.read_text(encoding="utf-8")
        revision = re.search(r'^revision:\s*str\s*=\s*"([^"]+)"', source, re.MULTILINE)
        parent = re.search(
            r'^down_revision:\s*str\s*\|\s*None\s*=\s*(?:"([^"]+)"|None)',
            source,
            re.MULTILINE,
        )
        assert revision is not None, migration
        assert parent is not None, migration
        revisions.add(revision.group(1))
        if parent.group(1):
            parents.add(parent.group(1))

    assert revisions - parents == {"20260921_0017"}
    assert not any(path.name.startswith("20260921_0018") for path in MIGRATIONS.glob("*.py"))
