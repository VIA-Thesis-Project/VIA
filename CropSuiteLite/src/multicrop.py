"""Isolated, selected-crop evaluations and area-weighted parcel comparisons.

The scientific engine evaluates its existing environmental grid. Parcel summaries
intersect that grid without resampling or pretending to increase its resolution.
"""
import configparser
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np
from pyproj import CRS, Transformer
import rasterio
from rasterio.windows import Window
from shapely.geometry import Polygon, mapping, shape
from shapely.ops import transform

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / 'config_access_esm1_5_ssp126_2021_2040.ini'
CATALOG = ROOT / 'plant_params/available'
BOUNDARY = ROOT.parent / 'data/huaura/boundary/huaura_province.geojson'
SCORES = ('crop_suitability', 'climate_suitability', 'soil_suitability')
SAFE_ID = re.compile(r'^[A-Za-z0-9_-]+$')
AREA_PROJECT = Transformer.from_crs('EPSG:4326', 'EPSG:6933', always_xy=True).transform


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path = Path(path)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False), encoding='utf-8')
    temporary.replace(path)


def list_crops(catalog=CATALOG):
    """IDs are filenames, not translated labels or user-supplied filesystem paths."""
    entries = []
    for path in sorted(Path(catalog).glob('*.inf')):
        if not SAFE_ID.fullmatch(path.stem):
            raise ValueError(f'Unsafe catalog identifier: {path.name}')
        values = dict(line.split('=', 1) for line in path.read_text().splitlines() if '=' in line)
        values = {k.strip(): v.strip() for k, v in values.items()}
        name = values.get('name', '')
        if not SAFE_ID.fullmatch(name):
            raise ValueError(f'Invalid engine crop name in {path.name}')
        entries.append({'id': path.stem, 'engine_name': name,
                        'growing_cycle_days': float(values['growing_cycle']),
                        'parameter_sha256': sha256(path)})
    return entries


def select_crops(ids, catalog=CATALOG):
    if isinstance(ids, str) or not ids:
        raise ValueError('Select at least one crop identifier.')
    if len(ids) != len(set(ids)):
        raise ValueError('The crop selection contains duplicates.')
    available = {entry['id']: entry for entry in list_crops(catalog)}
    unknown = [item for item in ids if item not in available]
    if unknown:
        raise ValueError(f'Unknown crop identifiers: {", ".join(unknown)}')
    return [available[item] for item in ids]


def load_geometry(path):
    path = Path(path)
    if path.stat().st_size > 5_000_000:
        raise ValueError('GeoJSON exceeds the 5 MB limit.')
    value = json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(value, dict):
        raise ValueError('GeoJSON must be an object.')
    declared = value.get('crs')
    if declared:
        crs = CRS.from_user_input(declared.get('properties', {}).get('name', ''))
        if not crs.equals(CRS.from_epsg(4326), ignore_axis_order=True):
            raise ValueError('GeoJSON coordinates must be WGS84 longitude/latitude.')
    if value.get('type') == 'FeatureCollection':
        features = value.get('features')
        if not isinstance(features, list) or len(features) != 1 or not isinstance(features[0], dict):
            raise ValueError('Submit exactly one parcel feature per evaluation.')
        value = features[0]
    if value.get('type') == 'Feature':
        value = value.get('geometry')
    if not isinstance(value, dict) or value.get('type') not in ('Polygon', 'MultiPolygon'):
        raise ValueError('A Polygon or MultiPolygon is required.')
    geometry = shape(value)
    if geometry.is_empty or not geometry.is_valid or not np.isfinite(geometry.bounds).all():
        raise ValueError('The parcel geometry is empty or invalid.')
    xmin, ymin, xmax, ymax = geometry.bounds
    if not (-180 <= xmin <= xmax <= 180 and -90 <= ymin <= ymax <= 90):
        raise ValueError('Coordinates must be longitude/latitude.')
    return geometry


