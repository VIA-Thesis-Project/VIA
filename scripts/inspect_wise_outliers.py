import pandas as pd
import numpy as np

base = "../data/huaura/raw/wise30sec/source/WISE30sec/Interchangeable_format"

full = pd.read_csv(f"{base}/HW30s_FULL.txt")
wd1 = pd.read_csv(f"{base}/HW30s_wD1.txt")

d1 = full[full["Layer"] == "D1"].copy()

params = ["BSAT", "ESP", "GYPS"]

for param in params:

    tmp = d1[
        ["NEWSUID", "SCID", "PROP", "CLAF", param]
    ].copy()

    tmp["PROP"] = pd.to_numeric(tmp["PROP"], errors="coerce")
    tmp[param] = pd.to_numeric(tmp[param], errors="coerce")

    valid = (
        tmp["PROP"].notna()
        & (tmp["PROP"] > 0)
        & tmp[param].notna()
        & (tmp[param] != -9)
    )

    calc = tmp[valid].copy()

    calc["weighted"] = (
        calc["PROP"] * calc[param]
    )

    agg = calc.groupby("NEWSUID").agg(
        weighted_sum=("weighted", "sum"),
        valid_prop=("PROP", "sum")
    )

    agg["CALC"] = (
        agg["weighted_sum"] /
        agg["valid_prop"]
    )

    off = wd1[
        ["NEWSUID", "PROP_aw", "PROP_misc", param]
    ].copy()

    off[param] = pd.to_numeric(
        off[param],
        errors="coerce"
    )

    merged = (
        agg.reset_index()
        .merge(off, on="NEWSUID", how="inner")
    )

    merged = merged[
        merged[param] != -9
    ].copy()

    merged["DIFF"] = (
        merged["CALC"] -
        merged[param]
    ).abs()

    worst = merged.sort_values(
        "DIFF",
        ascending=False
    ).head(10)

    print()
    print("=" * 70)
    print(param)
    print("=" * 70)

    print(
        worst[
            [
                "NEWSUID",
                "CALC",
                param,
                "DIFF",
                "valid_prop",
                "PROP_aw",
                "PROP_misc"
            ]
        ].to_string(index=False)
    )

    print()
    print("COMPONENTES DE LOS 3 PEORES CASOS")

    for newsuid in worst["NEWSUID"].head(3):

        print()
        print("---", newsuid, "---")

        rows = d1[
            d1["NEWSUID"] == newsuid
        ][
            [
                "NEWSUID",
                "SCID",
                "PROP",
                "CLAF",
                "BSAT",
                "ESP",
                "GYPS"
            ]
        ]

        print(rows.to_string(index=False))