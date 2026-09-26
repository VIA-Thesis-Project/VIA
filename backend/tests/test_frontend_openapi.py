"""OpenAPI contracts consumed by the frontend handoff."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import via_backend.app as app_module
from via_backend.config import Settings


class _Engine:
    def dispose(self) -> None:
        pass


class _Sessions:
    pass


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
COMMITTED_OPENAPI = REPOSITORY_ROOT / "docs" / "frontend" / "openapi.json"


def _schema(monkeypatch: Any) -> dict[str, Any]:
    monkeypatch.setattr(
        app_module,
        "create_database",
        lambda _url, **_kwargs: (_Engine(), _Sessions()),
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


def test_ia3_routes_publish_bearer_security_and_authoritative_parcel_reference(
    monkeypatch: Any,
) -> None:
    schema = _schema(monkeypatch)
    bearer = [{"BearerAuth": []}]

    protected_operations = (
        ("/projects", "get"),
        ("/projects", "post"),
        ("/projects/{project_id}", "get"),
        ("/projects/{project_id}/parcels", "get"),
        ("/projects/{project_id}/parcels", "post"),
        ("/projects/{project_id}/parcels/{parcel_id}", "get"),
        ("/projects/{project_id}/parcels/{parcel_id}/versions", "post"),
        ("/api/v1/evaluations", "get"),
        ("/api/v1/evaluations", "post"),
        ("/api/v1/evaluations/{evaluation_id}", "get"),
        ("/api/v1/evaluations/{evaluation_id}/result", "get"),
        ("/api/v1/evaluations/{evaluation_id}/evidence", "get"),
        ("/api/v1/evaluations/{evaluation_id}/limitations", "get"),
        ("/api/v1/evaluation-capabilities", "get"),
    )
    for path, method in protected_operations:
        assert schema["paths"][path][method]["security"] == bearer

    request_schema = schema["paths"]["/api/v1/evaluations"]["post"][
        "requestBody"
    ]["content"]["application/json"]["schema"]
    component_name = request_schema["$ref"].rsplit("/", maxsplit=1)[-1]
    properties = schema["components"]["schemas"][component_name]["properties"]

    assert "parcel_reference" in properties
    assert "parcel_snapshot" not in properties
    parcel_reference_name = properties["parcel_reference"]["$ref"].rsplit(
        "/", maxsplit=1
    )[-1]
    assert set(
        schema["components"]["schemas"][parcel_reference_name]["properties"]
    ) == {"project_id", "parcel_id", "parcel_version"}


def test_all_live_functional_routes_publish_bearer_security(monkeypatch: Any) -> None:
    schema = _schema(monkeypatch)
    bearer = [{"BearerAuth": []}]
    public_operations = {
        ("/health", "get"),
        ("/api/v1/auth/login", "post"),
        ("/api/v1/auth/refresh", "post"),
        ("/api/v1/auth/logout", "post"),
    }

    for path, path_item in schema["paths"].items():
        for method, operation in path_item.items():
            if method not in {"get", "post", "put", "patch", "delete"}:
                continue
            if (path, method) in public_operations:
                assert "security" not in operation
            else:
                assert operation["security"] == bearer, (path, method)


def test_openapi_publishes_role_and_cost_failures(monkeypatch: Any) -> None:
    schema = _schema(monkeypatch)
    expected = {
        ("/api/v1/auth/login", "post"): {"401", "429"},
        ("/api/v1/auth/refresh", "post"): {"401", "403", "429"},
        ("/api/v1/auth/logout", "post"): {"403"},
        ("/datasets", "post"): {"403"},
        ("/datasets/{dataset_id}/versions", "post"): {"403"},
        ("/datasets/{dataset_id}/versions/{version_id}/coverage", "post"): {"429"},
        (
            "/api/v1/decision-support/evaluations/{evaluation_id}/knowledge",
            "get",
        ): {"404", "409", "429", "503"},
        (
            "/api/v1/decision-support/evaluations/{evaluation_id}/recommendations",
            "post",
        ): {"403", "404", "409", "429", "503"},
    }

    for (path, method), statuses in expected.items():
        assert statuses <= set(schema["paths"][path][method]["responses"]), (path, method)

    assert "429" not in schema["paths"]["/api/v1/evaluations"]["post"]["responses"]
    recommendation_responses = schema["paths"][
        "/api/v1/decision-support/evaluations/{evaluation_id}/recommendations"
    ]["post"]["responses"]
    assert recommendation_responses["429"]["description"] == "Recommendation rate limit exceeded."


def test_openapi_response_dtos_do_not_publish_storage_or_secret_fields(
    monkeypatch: Any,
) -> None:
    schema = _schema(monkeypatch)
    components = schema["components"]["schemas"]

    assert "storage_reference" not in components["DatasetVersionResponse"]["properties"]
    assert (
        "source_storage_reference"
        not in components["LimitingFactorResponse"]["properties"]
    )
    assert "refresh_token" not in components["AuthenticationResponse"]["properties"]
    serialized = json.dumps(schema).casefold()
    for forbidden in (
        "/srv/",
        "/opt/",
        "database_url",
        "openai_api_key",
        "access_token_hash",
        "refresh_token_hash",
        "traceback",
    ):
        assert forbidden not in serialized


def test_evaluation_request_accepts_only_authoritative_references(monkeypatch: Any) -> None:
    schema = _schema(monkeypatch)
    request_ref = schema["paths"]["/api/v1/evaluations"]["post"]["requestBody"][
        "content"
    ]["application/json"]["schema"]["$ref"]
    request = schema["components"]["schemas"][request_ref.rsplit("/", 1)[-1]]

    assert set(request["properties"]) == {
        "parcel_reference",
        "requested_crops",
        "water_regimes",
        "environmental_inputs",
    }
    assert request["additionalProperties"] is False


def test_committed_openapi_matches_live_non_production_schema(monkeypatch: Any) -> None:
    committed = json.loads(COMMITTED_OPENAPI.read_text(encoding="utf-8"))

    assert committed == _schema(monkeypatch)
