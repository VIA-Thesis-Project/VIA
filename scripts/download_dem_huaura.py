import elevation
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from pathlib import Path


BASE = Path("../data/huaura")

boundary = BASE / "boundary" / "huaura_province.geojson"
output_raw = BASE / "raw" / "dem.tif"
output_crop = BASE / "terrain" / "huaura_dem.tif"


print("Leyendo límite Huaura")

gdf = gpd.read_file(boundary)

bounds = gdf.total_bounds
west, south, east, north = bounds

print("Bounds:")
print(bounds)


temp_dem = BASE / "raw" / "srtm_temp.tif"


print("Descargando SRTM DEM...")

elevation.clip(
    bounds=(west, south, east, north),
    output=str(temp_dem),
    product="SRTM1"
)


print("Recortando DEM al límite exacto")

with rasterio.open(temp_dem) as src:
    out_image, out_transform = mask(
        src,
        gdf.geometry,
        crop=True
    )

    out_meta = src.meta.copy()

    out_meta.update({
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })


output_raw.parent.mkdir(parents=True, exist_ok=True)

with rasterio.open(output_raw, "w", **out_meta) as dst:
    dst.write(out_image)


print("DEM generado:")
print(output_raw)

temp_dem.unlink()
