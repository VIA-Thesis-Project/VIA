"""Development-compatible ASGI module."""

from via_backend.app import create_app, create_production_app

app = create_app()

__all__ = ["app", "create_app", "create_production_app"]
