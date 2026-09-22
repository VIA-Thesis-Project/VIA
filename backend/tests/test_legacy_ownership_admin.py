from __future__ import annotations

import json
from contextlib import contextmanager
from dataclasses import dataclass, field
from uuid import UUID

import pytest

import via_backend.legacy_ownership_admin as ownership_admin

USER_ID = UUID("10000000-0000-0000-0000-000000000001")
OTHER_USER_ID = UUID("10000000-0000-0000-0000-000000000002")
PROJECT_ID = UUID("20000000-0000-0000-0000-000000000001")
OTHER_PROJECT_ID = UUID("20000000-0000-0000-0000-000000000002")
EVALUATION_ID = UUID("30000000-0000-0000-0000-000000000001")
OTHER_EVALUATION_ID = UUID("30000000-0000-0000-0000-000000000002")


class _Result:
    def __init__(
        self,
        *,
        scalar: object | None = None,
        row: tuple[object, ...] | None = None,
        scalars: tuple[object, ...] = (),
        rowcount: int = -1,
    ) -> None:
        self._scalar = scalar
        self._row = row
        self._scalars = scalars
        self.rowcount = rowcount

    def scalar_one_or_none(self) -> object | None:
        return self._scalar

    def one_or_none(self) -> tuple[object, ...] | None:
        return self._row

    def scalars(self) -> tuple[object, ...]:
        return self._scalars


@dataclass
class _FakeDatabase:
    users: dict[UUID, str] = field(default_factory=dict)
    projects: dict[UUID, UUID | None] = field(default_factory=dict)
    evaluations: dict[UUID, UUID | None] = field(default_factory=dict)
    updates: list[tuple[str, UUID, UUID]] = field(default_factory=list)


class _Connection:
    def __init__(self, database: _FakeDatabase) -> None:
        self._database = database

    def execute(self, statement: object, parameters: dict[str, object] | None = None) -> _Result:
        sql = " ".join(str(statement).split())
        parameters = parameters or {}

        if sql.startswith("SELECT id FROM farm_management.projects"):
            values = tuple(
                sorted(
                    key 
                    for key, owner in self._database.projects.items() 
                    if owner is None
                )
            )
            return _Result(scalars=values)
        if sql.startswith("SELECT id FROM agroclimatic_evaluation.evaluations"):
            values = tuple(
                sorted(key for key, owner in self._database.evaluations.items() if owner is None)
            )
            return _Result(scalars=values)
        if sql.startswith("SELECT status FROM identity_access.users"):
            user_id = parameters["user_id"]
            assert isinstance(user_id, UUID)
            return _Result(scalar=self._database.users.get(user_id))

        resource_id = parameters.get("resource_id")
        if isinstance(resource_id, UUID):
            if "farm_management.projects" in sql:
                resources = self._database.projects
                kind = "project"
            elif "agroclimatic_evaluation.evaluations" in sql:
                resources = self._database.evaluations
                kind = "evaluation"
            else:
                raise AssertionError(sql)

            if sql.startswith("SELECT owner_user_id"):
                if resource_id not in resources:
                    return _Result(row=None)
                return _Result(row=(resources[resource_id],))

            if sql.startswith("UPDATE"):
                target_user_id = parameters["target_user_id"]
                assert isinstance(target_user_id, UUID)
                if resource_id not in resources or resources[resource_id] is not None:
                    return _Result(rowcount=0)
                resources[resource_id] = target_user_id
                self._database.updates.append((kind, resource_id, target_user_id))
                return _Result(rowcount=1)

        raise AssertionError(f"Unexpected SQL: {sql}")


class _Engine:
    def __init__(self, database: _FakeDatabase) -> None:
        self.database = database
        self.dispose_calls = 0

    @contextmanager
    def connect(self):
        yield _Connection(self.database)

    @contextmanager
    def begin(self):
        yield _Connection(self.database)

    def dispose(self) -> None:
        self.dispose_calls += 1


def test_report_lists_exact_null_owner_ids_only() -> None:
    engine = _Engine(
        _FakeDatabase(
            projects={PROJECT_ID: None, OTHER_PROJECT_ID: OTHER_USER_ID},
            evaluations={EVALUATION_ID: None, OTHER_EVALUATION_ID: OTHER_USER_ID},
        )
    )
    store = ownership_admin.PostgreSQLLegacyOwnershipStore(engine)  # type: ignore[arg-type]

    report = store.report()

    assert report.project_ids == (PROJECT_ID,)
    assert report.evaluation_ids == (EVALUATION_ID,)


