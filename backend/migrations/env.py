"""Alembic environment for VIA database migrations."""

from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from via_backend.contexts.agroclimatic_evaluation.infrastructure import (
    orm as evaluation_orm,  # noqa: F401
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.database import (
    AGROCLIMATIC_EVALUATION_SCHEMA,
)
from via_backend.contexts.agroclimatic_evaluation.infrastructure.database import (
    Base as AgroclimaticEvaluationBase,
)
from via_backend.contexts.environmental_information.infrastructure import (
    orm as environmental_orm,  # noqa: F401, E501
)
from via_backend.contexts.environmental_information.infrastructure.database import (
    ENVIRONMENTAL_INFORMATION_SCHEMA,
)
from via_backend.contexts.environmental_information.infrastructure.database import (
    Base as EnvironmentalInformationBase,
)
from via_backend.contexts.farm_management.infrastructure import orm  # noqa: F401
from via_backend.contexts.farm_management.infrastructure.database import (
    FARM_MANAGEMENT_SCHEMA,
)
from via_backend.contexts.farm_management.infrastructure.database import (
    Base as FarmManagementBase,
)
from via_backend.contexts.identity_access.infrastructure import (
    orm as identity_orm,  # noqa: F401
)
from via_backend.contexts.identity_access.infrastructure.database import (
    IDENTITY_ACCESS_SCHEMA,
)
from via_backend.contexts.identity_access.infrastructure.database import (
    Base as IdentityAccessBase,
)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = os.getenv("VIA_DATABASE_URL") or config.get_main_option("sqlalchemy.url")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))

target_metadata = [
    FarmManagementBase.metadata,
    EnvironmentalInformationBase.metadata,
    AgroclimaticEvaluationBase.metadata,
    IdentityAccessBase.metadata,
]


def include_name(
    name: str | None, type_: str, parent_names: dict[str, str | None]
) -> bool:
    """Limit autogeneration to bounded-context-owned schemas."""
    del parent_names
    return type_ != "schema" or name in {
        FARM_MANAGEMENT_SCHEMA,
        ENVIRONMENTAL_INFORMATION_SCHEMA,
        AGROCLIMATIC_EVALUATION_SCHEMA,
        IDENTITY_ACCESS_SCHEMA,
    }


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        raise RuntimeError("Set VIA_DATABASE_URL before running Alembic migrations.")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    if not config.get_main_option("sqlalchemy.url"):
        raise RuntimeError("Set VIA_DATABASE_URL before running Alembic migrations.")
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
