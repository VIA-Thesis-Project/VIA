from pathlib import Path
import xarray as xr

root = Path("../data/huaura/raw/nex-gddp-cmip6")

bad = []

for f in root.rglob("*.nc"):
    try:
        with xr.open_dataset(f):
            pass
        print("OK:", f.name)
    except Exception as e:
        print("BAD:", f.name)
        bad.append(f)

print("\nArchivos dañados:")
for b in bad:
    print(b)