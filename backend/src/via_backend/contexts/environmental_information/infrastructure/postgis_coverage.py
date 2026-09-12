"""PostGIS implementation of extent-based coverage measurement."""

from __future__ import annotations

import json

from sqlalchemy import func, select, text
from sqlalchemy.exc import DBAPIError

from via_backend.infrastructure.database import SessionFactory

from ..application.ports import (
    CoverageComputation,
    InvalidSpatialInputError,
    SpatialCoverageUnavailableError,
)
from ..domain.coverage import (
    CoverageCompatibilityFailure,
    CoverageGeometry,
    CoverageMeasurement,
)
from ..domain.models import DatasetVersion
from ..domain.spatial import validate_crs
from .orm import DatasetVersionRecord

_AREA_METHOD = (
    "PostGIS ST_Area on WGS84 geography after EPSG:4326 transformation"
)


class PostGISCoverageCalculator:
    """Compare a supplied parcel geometry with a stored native-CRS extent."""

    def __init__(self, sessions: SessionFactory) -> None:
        self._sessions = sessions

    def measure(
        self, version: DatasetVersion, geometry: CoverageGeometry
    ) -> CoverageComputation:
        dataset_srid = validate_crs(version.crs)
        parcel_srid = validate_crs(geometry.crs)
        parcel_geojson = json.dumps(geometry.to_geojson(), separators=(",", ":"))

        with self._sessions() as session:
            extent_state = session.execute(
                select(
                    func.ST_SRID(DatasetVersionRecord.extent),
                    func.ST_IsValid(DatasetVersionRecord.extent),
                    func.ST_IsEmpty(DatasetVersionRecord.extent),
                ).where(DatasetVersionRecord.id == version.id)
            ).one_or_none()
            if extent_state is None:
                raise SpatialCoverageUnavailableError(
                    f"Dataset version {version.id} disappeared during coverage check."
                )
            stored_srid, extent_valid, extent_empty = extent_state
            if stored_srid != dataset_srid:
                return CoverageCompatibilityFailure(
                    reasons=(
                        "The recorded dataset CRS does not match the stored extent SRID.",
                    )
                )
            if not extent_valid or extent_empty:
                return CoverageCompatibilityFailure(
                    reasons=("The registered dataset extent is not a valid polygon.",)
                )
            if not _srid_is_transformable(session, dataset_srid):
                return CoverageCompatibilityFailure(
                    reasons=(
                        f"Dataset CRS {version.crs} is not transformable by PostGIS.",
                    )
                )
            if not _srid_is_transformable(session, parcel_srid):
                raise InvalidSpatialInputError(
                    f"Parcel CRS {geometry.crs} is not transformable by PostGIS."
                )

            try:
                parcel_valid, parcel_empty, geometry_type, validity_reason = (
                    session.execute(
                        text(
                            """
                            WITH parcel AS (
                                SELECT ST_SetSRID(
                                    ST_GeomFromGeoJSON(:parcel_geojson),
                                    :parcel_srid
                                ) AS geometry
                            )
                            SELECT
                                ST_IsValid(geometry),
                                ST_IsEmpty(geometry),
                                GeometryType(geometry),
                                ST_IsValidReason(geometry)
                            FROM parcel
                            """
                        ),
                        {
                            "parcel_geojson": parcel_geojson,
                            "parcel_srid": parcel_srid,
                        },
                    ).one()
                )
            except DBAPIError as error:
                raise InvalidSpatialInputError(
                    "Parcel geometry could not be constructed by PostGIS."
                ) from error
            if geometry_type not in {"POLYGON", "MULTIPOLYGON"}:
                raise InvalidSpatialInputError(
                    "Parcel geometry must be a Polygon or MultiPolygon."
                )
            if parcel_empty:
                raise InvalidSpatialInputError("Parcel geometry must not be empty.")
            if not parcel_valid:
                raise InvalidSpatialInputError(
                    f"Parcel geometry is topologically invalid: {validity_reason}."
                )

            try:
                parcel_area = float(
                    session.scalar(
                        text(
                            """
                            SELECT ST_Area(
                                ST_Transform(
                                    ST_SetSRID(
                                        ST_GeomFromGeoJSON(:parcel_geojson),
                                        :parcel_srid
                                    ),
                                    4326
                                )::geography
                            )
                            """
                        ),
                        {
                            "parcel_geojson": parcel_geojson,
                            "parcel_srid": parcel_srid,
                        },
                    )
                )
            except (DBAPIError, TypeError, ValueError) as error:
                raise InvalidSpatialInputError(
                    "Parcel geometry cannot be transformed to EPSG:4326 for area measurement."
                ) from error
            if parcel_area <= 0:
                raise InvalidSpatialInputError(
                    "Parcel geometry must have a positive geodesic area."
                )

            try:
                fully_covered, covered_area = session.execute(
                    text(
                        """
                        WITH parcel AS (
                            SELECT ST_SetSRID(
                                ST_GeomFromGeoJSON(:parcel_geojson),
                                :parcel_srid
                            ) AS geometry
                        ),
                        prepared AS (
                            SELECT
                                dataset.extent,
                                ST_Transform(
                                    parcel.geometry,
                                    ST_SRID(dataset.extent)
                                ) AS parcel_geometry
                            FROM environmental_information.dataset_versions AS dataset
                            CROSS JOIN parcel
                            WHERE dataset.id = :version_id
                        )
                        SELECT
                            ST_Covers(extent, parcel_geometry),
                            ST_Area(
                                ST_Transform(
                                    ST_Intersection(extent, parcel_geometry),
                                    4326
                                )::geography
                            )
                        FROM prepared
                        """
                    ),
                    {
                        "parcel_geojson": parcel_geojson,
                        "parcel_srid": parcel_srid,
                        "version_id": version.id,
                    },
                ).one()
            except DBAPIError:
                return CoverageCompatibilityFailure(
                    reasons=(
                        f"Dataset CRS {version.crs} could not be used for the spatial comparison.",
                    )
                )

        transformations: list[str] = []
        if geometry.crs != version.crs:
            transformations.append(
                f"parcel geometry: {geometry.crs} -> {version.crs}"
            )
        if geometry.crs != "EPSG:4326":
            transformations.append(
                f"parcel area: {geometry.crs} -> EPSG:4326 geography"
            )
        if version.crs != "EPSG:4326":
            transformations.append(
                f"intersection area: {version.crs} -> EPSG:4326 geography"
            )
        return CoverageMeasurement(
            parcel_area_m2=parcel_area,
            covered_area_m2=min(parcel_area, max(0.0, float(covered_area or 0.0))),
            fully_covered=bool(fully_covered),
            comparison_crs=version.crs,
            area_method=_AREA_METHOD,
            transformations=tuple(transformations),
        )


def _srid_is_transformable(session: object, srid: int) -> bool:
    value = session.scalar(  # type: ignore[attr-defined]
        text("SELECT EXISTS (SELECT 1 FROM spatial_ref_sys WHERE srid = :srid)"),
        {"srid": srid},
    )
    return bool(value)
