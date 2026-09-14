# CropSuiteLite integration boundary

CropSuiteLite is the existing scientific engine. The backend must preserve it behind an application capability instead of distributing its configuration, paths, process behavior, or scientific rules through controllers and domain objects.

## Intended boundary

`ICropSuitabilityEngine` is the Application port for requesting a verified suitability calculation. `CropSuiteAdapter` is the Infrastructure implementation that translates an approved application request into CropSuiteLite configuration and files, invokes the existing engine, and returns verified result and artifact references.

The names are concrete backend contracts in Agroclimatic Evaluation. Synchronous
Application orchestration, minimal per-crop persistence, and PostgreSQL polling
worker dispatch are now implemented:

```text
ExecuteEvaluation application use case
  -> load and claim a persisted queued Evaluation
  -> ICropSuitabilityEngine.evaluate(one requested crop)
  -> CropSuiteAdapter
  -> existing CropSuiteLite multicrop capability
  -> checked per-crop result
  -> persist one durable outcome and complete Evaluation lifecycle
```

## Mandatory dependency rules

- REST controllers must not call CropSuiteLite directly.
- Domain must not depend on CropSuiteLite, its Python modules, its files, Infrastructure, or HTTP.
- Application depends on a port or capability, not concrete CropSuiteLite internals.
- Infrastructure implements `CropSuiteAdapter` and owns translation of paths, INI configuration, subprocess execution, and engine-specific outputs.
- Long-running execution belongs in the worker, outside the HTTP request process.
- Public requests must select server-approved identifiers and options; they must not supply arbitrary paths or shell fragments.

## Existing PoC capability to preserve

- [`CropSuiteLite/evaluate.py`](../../CropSuiteLite/evaluate.py) is the current CLI entry point for catalog listing and selected-crop evaluation.
- [`CropSuiteLite/src/multicrop.py`](../../CropSuiteLite/src/multicrop.py) provides the blocking `run_evaluation(...)` service that a future worker-side adapter can wrap.
- [`CropSuiteLite/scripts/run_evaluation_engine.py`](../../CropSuiteLite/scripts/run_evaluation_engine.py) is invoked in a separate subprocess for engine isolation.
- [`CropSuiteLite/tests/test_multicrop.py`](../../CropSuiteLite/tests/test_multicrop.py) defines preservation constraints for selection, spatial handling, summaries, failures, and ranking.
- [`CropSuiteLite/docs/multicrop_evaluation.md`](../../CropSuiteLite/docs/multicrop_evaluation.md) documents current usage and verified limits.

The current implementation evaluates crops sequentially, creates an isolated directory and copied parameter file per crop, limits internal engine processes, persists progress after each crop, and lets later crops continue after one fails. Migration must preserve that behavior before considering reuse or parallelism.

## Implemented backend boundary

`application/ports.py` owns immutable `CropSuitabilityRequest`,
`CropSuitabilityResult`, status, summary, failure, and trace contracts together
with `ICropSuitabilityEngine`. A request contains only evaluation identity, one
server-approved crop identifier, and the immutable `ParcelSnapshot`; it contains
no engine paths, ORM types, HTTP types, process handles, or final
`EnvironmentalInputManifest`.

`infrastructure/cropsuite_adapter.py` implements the port. Infrastructure receives
the CropSuiteLite source root, a dedicated execution-workspace root, an explicit
scientific Python executable, optional server-side configuration/catalog paths,
and the internal process limit. The workspace is rejected if it is inside the
scientific source tree.

The adapter serializes Polygon or MultiPolygon snapshot geometry into that
workspace and launches the configured scientific Python interpreter in a separate
process. That process imports and calls the existing
`src.multicrop.run_evaluation(...)` capability with a singleton crop list.
CropSuiteLite therefore executes with its own scientific dependency environment,
while its existing per-crop isolation through
`scripts/run_evaluation_engine.py` remains unchanged. The adapter adds no crop
parallelism or queue semantics.

The adapter validates the selected crop, per-crop outcome, expected suitability
summary, timestamps, and reproducibility guard before returning. Per-crop
`failed`, `no_coverage`, and `succeeded` are separate. A valid suitability score
of zero remains `succeeded`; `no_coverage` retains a summary with no valid cells
and no mean. Missing or malformed engine output raises an explicit boundary
error rather than becoming a scientific score.

Current trace output includes the CropSuiteLite identifier, opaque PoC execution
reference, timestamps, elapsed time, preserved execution mode, parcel checksum,
available crop-parameter and effective-configuration checksums, and the
source-files-unchanged result. A durable engine commit/version, dependency
versions, dataset manifest, full evidence/artifact model, and retention policy
are not reliably available at this boundary and are explicitly deferred.

## Application orchestration and worker responsibilities

`AgroclimaticEvaluationExecutionService` now loads and claims a queued
evaluation, persists active lifecycle transitions, invokes the port once per
requested crop in deterministic order, persists each checked outcome, and
finishes the aggregate. An explicit per-crop failure remains an outcome and does
not make the orchestration fail; a boundary exception stops the sequence and
persists overall failure.

The PostgreSQL polling worker calls this use case and relies on its optimistic
claiming behavior. Future increments may add retry policy, cancellation, exact
environmental input resolution, artifact retention, and publication. Shared
inputs must remain immutable and a global output directory must not be used.

## Scientific preservation constraints

The adapter must not change crop parameter files, interpolation, precipitation units, masks, nodata handling, score combination, source grids, or scientific thresholds. A valid low or zero score is a possible result. Nodata remains absence of usable information. Parcel clipping must not be described as increasing the approximately 4.6 km source resolution.

## Future work not yet implemented

The repository provides the reliable current per-crop summary and trace fields
through read-only status, result, and evidence queries. HTTP omits raw diagnostic
messages and the opaque execution reference. Application publishes a finalized
result contract for future Decision Support use, but the final
`SuitabilityEvidence`/artifact model, retries, cancellation, quotas,
authorization, shared climate-preparation cache, compatible-run reuse, and
retention policy remain deferred. HTTP request creation remains separate from
scientific execution. Reuse still requires a manifest key covering engine,
parameters, inputs, scenario, management, scientific options, spatial scope, and
aggregation method.

## Implemented worker host

A separate backend worker process now polls PostgreSQL for queued evaluations
and delegates execution to `AgroclimaticEvaluationExecutionService`. The worker
composition root constructs the Infrastructure-owned `CropSuiteAdapter`; Domain
and Application remain unaware of CropSuiteLite filesystem or process details.

PostgreSQL remains the current durable source of work. Multiple worker processes
may discover the same evaluation, while the existing optimistic
`queued -> preparing` transition is the authoritative claim. Scientific
execution does not run inside a database transaction.

A crashed worker may leave an evaluation active. The current recovery mechanism
is explicit fail-only recovery to `failed`; heartbeats, leases, automatic stale
detection, retries, requeue and cancellation remain deferred.

## Source

See sections 11 through 14 and 22 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx).
