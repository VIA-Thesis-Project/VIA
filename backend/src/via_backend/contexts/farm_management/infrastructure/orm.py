"""Database records for Farm Management; these are not domain entities."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from geoalchemy2 import Geometry
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from .database import FARM_MANAGEMENT_SCHEMA, Base


class ProjectRecord(Base):
    __tablename__ = "projects"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ParcelRecord(Base):
    __tablename__ = "parcels"
    __table_args__ = (
        CheckConstraint("current_version >= 1", name="current_version_positive"),
        Index("ix_parcels_project_id", "project_id"),
    )

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, nullable=False
    )
    project_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(f"{FARM_MANAGEMENT_SCHEMA}.projects.id", ondelete="RESTRICT"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    current_version: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ParcelVersionRecord(Base):
    __tablename__ = "parcel_versions"
    __table_args__ = (
        CheckConstraint("number >= 1", name="number_positive"),
        CheckConstraint(
            "geometry_type IN ('Polygon', 'MultiPolygon')",
            name="geometry_type_supported",
        ),
        Index(
            "ix_parcel_versions_geometry",
            "geometry",
            postgresql_using="gist",
        ),
    )

    parcel_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey(f"{FARM_MANAGEMENT_SCHEMA}.parcels.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    number: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    geometry_type: Mapped[str] = mapped_column(String(12), nullable=False)
    geometry: Mapped[object] = mapped_column(
        Geometry(
            geometry_type="MULTIPOLYGON",
            srid=4326,
            dimension=2,
            spatial_index=False,
        ),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