def validate_parcel(parcel, boundary):
    if not boundary.covers(parcel):
        raise ValueError('The complete parcel must be inside Huaura.')
    if transform(AREA_PROJECT, parcel).area <= 0:
        raise ValueError('The parcel must have positive area.')


def cell_areas(geometry, shape_, affine, crs):
    """Intersection areas in the WGS84 equal-area projection EPSG:6933."""
    if CRS.from_user_input(crs).to_epsg() != 4326 or affine.b != 0 or affine.d != 0:
        raise ValueError('Expected the aligned north-up EPSG:4326 Huaura grid.')
    parcel_area = transform(AREA_PROJECT, geometry).area
    areas = np.zeros(shape_, dtype=np.float64)
    for row in range(shape_[0]):
        for col in range(shape_[1]):
            cell = Polygon([affine * (col, row), affine * (col + 1, row),
                            affine * (col + 1, row + 1), affine * (col, row + 1)])
            intersection = geometry.intersection(cell)
            if not intersection.is_empty:
                areas[row, col] = transform(AREA_PROJECT, intersection).area
    return areas, parcel_area


def score_summary(data, areas, parcel_area):
    values = np.asarray(data.data, dtype=float)
    valid = (~np.ma.getmaskarray(data) & np.isfinite(values)
             & (values >= 0) & (values <= 100) & (areas > 0))
    area = float(areas[valid].sum())
    return {'mean': float(np.average(values[valid], weights=areas[valid])) if area else None,
            'minimum': float(values[valid].min()) if area else None,
            'maximum': float(values[valid].max()) if area else None,
            'valid_cells': int(valid.sum()), 'valid_area_m2': area,
            'coverage_fraction': min(area / parcel_area, 1.0),
            'zero_suitability_area_m2': float(areas[valid & (values == 0)].sum())}, valid


def compare_crops(arrays, areas, parcel_area):
    """Rank only on identical valid support; no-data crops receive no rank."""
    if not arrays:
        return {'status': 'no_successful_crops', 'ranking': [], 'excluded_without_coverage': []}
    valid = {key: score_summary(data, areas, parcel_area)[1] for key, data in arrays.items()}
    usable = [key for key, mask in valid.items() if mask.any()]
    excluded = [key for key in arrays if key not in usable]
    common = np.logical_and.reduce([valid[key] for key in usable]) if usable else np.zeros(areas.shape, dtype=bool)
    common_area = float(areas[common].sum())
    ranking = []
    if common_area:
        ranking = [{'crop_id': key, 'mean': float(np.average(arrays[key].data[common], weights=areas[common]))}
                   for key in usable]
        ranking.sort(key=lambda entry: (-entry['mean'], entry['crop_id']))
        previous = None
        rank = 0
        for index, entry in enumerate(ranking, 1):
            if previous is None or not np.isclose(entry['mean'], previous, rtol=0, atol=1e-9):
                rank = index
            entry['rank'] = rank
            previous = entry['mean']
    return {'status': 'comparable' if common_area else 'no_common_coverage',
            'method': 'area_weighted_mean_on_common_valid_cells',
            'area_crs': 'EPSG:6933', 'common_valid_area_m2': common_area,
            'common_coverage_fraction': min(common_area / parcel_area, 1.0),
            'ranking': ranking, 'excluded_without_coverage': excluded}


def read_config(source):
    config = configparser.ConfigParser(interpolation=None)
    if not config.read(source):
        raise ValueError(f'Cannot read configuration: {source}')
    base = Path(source).resolve().parent
    for key, value in config['files'].items():
        config['files'][key] = str((base / value.replace('\\', '/')).resolve())
    for section in config.sections():
        if section.startswith('parameters.'):
            config[section]['data_directory'] = str((base / config[section]['data_directory'].replace('\\', '/')).resolve())
    return config


