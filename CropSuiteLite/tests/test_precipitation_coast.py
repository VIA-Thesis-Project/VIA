"""Missing source coverage must neither dilute rainfall nor gain rainfall."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest

import numpy as np
import xarray as xr

from src.downscaling import process_precday_interp


class PrecipitationCoastTest(unittest.TestCase):
    def resample(self, source, shape, land=None, mode='bilinear', nodata=np.nan):
        if land is None:
            land = np.ones(shape)
        before = source.copy()
        with tempfile.TemporaryDirectory() as tmp:
            with contextlib.redirect_stdout(io.StringIO()):
                process_precday_interp(0, source, [2, 0, 0, 2], 0.5, shape,
                                      land, tmp, nodata, mode)
            with xr.open_dataset(Path(tmp) / 'ds_prec_0.nc', mask_and_scale=False) as ds:
                result = ds.data.values.copy()
                self.assertEqual(ds.data.dtype, np.dtype('int16'))
                self.assertEqual(ds.data.attrs['_FillValue'], -32767)
        np.testing.assert_array_equal(source, before)
        return result

    def test_equal_grid_preserves_coast_and_legitimate_dry_days(self):
        source = np.array([[np.nan, 5.5, 0.0], [np.nan, 0.4, 0.5]])
        for mode in ('bilinear', 'nearest'):
            with self.subTest(mode=mode):
                # Destination land cannot extend the source's coverage.
                result = self.resample(source, source.shape, mode=mode)
                np.testing.assert_array_equal(result, [[-32767, 55, 0], [-32767, 0, 5]])

    def test_resizing_coast_never_dilutes_constant_land_rain(self):
        source = np.array([[np.nan, 5.5], [np.nan, 5.5]])
        for mode in ('bilinear', 'nearest'):
            # Non-integer scale and downsampling also need the exact target size.
            for shape in ((4, 6), (3, 5), (1, 2)):
                with self.subTest(mode=mode, shape=shape):
                    result = self.resample(source, shape, mode=mode)
                    self.assertEqual(result.shape, shape)
                    self.assertTrue(np.any(result == -32767))
                    self.assertTrue(np.any(result == 55))
                    np.testing.assert_array_equal(result[result != -32767], 55)
                    self.assertTrue(np.all(result[:, 0] == -32767))
                    self.assertTrue(np.all(result[:, -1] == 55))

    def test_destination_ocean_is_restored_for_zero_and_nan_masks(self):
        source = np.full((2, 2), 5.5)
        land = np.ones((4, 4))
        land[0, :] = 0
        land[-1, :] = np.nan
        result = self.resample(source, land.shape, land=land)
        np.testing.assert_array_equal(result[0], -32767)
        np.testing.assert_array_equal(result[-1], -32767)
        np.testing.assert_array_equal(result[1:3], 55)

    def test_all_missing_produces_only_nodata(self):
        for source in (np.full((2, 2), np.nan), np.full((2, 2), -9999)):
            with self.subTest(source=source):
                np.testing.assert_array_equal(self.resample(source, (3, 5), nodata=-9999), -32767)

    def test_numeric_nodata_and_nonfinite_values_are_not_dry_days(self):
        source = np.array([[9999, 5.5], [np.inf, -1.0]])
        result = self.resample(source, source.shape, nodata=9999)
        np.testing.assert_array_equal(result, [[-32767, 55], [-32767, -32767]])


if __name__ == '__main__':
    unittest.main()
