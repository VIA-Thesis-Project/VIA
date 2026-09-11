import pandas as pd
import numpy as np

base = "../data/huaura/raw/wise30sec/source/WISE30sec/Interchangeable_format"

full_path = f"{base}/HW30s_FULL.txt"
wd1_path = f"{base}/HW30s_wD1.txt"

print("Leyendo WISE30sec...")

full = pd.read_csv(full_path)
wd1 = pd.read_csv(wd1_path)

# Solo topsoil D1 = 0-20 cm
d1 = full[full["Layer"] == "D1"].copy()

params = ["BSAT", "ESP", "GYPS"]

results = pd.DataFrame()

for param in params:

    tmp = d1[["NEWSUID", "PROP", param]].copy()

    tmp["PROP"] = pd.to_numeric(
        tmp["PROP"],
        errors="coerce"
    )

    tmp[param] = pd.to_numeric(
        tmp[param],
        errors="coerce"
    )

    # WISE utiliza -9 como valor ausente
    valid = (
        tmp[param].notna()
        & (tmp[param] >= 0)
        & tmp["PROP"].notna()
        & (tmp["PROP"] > 0)
    )

    tmp = tmp[valid].copy()

    tmp["weighted"] = tmp[param] * tmp["PROP"]

    agg = tmp.groupby("NEWSUID").agg(
        weighted_sum=("weighted", "sum"),
        weight_sum=("PROP", "sum")
    )

    agg[f"{param}_CALC"] = (
        agg["weighted_sum"]
        / agg["weight_sum"]
    )

    if results.empty:
        results = agg[[f"{param}_CALC"]]
    else:
        results = results.join(
            agg[[f"{param}_CALC"]],
            how="outer"
        )


# Tabla oficial ponderada D1
official = wd1[
    ["NEWSUID", "BSAT", "ESP", "GYPS"]
].copy()

for param in params:
    official[param] = pd.to_numeric(
        official[param],
        errors="coerce"
    )

    official.loc[
        official[param] < 0,
        param
    ] = np.nan


comparison = (
    results.reset_index()
    .merge(
        official,
        on="NEWSUID",
        how="inner"
    )
)


print()
print("========================================")
print("COMPARACIÓN FULL vs wD1")
print("========================================")

for param in params:

    calc = comparison[f"{param}_CALC"]
    off = comparison[param]

    valid = calc.notna() & off.notna()

    diff = (
        calc[valid]
        - off[valid]
    ).abs()

    print()
    print(param)
    print("NEWSUID comparados:", valid.sum())
    print("Diferencia media:", diff.mean())
    print("Diferencia máxima:", diff.max())
    print(
        "% diferencia <= 0.5:",
        round((diff <= 0.5).mean() * 100, 2)
    )
    print(
        "% diferencia <= 1.0:",
        round((diff <= 1.0).mean() * 100, 2)
    )


print()
print("Ejemplo:")
print(
    comparison[
        [
            "NEWSUID",
            "BSAT_CALC", "BSAT",
            "ESP_CALC", "ESP",
            "GYPS_CALC", "GYPS"
        ]
    ].head(15).to_string(index=False)
)