def input_fingerprints(config, source_config, catalog, selected):
    paths = {Path(source_config), Path(config['files']['fine_dem']), Path(config['files']['land_sea_mask']),
             Path(config['files']['texture_classes']), BOUNDARY}
    paths.update(Path(config['files']['climate_data_dir']).rglob('*.tif'))
    paths.update(Path(config['files']['climate_data_dir']).rglob('*.nc'))
    paths.update(Path(catalog) / f'{crop["id"]}.inf' for crop in selected)
    for section in config.sections():
        if section.startswith('parameters.'):
            paths.update(Path(config[section]['data_directory']).glob('*.tif'))
    return {str(path.resolve()): sha256(path) for path in sorted(paths)}


def _run_engine(config_path, workdir, log_path):
    # Separate processes isolate engine globals, temporary directories and exits.
    with Path(log_path).open('w', encoding='utf-8') as log:
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/run_evaluation_engine.py'), str(config_path)],
                                cwd=workdir, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                                check=False)
    if result.returncode:
        raise RuntimeError(f'CropSuiteLite exited with code {result.returncode}; see engine.log.')


def summarize_outputs(output_folder, geometry, target):
    target.mkdir()
    summaries = {}
    template = None
    crop_data = None
    for name in SCORES:
        with rasterio.open(output_folder / f'{name}.tif') as src:
            data = src.read(1, masked=True)
            signature = (src.shape, src.transform, src.crs)
            if template is None:
                template = signature
                areas, parcel_area = cell_areas(geometry, src.shape, src.transform, src.crs)
                if not np.any(areas > 0):
                    raise ValueError('The parcel does not intersect the output grid.')
            elif signature != template:
                raise ValueError('Crop output grids do not match.')
            summaries[name], valid = score_summary(data, areas, parcel_area)
            if name == 'crop_suitability':
                crop_data = data.copy()
            rows, cols = np.nonzero(areas > 0)
            window = Window(int(cols.min()), int(rows.min()), int(cols.max() - cols.min() + 1), int(rows.max() - rows.min() + 1))
            masked = np.where(valid, data.data, -1).astype(np.int16)
            subset = masked[window.toslices()]
            profile = src.profile.copy()
            profile.update(driver='GTiff', width=int(window.width), height=int(window.height),
                           count=1, dtype='int16', nodata=-1, transform=src.window_transform(window))
            with rasterio.open(target / f'{name}.tif', 'w', **profile) as dst:
                dst.write(subset, 1)
    return summaries, crop_data, areas, parcel_area, template


