# Target evaluation flow

The target flow accepts a short HTTP request, records enough immutable context to
reproduce the evaluation, and delegates the long calculation to a recoverable
worker. The current execution increment implements the worker-callable
Application orchestration synchronously, but does not connect it to HTTP or a
queue.

## Request to result

```text
POST evaluation request
  -> authenticate and authorize project/parcel access
  -> resolve the requested ParcelVersion
  -> check Huaura scope and environmental coverage/data compatibility
  -> create an immutable ParcelSnapshot
  -> create and persist the Evaluation with crop and configuration references
  -> schedule a recoverable, idempotent job
  -> return an evaluation identifier for polling
  -> worker claims the job and resolves exact input versions
  -> CropSuiteAdapter invokes CropSuiteLite through ICropSuitabilityEngine
  -> validate outputs, units, grids, masks, values, and expected artifacts
  -> summarize the parcel and compare crops on common valid support
  -> persist result, evidence, artifact references, checksums, and final state
  -> GET polling/query endpoints return progress, result, and evidence
```

Authorization must precede calculation. A registered evaluation and its queue publication must be recoverable; an outbox is one proposed mechanism, not an implemented or settled choice. Durable results belong in the database and artifact storage, not only in the broker.

## Proposed future API states

| State | Meaning |
|---|---|
| `Queued` | Accepted and awaiting execution. |
| `Preparing` | Resolving exact inputs and preparing isolated work. |
| `Running` | CropSuiteLite is executing. |
| `Summarizing` | Outputs are being verified and reduced to parcel results. |
| `Succeeded` | Verified results and evidence are available. |
| `Failed` | Execution ended with an identified failure. |
| `Cancelled` | Cancellation completed and resources were released. |

Cancellation is proposed. It must not be reported as complete while an unmanaged scientific process continues.

## Implemented synchronous orchestration

`AgroclimaticEvaluationExecutionService` loads an already-persisted queued
evaluation and claims it with an optimistic `queued -> preparing` transition. It
then persists `preparing -> running`, evaluates requested crops sequentially
through `ICropSuitabilityEngine`, and commits one same-context durable
`crop_outcomes` row after each returned result. Once every requested crop has an
outcome it persists `running -> summarizing -> succeeded`.

Each repository call opens a short transaction; the blocking scientific call is
never enclosed in a database transaction. A future worker can call this same
Application use case without changing its semantics.

Returned per-crop `failed` and `no_coverage` values are completed scientific
outcomes and do not abort later crops. A valid score of zero remains `succeeded`.
Overall `succeeded` means every requested crop was attempted and durably reported,
not that every per-crop status succeeded. Boundary or other orchestration
exceptions stop remaining crops and persist overall `failed` with a minimal
reason; they do not fabricate a crop outcome.

Request creation remains request creation only. There is no HTTP run-now
endpoint, broker, worker, retry, or cancellation mechanism in this increment.

## Current PoC states and required mapping

The current local manifest uses request states `running`, `completed`, `partial`, and `failed`. Per-crop states are `running`, `succeeded`, `no_coverage`, and `failed`. A failed crop does not stop the others. Invalid requests fail before a job directory is created.

The future API requires an explicit mapping rather than renaming these values implicitly. In particular:

- PoC `partial` has no direct equivalent in the proposed top-level list unless the future result model represents a succeeded evaluation with incomplete per-crop outcomes or adds another state.
- Per-crop `no_coverage` is an information-availability outcome, not process failure and not suitability zero.
- `Cancelled`, `Queued`, `Preparing`, and `Summarizing` do not exist in the current PoC.
- `completed` does not guarantee that every crop has usable coverage; clients must inspect per-crop results.

Retry transitions, crash recovery, cancellation semantics, and the final
evidence/result model remain open decisions. The current no-retry executor
rejects every non-queued state.

## Proposed query endpoints

The architecture source proposes `POST /api/v1/evaluations` plus polling and read endpoints for evaluation status, result, and evidence. A `202 Accepted` response with an identifier and polling location is illustrative. Final routes and schemas must be decided before clients or migrations are generated.

## Reproducibility requirements

An evaluation must retain the parcel version and geometry, dataset versions, crop parameters, effective scientific configuration, engine version or commit, relevant dependency versions, scenario, management, spatial scope, transformation and aggregation methods, checksums, attempts, timestamps, and artifact references. Audit records answer who did what; scientific evidence answers which inputs and rules produced the estimate.

## Source

See sections 8, 9, 12, 14, and 19 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx), plus the current [`multicrop.py`](../../CropSuiteLite/src/multicrop.py) state behavior.
