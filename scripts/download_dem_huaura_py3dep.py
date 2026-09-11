import geopandas as gpd
import py3dep
import rioxarray
from pathlib import Path

print("Leyendo límite Huaura")

boundary = gpd.read_file(
    "../data/huaura/boundary/huaura_province.geojson"
)

boundary = boundary.to_crs("EPSG:4326")

bounds = boundary.total_bounds
print("Bounds:")
print(bounds)

output = Path("../data/huaura/raw/dem.tif")


print("Descargando DEM...")

dem = py3dep.get_dem(
    bounds,
    resolution=30
)

dem = dem.rio.write_crs("EPSG:5070")

dem = dem.rio.reproject("EPSG:4326")

print("DEM descargado")

# Guardar GeoTIFF

dem.rio.to_raster(output)

print("Guardado:")
print(output)