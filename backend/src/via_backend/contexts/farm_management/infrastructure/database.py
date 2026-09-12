"""SQLAlchemy metadata owned by Farm Management Infrastructure."""

from __future__ import annotations

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from via_backend.infrastructure.database import (
    NAMING_CONVENTION,
    SessionFactory,
    create_database,
)

FARM_MANAGEMENT_SCHEMA = "farm_management"

class Base(DeclarativeBase):
    """Declarative base for Farm Management persistence records."""

    metadata = MetaData(schema=FARM_MANAGEMENT_SCHEMA, naming_convention=NAMING_CONVENTION)
__all__ = ["Base", "SessionFactory", "create_database"]
