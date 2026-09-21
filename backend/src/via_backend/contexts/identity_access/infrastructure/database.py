"""SQLAlchemy metadata owned by Identity Access Infrastructure."""

from __future__ import annotations

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from via_backend.infrastructure.database import (
    NAMING_CONVENTION,
    SessionFactory,
    create_database,
)

IDENTITY_ACCESS_SCHEMA = "identity_access"


class Base(DeclarativeBase):
    """Declarative base for Identity Access persistence records."""

    metadata = MetaData(schema=IDENTITY_ACCESS_SCHEMA, naming_convention=NAMING_CONVENTION)


__all__ = ["Base", "IDENTITY_ACCESS_SCHEMA", "SessionFactory", "create_database"]
