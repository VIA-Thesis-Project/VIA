"""Regression checks for downscaled precipitation (tenths of mm) -> membership (mm).

Run from CropSuiteLite: .venv/Scripts/python.exe -m unittest discover -s tests -v
"""
import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest

import numpy as np
import rasterio
import xarray as xr

from src.climate_suitability_main import process_day_climsuit_memopt
from src.climate_suitability_main_xarray import process_day_climsuit_xarray
from src.downscaling import process_precday_interp
from src.read_plant_params import (
    get_plant_param_interp_forms_dict,
    read_crop_parameterizations_files,
)


ROOT = Path(__file__).resolve().parents[1]


class PrecipitationUnitsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.params = read_crop_parameterizations_files(
            ROOT / 'plant_params/available', verbose=False
        )
        cls.params = {'maize': cls.params['maize']}
        cls.forms = get_plant_param_interp_forms_dict(cls.params, {})['maize']

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.previous_cwd = Path.cwd()
        os.chdir(self.tmp.name)
        Path('temp').mkdir()
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(os.chdir, self.previous_cwd)

    @staticmethod
    def weather():
        # Four cells: 512, 51.2, 750 and 512 mm over 110 days.
        # The last cell has no rain in the first 15 days (sowing constraint).
        totals = np.array([[5120, 512], [7500, 5120]])
        prec = np.zeros((2, 2, 365), dtype=np.int16)
        for row, col in np.ndindex(2, 2):
            start = 15 if (row, col) == (1, 1) else 0
            n = 110 - start
            value, remainder = divmod(int(totals[row, col]), n)
            prec[row, col, start:110] = value
            prec[row, col, start:start + remainder] += 1
        return np.full_like(prec, 240), prec

    def test_downscaling_stores_tenths_for_both_methods(self):
        for day, method in enumerate(('nearest', 'bilinear')):
            with contextlib.redirect_stdout(io.StringIO()):
                process_precday_interp(
                    day, np.full((2, 2), 5.5), [2, 0, 0, 2],
                    0.5, (2, 2), np.ones((2, 2)), '.', -9999, method,
                )
            with xr.open_dataset(f'ds_prec_{day}.nc') as ds:
                np.testing.assert_array_equal(ds.data.values, np.full((2, 2), 55))

    def test_numpy_membership_and_sowing_threshold_use_consistent_units(self):
        temp, prec = self.weather()
        args = [0, 110, temp, prec, self.forms, False, np.ones((2, 2)),
                0, np.array([0]), [0] * 6, False, [0] * 4, [20, 15],
                False, [0, 24, 0, 2], 0, 0, 7, 5, 0, 0, []]
        with contextlib.redirect_stdout(io.StringIO()):
            process_day_climsuit_memopt(args)
        with rasterio.open('temp/0.tif') as src:
            # Linear maize membership: 512 mm -> 0.7704 -> integer score 77.
            np.testing.assert_array_equal(src.read(2), [[77, 0], [100, 0]])
            np.testing.assert_array_equal(src.read(1), np.full((2, 2), 100))

    def test_xarray_membership_matches_numpy(self):
        temp, prec = self.weather()
        def dataset(values):
            ds = xr.Dataset({'data': (('lat', 'lon', 'time'), values)},
                            coords={'lat': [1.5, 0.5], 'lon': [0.5, 1.5]})
            ds.lat.attrs['standard_name'] = 'latitude'
            ds.lon.attrs['standard_name'] = 'longitude'
            return ds
        mask = xr.DataArray(np.ones((2, 2)), dims=('lat', 'lon'),
                            coords={'lat': [1.5, 0.5], 'lon': [0.5, 1.5]})
        with contextlib.redirect_stdout(io.StringIO()):
            process_day_climsuit_xarray(
                0, dataset(temp), dataset(prec), mask,
                {'options': {'irrigation': 0}}, self.params, 'maize',
                np.array([0]), [2, 0, 0, 2], tmp_folder='temp',
            )
        with rasterio.open('temp/0.tif') as src:
            band = src.descriptions.index('precipitation') + 1
            np.testing.assert_array_equal(src.read(band), [[77, 0], [100, 0]])


if __name__ == '__main__':
    unittest.main()
