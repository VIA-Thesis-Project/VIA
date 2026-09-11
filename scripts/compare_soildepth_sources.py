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


# =========================================================
# BDTICM LOCAL
# =========================================================

print("Leyendo BDTICM local...")

with rasterio.open(BDT) as src:

    bdt = src.read(1).astype(np.float32)

    bdt_transform = src.transform
    bdt_crs = src.crs
    bdt_bounds = src.bounds

    bdt_nodata = src.nodata


valid_bdt = np.isfinite(bdt)

if bdt_nodata is not None and np.isfinite(bdt_nodata):
    valid_bdt &= bdt != bdt_nodata


print("BDT shape:", bdt.shape)
print(
    "BDT válidos:",
    int(valid_bdt.sum())
)


# =========================================================
# PELLETIER: LEER SOLO VENTANA DE HUAURA
# =========================================================

print("Leyendo Pelletier local...")

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
        window=window,
    ).astype(np.float32)

    pel_transform = src.window_transform(
        window
    )

    pel_crs = src.crs
    pel_nodata = src.nodata


if pel_nodata is not None:
    pel[pel == pel_nodata] = np.nan


print("Pelletier window:", window)
print("Pelletier shape:", pel.shape)


# =========================================================
# REPROYECTAR PELLETIER A LA GRILLA BDT
# =========================================================

print(
    "Alineando Pelletier "
    "a la grilla BDTICM..."
)

pel_on_bdt = np.full(
    bdt.shape,
    np.nan,
    dtype=np.float32,
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

    resampling=Resampling.nearest,
)


valid_pel = np.isfinite(
    pel_on_bdt
)

both = (
    valid_bdt
    & valid_pel
)


# =========================================================
# ESTADÍSTICAS GENERALES
# =========================================================

print()
print("==============================")
print("COBERTURA")
print("==============================")

print(
    "BDTICM válidos:",
    int(valid_bdt.sum())
)

print(
    "Pelletier válidos:",
    int(valid_pel.sum())
)

print(
    "Ambos válidos:",
    int(both.sum())
)


# =========================================================
# CRUCE DEL UMBRAL DE 2 METROS
# =========================================================

case_1 = (
    both
    & (bdt <= 200)
    & (pel_on_bdt <= 2)
)

case_2 = (
    both
    & (bdt <= 200)
    & (pel_on_bdt > 2)
)

case_3 = (
    both
    & (bdt > 200)
    & (pel_on_bdt > 2)
)

case_4 = (
    both
    & (bdt > 200)
    & (pel_on_bdt <= 2)
)


print()
print("==============================")
print("CRUCE BDTICM / PELLETIER")
print("==============================")


def show_case(name, mask):

    count = int(mask.sum())

    pct = (
        100 * count / both.sum()
        if both.sum()
        else 0
    )

    print(
        f"{name}: "
        f"{count} "
        f"({pct:.2f}%)"
    )


show_case(
    "BDT <=200 cm | Pelletier <=2 m",
    case_1,
)

show_case(
    "BDT <=200 cm | Pelletier >2 m",
    case_2,
)

show_case(
    "BDT >200 cm | Pelletier >2 m",
    case_3,
)

show_case(
    "BDT >200 cm | Pelletier <=2 m",
    case_4,
)


# =========================================================
# PELLETIER DONDE BDT > 200 CM
# =========================================================

deep = (
    both
    & (bdt > 200)
)


if deep.any():

    values = pel_on_bdt[deep]

    print()
    print("==============================")
    print("PELLETIER DONDE BDT >200 CM")
    print("==============================")

    print(
        "Valores:",
        np.unique(values)
    )

    print(
        "Percentiles:",
        np.percentile(
            values,
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


print()
print("Comparación terminada.")