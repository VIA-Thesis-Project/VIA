"""Generate the frontend OpenAPI snapshot without external service calls."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = REPOSITORY_ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

import via_backend.app as app_module
from via_backend.config import Settings


class _Engine:
    def dispose(self) -> None:
        pass


class _Sessions:
    pass


def main() -> None:
    app_module.create_database = lambda *_args, **_kwargs: (_Engine(), _Sessions())
    application = app_module.create_app(
        Settings(
            farm_management_repository="postgresql",
            environmental_information_repository="postgresql",
            agroclimatic_evaluation_repository="postgresql",
            database_url="postgresql+psycopg://example.invalid/via",
        )
    )
    destination = REPOSITORY_ROOT / "docs" / "frontend" / "openapi.json"
    destination.write_text(
        json.dumps(application.openapi(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
