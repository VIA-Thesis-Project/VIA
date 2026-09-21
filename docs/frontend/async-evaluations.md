# Asynchronous evaluations

Scientific work runs in the background worker. HTTP submission only queues the work.

## Lifecycle

The evaluation status vocabulary is:

```text
queued -> preparing -> running -> summarizing -> succeeded
                                   \-> failed
cancelled is also part of the domain vocabulary.
```

Use `GET /api/v1/evaluations/{evaluation_id}` as the polling endpoint. It returns:

- overall `status`;
- requested and completed crop counts;
- requested and completed execution counts;
- requested water regimes;
- parcel identity/version metadata;
- `failed`, a convenience boolean.

One requested crop across two water regimes means two scientific executions. Prefer `requested_execution_count` and `completed_execution_count` for progress indicators.

In the current read model, `completed_crop_count` mirrors the number of persisted outcomes rather than the number of unique crop IDs, so it can exceed `requested_crop_count` when multiple water regimes are requested.

## Polling behavior

Recommended frontend behavior:

1. Poll while status is `queued`, `preparing`, `running`, or `summarizing`.
2. Back off polling when work is long-running; do not issue concurrent duplicate polls for the same evaluation.
3. Stop normal polling on `succeeded`, `failed`, or `cancelled`.
4. Fetch `/result`, `/evidence`, and `/limitations` after completion, or fetch `/result` during execution when the UI intentionally supports partial output.

The backend does not currently publish a websocket/SSE progress channel or a retry-after interval. Polling cadence is therefore a frontend policy.

## Result availability is separate from lifecycle

`EvaluationResultResponse.availability` is one of:

- `pending`: no completed result is available yet;
- `partial`: some result data is available but the evaluation is not final;
- `final`: the evaluation succeeded and the result is finalized;
- `failed`: the evaluation ended in failure.

Do not infer availability only from the number of outcomes. Use the explicit field.
