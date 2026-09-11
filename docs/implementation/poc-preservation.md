# CropSuiteLite PoC preservation contract

The architecture migration must wrap and integrate the validated CropSuiteLite behavior without rewriting the scientific engine. This inventory describes what exists now and how future backend work should treat it. It does not claim agronomic validation beyond the repository evidence.

## Classification meanings

- **Preserve unchanged:** behavior or scientific semantics are a regression constraint.
- **Wrap behind adapter:** keep the behavior while hiding engine-specific details behind `ICropSuitabilityEngine` and `CropSuiteAdapter`.
- **Move responsibility later:** the PoC performs the work locally, but a future bounded context or infrastructure service should own the application responsibility without changing the calculation.
- **Candidate for future optimization:** consider only after compatibility, reproducibility, tests, and measured benefit are established.

## Entry points and execution

| Concern | Classification | Preservation requirement |
|---|---|---|
| `CropSuiteLite/evaluate.py` | Wrap behind adapter | Preserve catalog discovery, validated request selection, parcel/whole-Huaura modes, exit semantics, and delegation to the existing multicrop capability. A public controller must not invoke this CLI directly. |
| `CropSuiteLite/src/multicrop.py` | Wrap behind adapter | Preserve the blocking service behavior as the initial engine capability used by a worker-side adapter. Do not turn it into HTTP or move its engine details into Domain. |
| Sequential crop execution | Preserve unchanged | Keep selected crops in request order, one crop at a time. |
| Per-crop isolated subprocess and work directory | Preserve unchanged | Keep copied crop parameters, configuration, logs, temporaries, and outputs isolated so globals, exits, and paths cannot collide. |
| Limited internal processes | Preserve unchanged | Keep `max_workers` as a positive server-controlled limit for the engine within one crop. Queue concurrency is a separate future control. |
| Independent crop failures | Preserve unchanged | A failed crop records its failure and later crops continue. Preserve `partial`, failed-crop reporting, and successful artifacts. |
| Durable scheduling, retries, cancellation, and polling | Move responsibility later | These do not exist in the PoC. Future Application/Infrastructure and the worker must add them without changing the scientific calculation. |
| Shared climate preparation or result reuse | Candidate for future optimization | Currently every crop prepares its own derived climate files. Reuse requires an immutable compatibility key and must preserve isolated evidence. |

## Inputs, catalog, and spatial behavior

| Concern | Classification | Preservation requirement |
|---|---|---|
| Crop catalog | Preserve unchanged | Keep the 79 file-backed identifiers and variants, safe identifier validation, selected-order behavior, rejection of empty/duplicate/unknown selections, engine names, growing cycles, and parameter hashes. Catalog availability is not proof that all entries are agronomically validated. |
| Crop parameter files and scientific configuration | Preserve unchanged | Do not rewrite `.inf` files, `maize.inf`, membership functions, thresholds, scenarios, management rules, or scientific options merely to improve scores or satisfy software tests. |
| GeoJSON forms | Preserve unchanged | Accept one Polygon or MultiPolygon in WGS84 as a geometry, Feature, or single-feature FeatureCollection; preserve validation of object shape, CRS, finite bounds, topology, and file-size limit. |
| Huaura validation | Preserve unchanged | Require the complete parcel to be covered by the Huaura boundary and to have positive area. Continue distinguishing provincial containment from environmental-data coverage. |
| Subpixel parcels and holes | Preserve unchanged | Include intersecting cells even when the parcel does not contain their centers; calculate only actual intersection area, including holes. |
| Source grid and clipping | Preserve unchanged | Preserve source cell values and resolution. Parcel raster subsets may retain complete intersecting edge cells, while summaries use only the area inside the parcel. Do not claim added spatial detail. |
| Parcel geometry versioning | Move responsibility later | The PoC snapshots submitted geometry locally. Farm Management will own current ParcelVersion; Evaluation must retain the exact `ParcelSnapshot` used historically. |
| Pre-execution coverage service | Move responsibility later | Environmental Information will expose versioned compatibility and coverage. It must preserve the engine's validity semantics and must not infer coverage solely from being inside Huaura. |

## Scientific calculations and missing data

