import os

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask


BASE = "../data/huaura/raw/wise30sec/source/WISE30sec/Interchangeable_format"

WISE_RASTER = os.path.join(BASE, "wise_30sec_v1.tif")
WISE_LOOKUP = os.path.join(BASE, "wise_30sec_v1.tsv")
WISE_FULL = os.path.join(BASE, "HW30s_FULL.txt")

BOUNDARY = "../data/huaura/boundary/huaura_province.geojson"

OUTPUT_ROOT = "../data/huaura/raw/wise30sec_huaura"


PARAMETERS = {
    "BSAT": "base_saturation",
    "ESP": "sodicity",
    "GYPS": "gypsum",
}


print("Leyendo HW30s_FULL...")

full = pd.read_csv(WISE_FULL)

# CropSuite usa el topsoil para estas tres propiedades.
d1 = full[full["Layer"] == "D1"].copy()

print("Filas D1:", len(d1))


# ---------------------------------------------------------
# 1. Calcular propiedades por NEWSUID
#    usando la composición completa de la unidad de mapa.
# ---------------------------------------------------------

properties = {}

for source_param, output_param in PARAMETERS.items():

    tmp = d1[
        ["NEWSUID", "PROP", source_param]
    ].copy()

    tmp["PROP"] = pd.to_numeric(
        tmp["PROP"],
        errors="coerce"
    )

    tmp[source_param] = pd.to_numeric(
        tmp[source_param],
        errors="coerce"
    )

    # Los valores físicos de BSAT, ESP y GYPS
    # no pueden ser negativos.
    #
    # WISE utiliza valores negativos para códigos
    # especiales / unidades misceláneas / datos ausentes.
    valid = (
        tmp["PROP"].notna()
        & (tmp["PROP"] > 0)
        & tmp[source_param].notna()
        & (tmp[source_param] >= 0)
    )

    tmp = tmp[valid].copy()

    tmp["weighted"] = (
        tmp[source_param]
        * tmp["PROP"]
    )

    agg = tmp.groupby("NEWSUID").agg(
        weighted_sum=("weighted", "sum"),
        valid_prop=("PROP", "sum")
    )

    agg[output_param] = (
        agg["weighted_sum"]
        / agg["valid_prop"]
    )

    properties[output_param] = (
        agg[output_param].to_dict()
    )

    print(
        output_param,
        "NEWSUID válidos:",
        len(properties[output_param])
    )


# ---------------------------------------------------------
# 2. Leer tabla pixel_value -> NEWSUID
# ---------------------------------------------------------

print("\nLeyendo lookup raster -> NEWSUID...")

lookup = pd.read_csv(
    WISE_LOOKUP,
    sep="\t"
)

lookup.columns = [
    str(c).strip()
    for c in lookup.columns
]

print("Columnas lookup:", lookup.columns.tolist())


# El archivo oficial usa el nombre pixel_vaue
# (con ese typo).
pixel_column = None

for candidate in [
    "pixel_vaue",
    "pixel_value",
    "VALUE",
    "value"
]:
    if candidate in lookup.columns:
        pixel_column = candidate
        break


if pixel_column is None:
    raise RuntimeError(
        "No se encontró la columna de valor de píxel "
        f"en {lookup.columns.tolist()}"
    )


if "description" not in lookup.columns:
    raise RuntimeError(
        "No se encontró la columna description "
        "con el NEWSUID."
    )


lookup[pixel_column] = pd.to_numeric(
    lookup[pixel_column],
    errors="coerce"
)

lookup = lookup.dropna(
    subset=[pixel_column, "description"]
).copy()

lookup[pixel_column] = (
    lookup[pixel_column]
    .astype(np.int64)
)

pixel_to_newsuid = dict(
    zip(
        lookup[pixel_column],
        lookup["description"].astype(str)
    )
)

print(
    "Relaciones pixel -> NEWSUID:",
    len(pixel_to_newsuid)
)


# ---------------------------------------------------------
# 3. Recortar raster WISE a Huaura
# ---------------------------------------------------------

print("\nRecortando raster WISE a Huaura...")

gdf = gpd.read_file(BOUNDARY)

with rasterio.open(WISE_RASTER) as src:

    print("WISE CRS:", src.crs)
    print("WISE resolución:", src.res)

    if gdf.crs != src.crs:
        gdf = gdf.to_crs(src.crs)

    wise_crop, transform = mask(
        src,
        gdf.geometry,
        crop=True
    )

    profile = src.profile.copy()

    profile.update(
        driver="GTiff",
        height=wise_crop.shape[1],
        width=wise_crop.shape[2],
        transform=transform,
        count=1,
        dtype="float32",
        nodata=np.nan,
        compress="deflate"
    )


wise_ids = wise_crop[0]


print("Raster recortado:")
print("  size:", wise_ids.shape)
print(
    "  IDs distintos:",
    len(np.unique(wise_ids))
)


# ---------------------------------------------------------
# 4. Crear raster para cada parámetro
# ---------------------------------------------------------

for output_param in PARAMETERS.values():

    print("\nGenerando:", output_param)

    output = np.full(
        wise_ids.shape,
        np.nan,
        dtype=np.float32
    )

    param_values = properties[output_param]

    ids = np.unique(wise_ids)

    matched_ids = 0
    unmatched_ids = []

    for pixel_id_raw in ids:

        if not np.isfinite(pixel_id_raw):
            continue

        pixel_id = int(pixel_id_raw)

        # 0 = nodata en WISE
        if pixel_id == 0:
            continue

        newsuid = pixel_to_newsuid.get(pixel_id)

        if newsuid is None:
            unmatched_ids.append(pixel_id)
            continue

        value = param_values.get(newsuid)

        if value is None or not np.isfinite(value):
            continue

        output[wise_ids == pixel_id] = value

        matched_ids += 1


    out_dir = os.path.join(
        OUTPUT_ROOT,
        output_param
    )

    os.makedirs(
        out_dir,
        exist_ok=True
    )

    out_path = os.path.join(
        out_dir,
        f"{output_param}_0-20cm.tif"
    )

    with rasterio.open(
        out_path,
        "w",
        **profile
    ) as dst:

        dst.write(
            output,
            1
        )


    finite = np.isfinite(output)

    print("  Archivo:", out_path)
    print("  IDs asociados:", matched_ids)
    print("  IDs sin lookup:", unmatched_ids)

    if np.any(finite):

        print(
            "  Min:",
            float(np.nanmin(output))
        )

        print(
            "  Max:",
            float(np.nanmax(output))
        )

        print(
            "  Pixels válidos:",
            int(finite.sum())
        )

    else:

        print(
            "  ADVERTENCIA: raster sin datos válidos"
        )


print("\nWISE30sec Huaura terminado.")