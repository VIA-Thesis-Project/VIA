"""Fast tests for the VIA worker process host and operator CLI."""

from __future__ import annotations

import json
import signal
from datetime import UTC, datetime
from threading import Event
from uuid import UUID

import pytest

import via_backend.worker as worker_host
from via_backend.contexts.agroclimatic_evaluation.application import (
    ActiveEvaluationResult,
    ResourceConflictError,
    WorkerRunSummary,
)
from via_backend.contexts.agroclimatic_evaluation.domain import EvaluationStatus, WaterRegime


def test_shutdown_handler_only_requests_cooperative_stop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unexpected_database_access(*_args, **_kwargs):
        raise AssertionError("signal handler accessed the database")

    monkeypatch.setattr(worker_host, "create_database", unexpected_database_access)

    for signum in (signal.SIGINT, signal.SIGTERM):
        stop_event = Event()
        handler = worker_host.make_shutdown_handler(stop_event)

        handler(signum, None)

        assert stop_event.is_set()


def test_run_forever_does_not_poll_again_after_stop_is_requested() -> None:
    stop_event = Event()

    class FakeWorker:
        batch_size = 2

        def __init__(self) -> None:
            self.calls = 0

        def run_once(self, *, stop_requested):
            self.calls += 1
            assert not stop_requested()
            stop_event.set()
            return WorkerRunSummary(0, 0, 0, 0, 0)

    worker = FakeWorker()

    worker_host.run_forever(
        worker,  # type: ignore[arg-type]
        poll_interval_seconds=5.0,
        stop_event=stop_event,
    )

    assert worker.calls == 1


def test_run_forever_poll_wait_can_be_interrupted_by_stop() -> None:
    stop_event = Event()
    waits: list[float] = []

    class FakeWorker:
        batch_size = 2

        def __init__(self) -> None:
            self.calls = 0

        def run_once(self, *, stop_requested):
            self.calls += 1
            assert not stop_requested()
            return WorkerRunSummary(0, 0, 0, 0, 0)

    worker = FakeWorker()

    def interrupt_wait(seconds: float) -> bool:
        waits.append(seconds)
        stop_event.set()
        return True

    worker_host.run_forever(
        worker,  # type: ignore[arg-type]
        poll_interval_seconds=3.5,
        stop_event=stop_event,
        wait_for_stop=interrupt_wait,
    )

    assert worker.calls == 1
    assert waits == [3.5]


def test_active_cli_emits_only_safe_stable_fields(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv(
        "VIA_DATABASE_URL",
        "postgresql+psycopg://secret-user:secret-password@example.invalid/via",
    )
    result = ActiveEvaluationResult(
        evaluation_id=UUID(int=7),
        status=EvaluationStatus.RUNNING,
        created_at=datetime(2026, 9, 16, 18, 0, tzinfo=UTC),
        requested_crop_count=3,
        completed_crop_count=1,
        requested_water_regimes=(WaterRegime.RAINFED, WaterRegime.IRRIGATED),
        requested_execution_count=6,
        completed_execution_count=1,
    )
    observed_limits: list[int] = []

    def fake_list_active(_settings, *, limit: int):
        observed_limits.append(limit)
        return (result,)

    monkeypatch.setattr(worker_host, "list_active_evaluations", fake_list_active)

    worker_host.main(["active", "--limit", "7"])

    output = capsys.readouterr().out.strip()
    payload = json.loads(output)
    assert observed_limits == [7]
    assert payload == {
        "evaluation_id": str(result.evaluation_id),
        "status": "running",
        "created_at": "2026-09-16T18:00:00+00:00",
        "requested_crop_count": 3,
        "completed_crop_count": 1,
        "requested_water_regimes": ["rainfed", "irrigated"],
        "requested_execution_count": 6,
        "completed_execution_count": 1,
    }
    assert "secret-password" not in output
    assert "source_reference" not in output
    assert "storage_reference" not in output


def test_active_cli_rejects_non_positive_limit() -> None:
    with pytest.raises(SystemExit) as error:
        worker_host.main(["active", "--limit", "0"])

    assert error.value.code == 2


def test_recover_cli_requires_expected_status_and_reason() -> None:
    evaluation_id = str(UUID(int=8))

    with pytest.raises(SystemExit) as missing_status:
        worker_host.main(["recover", evaluation_id, "--reason", "operator confirmed"])
    assert missing_status.value.code == 2

    with pytest.raises(SystemExit) as missing_reason:
        worker_host.main(
            ["recover", evaluation_id, "--expected-status", "running"]
        )
    assert missing_reason.value.code == 2


def test_recover_cli_maps_only_active_expected_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VIA_DATABASE_URL", "postgresql+psycopg://example.invalid/via")
    evaluation_id = UUID(int=9)
    calls: list[tuple[UUID, EvaluationStatus, str]] = []

    def fake_recover(
        _settings,
        *,
        evaluation_id: UUID,
        expected_status: EvaluationStatus,
        reason: str,
    ) -> None:
        calls.append((evaluation_id, expected_status, reason))

    monkeypatch.setattr(worker_host, "recover_evaluation", fake_recover)

    worker_host.main(
        [
            "recover",
            str(evaluation_id),
            "--expected-status",
            "summarizing",
            "--reason",
            "worker container stopped",
        ]
    )

    assert calls == [
        (
            evaluation_id,
            EvaluationStatus.SUMMARIZING,
            "worker container stopped",
        )
    ]

    with pytest.raises(SystemExit) as invalid_status:
        worker_host.main(
            [
                "recover",
                str(evaluation_id),
                "--expected-status",
                "failed",
                "--reason",
                "invalid",
            ]
        )
    assert invalid_status.value.code == 2


def test_recover_cli_surfaces_stale_status_conflict(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VIA_DATABASE_URL", "postgresql+psycopg://example.invalid/via")

    def stale_recovery(*_args, **_kwargs) -> None:
        raise ResourceConflictError(
            "expected status running but actual status is summarizing"
        )

    monkeypatch.setattr(worker_host, "recover_evaluation", stale_recovery)

    with pytest.raises(ResourceConflictError, match="actual status is summarizing"):
        worker_host.main(
            [
                "recover",
                str(UUID(int=10)),
                "--expected-status",
                "running",
                "--reason",
                "stale observation",
            ]
        )


def test_main_closes_runtime_when_systemic_worker_failure_escapes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VIA_DATABASE_URL", "postgresql+psycopg://example.invalid/via")

    class FakeRuntime:
        worker = object()

        def __init__(self) -> None:
            self.closed = False

        def close(self) -> None:
            self.closed = True

    runtime = FakeRuntime()
    monkeypatch.setattr(worker_host, "create_worker", lambda _settings: runtime)
    monkeypatch.setattr(worker_host.signal, "signal", lambda *_args: None)

    def fail_run_forever(*_args, **_kwargs) -> None:
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(worker_host, "run_forever", fail_run_forever)

    with pytest.raises(RuntimeError, match="database unavailable"):
        worker_host.main(["run"])

    assert runtime.closed