| Concern | Classification | Preservation requirement |
|---|---|---|
| Environmental and precipitation regressions | Preserve unchanged | Keep tests for negative/zero/missing temperature, coastal coverage, precipitation quantization, NumPy/xarray equivalence, slope coverage, and mask restoration. |
| Precipitation units | Preserve unchanged | Downcaler's downscaled precipitation remains stored in tenths of millimetres and is converted consistently for membership and sowing rules. Do not change factors during backend integration. |
| Interpolation and masks | Preserve unchanged | Missing source coverage must not be diluted, extrapolated, or treated as dry/cold observations. Destination ocean and original coverage remain masked. |
| Zero versus nodata | Preserve unchanged | Suitability `0` is a valid score and participates in summaries. Nodata, NaN, sentinels, and values outside 0–100 are unavailable and excluded; exported invalid parcel cells remain nodata `-1`. |
| Soil gaps | Preserve unchanged | Do not fill original missing soil values or invent crop results. Empty valid sets remain nodata. |
| Score scale and coverage scale | Preserve unchanged | Suitability uses 0–100; coverage uses 0–1. Do not mix them or interpret ranking as suitability magnitude. |
| Scientific evidence in application storage | Move responsibility later | Persist units, versions, sources, methods, factors, and missingness outside the engine while preserving the engine outputs. Audit history is separate from scientific evidence. |

## Summaries, comparison, and evidence

| Concern | Classification | Preservation requirement |
|---|---|---|
| Parcel summaries | Preserve unchanged | For crop, climate, and soil suitability, retain intersection-area-weighted mean, minimum, maximum, valid cell count, valid area, coverage fraction, and zero-suitability area. Areas use EPSG:6933. |
| Common-support ranking | Preserve unchanged | Rank `crop_suitability` only on identical common valid area among crops with coverage; sort descending, preserve ties, publish common coverage, and exclude failed/no-coverage crops explicitly. No common area means no ranking. |
| Result interpretation | Preserve unchanged | A higher rank does not establish profitability or agronomic recommendation. A low or zero valid result must not be altered. |
| Input and code fingerprints | Preserve unchanged | Retain hashes of source configuration, environmental inputs, selected crop parameters, engine code, effective per-crop configuration, parcel snapshot, and exported artifacts where the PoC currently records them. |
| Local `evaluation.json` manifest | Wrap behind adapter | Preserve incremental per-crop writes, statuses, timestamps, execution mode, score scale, summary method, resolution notice, paths/references, and the source-files-unchanged guard. Map to persistent backend records and public DTOs without exposing internal paths. |
| Complete dependency/environment identity | Move responsibility later | Add engine commit/version and relevant dependency versions to durable scientific evidence; do not pretend the current local manifest is a complete application audit. |
| Artifact retention and deduplication | Candidate for future optimization | Define retention and compatible sharing only after checksums, ownership, backup, and reproducibility requirements are settled. |

## Tests that remain authoritative

- [`CropSuiteLite/tests/test_multicrop.py`](../../CropSuiteLite/tests/test_multicrop.py): catalog and request validation, spatial intersection, zero/nodata, common support, isolated failures, snapshots, and artifacts.
- [`CropSuiteLite/tests/test_environmental_coverage.py`](../../CropSuiteLite/tests/test_environmental_coverage.py): temperature, slope, climate coverage, NumPy/xarray parity, and missing-data exclusion.
- [`CropSuiteLite/tests/test_precipitation_units.py`](../../CropSuiteLite/tests/test_precipitation_units.py): tenths-of-millimetre storage and membership-unit consistency.
- [`CropSuiteLite/tests/test_precipitation_coast.py`](../../CropSuiteLite/tests/test_precipitation_coast.py): coastal masks, legitimate zero rainfall, resizing, and nodata.
- [`CropSuiteLite/tests/test_huaura_entrypoint.py`](../../CropSuiteLite/tests/test_huaura_entrypoint.py): the reviewed Huaura configuration runs without regenerating crop parameters.

The source document reports 22 automated tests and real technical runs for maize, potato, and rice. These establish regression evidence for the integration flow, not field validation, profitability, or validation of the remaining catalog.

## Migration gate

Before replacing any current behavior, demonstrate equivalence through the existing tests plus adapter-level tests for inputs, statuses, evidence, and artifacts. Changes to crop parameters, datasets, interpolation, units, masks, nodata, scoring, or GeoJSON behavior require an explicit scientific decision outside ordinary backend restructuring.

## Source

See sections 2, 11 through 15, 18, and 22 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx), [`CropSuiteLite/docs/multicrop_evaluation.md`](../../CropSuiteLite/docs/multicrop_evaluation.md), and [`CropSuiteLite/docs/huaura_environment_correction.md`](../../CropSuiteLite/docs/huaura_environment_correction.md).
