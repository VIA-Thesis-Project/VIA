"""HTTP discovery of deployment-selected scientific capabilities."""

import json
from pathlib import Path
from uuid import UUID

from fastapi import FastAPI
from fastapi.testclient import TestClient

from via_backend.app import create_app
from via_backend.config import Settings
from via_backend.contexts.agroclimatic_evaluation.application import (
    EvaluationCapabilitiesService,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    FilesystemCropCapabilityCatalog,
    FilesystemScientificInputBindingCatalog,
)
from via_backend.contexts.agroclimatic_evaluation.interfaces import (
    create_capabilities_router,
)
from via_backend.contexts.identity_access.application.public import AuthenticatedPrincipal
from via_backend.contexts.identity_access.domain import UserRole

AUTH_HEADERS = {"Authorization": "Bearer test-user"}


def _app(settings: Settings) -> FastAPI:
    app = FastAPI()

    def principal() -> AuthenticatedPrincipal:
        return AuthenticatedPrincipal(
            UUID("11111111-1111-4111-8111-111111111111"), UserRole.USER
        )

    app.include_router(
        create_capabilities_router(
            EvaluationCapabilitiesService(
                (
                    FilesystemCropCapabilityCatalog(settings.cropsuite_catalog)
                    if settings.cropsuite_catalog is not None
                    else None
                ),
                (
                    FilesystemScientificInputBindingCatalog(
                        settings.cropsuite_input_bindings
                    )
                    if settings.cropsuite_input_bindings is not None
                    else None
                ),
            ),
            principal,
        ),
        prefix="/api/v1",
    )
    return app


def _client(settings: Settings) -> TestClient:
    return TestClient(_app(settings), headers=AUTH_HEADERS)


def _catalog(tmp_path: Path) -> Path:
    catalog = tmp_path / "catalog"
    catalog.mkdir()

    (catalog / "maize.inf").write_text(
        "name = maize\ngrowing_cycle = 110.0\n",
        encoding="utf-8",
    )
    (catalog / "potato.inf").write_text(
        "name = potato\ngrowing_cycle = 120.0\n",
        encoding="utf-8",
    )

    return catalog


def _bindings(tmp_path: Path) -> Path:
    path = tmp_path / "input-bindings.json"

    path.write_text(
        json.dumps(
            {
                "bindings": [
                    {
                        "dataset_id": "11111111-1111-1111-1111-111111111111",
                        "dataset_version_id": "22222222-2222-2222-2222-222222222222",
                        "storage_reference": "fixture://environment-a",
                        "checksum": "fixture-checksum-a",
                        "source_sha256": ["a" * 64],
                    },
                    {
                        "dataset_id": "33333333-3333-3333-3333-333333333333",
                        "dataset_version_id": "44444444-4444-4444-4444-444444444444",
                        "storage_reference": "fixture://environment-b",
                        "checksum": "fixture-checksum-b",
                        "source_sha256": ["b" * 64],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    return path


def test_capabilities_publish_configured_crops_scenarios_and_bindings(
    tmp_path: Path,
) -> None:
    client = _client(
        Settings(
            cropsuite_catalog=_catalog(tmp_path),
            cropsuite_input_bindings=_bindings(tmp_path),
        )
    )

    response = client.get("/api/v1/evaluation-capabilities")

    assert response.status_code == 200
    assert response.json() == {
        "status": "partial",
        "crops": [
            {
                "crop_id": "maize",
                "display_name": "maize",
                "water_regimes": ["rainfed", "irrigated"],
            },
            {
                "crop_id": "potato",
                "display_name": "potato",
                "water_regimes": ["rainfed", "irrigated"],
            },
        ],
        "environmental_inputs": {
            "minimum_count": 1,
            "maximum_input_key_length": 120,
            "input_keys": [],
            "input_key_discovery": "arbitrary_unique",
            "requires_registered_dataset_version": True,
            "requires_scientific_binding": True,
            "scientifically_bound_dataset_versions": [
                {
                    "dataset_id": "11111111-1111-1111-1111-111111111111",
                    "dataset_version_id": "22222222-2222-2222-2222-222222222222",
                },
                {
                    "dataset_id": "33333333-3333-3333-3333-333333333333",
                    "dataset_version_id": "44444444-4444-4444-4444-444444444444",
                },
            ],
        },
        "limitations": [
            "Environmental input_key values are caller-defined unique logical "
            "identifiers and do not select scientific bindings. Dataset versions "
            "listed as scientifically bound are configured for this deployment, "
            "but execution may still fail later if runtime integrity checks fail."
        ],
    }


def test_capabilities_require_bearer_authentication() -> None:
    response = TestClient(create_app(Settings())).get(
        "/api/v1/evaluation-capabilities"
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_capabilities_do_not_expose_private_binding_details(
    tmp_path: Path,
) -> None:
    response = _client(
        Settings(
            cropsuite_catalog=_catalog(tmp_path),
            cropsuite_input_bindings=_bindings(tmp_path),
        )
    ).get("/api/v1/evaluation-capabilities")

    assert response.status_code == 200

    payload = response.json()
    serialized = json.dumps(payload)

    assert "storage_reference" not in serialized
    assert "source_sha256" not in serialized
    assert "checksum" not in serialized
    assert "fixture://environment" not in serialized


def test_capabilities_return_detail_error_when_catalog_is_not_configured() -> None:
    response = _client(Settings()).get(
        "/api/v1/evaluation-capabilities"
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Scientific crop capability discovery is not configured."
    }


def test_capabilities_return_detail_error_when_bindings_are_not_configured(
    tmp_path: Path,
) -> None:
    response = _client(
        Settings(
            cropsuite_catalog=_catalog(tmp_path),
        )
    ).get("/api/v1/evaluation-capabilities")

    assert response.status_code == 503
    assert response.json() == {
        "detail": (
            "Scientific environmental input binding discovery is not configured."
        )
    }


def test_capabilities_return_detail_error_when_bindings_are_invalid(
    tmp_path: Path,
) -> None:
    bindings = tmp_path / "invalid-bindings.json"
    bindings.write_text('{"bindings": []}', encoding="utf-8")

    response = _client(
        Settings(
            cropsuite_catalog=_catalog(tmp_path),
            cropsuite_input_bindings=bindings,
        )
    ).get("/api/v1/evaluation-capabilities")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Scientific environmental input binding discovery is unavailable."
    }
