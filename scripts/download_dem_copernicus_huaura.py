import requests
import geopandas as gpd
import rasterio
from rasterio.mask import mask

boundary = "../data/huaura/boundary/huaura_province.geojson"
output = "../data/huaura/raw/dem.tif"

gdf = gpd.read_file(boundary)

print("Descargando DEM OpenTopography")

url = (
"https://portal.opentopography.org/API/globaldem?"
"demtype=SRTMGL1"
"&south=-11.5"
"&north=-10.5"
"&west=-77.8"
"&east=-76.5"
"&outputFormat=GTiff"
)

r = requests.get(url)

print("Status:", r.status_code)
print("Bytes:", len(r.content))

open("dem_full.tif","wb").write(r.content)


src = rasterio.open("dem_full.tif")

print("DEM original:")
print(src.crs)
print(src.bounds)


out_image, out_transform = mask(
    src,
    gdf.geometry,
    crop=True
)


profile = src.profile

profile.update(
    height=out_image.shape[1],
    width=out_image.shape[2],
    transform=out_transform
)


with rasterio.open(output,"w",**profile) as dst:
    dst.write(out_image)


print("Guardado:")
print(output)