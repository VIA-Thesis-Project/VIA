import numpy as np
import rasterio

from pyproj import Transformer


MASK = "../data/huaura/masks/huaura_mask_005.tif"

SOURCES = {
    "clay": (
        "../data/huaura/raw/soilgrids/"
        "clay/clay_0-5cm_mean.tif"
    ),
    "wise": (
        "../data/huaura/raw/wise30sec_huaura/"
        "base_saturation/base_saturation_0-20cm.tif"
    ),
    "depth": (
        "../data/huaura/raw/soildepth_final/"
        "soildepth_0-200cm.tif"
    ),
}

AFFECTED = {
    (1, 10): ["clay", "wise"],
    (2, 13): ["depth"],
    (9, 15): ["wise"],
    (13, 2): ["clay", "depth"],
}


transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32718",
    always_xy=True,
)


with rasterio.open(MASK) as ref:
    ref_transform = ref.transform


for (row, col), source_names in AFFECTED.items():

    lon, lat = rasterio.transform.xy(
        ref_transform,
        row,
        col,
        offset="center"
    )

    x0, y0 = transformer.transform(
        lon,
        lat
    )

    print()
    print("=" * 60)
    print(
        f"CELDA ({row},{col}) "
        f"lon={lon:.6f} lat={lat:.6f}"
    )
    print("=" * 60)

    for name in source_names:

        path = SOURCES[name]

        with rasterio.open(path) as src:

            arr = src.read(
                1,
                masked=True
            )

            data = arr.data.astype(
                np.float64
            )

            valid = (
                ~np.ma.getmaskarray(arr)
                & np.isfinite(data)
            )

            rr, cc = np.where(valid)

            # Coordenada del centro de cada pixel válido
            xs, ys = rasterio.transform.xy(
                src.transform,
                rr,
                cc,
                offset="center"
            )

            xs = np.asarray(xs)
            ys = np.asarray(ys)

            # Pasar candidatos a UTM
            ux, uy = transformer.transform(
                xs,
                ys
            )

            dist = np.sqrt(
                (ux - x0) ** 2
                + (uy - y0) ** 2
            )

            idx = np.argmin(dist)

            nearest_row = int(rr[idx])
            nearest_col = int(cc[idx])

            nearest_value = float(
                data[
                    nearest_row,
                    nearest_col
                ]
            )

            nearest_lon = float(xs[idx])
            nearest_lat = float(ys[idx])
            nearest_dist = float(dist[idx])

            print()
            print("Fuente:", name)

            print(
                "  nearest value:",
                nearest_value
            )

            print(
                "  nearest source cell:",
                (
                    nearest_row,
                    nearest_col
                )
            )

            print(
                "  nearest lon/lat:",
                f"{nearest_lon:.6f}",
                f"{nearest_lat:.6f}"
            )

            print(
                "  distancia:",
                f"{nearest_dist:.1f} m"
            )

            print(
                "  resolución fuente:",
                src.res
            )


print()
print("Terminado.")