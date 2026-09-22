"""Explicit administration of legacy rows that predate ownership enforcement."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import Connection, Engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

from via_backend.config import Settings
from via_backend.infrastructure import create_database


@dataclass(frozen=True, slots=True)
class LegacyOwnershipReport:
    project_ids: tuple[UUID, ...]
    evaluation_ids: tuple[UUID, ...]


@dataclass(frozen=True, slots=True)
class LegacyOwnershipAssignment:
    target_user_id: UUID
    target_user_status: str
    project_ids: tuple[UUID, ...]
    evaluation_ids: tuple[UUID, ...]
    applied: bool


class LegacyOwnershipError(RuntimeError):
    """Raised when an explicit legacy ownership operation cannot be performed safely."""


class PostgreSQLLegacyOwnershipStore:
    """Fail-closed operations over only the two nullable legacy owner columns."""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def report(self) -> LegacyOwnershipReport:
        with self._engine.connect() as connection:
            projects = tuple(
                connection.execute(
                    text(
                        "SELECT id FROM farm_management.projects "
                        "WHERE owner_user_id IS NULL ORDER BY id"
                    )
                ).scalars()
            )
            evaluations = tuple(
                connection.execute(
                    text(
                        "SELECT id FROM agroclimatic_evaluation.evaluations "
                        "WHERE owner_user_id IS NULL ORDER BY id"
                    )
                ).scalars()
            )
        return LegacyOwnershipReport(
            project_ids=projects,
            evaluation_ids=evaluations,
        )

    def assign(
        self,
        *,
        target_user_id: UUID,
        project_ids: tuple[UUID, ...],
        evaluation_ids: tuple[UUID, ...],
        apply: bool,
    ) -> LegacyOwnershipAssignment:
        if not project_ids and not evaluation_ids:
            raise LegacyOwnershipError(
                "At least one explicit --project-id or --evaluation-id is required."
            )

        with self._engine.begin() as connection:
            target_user_status = self._require_target_user(connection, target_user_id)
            self._require_unowned_resources(
                connection,
                table="farm_management.projects",
                resource_kind="project",
                resource_ids=project_ids,
            )
            self._require_unowned_resources(
                connection,
                table="agroclimatic_evaluation.evaluations",
                resource_kind="evaluation",
                resource_ids=evaluation_ids,
            )
            if apply:
                self._assign_resources(
                    connection,
                    table="farm_management.projects",
                    resource_kind="project",
                    resource_ids=project_ids,
                    target_user_id=target_user_id,
                )
                self._assign_resources(
                    connection,
                    table="agroclimatic_evaluation.evaluations",
                    resource_kind="evaluation",
                    resource_ids=evaluation_ids,
                    target_user_id=target_user_id,
                )

        return LegacyOwnershipAssignment(
            target_user_id=target_user_id,
            target_user_status=target_user_status,
            project_ids=project_ids,
            evaluation_ids=evaluation_ids,
            applied=apply,
        )

    @staticmethod
    def _require_target_user(connection: Connection, target_user_id: UUID) -> str:
        status = connection.execute(
            text("SELECT status FROM identity_access.users WHERE id = :user_id FOR UPDATE"),
            {"user_id": target_user_id},
        ).scalar_one_or_none()
        if status is None:
            raise LegacyOwnershipError(f"Target user does not exist: {target_user_id}")
        return str(status)

    @staticmethod
    def _require_unowned_resources(
        connection: Connection,
        *,
        table: str,
        resource_kind: str,
        resource_ids: tuple[UUID, ...],
    ) -> None:
        for resource_id in resource_ids:
            row = connection.execute(
                text(f"SELECT owner_user_id FROM {table} WHERE id = :resource_id FOR UPDATE"),
                {"resource_id": resource_id},
            ).one_or_none()
            if row is None:
                raise LegacyOwnershipError(
                    f"Selected {resource_kind} does not exist: {resource_id}"
                )
            owner_user_id = row[0]
            if owner_user_id is not None:
                raise LegacyOwnershipError(
                    f"Selected {resource_kind} is already owned: "
                    f"{resource_id} owner_user_id={owner_user_id}"
                )

    @staticmethod
    def _assign_resources(
        connection: Connection,
        *,
        table: str,
        resource_kind: str,
        resource_ids: tuple[UUID, ...],
        target_user_id: UUID,
    ) -> None:
        for resource_id in resource_ids:
            result = connection.execute(
                text(
                    f"UPDATE {table} SET owner_user_id = :target_user_id "
                    "WHERE id = :resource_id AND owner_user_id IS NULL"
                ),
                {
                    "target_user_id": target_user_id,
                    "resource_id": resource_id,
                },
            )
            if result.rowcount != 1:
                raise LegacyOwnershipError(
                    f"Concurrent ownership change detected for {resource_kind}: {resource_id}"
                )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="via-legacy-ownership-admin")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser(
        "report",
        help="Report exact project/evaluation IDs whose owner_user_id is still NULL.",
    )

    assign = commands.add_parser(
        "assign",
        help="Validate an explicit legacy ownership assignment; add --apply to persist it.",
    )
    assign.add_argument("--target-user-id", required=True, type=UUID)
    assign.add_argument("--project-id", action="append", type=UUID, default=[])
    assign.add_argument("--evaluation-id", action="append", type=UUID, default=[])
    assign.add_argument(
        "--apply",
        action="store_true",
        help="Persist the validated assignment. Without this flag, the command is a dry-run.",
    )
    return parser


def _store_from_env() -> tuple[PostgreSQLLegacyOwnershipStore, Engine]:
    settings = Settings.from_env()
    if settings.database_url is None:
        raise SystemExit("VIA_DATABASE_URL is required for legacy ownership administration.")
    try:
        backend = make_url(settings.database_url).get_backend_name()
    except ArgumentError as error:
        raise SystemExit("VIA_DATABASE_URL must be a valid PostgreSQL URL.") from error
    if backend != "postgresql":
        raise SystemExit("Legacy ownership administration requires PostgreSQL persistence.")

    engine, _ = create_database(settings.database_url)
    return PostgreSQLLegacyOwnershipStore(engine), engine


def _serialize_report(report: LegacyOwnershipReport) -> str:
    return json.dumps(
        {
            "operation": "legacy-ownership-report",
            "projects_with_null_owner": [str(value) for value in report.project_ids],
            "evaluations_with_null_owner": [str(value) for value in report.evaluation_ids],
        },
        sort_keys=True,
    )


def _serialize_assignment(assignment: LegacyOwnershipAssignment) -> str:
    return json.dumps(
        {
            "operation": "legacy-ownership-assignment",
            "mode": "apply" if assignment.applied else "dry-run",
            "target_user_id": str(assignment.target_user_id),
            "target_user_status": assignment.target_user_status,
            "project_ids": [str(value) for value in assignment.project_ids],
            "evaluation_ids": [str(value) for value in assignment.evaluation_ids],
        },
        sort_keys=True,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run explicit legacy ownership reporting or assignment."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "assign" and not (args.project_id or args.evaluation_id):
        parser.error("assign requires at least one --project-id or --evaluation-id")

    store, engine = _store_from_env()
    try:
        if args.command == "report":
            print(_serialize_report(store.report()))
            return 0
        if args.command == "assign":
            project_ids = tuple(dict.fromkeys(args.project_id))
            evaluation_ids = tuple(dict.fromkeys(args.evaluation_id))
            assignment = store.assign(
                target_user_id=args.target_user_id,
                project_ids=project_ids,
                evaluation_ids=evaluation_ids,
                apply=args.apply,
            )
            print(_serialize_assignment(assignment))
            return 0
        raise AssertionError(f"Unhandled command {args.command!r}")
    except LegacyOwnershipError as error:
        raise SystemExit(str(error)) from error
    finally:
        engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())
