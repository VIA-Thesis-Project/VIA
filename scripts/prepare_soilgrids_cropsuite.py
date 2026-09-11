from pathlib import Path
import shutil


SRC = Path("../data/huaura/raw/soilgrids")

DST = Path("../data/huaura/raw/soilgrids_cropsuite")


mapping = {

    "clay": "clay_content",

    "sand": "sand_content",

    "cfvo": "coarse_fragments",

    "phh2o": "pH",

    "soc": "soil_organic_carbon",

    "cec": "base_saturation",

    "bdod": "soildepth"

}


def main():

    DST.mkdir(
        parents=True,
        exist_ok=True
    )


    for src_name, dst_name in mapping.items():

        src_dir = SRC / src_name

        dst_dir = DST / dst_name

        dst_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        for file in src_dir.glob("*.tif"):

            new_name = file.name.replace(
                src_name,
                dst_name
            )

            shutil.copy(
                file,
                dst_dir / new_name
            )

            print(
                dst_dir / new_name
            )


if __name__ == "__main__":
    main()