"""Migration topology and Decision Support binding ownership."""

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory


def test_policy_binding_migration_is_the_single_alembic_head() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    script = ScriptDirectory.from_config(Config(str(backend_root / "alembic.ini")))
    assert script.get_heads() == ["20261001_0020"]
    revision = script.get_revision("20260927_0018")
    assert revision is not None
    assert revision.down_revision == "20260921_0017"
