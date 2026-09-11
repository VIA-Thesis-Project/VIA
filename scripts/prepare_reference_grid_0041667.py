import os

import geopandas as gpd
import numpy as np
import rasterio

from rasterio.features import rasterize
from rasterio.transform import from_origin


ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

BOUNDARY = os.path.join(
    ROOT,
    "data",
    "huaura",
    "boundary",
    "huaura_province.geojson",
)

OUTPUT = os.path.join(
    ROOT,
    "data",
    "huaura",
    "masks",
    "huaura_mask_0041667.tif",
)


# --------------------------------------------------
# Grilla nativa CropSuite resolution=4
# 2.5 arc-min = 1/24 grado
# --------------------------------------------------

RES = 1.0 / 24.0

XMIN = -77.7035
YMAX = -10.6069

COLS = 28
ROWS = 21

XMAX = XMIN + COLS * RES
YMIN = YMAX - ROWS * RES


transform = from_origin(
    XMIN,
    YMAX,
    RES,
    RES
)


# --------------------------------------------------
# Provincia de Huaura
# --------------------------------------------------

gdf = gpd.read_file(BOUNDARY)

if gdf.crs is None:
    gdf = gdf.set_crs("EPSG:4326")

gdf = gdf.to_crs("EPSG:4326")


# --------------------------------------------------
# Rasterización
#
# CropSuite preprocessor:
# 2 = interior de Huaura
# 0 = exterior
# --------------------------------------------------

shapes = (
    (geom, 2)
    for geom in gdf.geometry
    if geom is not None
    and not geom.is_empty
)

mask = rasterize(
    shapes=shapes,
    out_shape=(ROWS, COLS),
    transform=transform,
    fill=0,
    default_value=2,
    dtype="uint8",
    all_touched=False,
)


# --------------------------------------------------
# Guardar
# --------------------------------------------------

profile = {
    "driver": "GTiff",
    "height": ROWS,
    "width": COLS,
    "count": 1,
    "dtype": "uint8",
    "crs": "EPSG:4326",
    "transform": transform,
    "nodata": None,
    "compress": "LZW",
}

os.makedirs(
    os.path.dirname(OUTPUT),
    exist_ok=True
)

with rasterio.open(
    OUTPUT,
    "w",
    **profile
) as dst:
    dst.write(mask, 1)


print("MASK CREADA")
print("------------")
print("Archivo:", OUTPUT)
print("Resolucion:", RES)
print("Filas:", ROWS)
print("Columnas:", COLS)

print(
    "Bounds:",
    XMIN,
    YMIN,
    XMAX,
    YMAX
)

print(
    "Huaura cells:",
    int(np.sum(mask == 2))
)

print(
    "Outside cells:",
    int(np.sum(mask == 0))
)

print(
    "Unique:",
    np.unique(mask)
)