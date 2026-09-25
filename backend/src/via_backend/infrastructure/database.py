"""Host-level SQLAlchemy engine and session construction."""

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

SessionFactory = sessionmaker[Session]


def create_database(
    database_url: str,
    *,
    transaction_pooler: bool = False,
    pool_size: int | None = None,
    max_overflow: int | None = None,
    pool_timeout_seconds: int | None = None,
    pool_recycle_seconds: int | None = None,
) -> tuple[Engine, SessionFactory]:
    """Create the shared engine and short-lived session factory."""
    if transaction_pooler:
        engine = create_engine(
            database_url,
            poolclass=NullPool,
            connect_args={"prepare_threshold": None},
        )
        return engine, sessionmaker(bind=engine, expire_on_commit=False)

    engine_options: dict[str, object] = {"pool_pre_ping": True}
    if pool_size is not None:
        engine_options["pool_size"] = pool_size
    if max_overflow is not None:
        engine_options["max_overflow"] = max_overflow
    if pool_timeout_seconds is not None:
        engine_options["pool_timeout"] = pool_timeout_seconds
    if pool_recycle_seconds is not None:
        engine_options["pool_recycle"] = pool_recycle_seconds
    engine = create_engine(database_url, **engine_options)
    return engine, sessionmaker(bind=engine, expire_on_commit=False)
