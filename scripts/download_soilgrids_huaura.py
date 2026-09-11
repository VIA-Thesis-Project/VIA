import os
import rasterio
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
import geopandas as gpd
from pathlib import Path


# ============================
# CONFIGURACIÓN
# ============================

BASE = Path("../data/huaura")

BOUNDARY = BASE / "boundary/huaura_province.geojson"

OUTPUT = BASE / "raw/soilgrids"


SOIL_VARIABLES = {

    "clay": [
        "0-5cm",
        "5-15cm",
        "15-30cm",
        "30-60cm",
        "60-100cm",
        "100-200cm"
    ],

    "sand": [
        "0-5cm",
        "5-15cm",
        "15-30cm",
        "30-60cm",
        "60-100cm",
        "100-200cm"
    ],

    "cfvo": [
        "0-5cm",
        "5-15cm",
        "15-30cm",
        "30-60cm",
        "60-100cm",
        "100-200cm"
    ],

    "phh2o": [
        "0-5cm",
        "5-15cm",
        "15-30cm",
        "30-60cm",
        "60-100cm",
        "100-200cm"
    ],

    "soc": [
        "0-5cm",
        "5-15cm",
        "15-30cm",
        "30-60cm",
        "60-100cm",
        "100-200cm"
    ],

    "bdod": [
        "0-5cm",
        "5-15cm",
        "15-30cm",
        "30-60cm",
        "60-100cm",
        "100-200cm"
    ],

    "cec": [
        "0-5cm",
        "5-15cm",
        "15-30cm",
        "30-60cm",
        "60-100cm",
        "100-200cm"
    ]
}


URL_BASE = "https://files.isric.org/soilgrids/latest/data"


# ============================
# FUNCIONES
# ============================


def get_vrt(variable, depth):

    return (
        f"{URL_BASE}/{variable}/"
        f"{variable}_{depth}_mean.vrt"
    )



def crop_reproject(vrt, polygon, output):

    print("Procesando:")
    print(vrt)

    with rasterio.open(vrt) as src:

        # transformar polígono al CRS SoilGrids
        polygon_proj = polygon.to_crs(src.crs)

        geometries = [
            geom.__geo_interface__
            for geom in polygon_proj.geometry
        ]

        clipped, transform = mask(
            src,
            geometries,
            crop=True
        )


        profile = src.profile.copy()

        profile.update(
            {
                "driver": "GTiff",
                "height": clipped.shape[1],
                "width": clipped.shape[2],
                "transform": transform,
                "compress": "LZW"
            }
        )


        tmp = output.with_suffix(".tmp.tif")

        with rasterio.open(tmp, "w", **profile) as dst:
            dst.write(clipped)


    # reproyectar a EPSG4326

    with rasterio.open(tmp) as src:

        transform, width, height = calculate_default_transform(
            src.crs,
            "EPSG:4326",
            src.width,
            src.height,
            *src.bounds
        )


        profile = src.profile.copy()

        profile.update(
            {
                "crs": "EPSG:4326",
                "transform": transform,
                "width": width,
                "height": height
            }
        )


        with rasterio.open(output, "w", **profile) as dst:

            for i in range(1, src.count + 1):

                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs="EPSG:4326",
                    resampling=Resampling.bilinear
                )


    os.remove(tmp)

    print("Guardado:")
    print(output)



# ============================
# MAIN
# ============================


def main():

    print("Leyendo límite Huaura")

    gdf = gpd.read_file(BOUNDARY)


    for variable, depths in SOIL_VARIABLES.items():

        out_dir = OUTPUT / variable
        out_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        for depth in depths:

            output = (
                out_dir /
                f"{variable}_{depth}_mean.tif"
            )


            if output.exists():

                print(
                    "Existe:",
                    output
                )
                continue


            vrt = get_vrt(
                variable,
                depth
            )


            try:

                crop_reproject(
                    vrt,
                    gdf,
                    output
                )

            except Exception as e:

                print(
                    "ERROR:",
                    variable,
                    depth,
                    e
                )


if __name__ == "__main__":

    main()