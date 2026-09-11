import os

import numpy as np
import rasterio

from pyproj import Transformer


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


PROCESSED = {
    "soilgrids": os.path.join(
        ROOT,
        "data",
        "huaura",
        "processed_0041667",
        "soil",
        "clay_content",
        "clay_0-5cm_mean.tif",
    ),

    "wise": os.path.join(
        ROOT,
        "data",
        "huaura",
        "processed_0041667",
        "soil",
        "base_saturation",
        "bsat_0-20cm.tif",
    ),

    "depth": os.path.join(
        ROOT,
        "data",
        "huaura",
        "processed_0041667",
        "soil",
        "soildepth",
        "depth_0-NA.tif",
    ),
}


RAW = {
    "soilgrids": os.path.join(
        ROOT,
        "data",
        "huaura",
        "raw",
        "soil_final_gapfilled",
        "clay_content",
        "clay_0-5cm_mean.tif",
    ),

    "wise": os.path.join(
        ROOT,
        "data",
        "huaura",
        "raw",
        "soil_final_gapfilled",
        "base_saturation",
        "bsat_0-20cm.tif",
    ),

    "depth": os.path.join(
        ROOT,
        "data",
        "huaura",
        "raw",
        "soil_final_gapfilled",
        "soildepth",
        "depth_0-NA.tif",
    ),
}


transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32718",
    always_xy=True,
)


with rasterio.open(MASK) as ref:

    inside = ref.read(1) == 2
    ref_transform = ref.transform


print(
    "CELDAS HUAURA:",
    int(inside.sum())
)

print()


for name in [
    "soilgrids",
    "wise",
    "depth",
]:

    with rasterio.open(
        PROCESSED[name]
    ) as src:

        arr = src.read(1)


    missing = (
        inside
        & ~np.isfinite(arr)
    )

    cells = np.argwhere(
        missing
    )


    print("=" * 65)
    print(
        name.upper(),
        "- missing:",
        len(cells)
    )
    print("=" * 65)


    with rasterio.open(
        RAW[name]
    ) as raw:

        raw_arr = raw.read(
            1,
            masked=True
        )

        data = raw_arr.data.astype(
            np.float64
        )

        raw_mask = (
            np.ma.getmaskarray(raw_arr)
            | ~np.isfinite(data)
        )

        valid = ~raw_mask

        rr_valid, cc_valid = np.where(
            valid
        )

        xs_valid, ys_valid = (
            rasterio.transform.xy(
                raw.transform,
                rr_valid,
                cc_valid,
                offset="center",
            )
        )

        xs_valid = np.asarray(
            xs_valid
        )

        ys_valid = np.asarray(
            ys_valid
        )

        ux_valid, uy_valid = (
            transformer.transform(
                xs_valid,
                ys_valid,
            )
        )


        for row, col in cells:

            lon, lat = rasterio.transform.xy(
                ref_transform,
                int(row),
                int(col),
                offset="center",
            )

            raw_row, raw_col = raw.index(
                lon,
                lat
            )


            if (
                0 <= raw_row < raw.height
                and
                0 <= raw_col < raw.width
            ):

                raw_value = raw_arr[
                    raw_row,
                    raw_col
                ]

                if np.ma.is_masked(
                    raw_value
                ):
                    raw_txt = "NODATA"

                else:
                    raw_txt = float(
                        raw_value
                    )

            else:
                raw_txt = "OUTSIDE"


            x0, y0 = transformer.transform(
                lon,
                lat
            )

            distances = np.sqrt(
                (ux_valid - x0) ** 2
                +
                (uy_valid - y0) ** 2
            )

            idx = int(
                np.argmin(
                    distances
                )
            )

            nr = int(
                rr_valid[idx]
            )

            nc = int(
                cc_valid[idx]
            )

            nearest_value = float(
                data[nr, nc]
            )

            nearest_distance = float(
                distances[idx]
            )


            print()

            print(
                f"grid=({row},{col})"
            )

            print(
                "  lon/lat:",
                f"{lon:.6f}",
                f"{lat:.6f}"
            )

            print(
                "  RAW:",
                raw_txt
            )

            print(
                "  raw cell:",
                (
                    raw_row,
                    raw_col
                )
            )

            print(
                "  nearest valid:",
                nearest_value
            )

            print(
                "  distance:",
                f"{nearest_distance:.1f} m"
            )

            print(
                "  raw resolution:",
                raw.res
            )


    print()


print("TERMINADO")