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
| 401 | missing, invalid, expired, revoked, or disabled-user access session; refresh may also be invalid/reused | serialize one refresh attempt and retry once; otherwise return to login |
| 403 | authenticated but role/origin policy denies the operation | do not refresh; hide/disable unauthorized actions and show permission feedback |
| 404 | requested project, parcel, dataset, evaluation, or Decision Support context was not found | show not-found/state refresh; do not retry blindly |
| 409 | current state conflicts with the requested action; Decision Support also uses this when context is not final | refresh state; for recommendations wait for final evaluation |
| 422 | request validation/domain command is invalid | show field/action feedback; preserve server detail |
| 429 | per-minute rate limit or daily/active quota was reached | honor `Retry-After`, prevent request storms, and show when retry is allowed |
| 503 | scientific capability discovery, coverage service, or knowledge/recommendation provider is unavailable | show temporary-unavailable state and allow retry |

FastAPI may return its structured validation error array under `detail` for schema validation failures. Client code should therefore accept `detail` as either a string or structured validation payload.

Do not parse server error strings to infer scientific states. Scientific states are explicit fields/enums on successful result responses.

Do not refresh on `403`, `404`, `422`, or `429`. A `401` retry loop must be capped at one refresh and one replay. Because refresh tokens rotate, concurrent refreshes from multiple tabs can look like token reuse and revoke the full family; coordinate refresh with a cross-tab lock such as Web Locks, with a BroadcastChannel fallback.

## Capabilities 503

If `/api/v1/evaluation-capabilities` returns `503`, disable new scientific-evaluation configuration that depends on crop discovery. Existing evaluation history can still be displayed through its own endpoints.

## Decision Support 503

A recommendation provider failure does not invalidate the scientific evaluation. Keep the evaluation result visible and present recommendation generation as separately unavailable/retryable.
