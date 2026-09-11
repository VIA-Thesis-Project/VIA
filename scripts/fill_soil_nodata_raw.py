import os
import shutil

import numpy as np
import rasterio


ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

SOURCE = os.path.join(
    ROOT,
    "data",
    "huaura",
    "raw",
    "soil_final",
)

OUTPUT = os.path.join(
    ROOT,
    "data",
    "huaura",
    "raw",
    "soil_final_gapfilled",
)

MASK = os.path.join(
    ROOT,
    "data",
    "huaura",
    "masks",
    "huaura_mask_005.tif",
)


# Celdas de la grilla 0.05° donde comprobamos
# NODATA real de la fuente.
#
# SoilGrids:
#   (1,10)
#   (13,2)
#
# WISE:
#   (1,10)
#   (9,15)
#
# soildepth:
#   (2,13)
#   (13,2)

SOILGRIDS_FOLDERS = [
    "clay_content",
    "sand_content",
    "coarse_fragments",
    "pH",
    "soil_organic_carbon",
]

WISE_FOLDERS = [
    "base_saturation",
    "gypsum",
    "sodicity",
]

TARGETS = {}

for folder in SOILGRIDS_FOLDERS:
    TARGETS[folder] = [
        (1, 10),
        (13, 2),
    ]

for folder in WISE_FOLDERS:
    TARGETS[folder] = [
        (1, 10),
        (9, 15),
    ]

TARGETS["soildepth"] = [
    (2, 13),
    (13, 2),
]


# ---------------------------------------------------------
# Copia preservando el dataset original
# ---------------------------------------------------------

if os.path.isdir(OUTPUT):
    shutil.rmtree(OUTPUT)

shutil.copytree(
    SOURCE,
    OUTPUT
)

print("Copia creada:")
print(OUTPUT)
print()


# ---------------------------------------------------------
# Coordenadas centrales de las celdas objetivo
# ---------------------------------------------------------

with rasterio.open(MASK) as ref:

    target_coordinates = {}

    for folder, cells in TARGETS.items():

        target_coordinates[folder] = []

        for row, col in cells:

            lon, lat = rasterio.transform.xy(
                ref.transform,
                row,
                col,
                offset="center"
            )

            target_coordinates[folder].append(
                (
                    row,
                    col,
                    float(lon),
                    float(lat),
                )
            )


# ---------------------------------------------------------
# Nearest-valid a resolución RAW
# ---------------------------------------------------------

def is_invalid(arr, mask, row, col):

    if row < 0 or col < 0:
        return True

    if row >= arr.shape[0]:
        return True

    if col >= arr.shape[1]:
        return True

    if mask[row, col]:
        return True

    return not np.isfinite(
        float(arr[row, col])
    )


def nearest_valid(arr, mask, row, col):

    valid = (
        ~mask
        & np.isfinite(arr)
    )

    rr, cc = np.where(valid)

    if len(rr) == 0:
        raise RuntimeError(
            "Raster sin píxeles válidos."
        )

    # Las grillas fuente tienen celdas cuadradas,
    # por lo que la distancia en índices identifica
    # correctamente el vecino raster más próximo.
    d2 = (
        (rr - row) ** 2
        + (cc - col) ** 2
    )

    idx = int(np.argmin(d2))

    nr = int(rr[idx])
    nc = int(cc[idx])

    return (
        nr,
        nc,
        float(arr[nr, nc]),
        float(np.sqrt(d2[idx])),
    )


filled_total = 0


for folder, targets in target_coordinates.items():

    folder_path = os.path.join(
        OUTPUT,
        folder,
    )

    files = sorted(
        fn
        for fn in os.listdir(folder_path)
        if fn.lower().endswith(
            (".tif", ".tiff")
        )
    )

    print("=" * 70)
    print(folder)
    print("=" * 70)

    for filename in files:

        path = os.path.join(
            folder_path,
            filename,
        )

        with rasterio.open(
            path,
            "r+"
        ) as src:

            masked = src.read(
                1,
                masked=True
            )

            arr = masked.data.copy()

            invalid_mask = (
                np.ma.getmaskarray(masked)
                | ~np.isfinite(arr)
            )

            changed = False

            for (
                grid_row,
                grid_col,
                lon,
                lat,
            ) in targets:

                src_row, src_col = src.index(
                    lon,
                    lat
                )

                if not is_invalid(
                    arr,
                    invalid_mask,
                    src_row,
                    src_col,
                ):

                    print(
                        filename,
                        f"grid=({grid_row},{grid_col})",
                        "ya válido:",
                        float(
                            arr[
                                src_row,
                                src_col
                            ]
                        ),
                    )

                    continue

                (
                    nr,
                    nc,
                    value,
                    pixel_distance,
                ) = nearest_valid(
                    arr,
                    invalid_mask,
                    src_row,
                    src_col,
                )

                arr[
                    src_row,
                    src_col
                ] = value

                invalid_mask[
                    src_row,
                    src_col
                ] = False

                changed = True
                filled_total += 1

                print(
                    filename,
                    f"grid=({grid_row},{grid_col})",
                    f"raw=({src_row},{src_col})",
                    "<-",
                    f"({nr},{nc})",
                    "value=",
                    value,
                    "pixel_distance=",
                    round(pixel_distance, 3),
                )

            if changed:

                src.write(
                    arr,
                    1
                )

    print()


print()
print("==============================")
print("GAP FILL TERMINADO")
print("==============================")

print(
    "Valores rellenados:",
    filled_total
)

print(
    "Salida:",
    OUTPUT
)