"""OpenAPI contracts consumed by the frontend handoff."""

from __future__ import annotations

from typing import Any

import via_backend.app as app_module
from via_backend.config import Settings


class _Engine:
    def dispose(self) -> None:
        pass


class _Sessions:
    pass


def _schema(monkeypatch: Any) -> dict[str, Any]:
    monkeypatch.setattr(
        app_module,
        "create_database",
        lambda _: (_Engine(), _Sessions()),
    )
    app = app_module.create_app(
        Settings(
            farm_management_repository="postgresql",
            environmental_information_repository="postgresql",
            agroclimatic_evaluation_repository="postgresql",
            database_url="postgresql+psycopg://example.invalid/via",
        )
    )
    return app.openapi()


def test_decision_support_responses_publish_real_schemas(monkeypatch: Any) -> None:
    schema = _schema(monkeypatch)
    base = "/api/v1/decision-support/evaluations/{evaluation_id}"

    knowledge = schema["paths"][f"{base}/knowledge"]["get"]["responses"]["200"]
    created = schema["paths"][f"{base}/recommendations"]["post"]["responses"]["200"]
    listed = schema["paths"][f"{base}/recommendations"]["get"]["responses"]["200"]

    assert knowledge["content"]["application/json"]["schema"]["$ref"].endswith(
        "/RetrievedKnowledge"
    )
    assert created["content"]["application/json"]["schema"]["$ref"].endswith(
        "/RecommendationRun"
    )
    assert listed["content"]["application/json"]["schema"]["type"] == "array"
    assert listed["content"]["application/json"]["schema"]["items"]["$ref"].endswith(
        "/RecommendationRun"
    )


def test_frontend_operation_ids_are_explicit_and_unique(monkeypatch: Any) -> None:
    schema = _schema(monkeypatch)
    operation_ids = [
        operation["operationId"]
        for path_item in schema["paths"].values()
        for method, operation in path_item.items()
        if method in {"get", "post", "put", "patch", "delete"}
    ]

    assert len(operation_ids) == len(set(operation_ids))
    assert {
        "auth_login",
        "auth_refresh",
        "auth_logout",
        "auth_me",
        "list_projects",
        "create_project",
        "get_project",
        "create_parcel",
        "list_parcels",
        "get_parcel",
        "create_parcel_version",
        "list_datasets",
        "create_dataset",
        "get_dataset",
        "create_dataset_version",
        "list_dataset_versions",
        "get_dataset_version",
        "check_dataset_coverage",
        "request_evaluation",
        "list_evaluations",
        "get_evaluation",
        "get_evaluation_result",
        "get_evaluation_evidence",
        "get_evaluation_limitations",
        "get_evaluation_knowledge",
        "create_evaluation_recommendation",
        "list_evaluation_recommendations",
        "get_evaluation_capabilities",
    } <= set(operation_ids)
