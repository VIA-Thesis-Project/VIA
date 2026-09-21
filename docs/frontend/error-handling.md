# Error handling

FastAPI validation and domain errors use JSON responses. Application-level errors exposed by the documented routers use the shape:

```json
{
  "detail": "Human-readable explanation"
}
```

Recommended frontend handling:

| Status | Meaning in current API | UI behavior |
| --- | --- | --- |
| 404 | requested project, parcel, dataset, evaluation, or Decision Support context was not found | show not-found/state refresh; do not retry blindly |
| 409 | current state conflicts with the requested action; Decision Support also uses this when context is not final | refresh state; for recommendations wait for final evaluation |
| 422 | request validation/domain command is invalid | show field/action feedback; preserve server detail |
| 503 | scientific capability discovery, coverage service, or knowledge/recommendation provider is unavailable | show temporary-unavailable state and allow retry |

FastAPI may return its structured validation error array under `detail` for schema validation failures. Client code should therefore accept `detail` as either a string or structured validation payload.

Do not parse server error strings to infer scientific states. Scientific states are explicit fields/enums on successful result responses.

## Capabilities 503

If `/api/v1/evaluation-capabilities` returns `503`, disable new scientific-evaluation configuration that depends on crop discovery. Existing evaluation history can still be displayed through its own endpoints.

## Decision Support 503

A recommendation provider failure does not invalidate the scientific evaluation. Keep the evaluation result visible and present recommendation generation as separately unavailable/retryable.
