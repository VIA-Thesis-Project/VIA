# CropSuiteLite integration boundary

CropSuiteLite is the existing scientific engine. The backend must preserve it behind an application capability instead of distributing its configuration, paths, process behavior, or scientific rules through controllers and domain objects.

## Intended boundary

`ICropSuitabilityEngine` is the Application port for requesting a verified suitability calculation. `CropSuiteAdapter` is the Infrastructure implementation that translates an approved application request into CropSuiteLite configuration and files, invokes the existing engine, and returns verified result and artifact references.

The names express the intended architecture; no concrete backend interface exists yet. Any signature below is illustrative pseudocode, not a current Python API:

```text
Application use case
  -> ICropSuitabilityEngine.evaluate(verified input references)
  -> CropSuiteAdapter
  -> existing CropSuiteLite multicrop capability
  -> verified result and evidence references
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

## Worker responsibilities

The future worker should load a persisted evaluation, verify its transition, create isolated work storage, resolve exact dataset/parameter/engine versions, call the port, verify expected artifacts and grid compatibility, summarize the parcel, persist per-crop outcomes and evidence, and publish a final state. It must treat shared inputs as immutable and avoid a global output directory.

## Scientific preservation constraints

The adapter must not change crop parameter files, interpolation, precipitation units, masks, nodata handling, score combination, source grids, or scientific thresholds. A valid low or zero score is a possible result. Nodata remains absence of usable information. Parcel clipping must not be described as increasing the approximately 4.6 km source resolution.

## Future work not yet implemented

The repository does not yet provide a durable queue, retries, recovery, cancellation, quotas, API authorization, database persistence, shared climate-preparation cache, compatible-run reuse, or retention policy. Reuse requires a manifest key covering engine, parameters, inputs, scenario, management, scientific options, spatial scope, and aggregation method. The distinction between a reusable `ScientificRun` and a parcel-specific `ParcelAssessment` is a proposed model, not current code.

## Source

See sections 11 through 14 and 22 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx).
