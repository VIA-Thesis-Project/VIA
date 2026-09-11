import geopandas as gpd
import rasterio
from rasterio.transform import from_bounds
from rasterio.features import rasterize
import numpy as np


input_geojson = "../data/huaura/boundary/huaura_province.geojson"
output_tif = "../data/huaura/boundary/huaura_boundary.tif"


# Resolución aproximada CropSuiteLite
resolution = 0.05


gdf = gpd.read_file(input_geojson)

# asegurar WGS84
gdf = gdf.to_crs("EPSG:4326")


minx, miny, maxx, maxy = gdf.total_bounds


width = int((maxx-minx)/resolution)
height = int((maxy-miny)/resolution)


transform = from_bounds(
    minx,
    miny,
    maxx,
    maxy,
    width,
    height
)


mask = rasterize(
    [(geom, 2) for geom in gdf.geometry],
    out_shape=(height,width),
    transform=transform,
    fill=0,
    dtype="uint8"
)


with rasterio.open(
    output_tif,
    "w",
    driver="GTiff",
    height=height,
    width=width,
    count=1,
    dtype="uint8",
    crs="EPSG:4326",
    transform=transform,
) as dst:

    dst.write(mask,1)


print("Mask created:")
print(output_tif)
print("Size:", width, height)