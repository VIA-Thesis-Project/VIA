import os

import geopandas as gpd
import numpy as np
import rasterio

from rasterio.features import rasterize


ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

LAND_GEOJSON = os.path.join(
    ROOT,
    "data",
    "huaura",
    "raw",
    "landsea",
    "ne_10m_land.geojson",
)

REFERENCE = os.path.join(
    ROOT,
    "data",
    "huaura",
    "masks",
    "huaura_mask_0041667.tif",
)

OUTPUT = os.path.join(
    ROOT,
    "data",
    "huaura",
    "processed_0041667",
    "landsea.tif",
)


# ---------------------------------------------------------
# Grilla objetivo
# ---------------------------------------------------------

with rasterio.open(REFERENCE) as ref:

    profile = ref.profile.copy()

    transform = ref.transform

    width = ref.width
    height = ref.height

    bounds = ref.bounds
    crs = ref.crs


print("Referencia:")
print("  tamaño:", width, "x", height)
print("  CRS:", crs)
print("  bounds:", bounds)
print()


# ---------------------------------------------------------
# Leer polígonos de tierra
# ---------------------------------------------------------

land = gpd.read_file(
    LAND_GEOJSON,
    bbox=(
        bounds.left,
        bounds.bottom,
        bounds.right,
        bounds.top,
    ),
)

if land.crs is None:

    land = land.set_crs(
        "EPSG:4326"
    )

land = land.to_crs(crs)

print(
    "Geometrías de tierra encontradas:",
    len(land)
)


# ---------------------------------------------------------
# Rasterización
# ---------------------------------------------------------

shapes = (
    (geom, 1)
    for geom in land.geometry
    if geom is not None
    and not geom.is_empty
)

landsea = rasterize(
    shapes=shapes,
    out_shape=(
        height,
        width
    ),
    transform=transform,
    fill=0,
    default_value=1,
    dtype="uint8",
    all_touched=False,
)


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

os.makedirs(
    os.path.dirname(OUTPUT),
    exist_ok=True
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


print()
print("Land/Sea mask creado:")
print(OUTPUT)

print()
print(
    "Tierra:",
    int(
        np.count_nonzero(
            landsea == 1
        )
    )
)

print(
    "Mar:",
    int(
        np.count_nonzero(
            landsea == 0
        )
    )
)

print(
    "Valores únicos:",
    np.unique(landsea)
)