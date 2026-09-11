import rasterio
from rasterio.merge import merge
from rasterio.mask import mask
from rasterio.session import AWSSession
import geopandas as gpd
import os

boundary = "../data/huaura/boundary/huaura_province.geojson"
output = "../data/huaura/raw/dem.tif"

gdf = gpd.read_file(boundary)

tiles = [
    "N10W078",
    "N10W077",
    "N11W078",
    "N11W077"
]

files = []

print("Descargando tiles SRTM")

for tile in tiles:

    url = (
        f"https://s3.amazonaws.com/elevation-tiles-prod/skadi/N{tile[1:3]}/"
        f"{tile}.hgt.gz"
    )

    print(url)

print("Usaremos GDAL virtual raster")
