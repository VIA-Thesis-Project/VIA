import requests
import gzip
import shutil
import os
import rasterio
from rasterio.merge import merge
from rasterio.mask import mask
import geopandas as gpd

boundary = "../data/huaura/boundary/huaura_province.geojson"
output = "../data/huaura/raw/dem.tif"

tiles=[
    "S11W078",
    "S11W077",
    "S12W078",
    "S12W077"
]

files=[]

os.makedirs("srtm_tiles", exist_ok=True)

for tile in tiles:

    hgt = f"srtm_tiles/{tile}.hgt"

    if not os.path.exists(hgt):

        url = (
            f"https://s3.amazonaws.com/elevation-tiles-prod/skadi/"
            f"{tile[0:3]}/{tile}.hgt.gz"
        )

        print("Descargando:", url)

        r=requests.get(url)

        print("Status:",r.status_code)

        gz=f"srtm_tiles/{tile}.hgt.gz"

        open(gz,"wb").write(r.content)

        with gzip.open(gz,'rb') as f:
            with open(hgt,'wb') as out:
                shutil.copyfileobj(f,out)

    files.append(hgt)


print("Convirtiendo HGT")

from rasterio.transform import from_origin

srcs=[]

for tile in tiles:

    f=f"srtm_tiles/{tile}.hgt"

    lat=int(tile[1:3])
    lon=int(tile[4:8])

    transform = from_origin(
        lon,
        lat+1,
        1/3600,
        1/3600
    )

    src = rasterio.open(
        f,
        driver="SRTMHGT",
        transform=transform,
        crs="EPSG:4326"
    )

    srcs.append(src)


mosaic, transform = merge(srcs)

profile = srcs[0].profile.copy()

profile.update(
    driver="GTiff",
    crs="EPSG:4326"
)

profile.update(
    driver="GTiff",
    height=mosaic.shape[1],
    width=mosaic.shape[2],
    transform=transform,
    crs="EPSG:4326"
)


tmp="srtm_full.tif"

with rasterio.open(tmp,"w",**profile) as dst:
    dst.write(mosaic)


print("Recortando Huaura")

gdf=gpd.read_file(boundary)

src=rasterio.open(tmp)

out_image,out_transform=mask(
    src,
    gdf.geometry,
    crop=True
)


profile.update(
    height=out_image.shape[1],
    width=out_image.shape[2],
    transform=out_transform
)


with rasterio.open(output,"w",**profile) as dst:
    dst.write(out_image)


print("DEM generado:")
print(output)