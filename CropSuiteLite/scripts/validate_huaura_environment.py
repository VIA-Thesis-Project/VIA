"""Run the full pipeline in a fresh folder and verify environmental coverage.

From CropSuiteLite: .venv/Scripts/python.exe scripts/validate_huaura_environment.py
Original inputs, config, caches and results are left unchanged.
"""
import configparser
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

import numpy as np
import rasterio
import xarray as xr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from CropSuite import CropSuiteLite


def counts(array):
    values, sizes = np.unique(array, return_counts=True)
    return {str(float(v)): int(n) for v, n in zip(values, sizes)}


def main():
    source_config = ROOT / 'config_access_esm1_5_ssp126_2021_2040.ini'
    config = configparser.ConfigParser()
    config.read(source_config)
    for key, value in config['files'].items():
        config['files'][key] = str((ROOT / value).resolve())
    for section in config.sections():
        if section.startswith('parameters.'):
            config[section]['data_directory'] = str((ROOT / config[section]['data_directory']).resolve())
    original_output = Path(config['files']['output_dir'] + '_novar')
    inputs = [source_config, Path(config['files']['fine_dem']), Path(config['files']['land_sea_mask'])]
    inputs += list(Path(config['files']['climate_data_dir']).glob('*.tif'))
    inputs += list(Path(config['files']['plant_param_dir']).glob('*.inf'))
    for section in config.sections():
        if section.startswith('parameters.'):
            inputs += list(Path(config[section]['data_directory']).glob('*.tif'))
    fingerprints = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    parent = ROOT / 'results/huaura_environment_validation'
    parent.mkdir(parents=True, exist_ok=True)
    audit = Path(tempfile.mkdtemp(prefix='run_', dir=parent))
    config['files']['output_dir'] = str(audit / 'simulation')
    config['options']['remove_downscaled_climate'] = 'n'
    run_config = audit / 'config.ini'
    with run_config.open('w') as file:
        config.write(file)
    previous_cwd = Path.cwd()
    try:
        os.chdir(audit)
        model = CropSuiteLite(str(run_config))
        model.run()
        report = {'audit_directory': str(audit), 'scope': 'Environmental coverage validation; not a parcel assessment.',
                  'daily_validation': {}, 'outputs': {}}
        with rasterio.open(config['files']['land_sea_mask']) as src:
            land = src.read(1) == 1
            transform = src.transform
        with rasterio.open(ROOT.parent / 'data/huaura/masks/huaura_mask_0041667.tif') as src:
            huaura = src.read(1) > 0
        climate_valid = land.copy()
        for variable in ('Temp', 'Prec'):
            with rasterio.open(Path(config['files']['climate_data_dir']) / f'{variable}_avg.tif') as src:
                raw = src.read()
                nodata = src.nodata
            valid = np.isfinite(raw)
            if nodata is not None:
                valid &= raw != nodata
            valid &= ((raw >= -100) & (raw <= 60)) if variable == 'Temp' else raw >= 0
            valid &= land[None]
            climate_valid &= valid.all(axis=0)
            values = raw.astype(float)
            if variable == 'Prec':
                threshold = float(config['options']['downscaling_precipitation_per_day_threshold'])
                values[values < threshold] = 0
            expected = np.full(raw.shape, -32767, dtype=np.int16)
            expected[valid] = (values[valid] * 10).astype(np.int16)
            daily = []
            for day in range(365):
                path = Path(model._output_dir) / f'ds_{variable.lower()}_{day}.nc'
                with xr.open_dataset(path, mask_and_scale=False) as ds:
                    daily.append(ds.data.values.copy())
            daily = np.asarray(daily)
            np.testing.assert_array_equal(daily, expected)
            report['daily_validation'][variable] = {
                'days': len(daily), 'unexpected_differences': int(np.count_nonzero(daily != expected)),
                'valid_huaura_land_cells_all_year': int((valid.all(axis=0) & huaura).sum()),
                'all_year_zero_huaura_land_cells': int(((daily == 0).all(axis=0) & huaura & land).sum()),
            }
        result_dir = Path(str(model.output_path) + '_novar') / model.area_name
        with rasterio.open(config['files']['fine_dem']) as src:
            dem = src.read(1, masked=True)
            dem_valid = ~np.ma.getmaskarray(dem) & np.isfinite(dem.data)
        with rasterio.open(result_dir / 'slope_combined.tif') as src:
            slope = src.read(1, masked=True)
            slope_valid = ~np.ma.getmaskarray(slope) & np.isfinite(slope.data)
        assert slope_valid[huaura & land].all()
        report['slope'] = {'valid_dem_huaura_land_cells': int(dem_valid[huaura & land].sum()),
                           'valid_slope_huaura_land_cells': int(slope_valid[huaura & land].sum())}
        for name in ('climate_suitability', 'crop_suitability', 'soil_suitability', 'crop_suitability_multi'):
            path = result_dir / 'maize' / f'{name}.tif'
            with rasterio.open(path) as src:
                data = src.read(1)
                np.testing.assert_allclose(tuple(src.transform), tuple(transform), atol=1e-12, rtol=0)
                assert src.crs.to_epsg() == 4326
            assert np.all(data[~climate_valid] == -1)
            if name == 'climate_suitability':
                np.testing.assert_array_equal(data >= 0, climate_valid)
            entry = {'path': str(path), 'whole_grid_counts': counts(data),
                     'huaura_land_counts': counts(data[huaura & land])}
            old = original_output / model.area_name / 'maize' / f'{name}.tif'
            if old.exists():
                with rasterio.open(old) as src:
                    entry['previous_huaura_land_counts'] = counts(src.read(1)[huaura & land])
            report['outputs'][name] = entry
        report['inputs_unchanged'] = all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in fingerprints.items())
        report['input_sha256'] = fingerprints
        assert report['inputs_unchanged']
        (audit / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(f'VALIDATION PASSED: {audit / "report.json"}')
    finally:
        os.chdir(previous_cwd)


if __name__ == '__main__':
    main()
