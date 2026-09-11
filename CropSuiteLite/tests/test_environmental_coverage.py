import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import warnings

import numpy as np
import rasterio
from rasterio.transform import from_origin
import xarray as xr

from src.downscaling import process_tempday_interp
from src.crop_suitability_main import calculate_slope
from src.climate_suitability_main import process_day_climsuit_memopt
from src.climate_suitability_main_xarray import process_day_climsuit_xarray
from src.read_plant_params import read_crop_parameterizations_files, get_plant_param_interp_forms_dict
from src.spatial_validity import climate_coverage

ROOT = Path(__file__).resolve().parents[1]


class EnvironmentalCoverageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.previous_cwd = Path.cwd()
        os.chdir(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(os.chdir, self.previous_cwd)
        Path('temp').mkdir()

    def test_temperature_preserves_negative_zero_and_missing_on_equal_grid(self):
        original = np.array([[np.nan, -5.5, 0], [-9999, 22.5, 25]], dtype=float)
        land = np.ones(original.shape)
        land[1, 2] = 0
        for day, mode in enumerate(('nearest', 'bilinear')):
            with patch('src.downscaling.read_timestep', return_value=(original, -9999)), contextlib.redirect_stdout(io.StringIO()):
                process_tempday_interp(day, 'unused', [2, 0, 0, 3], original.shape, land, '.', mode)
            with xr.open_dataset(f'ds_temp_{day}.nc', mask_and_scale=False) as ds:
                np.testing.assert_array_equal(ds.data, [[-32767, -55, 0], [-32767, 225, -32767]])
        self.assertTrue(np.isnan(original[0, 0]))
        self.assertEqual(original[1, 0], -9999)

    def test_temperature_coast_resizes_without_dilution_or_extrapolated_coverage(self):
        original = np.array([[np.nan, 20], [np.nan, 20]])
        with patch('src.downscaling.read_timestep', return_value=(original, np.nan)), contextlib.redirect_stdout(io.StringIO()):
            process_tempday_interp(0, 'unused', [2, 0, 0, 2], (4, 6), np.ones((4, 6)), '.', 'bilinear')
        with xr.open_dataset('ds_temp_0.nc', mask_and_scale=False) as ds:
            np.testing.assert_array_equal(ds.data.values[:, :3], -32767)
            np.testing.assert_array_equal(ds.data.values[:, 3:], 200)

    def test_slope_of_plane_survives_coast_and_internal_nodata(self):
        yy, xx = np.indices((5, 6))
        dem = (3 * xx + 4 * yy).astype(float)
        dem[:, 0] = np.nan
        dem[2, 3] = np.nan
        transform = from_origin(0, 0.05, 0.01, 0.01)
        with rasterio.open('dem.tif', 'w', driver='GTiff', height=5, width=6,
                           count=1, dtype='float64', transform=transform,
                           crs='EPSG:4326', nodata=np.nan) as dst:
            dst.write(dem, 1)
        result = calculate_slope('dem.tif', dem.shape, [0, 0.05, 0.06, 0])
        np.testing.assert_array_equal(np.isfinite(result), np.isfinite(dem))
        expected = np.degrees(np.arctan(5 / (6371000 * np.deg2rad(0.01))))
        np.testing.assert_allclose(result[np.isfinite(dem)], expected)

    def test_isolated_dem_pixel_has_no_slope_estimate(self):
        dem = np.full((3, 3), np.nan)
        dem[1, 1] = 100
        with patch('src.crop_suitability_main.load_specified_lines', return_value=(dem[None], np.nan)):
            self.assertTrue(np.isnan(calculate_slope('unused', dem.shape, [0, 3, 3, 0])).all())

    def weather(self):
        temp = np.full((2, 3, 365), 240., dtype=float)
        prec = np.full_like(temp, 47.)
        prec[0, 1] = 0                 # Valid dry cell: suitability 0, not nodata.
        prec[0, 2] = np.nan            # Missing rain.
        temp[1, 0, 200] = -32767       # Missing outside current growing cycle.
        temp[1, 1] = 0                # Valid cold cell: suitability 0, not nodata.
        land = np.ones((2, 3))
        land[1, 2] = 0
        return temp, prec, land

    def test_coverage_distinguishes_dry_cold_missing_and_irrigated(self):
        temp, prec, land = self.weather()
        np.testing.assert_array_equal(climate_coverage(temp, prec, land), [[True, True, False], [False, True, False]])
        self.assertTrue(climate_coverage(temp, prec, land, irrigated=True)[0, 2])

    def test_daily_numpy_and_xarray_keep_nodata_out_of_membership(self):
        params = read_crop_parameterizations_files(ROOT / 'plant_params/available', verbose=False)
        params = {'maize': params['maize']}
        forms = get_plant_param_interp_forms_dict(params, {})['maize']
        temp, prec, land = self.weather()
        args = [0, 110, temp, prec, forms, False, land, 0, np.array([0]),
                [0] * 6, False, [0] * 4, [20, 15], False, [0, 24, 0, 2],
                0, 0, 7, 5, 0, 0, []]
        with warnings.catch_warnings(), contextlib.redirect_stdout(io.StringIO()):
            warnings.simplefilter('error', RuntimeWarning)
            process_day_climsuit_memopt(args)
        with rasterio.open('temp/0.tif') as src:
            numpy_result = src.read()
        valid = climate_coverage(temp, prec, land)
        np.testing.assert_array_equal(numpy_result[:, ~valid], -1)
        self.assertEqual(numpy_result[1, 0, 1], 0)
        self.assertEqual(numpy_result[0, 1, 1], 0)
        self.assertGreater(numpy_result[1, 0, 0], 75)

        def dataset(data):
            ds = xr.Dataset({'data': (('lat', 'lon', 'time'), data)},
                            coords={'lat': [1.5, .5], 'lon': [.5, 1.5, 2.5]})
            ds.lat.attrs['standard_name'] = 'latitude'
            ds.lon.attrs['standard_name'] = 'longitude'
            return ds
        mask = xr.DataArray(land, dims=('lat', 'lon'),
                            coords={'lat': [1.5, .5], 'lon': [.5, 1.5, 2.5]})
        with warnings.catch_warnings(), contextlib.redirect_stdout(io.StringIO()):
            warnings.simplefilter('error', RuntimeWarning)
            process_day_climsuit_xarray(0, dataset(temp), dataset(prec), mask,
                {'options': {'irrigation': 0}}, params, 'maize', np.array([0]),
                [2, 0, 0, 3], tmp_folder='temp')
        with rasterio.open('temp/0.tif') as src:
            for i, name in enumerate(('temperature', 'precipitation', 'failure_suit', 'sunshine_hours')):
                np.testing.assert_array_equal(src.read(src.descriptions.index(name) + 1), numpy_result[i])


if __name__ == '__main__':
    unittest.main()
