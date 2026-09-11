import os

import geopandas as gpd
import numpy as np
import rasterio

from shapely.geometry import box


ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

MASK = os.path.join(
    ROOT,
    "data",
    "huaura",
    "masks",
    "huaura_mask_0041667.tif",
)

LANDSEA = os.path.join(
    ROOT,
    "data",
    "huaura",
    "processed_0041667",
    "landsea.tif",
)

BOUNDARY = os.path.join(
    ROOT,
    "data",
    "huaura",
    "boundary",
    "huaura_province.geojson",
)

LAND = os.path.join(
    ROOT,
    "data",
    "huaura",
    "raw",
    "landsea",
    "ne_10m_land.geojson",
)


# ---------------------------------------------------------
# Encontrar celda Huaura marcada como mar
# ---------------------------------------------------------

with rasterio.open(MASK) as msrc:

    mask = msrc.read(1)
    transform = msrc.transform

with rasterio.open(LANDSEA) as lsrc:

    landsea = lsrc.read(1)


problem = (
    (mask == 2)
    &
    (landsea == 0)
)

cells = np.argwhere(problem)

print(
    "Celdas Huaura marcadas como mar:",
    len(cells)
)

print()


# ---------------------------------------------------------
# Geometrías
# ---------------------------------------------------------

huaura = gpd.read_file(
    BOUNDARY
).to_crs(
    "EPSG:4326"
)

land = gpd.read_file(
    LAND,
    bbox=(
        -77.8,
        -11.6,
        -76.4,
        -10.5,
    )
).to_crs(
    "EPSG:4326"
)

huaura_geom = huaura.geometry.union_all()
land_geom = land.geometry.union_all()


# ---------------------------------------------------------
# Analizar cada celda
# ---------------------------------------------------------

for row, col in cells:

    row = int(row)
    col = int(col)

    lon, lat = rasterio.transform.xy(
        transform,
        row,
        col,
        offset="center",
    )

    left, top = rasterio.transform.xy(
        transform,
        row,
        col,
        offset="ul",
    )

    right, bottom = rasterio.transform.xy(
        transform,
        row,
        col,
        offset="lr",
    )

    cell = box(
        left,
        bottom,
        right,
        top,
    )


    # Proyectar a UTM 18S para áreas métricas
    gs = gpd.GeoSeries(
        [
            cell,
            cell.intersection(
                huaura_geom
            ),
            cell.intersection(
                land_geom
            ),
        ],
        crs="EPSG:4326",
    ).to_crs(
        "EPSG:32718"
    )

    cell_area = gs.iloc[0].area
    huaura_area = gs.iloc[1].area
    land_area = gs.iloc[2].area


    print(
        "cell:",
        (row, col)
    )

    print(
        "center:",
        f"{lon:.6f}",
        f"{lat:.6f}"
    )

    print(
        "centro dentro Huaura:",
        huaura_geom.covers(
            gpd.points_from_xy(
                [lon],
                [lat]
            )[0]
        )
    )

    print(
        "centro Natural Earth land:",
        land_geom.covers(
            gpd.points_from_xy(
                [lon],
                [lat]
            )[0]
        )
    )

    print(
        "celda cubierta por Huaura:",
        f"{100 * huaura_area / cell_area:.2f}%"
    )

    print(
        "celda cubierta por tierra NE:",
        f"{100 * land_area / cell_area:.2f}%"
    )

    print()