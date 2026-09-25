"""Tests for host-level SQLAlchemy database construction."""

from __future__ import annotations

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.pool import NullPool, QueuePool

import via_backend.infrastructure.database as database_module
import via_backend.worker as worker_module
from via_backend.config import WorkerSettings


def test_create_database_defaults_to_queue_pool() -> None:
    engine, _sessions = database_module.create_database(
        "postgresql+psycopg://user:password@example.invalid/via"
    )

    try:
        assert isinstance(engine.pool, QueuePool)
    finally:
        engine.dispose()


def test_create_database_transaction_pooler_uses_null_pool() -> None:
    engine, _sessions = database_module.create_database(
        "postgresql+psycopg://user:password@example.invalid/via",
        transaction_pooler=True,
    )

    try:
        assert isinstance(engine.pool, NullPool)
    finally:
        engine.dispose()


def test_transaction_pooler_uses_psycopg_without_local_queue_pool_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    fallback_engine = create_engine("sqlite://")

    def capture_create_engine(database_url: str, **kwargs: object) -> Engine:
        captured["database_url"] = database_url
        captured.update(kwargs)
        return fallback_engine

    monkeypatch.setattr(database_module, "create_engine", capture_create_engine)

    database_module.create_database(
        "postgresql+psycopg://user:password@example.invalid/via",
        transaction_pooler=True,
        pool_size=99,
        max_overflow=98,
        pool_timeout_seconds=97,
        pool_recycle_seconds=96,
    )

    assert captured["poolclass"] is NullPool
    assert captured["connect_args"] == {"prepare_threshold": None}
    assert "pool_size" not in captured
    assert "max_overflow" not in captured
    assert "pool_timeout" not in captured
    assert "pool_recycle" not in captured
    assert "pool_pre_ping" not in captured


def test_worker_database_construction_keeps_queue_pool_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[tuple[object, ...], dict[str, object]]] = []

    def capture_create_database(*args: object, **kwargs: object) -> tuple[object, object]:
        calls.append((args, kwargs))
        return object(), object()

    monkeypatch.setattr(worker_module, "create_database", capture_create_database)
    settings = WorkerSettings(
        database_url="postgresql+psycopg://example.invalid/via",
        database_pool_size=2,
        database_max_overflow=1,
        database_pool_timeout_seconds=15,
        database_pool_recycle_seconds=120,
    )

    worker_module._create_worker_database(settings)

    assert calls == [
        (
            ("postgresql+psycopg://example.invalid/via",),
            {
                "pool_size": 2,
                "max_overflow": 1,
                "pool_timeout_seconds": 15,
                "pool_recycle_seconds": 120,
            },
        )
    ]
    assert not hasattr(settings, "database_transaction_pooler")
