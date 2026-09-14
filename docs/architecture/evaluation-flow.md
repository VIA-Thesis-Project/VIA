# Target evaluation flow

The evaluation flow accepts a short HTTP request, records enough immutable context
to reproduce the evaluation, and leaves the new resource in `queued`. A separate
worker process polls PostgreSQL for queued evaluation IDs and delegates each ID to
the existing synchronous Application execution service. HTTP never executes the
scientific calculation.

## Request to result

```text
POST evaluation request
  -> authenticate and authorize project/parcel access
  -> resolve the requested ParcelVersion
  -> check Huaura scope and environmental coverage/data compatibility
  -> create an immutable ParcelSnapshot
  -> create and persist the Evaluation with crop and configuration references
  -> leave the Evaluation queued as the durable source of truth
  -> return an evaluation identifier for polling
  -> separate worker polls PostgreSQL in created_at/id order
  -> worker delegates the ID to the Application execution service
  -> executor optimistically claims queued -> preparing
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

## Implemented worker-backed orchestration

`AgroclimaticEvaluationExecutionService` loads an already-persisted queued
evaluation and claims it with an optimistic `queued -> preparing` transition. It
then persists `preparing -> running`, evaluates requested crops sequentially
through `ICropSuitabilityEngine`, and commits one same-context durable
`crop_outcomes` row after each returned result. Once every requested crop has an
outcome it persists `running -> summarizing -> succeeded`.

Each repository call opens a short transaction; the blocking scientific call is
never enclosed in a database transaction. The separate `via-worker run` process
discovers a bounded batch of queued IDs in FIFO order (`created_at`, then `id`)
and calls this same use case. Two worker processes may observe the same row; the
optimistic queued claim is authoritative, and the losing `ResourceConflictError`
is benign contention rather than an evaluation failure.

Returned per-crop `failed` and `no_coverage` values are completed scientific
outcomes and do not abort later crops. A valid score of zero remains `succeeded`.
Overall `succeeded` means every requested crop was attempted and durably reported,
not that every per-crop status succeeded. Boundary or other orchestration
exceptions stop remaining crops and persist overall `failed` with a minimal
reason; they do not fabricate a crop outcome.

Request creation remains request creation only. There is no HTTP run-now or
recovery endpoint, broker, automatic retry, or cancellation mechanism. One worker
process executes evaluations sequentially; crop execution inside each evaluation
also remains sequential.

## Current PoC states and required mapping

The current local manifest uses request states `running`, `completed`, `partial`, and `failed`. Per-crop states are `running`, `succeeded`, `no_coverage`, and `failed`. A failed crop does not stop the others. Invalid requests fail before a job directory is created.

The future API requires an explicit mapping rather than renaming these values implicitly. In particular:

- PoC `partial` has no direct equivalent in the proposed top-level list unless the future result model represents a succeeded evaluation with incomplete per-crop outcomes or adds another state.
- Per-crop `no_coverage` is an information-availability outcome, not process failure and not suitability zero.
- `Cancelled`, `Queued`, `Preparing`, and `Summarizing` do not exist in the current PoC.
- `completed` does not guarantee that every crop has usable coverage; clients must inspect per-crop results.

The worker has no heartbeat, lease, automatic stale timeout, takeover, retry, or
requeue. SIGINT does not attempt mid-CropSuite cancellation. Process death or
interruption can therefore leave an evaluation in `preparing`, `running`, or
`summarizing`. An operator who has confirmed the process is gone may run
`via-worker recover <id> --reason <text>`; the Application recovery use case uses
the aggregate's existing failure behavior and optimistic expected status to mark
only an active evaluation `failed`. Already-persisted outcomes remain, missing
outcomes are not fabricated, and the evaluation is never restarted or requeued.
Automatic crash recovery, retry, cancellation semantics, and the final
evidence/result model remain open decisions.

## Implemented query endpoints

Agroclimatic Evaluation now exposes its versioned read surface:

- `GET /api/v1/evaluations/{evaluation_id}` returns lifecycle status, deterministic requested-crop order, requested and completed crop counts, creation time, and safe parcel-snapshot identity fields. It does not invent a progress percentage.
- `GET /api/v1/evaluations/{evaluation_id}/result` returns the outcomes currently persisted in request order. Its explicit availability is `pending` when none are persisted, `partial` while an active evaluation has outcomes, `final` only after overall `succeeded`, and `failed` after overall orchestration failure.
- `GET /api/v1/evaluations/{evaluation_id}/evidence` returns the currently persisted safe per-crop trace subset with the same availability semantics.

Lifecycle status and per-crop outcome status are separate. A `succeeded` crop with mean zero remains a valid result; `no_coverage` retains null summary values and zero valid support; `failed` has no suitability summary. Public resources do not expose persisted diagnostic messages or the opaque execution reference.

Application also publishes the immutable `FinalizedEvaluationResult` contract through `FinalizedEvaluationResultReader`. The reader accepts only overall `succeeded` evaluations and exposes ordered outcomes, current suitability summaries, safe trace metadata, and snapshot identity without repositories, ORM records, tables, CropSuiteLite types, or filesystem paths.

Decision Support remains deferred. The current independent per-crop summaries do not contain the common-valid-support comparison required by ADR-009. Consumers must not sort independent means and call that a ranking; common-support ranking remains a later scientifically justified contract.

## Reproducibility requirements

An evaluation must retain the parcel version and geometry, dataset versions, crop parameters, effective scientific configuration, engine version or commit, relevant dependency versions, scenario, management, spatial scope, transformation and aggregation methods, checksums, attempts, timestamps, and artifact references. Audit records answer who did what; scientific evidence answers which inputs and rules produced the estimate.

## Source

See sections 8, 9, 12, 14, and 19 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx), plus the current [`multicrop.py`](../../CropSuiteLite/src/multicrop.py) state behavior.
