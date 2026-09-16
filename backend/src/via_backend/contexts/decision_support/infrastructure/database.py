"""SQLAlchemy metadata owned by Decision Support Infrastructure."""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from via_backend.infrastructure.database import NAMING_CONVENTION

DECISION_SUPPORT_SCHEMA = "decision_support"


class Base(DeclarativeBase):
    """Declarative base for Decision Support persistence records."""

    metadata = MetaData(
        schema=DECISION_SUPPORT_SCHEMA,
        naming_convention=NAMING_CONVENTION,
    )