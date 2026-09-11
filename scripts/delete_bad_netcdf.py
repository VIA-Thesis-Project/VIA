from pathlib import Path
import xarray as xr

root = Path("../data/huaura/raw/nex-gddp-cmip6")

for f in root.rglob("*.nc"):
    try:
        with xr.open_dataset(f):
            pass
    except Exception:
        print("Deleting:", f)
        f.unlink()

print("Finished")