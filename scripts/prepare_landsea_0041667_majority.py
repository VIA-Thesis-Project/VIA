import os

import geopandas as gpd
import numpy as np
import rasterio

from shapely.geometry import box


ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

REFERENCE = os.path.join(
    ROOT,
    "data",
    "huaura",
    "masks",
    "huaura_mask_0041667.tif",
)

LAND = os.path.join(
    ROOT,
    "data",
    "huaura",
    "raw",
    "landsea",
    "ne_10m_land.geojson",
)

OUTPUT = os.path.join(
    ROOT,
    "data",
    "huaura",
    "processed_0041667",
    "landsea.tif",
)


# ---------------------------------------------------------
# Referencia
# ---------------------------------------------------------

with rasterio.open(REFERENCE) as ref:

    profile = ref.profile.copy()

    transform = ref.transform

    height = ref.height
    width = ref.width

    bounds = ref.bounds
    crs = ref.crs


# ---------------------------------------------------------
# Natural Earth Land
# ---------------------------------------------------------

land = gpd.read_file(
    LAND,
    bbox=(
        bounds.left,
        bounds.bottom,
        bounds.right,
        bounds.top,
    ),
)

if land.crs is None:
    land = land.set_crs("EPSG:4326")

land = land.to_crs(crs)

land_geom = land.geometry.union_all()


# ---------------------------------------------------------
# Calcular fracción terrestre por celda
# ---------------------------------------------------------

landsea = np.zeros(
    (height, width),
    dtype="uint8"
)


for row in range(height):

    for col in range(width):

        left, top = rasterio.transform.xy(
            transform,
            row,
            col,
            offset="ul"
        )

        right, bottom = rasterio.transform.xy(
            transform,
            row,
            col,
            offset="lr"
        )

        cell = box(
            left,
            bottom,
            right,
            top
        )

        intersection = cell.intersection(
            land_geom
        )


        # Área métrica UTM 18S
        areas = gpd.GeoSeries(
            [
                cell,
                intersection,
            ],
            crs=crs
        ).to_crs(
            "EPSG:32718"
        )

        cell_area = areas.iloc[0].area
        land_area = areas.iloc[1].area

        fraction = (
            land_area / cell_area
            if cell_area > 0
            else 0
        )


        # Mayoría de superficie
        if fraction >= 0.50:
            landsea[row, col] = 1


# ---------------------------------------------------------
# Guardar
# ---------------------------------------------------------

profile.update(
    driver="GTiff",
    dtype="uint8",
    count=1,
    nodata=None,
    compress="LZW",
)

with rasterio.open(
    OUTPUT,
    "w",
    **profile
) as dst:

    dst.write(
        landsea,
        1
    )


print("LAND/SEA MAJORITY CREADO")
print("------------------------")

print(
    "Tierra:",
    int(
        (landsea == 1).sum()
    )
)

print(
    "Mar:",
    int(
        (landsea == 0).sum()
    )
)

print(
    "Unique:",
    np.unique(landsea)
)
