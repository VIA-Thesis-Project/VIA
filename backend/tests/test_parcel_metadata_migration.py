"""Parcel metadata migration remains the single Alembic head."""

from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory


def test_parcel_metadata_migration_head() -> None:
    root = Path(__file__).resolve().parents[1]
    script = ScriptDirectory.from_config(Config(str(root / "alembic.ini")))
    assert script.get_heads() == ["20260927_0019"]
    revision = script.get_revision("20260927_0019")
    assert revision is not None
    assert revision.down_revision == "20260927_0018"
