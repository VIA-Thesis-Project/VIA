import os

import numpy as np
import rasterio

from rasterio.windows import from_bounds
from rasterio.warp import reproject, Resampling


BDT = (
    "../data/huaura/raw/soildepth/"
    "bdticm_huaura_cm.tif"
)

PELLETIER = (
    "../data/huaura/raw/pelletier/"
    "upland_hill-slope_soil_thickness.tif"
)

OUTPUT = (
    "../data/huaura/raw/soildepth_final/"
    "soildepth_0-200cm.tif"
)


MAX_DEPTH_CM = 5000.0


os.makedirs(
    os.path.dirname(OUTPUT),
    exist_ok=True
)


print("Leyendo BDTICM local...")

with rasterio.open(BDT) as src:

    bdt = src.read(1).astype(np.float32)

    bdt_transform = src.transform
    bdt_crs = src.crs
    bdt_bounds = src.bounds

    profile = src.profile.copy()


valid_bdt = np.isfinite(bdt)


print(
    "BDTICM válidos:",
    int(valid_bdt.sum())
)


# =========================================================
# PELLETIER
# =========================================================

print("Leyendo Pelletier...")

with rasterio.open(PELLETIER) as src:

    window = from_bounds(
        bdt_bounds.left,
        bdt_bounds.bottom,
        bdt_bounds.right,
        bdt_bounds.top,
        src.transform,
    )

    window = (
        window
        .round_offsets()
        .round_lengths()
    )

    pel = src.read(
        1,
        window=window
    ).astype(np.float32)

    pel_transform = src.window_transform(
        window
    )

    pel_crs = src.crs
    pel_nodata = src.nodata


if pel_nodata is not None:
    pel[pel == pel_nodata] = np.nan


# =========================================================
# ALINEAR PELLETIER A BDT
# =========================================================

print("Alineando Pelletier...")

pel_on_bdt = np.full(
    bdt.shape,
    np.nan,
    dtype=np.float32
)


reproject(
    source=pel,
    destination=pel_on_bdt,

    src_transform=pel_transform,
    src_crs=pel_crs,
    src_nodata=np.nan,

    dst_transform=bdt_transform,
    dst_crs=bdt_crs,
    dst_nodata=np.nan,

    resampling=Resampling.nearest
)


# Pelletier está expresado en metros.
valid_pel = (
    valid_bdt
    & np.isfinite(pel_on_bdt)
    & (pel_on_bdt > 0)
    & (pel_on_bdt <= 2.0)
)


# =========================================================
# COMBINACIÓN
# =========================================================

print("Combinando fuentes...")

depth_cm = np.full(
    bdt.shape,
    np.nan,
    dtype=np.float32
)


# Base: BDTICM
depth_cm[valid_bdt] = np.minimum(
    bdt[valid_bdt],
    MAX_DEPTH_CM
)


# Pelletier tiene prioridad para suelo somero
depth_cm[valid_pel] = (
    pel_on_bdt[valid_pel] * 100.0
)


valid_final = np.isfinite(depth_cm)


# =========================================================
# ESTADÍSTICAS DE PROCEDENCIA
# =========================================================

used_pel = valid_final & valid_pel

used_bdt = (
    valid_final
    & ~valid_pel
    & valid_bdt
)


print()
print("==============================")
print("PROCEDENCIA")
print("==============================")

print(
    "Pelletier:",
    int(used_pel.sum())
)

print(
    "BDTICM fallback:",
    int(used_bdt.sum())
)

print(
    "Total:",
    int(valid_final.sum())
)


# =========================================================
# GUARDAR
# =========================================================

profile.update(
    driver="GTiff",
    count=1,
    dtype="float32",
    nodata=np.nan,
    compress="deflate"
)


print()
print("Guardando...")

with rasterio.open(
    OUTPUT,
    "w",
    **profile
) as dst:

    dst.write(
        depth_cm,
        1
    )


# =========================================================
# VALIDACIÓN
# =========================================================

print()
print("==============================")
print("SOILDEPTH HUAURA")
print("==============================")

print("Archivo:", OUTPUT)
print("Shape:", depth_cm.shape)

print(
    "Pixels válidos:",
    int(valid_final.sum())
)

print(
    "Min cm:",
    float(np.nanmin(depth_cm))
)

print(
    "Max cm:",
    float(np.nanmax(depth_cm))
)

print(
    "Percentiles cm:",
    np.percentile(
        depth_cm[valid_final],
        [
            0,
            25,
            50,
            75,
            90,
            95,
            99,
            100
        ]
    )
)

print()
print(
    "Percentiles metros "
    "(como los verá CropSuite):",
    np.percentile(
        depth_cm[valid_final] / 100.0,
        [
            0,
            25,
            50,
            75,
            90,
            95,
            99,
            100
        ]
    )
)

print()
print("Terminado.")