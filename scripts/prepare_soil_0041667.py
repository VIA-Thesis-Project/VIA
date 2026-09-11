import os
import glob

import numpy as np
import rasterio

from rasterio.warp import reproject, Resampling


ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

INPUT = os.path.join(
    ROOT,
    "data",
    "huaura",
    "raw",
    "soil_final",
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
    "soil",
)


with rasterio.open(REFERENCE) as ref:

    mask = ref.read(1)

    dst_transform = ref.transform
    dst_crs = ref.crs

    width = ref.width
    height = ref.height

    base_profile = ref.profile.copy()


os.makedirs(
    OUTPUT,
    exist_ok=True
)


files = glob.glob(
    os.path.join(
        INPUT,
        "**",
        "*.tif"
    ),
    recursive=True
)


print(
    "TIFF encontrados:",
    len(files)
)

print()


bad = []


for src_path in sorted(files):

    relative = os.path.relpath(
        src_path,
        INPUT
    )

    dst_path = os.path.join(
        OUTPUT,
        relative
    )

    os.makedirs(
        os.path.dirname(dst_path),
        exist_ok=True
    )


    dst = np.full(
        (height, width),
        np.nan,
        dtype="float32",
    )


    with rasterio.open(src_path) as src:

        reproject(
            source=rasterio.band(
                src,
                1
            ),

            destination=dst,

            src_transform=src.transform,
            src_crs=src.crs,
            src_nodata=src.nodata,

            dst_transform=dst_transform,
            dst_crs=dst_crs,
            dst_nodata=np.nan,

            resampling=Resampling.nearest,
        )


    # Solo provincia de Huaura
    dst[mask != 2] = np.nan


    profile = base_profile.copy()

    profile.update(
        driver="GTiff",
        dtype="float32",
        count=1,
        nodata=np.nan,
        compress="LZW",
    )


    with rasterio.open(
        dst_path,
        "w",
        **profile
    ) as out:

        out.write(
            dst,
            1
        )


    inside = mask == 2

    valid = (
        inside
        & np.isfinite(dst)
    )

    missing = (
        inside
        & ~np.isfinite(dst)
    )


    nvalid = int(
        valid.sum()
    )

    nmissing = int(
        missing.sum()
    )


    print(
        relative,
        "| valid",
        nvalid,
        "| missing",
        nmissing,
        "| min",
        (
            float(
                np.nanmin(
                    dst[valid]
                )
            )
            if nvalid
            else None
        ),
        "| max",
        (
            float(
                np.nanmax(
                    dst[valid]
                )
            )
            if nvalid
            else None
        ),
    )


    if nmissing > 0:

        bad.append(
            (
                relative,
                nmissing
            )
        )


print()

print(
    "TOTAL:",
    len(files)
)

print(
    "ARCHIVOS CON HUECOS:",
    len(bad)
)

for fn, n in bad:

    print(
        " ",
        fn,
        "->",
        n
    )