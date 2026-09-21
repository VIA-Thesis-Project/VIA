# Scientific result semantics

This page contains UI-critical interpretation rules.

## Suitability scale

Suitability `mean`, `minimum`, and `maximum` are on a `0..100` scale when present. A value of `0` is a valid suitability result. It must not be rendered as missing data.

`suitability` itself can be `null` for an outcome that does not have a usable suitability summary. Outcome status explains whether the execution `succeeded`, had `no_coverage`, or `failed`.

## Coverage and no-data

`coverage_fraction` is a fraction in `0..1` of parcel area with valid scientific cells. No-data cells are excluded from valid coverage.

These cases are different:

| State | Meaning |
| --- | --- |
| `mean = 0`, `coverage_fraction > 0` | valid analyzed cells produced zero suitability |
| `status = no_coverage` | no usable spatial support for that crop/scenario |
| `suitability = null` | no usable summary is available for the outcome |
| `coverage_fraction < 1` | part of the parcel lacked valid scientific cells |

Never coerce `null`, no-data, or `no_coverage` to zero.

## Cross-crop ranking

Use `comparable_crops` to rank crops. It is computed on common valid spatial support and publishes a rank and mean for that comparable support.

Do not rank the raw `outcomes[*].suitability.mean` values across crops. Those summaries can cover different cells/areas.

`common_support.status` can be:

- `comparable`;
- `no_common_coverage`;
- `no_successful_crops`.

When common support is not comparable, suppress or clearly disable a comparative ranking.

## Water regimes

`rainfed` and `irrigated` are separate scientific scenarios. Results from one must not be merged into the other.

An `irrigated` scenario means the scientific configuration was evaluated as irrigated. It does not prove that water rights, water supply, pumps, canals, cost, or irrigation infrastructure exist on the parcel.

## Limiting factors

Limitation evidence can be `available`, `partial`, or `unavailable`. Each factor contains `affected_fraction` in `0..1`, plus affected cells/area and a `dominant` flag.

`affected_fraction` describes the fraction of valid analyzed area affected by the factor. It is not the same as missing coverage and must not be added to no-data percentages.

## Scientific trace

Evidence includes safe trace metadata such as engine identifier, timing, execution mode, parcel/parameter/configuration hashes, and source hashes. Treat hashes as traceability data. Do not turn them into download paths or infer local storage locations.
