import glob
import os
import shutil


ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATA = os.path.join(
    ROOT,
    "data",
    "huaura",
)

SOILGRIDS = os.path.join(
    DATA,
    "raw",
    "soilgrids",
)

WISE = os.path.join(
    DATA,
    "raw",
    "wise30sec_huaura",
)

SALINITY = os.path.join(
    DATA,
    "raw",
    "salinity",
    "salinity_2016.tif",
)

SOILDEPTH = os.path.join(
    DATA,
    "raw",
    "soildepth_final",
    "soildepth_0-200cm.tif",
)

OUT = os.path.join(
    DATA,
    "raw",
    "soil_final",
)


# ---------------------------------------------------------
# Limpiar salida
# ---------------------------------------------------------

if os.path.isdir(OUT):
    shutil.rmtree(OUT)

os.makedirs(OUT)


def copy_files(src_dir, dst_name):

    files = sorted(
        glob.glob(
            os.path.join(src_dir, "*.tif")
        )
    )

    if not files:
        raise RuntimeError(
            f"No hay TIFF en: {src_dir}"
        )

    dst_dir = os.path.join(
        OUT,
        dst_name,
    )

    os.makedirs(dst_dir)

    for src in files:

        dst = os.path.join(
            dst_dir,
            os.path.basename(src),
        )

        shutil.copy2(src, dst)

    return files


def copy_single(src, dst_dir_name, dst_filename):

    if not os.path.isfile(src):
        raise RuntimeError(
            f"No existe: {src}"
        )

    dst_dir = os.path.join(
        OUT,
        dst_dir_name,
    )

    os.makedirs(
        dst_dir,
        exist_ok=True,
    )

    dst = os.path.join(
        dst_dir,
        dst_filename,
    )

    shutil.copy2(src, dst)

    return dst


print("Copiando SoilGrids...")


# SoilGrids válidos
soilgrids_map = {
    "clay": "clay_content",
    "sand": "sand_content",
    "cfvo": "coarse_fragments",
    "phh2o": "pH",
    "soc": "soil_organic_carbon",
}


for source_name, target_name in soilgrids_map.items():

    files = copy_files(
        os.path.join(
            SOILGRIDS,
            source_name,
        ),
        target_name,
    )

    print(
        target_name,
        "->",
        len(files),
        "archivos"
    )


print()
print("Copiando WISE30sec...")


copy_single(
    os.path.join(
        WISE,
        "base_saturation",
        "base_saturation_0-20cm.tif",
    ),
    "base_saturation",
    "bsat_0-20cm.tif",
)

copy_single(
    os.path.join(
        WISE,
        "sodicity",
        "sodicity_0-20cm.tif",
    ),
    "sodicity",
    "sod_0-20cm.tif",
)

copy_single(
    os.path.join(
        WISE,
        "gypsum",
        "gypsum_0-20cm.tif",
    ),
    "gypsum",
    "gyps_0-20cm.tif",
)


print("WISE: OK")


print()
print("Copiando salinidad...")


# "0-NA" es solo un token de ordenamiento para CropSuite.
# El Global Soil Salinity Map no representa una de las
# seis capas estándar de SoilGrids.
copy_single(
    SALINITY,
    "salinity",
    "sal_0-NA.tif",
)


print("Salinidad: OK")


print()
print("Copiando soildepth...")


# Profundidad total, no intervalo de horizonte.
copy_single(
    SOILDEPTH,
    "soildepth",
    "depth_0-NA.tif",
)


print("Soildepth: OK")


# ---------------------------------------------------------
# Validación
# ---------------------------------------------------------

print()
print("==============================")
print("SOIL FINAL")
print("==============================")


expected = [
    "base_saturation",
    "clay_content",
    "coarse_fragments",
    "gypsum",
    "pH",
    "salinity",
    "sand_content",
    "soil_organic_carbon",
    "sodicity",
    "soildepth",
]


for parameter in expected:

    folder = os.path.join(
        OUT,
        parameter,
    )

    files = sorted(
        glob.glob(
            os.path.join(
                folder,
                "*.tif",
            )
        )
    )

    print(
        f"{parameter}: "
        f"{len(files)} archivo(s)"
    )

    for fn in files:
        print(
            "   ",
            os.path.basename(fn)
        )


print()
print("Carpeta final:")
print(OUT)

print()
print("Terminado.")