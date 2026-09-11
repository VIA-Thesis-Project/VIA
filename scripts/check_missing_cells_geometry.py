import geopandas as gpd
import numpy as np
import rasterio
from pathlib import Path

from shapely.geometry import Point


MASK = "../data/huaura/masks/huaura_mask_005.tif"

BOUNDARY = (
    "../data/huaura/boundary/"
    "huaura_province.geojson"
)

FILES = {
    "clay": (
        "../data/huaura/processed/soil/"
        "clay_content/clay_0-5cm_mean.tif"
    ),
    "wise": (
        "../data/huaura/processed/soil/"
        "base_saturation/bsat_0-20cm.tif"
    ),
    "depth": (
        "../data/huaura/processed/soil/"
        "soildepth/depth_0-NA.tif"
    ),
    "salinity": (
        "../data/huaura/processed/soil/"
        "salinity/sal_0-NA.tif"
    ),
    "dem": (
        "../data/huaura/processed/dem.tif"
    ),
}


# These comparisons intentionally refer to the former grid, now archived.
_archived_processed = Path(__file__).resolve().parents[2] / 'poc_via_cslite_archive/cleanup_20260910_012022/archived/data/huaura/processed'
FILES = {key: str(_archived_processed / Path(value).relative_to('../data/huaura/processed'))
         for key, value in FILES.items()}

# ---------------------------------------------------------
# Máscara
# ---------------------------------------------------------

with rasterio.open(MASK) as src:

    mask = src.read(1)
    transform = src.transform

inside_mask = mask == 2


# ---------------------------------------------------------
# Provincia
# ---------------------------------------------------------

gdf = gpd.read_file(BOUNDARY)

if gdf.crs is None:
    gdf = gdf.set_crs("EPSG:4326")

gdf = gdf.to_crs("EPSG:4326")

province = gdf.geometry.union_all()


# Para distancias en metros
gdf_utm = gdf.to_crs("EPSG:32718")
province_utm = gdf_utm.geometry.union_all()


# ---------------------------------------------------------
# Detectar faltantes
# ---------------------------------------------------------

missing_by_file = {}
all_missing = set()


for name, path in FILES.items():

    with rasterio.open(path) as src:

        x = src.read(1)

    missing = (
        inside_mask
        & ~np.isfinite(x)
    )

    cells = set(
        map(
            tuple,
            np.argwhere(missing)
        )
    )

    missing_by_file[name] = cells
    all_missing |= cells


print(
    "Celdas máscara:",
    int(inside_mask.sum())
)

print(
    "Celdas distintas con algún faltante:",
    len(all_missing)
)

print()


# ---------------------------------------------------------
# Geometría de cada celda
# ---------------------------------------------------------

for row, col in sorted(all_missing):

    lon, lat = rasterio.transform.xy(
        transform,
        row,
        col,
        offset="center"
    )

    point = Point(lon, lat)

    center_inside = province.covers(point)

    point_gdf = gpd.GeoSeries(
        [point],
        crs="EPSG:4326"
    ).to_crs("EPSG:32718")

    point_utm = point_gdf.iloc[0]

    distance_boundary = (
        point_utm.distance(
            province_utm.boundary
        )
    )

    missing_sources = [
        name
        for name, cells
        in missing_by_file.items()
        if (row, col) in cells
    ]

    print(
        f"cell=({row},{col}) "
        f"lon={lon:.6f} "
        f"lat={lat:.6f}"
    )

    print(
        "  centro dentro de Huaura:",
        center_inside
    )

    print(
        "  distancia al límite:",
        f"{distance_boundary:.0f} m"
    )

    print(
        "  faltante en:",
        ", ".join(missing_sources)
    )

    print()
