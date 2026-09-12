"""SQLAlchemy metadata owned by Environmental Information Infrastructure."""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from via_backend.infrastructure.database import NAMING_CONVENTION

ENVIRONMENTAL_INFORMATION_SCHEMA = "environmental_information"


class Base(DeclarativeBase):
    """Declarative base for Environmental Information persistence records."""

    metadata = MetaData(
        schema=ENVIRONMENTAL_INFORMATION_SCHEMA,
        naming_convention=NAMING_CONVENTION,
    )
