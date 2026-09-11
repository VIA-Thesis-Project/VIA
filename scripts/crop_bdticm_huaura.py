import os
import time

import geopandas as gpd
import numpy as np
import rasterio

from rasterio.errors import RasterioIOError
from rasterio.features import geometry_mask
from rasterio.windows import Window, from_bounds


SOURCE = (
    "https://files.isric.org/soilgrids/former/"
    "2017-03-10/data/BDTICM_M_250m_ll.tif"
)

BOUNDARY = (
    "../data/huaura/boundary/"
    "huaura_province.geojson"
)

OUTPUT = (
    "../data/huaura/raw/soildepth/"
    "bdticm_huaura_cm.tif"
)


CHUNK_ROWS = 8
MAX_RETRIES = 10


os.makedirs(
    os.path.dirname(OUTPUT),
    exist_ok=True
)


def read_remote_chunk(window):
    """
    Lee un bloque remoto.
    Si falla el strip HTTP, cierra y vuelve
    a abrir el TIFF antes del siguiente intento.
    """

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            with rasterio.Env(
                GDAL_HTTP_MAX_RETRY="3",
                GDAL_HTTP_RETRY_DELAY="1",
                GDAL_HTTP_TCP_KEEPALIVE="YES",
                GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
            ):

                with rasterio.open(SOURCE) as src:

                    arr = src.read(
                        1,
                        window=window,
                    )

            return arr

        except RasterioIOError as exc:

            print(
                f"  Falló bloque "
                f"fila {int(window.row_off)} "
                f"(intento {attempt}/{MAX_RETRIES})"
            )

            if attempt == MAX_RETRIES:
                raise exc

            time.sleep(
                min(2 * attempt, 10)
            )


print("Leyendo límite de Huaura...")

gdf = gpd.read_file(BOUNDARY)


# ---------------------------------------------------------
# Obtener metadatos y ventana
# ---------------------------------------------------------

print("Abriendo metadatos BDTICM remoto...")

with rasterio.Env(
    GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR"
):

    with rasterio.open(SOURCE) as src:

        gdf = gdf.to_crs(src.crs)

        minx, miny, maxx, maxy = (
            gdf.total_bounds
        )

        window = from_bounds(
            minx,
            miny,
            maxx,
            maxy,
            src.transform,
        )

        window = (
            window
            .round_offsets()
            .round_lengths()
        )

        col_off = int(window.col_off)
        row_off = int(window.row_off)
        width = int(window.width)
        height = int(window.height)

        transform = src.window_transform(
            window
        )

        profile = src.profile.copy()

        nodata = src.nodata
        crs = src.crs


print(
    "Window:",
    Window(
        col_off,
        row_off,
        width,
        height,
    )
)

print(
    f"Leyendo {height} filas "
    f"en bloques de {CHUNK_ROWS}..."
)


# ---------------------------------------------------------
# Lectura resistente por bloques
# ---------------------------------------------------------

data = np.full(
    (height, width),
    np.nan,
    dtype=np.float32,
)


for local_row in range(
    0,
    height,
    CHUNK_ROWS,
):

    rows = min(
        CHUNK_ROWS,
        height - local_row,
    )

    current_window = Window(
        col_off=col_off,
        row_off=row_off + local_row,
        width=width,
        height=rows,
    )

    block = read_remote_chunk(
        current_window
    ).astype(np.float32)

    data[
        local_row:local_row + rows,
        :
    ] = block

    print(
        f"  {min(local_row + rows, height)}"
        f"/{height} filas"
    )


# ---------------------------------------------------------
# Nodata + máscara exacta de Huaura
# ---------------------------------------------------------

print("Aplicando máscara provincial...")

outside = geometry_mask(
    gdf.geometry,
    out_shape=data.shape,
    transform=transform,
    invert=False,
)

invalid = outside.copy()

if nodata is not None:
    invalid |= data == nodata

data[invalid] = np.nan


# ---------------------------------------------------------
# Guardar local
# ---------------------------------------------------------

profile.update(
    driver="GTiff",
    height=height,
    width=width,
    transform=transform,
    crs=crs,
    count=1,
    dtype="float32",
    nodata=np.nan,
    compress="deflate",
)


print("Guardando raster local...")

with rasterio.open(
    OUTPUT,
    "w",
    **profile,
) as dst:

    dst.write(
        data,
        1,
    )


# ---------------------------------------------------------
# Validación
# ---------------------------------------------------------

valid = np.isfinite(data)

print()
print("==============================")
print("BDTICM HUAURA TERMINADO")
print("==============================")

print("Archivo:", OUTPUT)
print("Shape:", data.shape)
print(
    "Pixels válidos:",
    int(valid.sum())
)

if valid.any():

    print(
        "Min cm:",
        float(np.nanmin(data))
    )

    print(
        "Max cm:",
        float(np.nanmax(data))
    )

    print(
        "Percentiles:",
        np.percentile(
            data[valid],
            [
                0,
                25,
                50,
                75,
                90,
                95,
                99,
                100,
            ],
        )
    )