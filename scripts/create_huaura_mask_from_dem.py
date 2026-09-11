import geopandas as gpd
import rasterio
from rasterio.mask import mask
from rasterio.features import geometry_mask
from pathlib import Path
import numpy as np


boundary_file = "../data/huaura/boundary/huaura_province.geojson"
dem_file = "../data/huaura/raw/dem.tif"

output = "../data/huaura/boundary/huaura_boundary.tif"


print("Leyendo límite")
gdf = gpd.read_file(boundary_file)


with rasterio.open(dem_file) as src:

    print("DEM CRS:", src.crs)

    gdf = gdf.to_crs(src.crs)

    geom = [gdf.geometry.iloc[0]]

    mask_arr = geometry_mask(
        geom,
        out_shape=(src.height, src.width),
        transform=src.transform,
        invert=True
    )

    profile = src.profile

    profile.update(
        dtype="uint8",
        count=1,
        nodata=0
    )

    with rasterio.open(output, "w", **profile) as dst:
        dst.write(mask_arr.astype("uint8"), 1)


print("Máscara creada:")
print(output)