def run_evaluation(crops, parcel_path, output_root=None, source_config=DEFAULT_CONFIG,
                   catalog=CATALOG, max_workers=2, progress=None):
    """Run one parcel request with N selected crops, sequentially and in isolation.

    Returns a JSON-serializable result and writes evaluation.json after each crop.
    Engine failures are per-crop; invalid requests fail before creating a job.
    """
    selected = select_crops(crops, catalog)
    if isinstance(max_workers, bool) or not isinstance(max_workers, int) or max_workers < 1:
        raise ValueError('max_workers must be a positive integer.')
    parcel = load_geometry(parcel_path)
    validate_parcel(parcel, load_geometry(BOUNDARY))
    config = read_config(source_config)
    sources = input_fingerprints(config, source_config, catalog, selected)
    output_root = Path(output_root or ROOT / 'results/evaluations').resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    job = Path(tempfile.mkdtemp(prefix='evaluation_', dir=output_root))
    snapshot = {'type': 'Feature', 'properties': {}, 'geometry': mapping(parcel)}
    write_json(job / 'parcel.geojson', snapshot)
    code = [ROOT / 'CropSuite.py', ROOT / 'scripts/run_evaluation_engine.py', *sorted((ROOT / 'src').glob('*.py'))]
    report = {'schema_version': 1, 'evaluation_id': job.name, 'directory': str(job),
              'created_at': datetime.now(timezone.utc).isoformat(), 'status': 'running',
              'selected_crops': crops, 'execution': 'sequential_isolated_processes',
              'scope': 'regional_grid_with_parcel_intersection',
              'score_scale': [0, 100], 'parcel_sha256': sha256(job / 'parcel.geojson'),
              'source_sha256': sources, 'engine_sha256': {str(p.relative_to(ROOT)): sha256(p) for p in code},
              'summary_method': 'intersection_area_weighting_EPSG6933',
              'result_variant': 'novar', 'crops': [],
              'resolution_notice': 'Parcel clipping preserves source cell values; it does not add spatial detail.'}
    write_json(job / 'evaluation.json', report)
    arrays = {}
    grid = None
    areas = None
    parcel_area = transform(AREA_PROJECT, parcel).area
    for entry in selected:
        crop_id = entry['id']
        folder = job / crop_id
        folder.mkdir()
        params = folder / 'plant_params'
        params.mkdir()
        src = Path(catalog) / f'{crop_id}.inf'
        shutil.copyfile(src, params / src.name)
        crop_config = read_config(source_config)
        crop_config['files']['plant_param_dir'] = str(params)
        crop_config['files']['output_dir'] = str(folder / 'simulation')
        crop_config['options'].update({'max_workers': str(max_workers), 'no_tiles': '1',
                                       'output_format': 'geotiff', 'remove_downscaled_climate': 'n'})
        crop_config['membershipfunctions']['plot_for_each_crop'] = 'n'
        config_path = folder / 'config.ini'
        with config_path.open('w') as handle:
            crop_config.write(handle)
        outcome = {**entry, 'status': 'running', 'engine_log': str(folder / 'engine.log'),
                   'config_sha256': sha256(config_path)}
        report['crops'].append(outcome)
        write_json(job / 'evaluation.json', report)
        if progress:
            progress(crop_id, 'running')
        started = time.monotonic()
        try:
            _run_engine(config_path, folder, folder / 'engine.log')
            outputs = list((folder / 'simulation_novar').glob(f'Area_*/{entry["engine_name"]}/crop_suitability.tif'))
            if len(outputs) != 1:
                raise RuntimeError('Expected exactly one completed output grid for this crop.')
            summaries, data, crop_areas, parcel_area, signature = summarize_outputs(outputs[0].parent, parcel, folder / 'parcel')
            if grid is not None and signature != grid:
                raise ValueError('Different crop grids cannot be ranked together.')
            grid, areas = signature, crop_areas
            arrays[crop_id] = data
            outcome.update(status='succeeded' if summaries['crop_suitability']['valid_cells'] else 'no_coverage',
                           scores=summaries, result_directory=str(outputs[0].parent),
                           parcel_directory=str(folder / 'parcel'),
                           artifact_sha256={str(p.relative_to(folder)): sha256(p)
                                            for p in sorted((folder / 'parcel').glob('*.tif'))})
        except Exception as error:
            outcome.update(status='failed', error=f'{type(error).__name__}: {error}')
        outcome['elapsed_seconds'] = round(time.monotonic() - started, 3)
        write_json(job / 'evaluation.json', report)
        if progress:
            progress(crop_id, outcome['status'])
    report['comparison'] = compare_crops(arrays, areas, parcel_area)
    report['parcel_area_m2'] = parcel_area
    report['source_files_unchanged'] = all(Path(path).is_file() and sha256(path) == value for path, value in sources.items())
    failures = sum(entry['status'] == 'failed' for entry in report['crops'])
    report['status'] = 'failed' if failures == len(selected) else ('partial' if failures else 'completed')
    if not report['source_files_unchanged']:
        report.update(status='failed', error='Input files changed during the evaluation; results are not reproducible.')
        report['comparison']['ranking'] = []
    report['comparison']['failed_crops'] = [entry['id'] for entry in report['crops'] if entry['status'] == 'failed']
    report['comparison']['all_selected_crops_comparable'] = len(report['comparison']['ranking']) == len(selected)
    report['finished_at'] = datetime.now(timezone.utc).isoformat()
    write_json(job / 'evaluation.json', report)
    return report
