"""SQLAlchemy metadata owned by Agroclimatic Evaluation Infrastructure."""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from via_backend.infrastructure.database import NAMING_CONVENTION

AGROCLIMATIC_EVALUATION_SCHEMA = "agroclimatic_evaluation"


class Base(DeclarativeBase):
    """Declarative base for Agroclimatic Evaluation persistence records."""

    metadata = MetaData(
        schema=AGROCLIMATIC_EVALUATION_SCHEMA,
        naming_convention=NAMING_CONVENTION,
    )
