import os
import glob
import hashlib

import geopandas as gpd
import numpy as np
import rasterio

from rasterio.features import rasterize
from scipy.ndimage import label
from scipy.spatial import cKDTree
from pyproj import Transformer


ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

BOUNDARY = os.path.join(
    ROOT,
    "data",
    "huaura",
    "boundary",
    "huaura_province.geojson",
)

RAW = os.path.join(
    ROOT,
    "data",
    "huaura",
    "raw",
    "soil_final_gapfilled",
)


GROUPS = {
    "SOILGRIDS": (
        glob.glob(
            os.path.join(
                RAW,
                "clay_content",
                "*.tif"
            )
        )
        +
        glob.glob(
            os.path.join(
                RAW,
                "sand_content",
                "*.tif"
            )
        )
        +
        glob.glob(
            os.path.join(
                RAW,
                "coarse_fragments",
                "*.tif"
            )
        )
        +
        glob.glob(
            os.path.join(
                RAW,
                "pH",
                "*.tif"
            )
        )
        +
        glob.glob(
            os.path.join(
                RAW,
                "soil_organic_carbon",
                "*.tif"
            )
        )
    ),

    "WISE": (
        glob.glob(
            os.path.join(
                RAW,
                "base_saturation",
                "*.tif"
            )
        )
        +
        glob.glob(
            os.path.join(
                RAW,
                "gypsum",
                "*.tif"
            )
        )
        +
        glob.glob(
            os.path.join(
                RAW,
                "sodicity",
                "*.tif"
            )
        )
    ),

    "DEPTH": glob.glob(
        os.path.join(
            RAW,
            "soildepth",
            "*.tif"
        )
    ),
}


province = gpd.read_file(
    BOUNDARY
)

if province.crs is None:
    province = province.set_crs(
        "EPSG:4326"
    )


transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32718",
    always_xy=True,
)


for group_name, files in GROUPS.items():

    print()
    print("=" * 70)
    print(group_name)
    print("=" * 70)

    patterns = {}

    for path in sorted(files):

        with rasterio.open(path) as src:

            geom = province.to_crs(
                src.crs
            )

            inside = rasterize(
                (
                    (g, 1)
                    for g in geom.geometry
                    if g is not None
                    and not g.is_empty
                ),
                out_shape=(
                    src.height,
                    src.width
                ),
                transform=src.transform,
                fill=0,
                default_value=1,
                dtype="uint8",
                all_touched=False,
            ).astype(bool)

            arr = src.read(
                1,
                masked=True
            )

            invalid = (
                np.ma.getmaskarray(arr)
                |
                ~np.isfinite(
                    arr.data
                )
            )

            missing = (
                inside
                &
                invalid
            )

            # Incluimos shape en la firma
            signature = hashlib.sha1(
                (
                    str(missing.shape).encode()
                    +
                    missing.tobytes()
                )
            ).hexdigest()

            if signature not in patterns:

                patterns[signature] = {
                    "files": [],
                    "missing": missing,
                    "inside": inside,
                    "transform": src.transform,
                    "crs": src.crs,
                }

            patterns[
                signature
            ][
                "files"
            ].append(
                os.path.relpath(
                    path,
                    RAW
                )
            )


    print(
        "Archivos:",
        len(files)
    )

    print(
        "Patrones NODATA distintos:",
        len(patterns)
    )

    print()


    for pnum, info in enumerate(
        patterns.values(),
        start=1
    ):

        missing = info["missing"]
        inside = info["inside"]
        transform = info["transform"]

        structure = np.ones(
            (3, 3),
            dtype=np.uint8
        )

        labeled, ncomp = label(
            missing,
            structure=structure
        )

        sizes = []

        for cid in range(
            1,
            ncomp + 1
        ):

            sizes.append(
                int(
                    np.sum(
                        labeled == cid
                    )
                )
            )


        valid = (
            inside
            &
            ~missing
        )


        # -------------------------------------------------
        # Distancia de cada NODATA al píxel válido
        # más cercano dentro de Huaura
        # -------------------------------------------------

        rr_v, cc_v = np.where(
            valid
        )

        rr_m, cc_m = np.where(
            missing
        )


        if len(rr_m) > 0:

            xv, yv = rasterio.transform.xy(
                transform,
                rr_v,
                cc_v,
                offset="center"
            )

            xm, ym = rasterio.transform.xy(
                transform,
                rr_m,
                cc_m,
                offset="center"
            )

            xv = np.asarray(xv)
            yv = np.asarray(yv)

            xm = np.asarray(xm)
            ym = np.asarray(ym)


            if str(
                info["crs"]
            ).upper() == "EPSG:4326":

                xv, yv = transformer.transform(
                    xv,
                    yv
                )

                xm, ym = transformer.transform(
                    xm,
                    ym
                )


            valid_coords = np.column_stack(
                [xv, yv]
            )

            missing_coords = np.column_stack(
                [xm, ym]
            )

            tree = cKDTree(
                valid_coords
            )

            distances, _ = tree.query(
                missing_coords,
                k=1
            )

            min_dist = float(
                np.min(distances)
            )

            median_dist = float(
                np.median(distances)
            )

            max_dist = float(
                np.max(distances)
            )

        else:

            min_dist = 0.0
            median_dist = 0.0
            max_dist = 0.0


        print(
            f"Patrón {pnum}"
        )

        print(
            "  archivos:",
            len(
                info["files"]
            )
        )

        print(
            "  NODATA dentro Huaura:",
            int(
                missing.sum()
            )
        )

        print(
            "  componentes:",
            ncomp
        )

        print(
            "  tamaños componentes:",
            sorted(
                sizes,
                reverse=True
            )[:20]
        )

        print(
            "  distancia nearest-valid:"
        )

        print(
            "    min:",
            f"{min_dist:.1f} m"
        )

        print(
            "    mediana:",
            f"{median_dist:.1f} m"
        )

        print(
            "    max:",
            f"{max_dist:.1f} m"
        )

        print(
            "  primer archivo:",
            info["files"][0]
        )

        print()


print("DIAGNOSTICO TERMINADO")