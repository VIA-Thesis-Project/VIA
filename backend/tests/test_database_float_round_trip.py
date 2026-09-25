"""Database-engine precision configuration tests."""

from unittest.mock import Mock

from via_backend.infrastructure import database as database_module


def test_float_round_trip_hook_sets_transaction_local_precision(
    monkeypatch,
) -> None:
    engine = Mock()
    captured: dict[str, object] = {}

    def capture_listener(target, identifier, listener) -> None:
        captured["target"] = target
        captured["identifier"] = identifier
        captured["listener"] = listener

    monkeypatch.setattr(database_module.event, "listen", capture_listener)

    database_module._configure_float_round_trip(engine)

    assert captured["target"] is engine
    assert captured["identifier"] == "begin"

    connection = Mock()
    listener = captured["listener"]
    assert callable(listener)

    listener(connection)

    connection.exec_driver_sql.assert_called_once_with(
        "SET LOCAL extra_float_digits = 3"
    )
