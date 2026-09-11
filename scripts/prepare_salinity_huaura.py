import os

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask


SOURCE = (
    "https://files.isric.org/public/"
    "global_soil_salinity/salmap2016.vrt"
)

BOUNDARY = (
    "../data/huaura/boundary/"
    "huaura_province.geojson"
)

OUTPUT = (
    "../data/huaura/raw/salinity/"
    "salinity_2016.tif"
)


# Conversión metodológica explícita:
# clase ISRIC -> límite inferior ECe [dS/m]
CLASS_TO_ECE = {
    0: 0.0,
    1: 2.0,
    2: 4.0,
    3: 8.0,
    4: 16.0,
}


os.makedirs(
    os.path.dirname(OUTPUT),
    exist_ok=True
)


print("Leyendo límite de Huaura...")

gdf = gpd.read_file(BOUNDARY)


print("Abriendo ISRIC Global Soil Salinity Map 2016...")

with rasterio.open(SOURCE) as src:

    print("CRS:", src.crs)
    print("Resolución:", src.res)

    if gdf.crs != src.crs:
        gdf = gdf.to_crs(src.crs)

    # filled=False conserva máscara fuera de Huaura.
    cropped, transform = mask(
        src,
        gdf.geometry,
        crop=True,
        filled=False
    )

    classes = cropped[0]

    data = classes.data
    geom_mask = np.ma.getmaskarray(classes)

    print(
        "Clases dentro de Huaura:",
        np.unique(data[~geom_mask])
    )

    ece = np.full(
        data.shape,
        np.nan,
        dtype=np.float32
    )

    for sal_class, ece_value in CLASS_TO_ECE.items():

        valid = (
            (~geom_mask)
            & (data == sal_class)
        )

        ece[valid] = ece_value


    profile = src.profile.copy()

    profile.update(
        driver="GTiff",
        height=ece.shape[0],
        width=ece.shape[1],
        transform=transform,
        count=1,
        dtype="float32",
        nodata=np.nan,
        compress="deflate"
    )


with rasterio.open(
    OUTPUT,
    "w",
    **profile
) as dst:

    dst.write(ece, 1)


valid = np.isfinite(ece)

print()
print("Salinidad generada:")
print(OUTPUT)

print("Shape:", ece.shape)
print("Pixels válidos:", int(valid.sum()))

if valid.any():

    print(
        "Valores ECe:",
        np.unique(ece[valid])
    )

    print(
        "Min:",
        float(np.nanmin(ece))
    )

    print(
        "Max:",
        float(np.nanmax(ece))
    )

print()
print("Terminado.")