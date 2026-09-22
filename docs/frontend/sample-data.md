# Sample data

Everything in `fixtures/` is illustrative contract data. UUIDs, timestamps, crop values, suitability values, and environmental input keys are examples only.

Environmental `input_key` values in fixtures are illustrative logical identifiers. They are not reserved deployment keys and do not select scientific bindings.

## Evaluation request

See `fixtures/evaluation-request.example.json`. Before submitting it:

1. replace project, parcel, and dataset UUIDs with registered resources;
2. select the exact owned `ParcelVersion` and send only its IDs/version in `parcel_reference`;
3. obtain crop identifiers and `scientifically_bound_dataset_versions` from `/api/v1/evaluation-capabilities`;
4. select a bound dataset version and resolve its visible metadata through the dataset endpoints;
5. generate a unique logical environmental `input_key`, for example `environmental-input-1`.

Do not add geometry, CRS, capture time, or `parcel_snapshot` to the evaluation request. The backend resolves and persists those fields from the selected immutable parcel version.

## Polling response

`fixtures/evaluation-status-running.example.json` shows a two-scenario evaluation with one execution complete and one still running. Progress should be calculated from execution counts.

## Final result

`fixtures/evaluation-result-final.example.json` demonstrates the relationship among:

- per-outcome suitability;
- common spatial support;
- `comparable_crops` ranking;
- per-water-regime `scenarios`.

The numeric values are not agronomic recommendations and must not be reused as thresholds or defaults.
