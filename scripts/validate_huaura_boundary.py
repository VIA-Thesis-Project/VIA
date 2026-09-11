import geopandas as gpd
from pathlib import Path


file = Path(
    "data/huaura/boundary/huaura_province.geojson"
)


print("Cargando Huaura...")

gdf = gpd.read_file(file)


print("\nInformación:")
print(gdf)


print("\nCRS:")
print(gdf.crs)


print("\nGeometría válida:")
print(gdf.is_valid)


print("\nTipo geometría:")
print(gdf.geom_type)


print("\nÁrea aproximada:")
print(
    gdf.to_crs("EPSG:32718").area / 1_000_000
)