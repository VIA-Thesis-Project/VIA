import os

import numpy as np
import rasterio

from rasterio.warp import reproject, Resampling


ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

RAW_DEM = os.path.join(
    ROOT,
    "data",
    "huaura",
    "raw",
    "dem.tif",
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
    "dem.tif",
)


with rasterio.open(REFERENCE) as ref:

    mask = ref.read(1)

    profile = ref.profile.copy()

    dst_transform = ref.transform
    dst_crs = ref.crs

    height = ref.height
    width = ref.width


dst = np.full(
    (height, width),
    np.nan,
    dtype="float32",
)


with rasterio.open(RAW_DEM) as src:

    reproject(
        source=rasterio.band(src, 1),
        destination=dst,

        src_transform=src.transform,
        src_crs=src.crs,
        src_nodata=src.nodata,

        dst_transform=dst_transform,
        dst_crs=dst_crs,
        dst_nodata=np.nan,

        resampling=Resampling.bilinear,
    )


# Mantener únicamente Huaura
dst[mask != 2] = np.nan


profile.update(
    driver="GTiff",
    dtype="float32",
    count=1,
    nodata=np.nan,
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
) as out:

    out.write(
        dst,
        1
    )


valid = (
    (mask == 2)
    & np.isfinite(dst)
)


missing = (
    (mask == 2)
    & ~np.isfinite(dst)
)


print("DEM 0041667 CREADO")
print("------------------")

print(
    "Archivo:",
    OUTPUT
)

print(
    "Shape:",
    dst.shape
)

print(
    "Huaura cells:",
    int(
        (mask == 2).sum()
    )
)

print(
    "Valid inside:",
    int(valid.sum())
)

print(
    "Missing inside:",
    int(missing.sum())
)

if valid.any():

    print(
        "Min:",
        float(
            np.nanmin(dst[valid])
        )
    )

    print(
        "Max:",
        float(
            np.nanmax(dst[valid])
        )
    )