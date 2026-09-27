import configparser
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import rasterio
from rasterio.transform import from_origin
from shapely.geometry import Polygon, box, mapping
from shapely.ops import transform as geometry_transform
from src import multicrop as mc


class MulticropTest(unittest.TestCase):
    def test_huaura_supported_catalog_is_selectable(self):
        catalog = mc.ROOT / 'plant_params/huaura_supported'
        expected = {'maize', 'sugarcane', 'avocado', 'asparagus',
                    'mango', 'citrus', 'strawberry'}
        entries = mc.list_crops(catalog)
        self.assertEqual(len(entries), 7)
        self.assertEqual({entry['id'] for entry in entries}, expected)
        self.assertEqual({entry['engine_name'] for entry in entries}, expected)
        self.assertEqual([entry['id'] for entry in mc.select_crops(['strawberry'], catalog)],
                         ['strawberry'])
        with self.assertRaises(ValueError):
            mc.select_crops(['strawberries'], catalog)
        with self.assertRaises(ValueError):
            mc.select_crops(['alfalfa'], catalog)

    def test_complete_catalog_and_invalid_selections(self):
        entries = mc.list_crops()
        self.assertEqual(len(entries), 79)
        self.assertEqual(len({item['id'] for item in entries}), 79)
        self.assertEqual([x['id'] for x in mc.select_crops(['rice', 'potato'])], ['rice', 'potato'])
        for invalid in ([], ['maize', 'maize'], ['../maize'], ['not-a-crop'], 'maize'):
            with self.assertRaises(ValueError):
                mc.select_crops(invalid)

    def test_subpixel_polygon_holes_and_outside_boundary(self):
        affine = from_origin(-77.5, -11, .04, .04)
        parcel = box(-77.499, -11.009, -77.491, -11.001)
        weights, area, support = mc.cell_areas(parcel, (2, 2), affine, 'EPSG:4326')
        self.assertEqual(np.count_nonzero(weights), 1)
        self.assertAlmostEqual(weights.sum() / area, 1)
        self.assertAlmostEqual(support, area)
        hole = box(-77.497, -11.007, -77.493, -11.003)
        weights_hole, area_hole, support_hole = mc.cell_areas(parcel.difference(hole), (2, 2), affine, 'EPSG:4326')
        self.assertLess(area_hole, area)
        self.assertAlmostEqual(weights_hole.sum() / area_hole, 1)
        self.assertAlmostEqual(support_hole, area_hole)
        mc.validate_parcel(parcel, box(-78, -12, -77, -10))
        with self.assertRaises(ValueError):
            mc.validate_parcel(parcel, box(-76, -12, -75, -10))

    def test_diagonal_parcel_uses_one_partition_for_full_area_and_common_support(self):
        parcel = Polygon([(-77.5017, -11.0037), (-77.5071, -10.9939),
                          (-77.5016, -10.996)])
        affine = from_origin(-77.51, -10.99, .0041667, .0041667)
        areas, parcel_area, grid_support = mc.cell_areas(parcel, (5, 5), affine, 'EPSG:4326')
        old_parcel_area = geometry_transform(mc.AREA_PROJECT, parcel).area
        self.assertGreater(grid_support - old_parcel_area, 1.0)
        self.assertEqual(parcel_area, grid_support)
        self.assertAlmostEqual(grid_support, sum(areas.flat))

        values = np.arange(25, dtype=float).reshape(5, 5)
        crop = np.ma.array(values, mask=np.zeros((5, 5), dtype=bool))
        result = mc.compare_crops({'maize': crop}, areas, parcel_area)
        self.assertEqual(result['common_valid_area_m2'], grid_support)
        self.assertEqual(result['parcel_grid_support_area_m2'], grid_support)
        self.assertEqual(result['common_coverage_fraction'], 1.0)
        self.assertAlmostEqual(result['ranking'][0]['mean'],
                               np.average(values[areas > 0], weights=areas[areas > 0]))

    def test_partial_grid_and_nodata_keep_whole_parcel_denominator(self):
        parcel = Polygon([(-77.5017, -11.0037), (-77.5071, -10.9939),
                          (-77.5016, -10.996)])
        affine = from_origin(-77.51, -10.99, .0041667, .0041667)
        areas, parcel_area, grid_support = mc.cell_areas(parcel, (2, 2), affine, 'EPSG:4326')
        self.assertGreater(parcel_area, grid_support)
        crop = np.ma.array(np.full((2, 2), 60.0), mask=np.zeros((2, 2), dtype=bool))
        full_valid = mc.compare_crops({'maize': crop}, areas, parcel_area)
        self.assertEqual(full_valid['common_valid_area_m2'], grid_support)
        self.assertEqual(full_valid['common_coverage_fraction'], grid_support / parcel_area)
        self.assertLess(full_valid['common_coverage_fraction'], 1.0)

        crop.mask[1, 1] = True
        partial_valid = mc.compare_crops({'maize': crop}, areas, parcel_area)
        self.assertLess(partial_valid['common_valid_area_m2'], grid_support)
        self.assertEqual(partial_valid['common_coverage_fraction'],
                         partial_valid['common_valid_area_m2'] / parcel_area)
        self.assertEqual(partial_valid['ranking'][0]['mean'], 60.0)

    def test_degenerate_grid_and_real_support_excess_are_rejected(self):
        parcel = box(-77.5, -11.01, -77.49, -11.0)
        with self.assertRaisesRegex(ValueError, 'aligned north-up'):
            mc.cell_areas(parcel, (2, 2), from_origin(-77.5, -11, 0, .01), 'EPSG:4326')
        crop = np.ma.array([[50.0, 50.0]], mask=[[False, False]])
        with self.assertRaisesRegex(ValueError, 'exceeds parcel area'):
            mc.compare_crops({'maize': crop}, np.array([[6.0, 6.0]]), 10.0)

    def test_zero_is_valid_and_ranking_uses_common_support_with_ties(self):
        weights = np.array([[1., 3., 6.]])
        maize = np.ma.array([[0, 100, -1]], mask=[[False, False, True]])
        rice = np.ma.array([[0, -1, 100]], mask=[[False, True, False]])
        missing = np.ma.masked_all((1, 3))
        summary, _ = mc.score_summary(maize, weights, 10)
        self.assertEqual(summary['mean'], 75)
        self.assertEqual(summary['coverage_fraction'], .4)
        self.assertEqual(summary['zero_suitability_area_m2'], 1)
        result = mc.compare_crops({'maize': maize, 'rice': rice, 'missing': missing}, weights, 10)
        self.assertEqual(result['common_coverage_fraction'], .1)
        self.assertEqual([x['rank'] for x in result['ranking']], [1, 1])
        self.assertEqual([x['mean'] for x in result['ranking']], [0, 0])
        self.assertEqual(result['excluded_without_coverage'], ['missing'])
        disjoint = mc.compare_crops({'maize': maize, 'rice': np.ma.array([[1, 1, 1]], mask=[[True, True, False]])}, weights, 10)
        self.assertEqual(disjoint['ranking'], [])
        self.assertEqual(disjoint['status'], 'no_common_coverage')

    def test_geojson_rejects_multiple_features_invalid_shapes_and_crs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'parcel.json'
            for value in (None, [], {'type': 'FeatureCollection', 'features': None},
                          {'type': 'FeatureCollection', 'features': [None]},
                          {'type': 'FeatureCollection', 'features': []},
                          {'type': 'Point', 'coordinates': [-77.5, -11]},
                          {'type': 'Polygon', 'coordinates': [[[0, 0], [1, 1], [1, 0], [0, 1], [0, 0]]]},
                          {**mapping(box(-77.5, -11, -77.4, -10.9)),
                           'crs': {'type': 'name', 'properties': {'name': 'EPSG:3857'}}}):
                path.write_text(json.dumps(value))
                with self.assertRaises(ValueError):
                    mc.load_geometry(path)

    def test_invalid_scores_are_nodata_in_exported_parcel(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            for name in mc.SCORES:
                with rasterio.open(directory / f'{name}.tif', 'w', driver='GTiff', width=4, height=1,
                                   count=1, dtype='float32', crs='EPSG:4326',
                                   transform=from_origin(-77.5, -11, .04, .04)) as dst:
                    dst.write(np.array([[0, np.nan, 101, -32767]], dtype='float32'), 1)
            summaries, *_ = mc.summarize_outputs(directory, box(-77.5, -11.04, -77.34, -11), directory / 'parcel')
            self.assertEqual(summaries['crop_suitability']['valid_cells'], 1)
            with rasterio.open(directory / 'parcel/crop_suitability.tif') as src:
                self.assertEqual(src.read(1).tolist(), [[0, -1, -1, -1]])

    def test_all_engine_failures_produce_report_without_ranking(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(mc, '_run_engine', side_effect=RuntimeError('Synthetic engine failure')):
                report = mc.run_evaluation(['maize', 'rice'], mc.BOUNDARY, directory)
            self.assertEqual(report['status'], 'failed')
            self.assertEqual(report['comparison']['status'], 'no_successful_crops')
            self.assertEqual(report['comparison']['ranking'], [])
            self.assertEqual(report['comparison']['failed_crops'], ['maize', 'rice'])

    def test_failure_isolated_selection_snapshots_and_outputs(self):
        boundary = mc.load_geometry(mc.BOUNDARY)
        center = boundary.representative_point()
        parcel = box(center.x - .001, center.y - .001, center.x + .001, center.y + .001)
        self.assertTrue(boundary.covers(parcel))
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            geojson = directory / 'parcel.geojson'
            geojson.write_text(json.dumps(mapping(parcel)))
            calls = []

            def engine(config_path, workdir, log_path):
                conf = configparser.ConfigParser()
                conf.read(config_path)
                params = Path(conf['files']['plant_param_dir'])
                self.assertEqual([x.name for x in params.glob('*.inf')], [f'{workdir.name}.inf'])
                self.assertEqual(mc.sha256(params / f'{workdir.name}.inf'), mc.sha256(mc.CATALOG / f'{workdir.name}.inf'))
                calls.append(workdir.name)
                if workdir.name == 'rice':
                    raise RuntimeError('Synthetic engine failure')
                dest = Path(conf['files']['output_dir'] + '_novar') / 'Area_test' / workdir.name
                dest.mkdir(parents=True)
                for name in mc.SCORES:
                    with rasterio.open(dest / f'{name}.tif', 'w', driver='GTiff', width=1, height=1,
                                       count=1, dtype='int16', nodata=-1, crs='EPSG:4326',
                                       transform=from_origin(center.x-.02, center.y+.02, .04, .04)) as dst:
                        dst.write(np.array([[0 if workdir.name == 'maize' else 80]], dtype='int16'), 1)

            with patch.object(mc, '_run_engine', side_effect=engine):
                report = mc.run_evaluation(['maize', 'rice', 'potato'], geojson, directory / 'results')
            self.assertEqual(calls, ['maize', 'rice', 'potato'])
            self.assertEqual(report['status'], 'partial')
            self.assertTrue(report['source_files_unchanged'])
            self.assertEqual(report['comparison']['failed_crops'], ['rice'])
            self.assertFalse(report['comparison']['all_selected_crops_comparable'])
            self.assertEqual(report['comparison']['ranking'][0]['crop_id'], 'potato')
            self.assertEqual([x['status'] for x in report['crops']], ['succeeded', 'failed', 'succeeded'])
            self.assertTrue((Path(report['directory']) / 'parcel.geojson').exists())
            self.assertTrue((Path(report['directory']) / 'potato/parcel/crop_suitability.tif').exists())


if __name__ == '__main__':
    unittest.main()