def test_assignment_is_dry_run_by_default_and_never_infers_related_resources() -> None:
    engine = _Engine(
        _FakeDatabase(
            users={USER_ID: "active"},
            projects={PROJECT_ID: None, OTHER_PROJECT_ID: None},
            evaluations={EVALUATION_ID: None, OTHER_EVALUATION_ID: None},
        )
    )
    store = ownership_admin.PostgreSQLLegacyOwnershipStore(
        engine  # type: ignore[arg-type]
    )

    result = store.assign(
        target_user_id=USER_ID,
        project_ids=(PROJECT_ID,),
        evaluation_ids=(),
        apply=False,
    )

    assert result.applied is False
    assert engine.database.projects[PROJECT_ID] is None
    assert engine.database.projects[OTHER_PROJECT_ID] is None
    assert engine.database.evaluations[EVALUATION_ID] is None
    assert engine.database.updates == []


def test_apply_assigns_only_explicit_unowned_ids_to_explicit_existing_user() -> None:
    engine = _Engine(
        _FakeDatabase(
            users={USER_ID: "active"},
            projects={PROJECT_ID: None, OTHER_PROJECT_ID: None},
            evaluations={EVALUATION_ID: None, OTHER_EVALUATION_ID: None},
        )
    )
    store = ownership_admin.PostgreSQLLegacyOwnershipStore(engine)  # type: ignore[arg-type]

    result = store.assign(
        target_user_id=USER_ID,
        project_ids=(PROJECT_ID,),
        evaluation_ids=(EVALUATION_ID,),
        apply=True,
    )

    assert result.applied is True
    assert engine.database.projects == {PROJECT_ID: USER_ID, OTHER_PROJECT_ID: None}
    assert engine.database.evaluations == {
        EVALUATION_ID: USER_ID,
        OTHER_EVALUATION_ID: None,
    }
    assert engine.database.updates == [
        ("project", PROJECT_ID, USER_ID),
        ("evaluation", EVALUATION_ID, USER_ID),
    ]


def test_assignment_rejects_missing_target_user_and_preowned_resource() -> None:
    missing_user_engine = _Engine(_FakeDatabase(projects={PROJECT_ID: None}))
    missing_user_store = ownership_admin.PostgreSQLLegacyOwnershipStore(  # type: ignore[arg-type]
        missing_user_engine  # type: ignore[arg-type]
    )
    with pytest.raises(ownership_admin.LegacyOwnershipError, match="Target user does not exist"):
        missing_user_store.assign(
            target_user_id=USER_ID,
            project_ids=(PROJECT_ID,),
            evaluation_ids=(),
            apply=True,
        )

    owned_engine = _Engine(
        _FakeDatabase(
            users={USER_ID: "active"},
            projects={PROJECT_ID: OTHER_USER_ID},
        )
    )
    owned_store = ownership_admin.PostgreSQLLegacyOwnershipStore(owned_engine)  # type: ignore[arg-type]
    with pytest.raises(ownership_admin.LegacyOwnershipError, match="already owned"):
        owned_store.assign(
            target_user_id=USER_ID,
            project_ids=(PROJECT_ID,),
            evaluation_ids=(),
            apply=True,
        )
    assert owned_engine.database.projects[PROJECT_ID] == OTHER_USER_ID
    assert owned_engine.database.updates == []


def test_cli_requires_explicit_resource_id_before_database_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        ownership_admin,
        "_store_from_env",
        lambda: (_ for _ in ()).throw(AssertionError("database must not be opened")),
    )

    with pytest.raises(SystemExit):
        ownership_admin.main(["assign", "--target-user-id", str(USER_ID)])


def test_cli_outputs_auditable_json_and_disposes_engine(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    engine = _Engine(_FakeDatabase())

    class _Store:
        def assign(self, **kwargs: object) -> ownership_admin.LegacyOwnershipAssignment:
            assert kwargs == {
                "target_user_id": USER_ID,
                "project_ids": (PROJECT_ID,),
                "evaluation_ids": (EVALUATION_ID,),
                "apply": False,
            }
            return ownership_admin.LegacyOwnershipAssignment(
                target_user_id=USER_ID,
                target_user_status="active",
                project_ids=(PROJECT_ID,),
                evaluation_ids=(EVALUATION_ID,),
                applied=False,
            )

    monkeypatch.setattr(ownership_admin, "_store_from_env", lambda: (_Store(), engine))

    assert ownership_admin.main(
        [
            "assign",
            "--target-user-id",
            str(USER_ID),
            "--project-id",
            str(PROJECT_ID),
            "--evaluation-id",
            str(EVALUATION_ID),
        ]
    ) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "evaluation_ids": [str(EVALUATION_ID)],
        "mode": "dry-run",
        "operation": "legacy-ownership-assignment",
        "project_ids": [str(PROJECT_ID)],
        "target_user_id": str(USER_ID),
        "target_user_status": "active",
    }
    assert engine.dispose_calls == 1
