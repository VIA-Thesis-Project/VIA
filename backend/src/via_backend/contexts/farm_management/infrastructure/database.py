"""SQLAlchemy database primitives owned by Farm Management Infrastructure."""

from __future__ import annotations

from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

FARM_MANAGEMENT_SCHEMA = "farm_management"

NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Declarative base for Farm Management persistence records."""

    metadata = MetaData(schema=FARM_MANAGEMENT_SCHEMA, naming_convention=NAMING_CONVENTION)


SessionFactory = sessionmaker[Session]


def create_database(database_url: str) -> tuple[Engine, SessionFactory]:
    """Create the engine and short-lived session factory used by repositories."""
    engine = create_engine(database_url, pool_pre_ping=True)
    return engine, sessionmaker(bind=engine, expire_on_commit=False)
