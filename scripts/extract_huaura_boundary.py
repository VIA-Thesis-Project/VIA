import geopandas as gpd
from pathlib import Path

input_file = Path(
    "downloads/gadm/gadm41_PER_2.json"
)

output_file = Path(
    "data/huaura/boundary/huaura_province.geojson"
)


print("Leyendo límites administrativos...")

gdf = gpd.read_file(input_file)

print("Columnas disponibles:")
print(gdf.columns)


print("\nProvincias Lima:")
print(
    gdf[
        gdf["NAME_1"]=="Lima"
    ]["NAME_2"].unique()
)


huaura = gdf[
    (gdf["NAME_1"]=="Lima") &
    (gdf["NAME_2"].str.upper()=="HUAURA")
]


if huaura.empty:
    raise Exception(
        "No se encontró Huaura"
    )


# GeoJSON estándar
huaura = huaura.to_crs("EPSG:4326")


huaura.to_file(
    output_file,
    driver="GeoJSON"
)


print("\nArchivo creado:")
print(output_file)


print("\nBounding box:")
print(huaura.total_bounds)