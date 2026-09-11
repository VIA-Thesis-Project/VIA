"""Public CLI for crop catalog discovery and selected-crop parcel evaluations."""
import argparse
import json
from pathlib import Path
import sys

from src.multicrop import BOUNDARY, DEFAULT_CONFIG, list_crops, run_evaluation


def main(argv=None):
    parser = argparse.ArgumentParser(description='Evaluate selected crops for the same Huaura parcel.')
    parser.add_argument('--list-crops', action='store_true', help='Print the complete catalog as JSON.')
    parser.add_argument('--crops', nargs='+', help='Catalog IDs, for example maize potato rice.')
    area = parser.add_mutually_exclusive_group()
    area.add_argument('--parcel', type=Path, help='Single Polygon/MultiPolygon GeoJSON inside Huaura.')
    area.add_argument('--whole-huaura', action='store_true', help='Explicitly assess the province boundary, for diagnostics.')
    parser.add_argument('--output', type=Path, help='Parent folder for a new isolated evaluation.')
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG)
    parser.add_argument('--max-workers', type=int, default=2, help='Engine processes per crop; crops run sequentially.')
    args = parser.parse_args(argv)
    if args.list_crops:
        print(json.dumps(list_crops(), ensure_ascii=False, indent=2))
        return 0
    if not args.crops or not (args.parcel or args.whole_huaura):
        parser.error('Provide --crops and either --parcel or --whole-huaura.')
    try:
        report = run_evaluation(args.crops, args.parcel or BOUNDARY, args.output, args.config,
                                max_workers=args.max_workers,
                                progress=lambda crop, status: print(f'{crop}: {status}', flush=True))
    except (ValueError, OSError) as error:
        parser.exit(2, f'{error}\n')
    print(f'Report: {Path(report["directory"]) / "evaluation.json"}')
    print(json.dumps({'status': report['status'], 'comparison': report['comparison']}, indent=2))
    return 0 if report['status'] == 'completed' else 1


if __name__ == '__main__':
    sys.exit(main())
