import numpy as np
import rasterio
from pathlib import Path


MASK = "../data/huaura/masks/huaura_mask_005.tif"

SOURCES = {
    "clay": (
        "../data/huaura/raw/soilgrids/"
        "clay/clay_0-5cm_mean.tif"
    ),
    "wise": (
        "../data/huaura/raw/wise30sec_huaura/"
        "base_saturation/base_saturation_0-20cm.tif"
    ),
    "depth": (
        "../data/huaura/raw/soildepth_final/"
        "soildepth_0-200cm.tif"
    ),
    "salinity": (
        "../data/huaura/raw/salinity/"
        "salinity_2016.tif"
    ),
    "dem": (
        "../data/huaura/raw/dem.tif"
    ),
}

PROCESSED = {
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


# Preserve this historical comparison against the archived former grid.
_archived_processed = Path(__file__).resolve().parents[2] / 'poc_via_cslite_archive/cleanup_20260910_012022/archived/data/huaura/processed'
PROCESSED = {key: str(_archived_processed / Path(value).relative_to('../data/huaura/processed'))
             for key, value in PROCESSED.items()}

with rasterio.open(MASK) as src:
    mask = src.read(1)
    transform = src.transform
    inside = mask == 2


# ---------------------------------------------------------
# Detectar todas las celdas faltantes en processed
# ---------------------------------------------------------

missing_by_source = {}
all_missing = set()

for name, path in PROCESSED.items():

    with rasterio.open(path) as src:
        arr = src.read(1)

    miss = inside & ~np.isfinite(arr)

    cells = set(
        map(
            tuple,
            np.argwhere(miss)
        )
    )

    missing_by_source[name] = cells
    all_missing |= cells


# ---------------------------------------------------------
# Muestrear los RAW en el centro de esas celdas
# ---------------------------------------------------------

print(
    "Celdas distintas a revisar:",
    len(all_missing)
)

print()


for row, col in sorted(all_missing):

    lon, lat = rasterio.transform.xy(
        transform,
        row,
        col,
        offset="center"
    )

    print(
        f"cell=({row},{col}) "
        f"lon={lon:.6f} "
        f"lat={lat:.6f}"
    )

    affected = [
        name
        for name, cells
        in missing_by_source.items()
        if (row, col) in cells
    ]

    print(
        "  faltante processed:",
        ", ".join(affected)
    )

    for name in affected:

        path = SOURCES[name]

        with rasterio.open(path) as src:

            value = list(
                src.sample(
                    [(lon, lat)],
                    indexes=1,
                    masked=True,
                )
            )[0][0]

            bounds = src.bounds

            in_bounds = (
                bounds.left <= lon <= bounds.right
                and bounds.bottom <= lat <= bounds.top
            )

            if np.ma.is_masked(value):
                txt = "NODATA"
            else:
                try:
                    txt = float(value)

                    if not np.isfinite(txt):
                        txt = "NaN"

                except Exception:
                    txt = str(value)

        print(
            f"  RAW {name}:",
            txt,
            "| dentro bounds:",
            in_bounds,
        )

    print()
