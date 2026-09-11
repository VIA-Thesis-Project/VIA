import os
import shutil
import zipfile

import earthaccess


ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

OUT_DIR = os.path.join(
    ROOT,
    "data",
    "huaura",
    "raw",
    "pelletier",
)

ZIP_PATH = os.path.join(
    OUT_DIR,
    "Global_Soil_Regolith_Sediment_1304.zip",
)

TARGET_PATH = os.path.join(
    OUT_DIR,
    "average_soil_and_sedimentary-deposit_thickness.tif",
)

URL = (
    "https://data.ornldaac.earthdata.nasa.gov/"
    "protected/bundle/"
    "Global_Soil_Regolith_Sediment_1304.zip"
)

os.makedirs(OUT_DIR, exist_ok=True)


print("Autenticación NASA Earthdata...")

auth = earthaccess.login(
    strategy="interactive",
    persist=False,
)

session = auth.get_session()


# ---------------------------------------------------------
# Descarga reanudable
# ---------------------------------------------------------

existing = (
    os.path.getsize(ZIP_PATH)
    if os.path.exists(ZIP_PATH)
    else 0
)

headers = {}

if existing > 0:
    headers["Range"] = f"bytes={existing}-"
    print(
        "Intentando reanudar desde:",
        round(existing / 1024 / 1024, 1),
        "MB",
    )


with session.get(
    URL,
    stream=True,
    headers=headers,
    allow_redirects=True,
    timeout=(30, 180),
) as r:

    print("Status:", r.status_code)

    r.raise_for_status()

    if existing > 0 and r.status_code == 206:
        mode = "ab"
        downloaded = existing
    else:
        mode = "wb"
        downloaded = 0

    content_length = int(
        r.headers.get("content-length", 0)
    )

    expected = (
        downloaded + content_length
        if content_length
        else None
    )

    with open(ZIP_PATH, mode) as f:

        next_report = downloaded + 50 * 1024 * 1024

        for chunk in r.iter_content(
            chunk_size=1024 * 1024
        ):

            if not chunk:
                continue

            f.write(chunk)
            downloaded += len(chunk)

            if downloaded >= next_report:

                print(
                    "Descargado:",
                    round(
                        downloaded / 1024 / 1024,
                        1,
                    ),
                    "MB",
                )

                next_report += 50 * 1024 * 1024


print()
print(
    "ZIP descargado:",
    round(
        os.path.getsize(ZIP_PATH)
        / 1024 / 1024,
        1,
    ),
    "MB",
)


# ---------------------------------------------------------
# Extraer solo el GeoTIFF necesario
# ---------------------------------------------------------

print("Buscando raster Pelletier...")

with zipfile.ZipFile(ZIP_PATH) as z:

    matches = [
        name
        for name in z.namelist()
        if name.lower().endswith(
            "average_soil_and_sedimentary-deposit_thickness.tif"
        )
    ]

    if len(matches) != 1:
        raise RuntimeError(
            f"Se esperaba 1 raster y se encontraron: {matches}"
        )

    source_name = matches[0]

    print("Encontrado:", source_name)

    with z.open(source_name) as src:
        with open(TARGET_PATH, "wb") as dst:
            shutil.copyfileobj(src, dst)


print()
print("Pelletier listo:")
print(TARGET_PATH)