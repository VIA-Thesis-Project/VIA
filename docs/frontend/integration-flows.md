# Frontend integration flows

## 1. Establish and restore the session

1. Login through `POST /api/v1/auth/login`; keep the returned access token in memory.
2. Call `GET /api/v1/auth/me` with Bearer auth to hydrate the current user and role.
3. Let the browser retain the refresh token only as the API's `HttpOnly` cookie. Never read or mirror it into JavaScript or `localStorage`.
4. On a protected-request `401`, allow exactly one refresh request at a time across the app and across browser tabs. Broadcast only the fact that rotation completed (and the replacement access token if the application's threat model permits it), never the refresh cookie.
5. Retry the original request once. If refresh fails, return to login. Logout through `POST /api/v1/auth/logout`.

## 2. Bootstrap the functional UI

1. Call `GET /health` to verify the API process is reachable.
2. Call `GET /api/v1/evaluation-capabilities` before rendering crop/scenario selection.
3. Load projects with `GET /projects` and datasets with `GET /datasets` as needed.

If capabilities returns `503`, show scientific evaluation as temporarily unavailable. Do not replace the response with a hardcoded crop list.

## 3. Create or select a parcel version

Projects own multiple parcels. Parcel creation and every revised geometry must be completely covered by the authoritative Huaura AOI; outside or boundary-crossing geometry returns `422`. Parcels keep immutable `ParcelVersion` history.

When starting an evaluation, send only `parcel_reference` with `project_id`, `parcel_id`, and the selected version number. The backend resolves that exact owned version and persists its authoritative geometry, CRS, and capture time. Updating the parcel later must not retroactively change the historical evaluation shown by the UI.

## 4. Select environmental dataset versions

1. Read `scientifically_bound_dataset_versions` from `GET /api/v1/evaluation-capabilities`.
2. Resolve each returned `dataset_id` + `dataset_version_id` through the dataset endpoints to obtain user-facing metadata.
3. Optionally call the coverage endpoint for a candidate version against the parcel geometry before submission.
4. Generate a unique logical `input_key`, for example `environmental-input-1`.
5. Build `environmental_inputs` using the selected bound `dataset_id` + `dataset_version_id` pair and the generated `input_key`.

The capability contract reports `input_key_discovery = "arbitrary_unique"`. The key has no scientific-selection semantics and must not be treated as a hidden deployment convention. Scientific binding selection is determined by the exact dataset version. A listed bound version can still fail later runtime integrity checks.

## 5. Queue an evaluation

Submit `POST /api/v1/evaluations`. Treat the returned evaluation as accepted work, not as a completed scientific result.

Store the returned evaluation ID and begin polling `GET /api/v1/evaluations/{evaluation_id}`. See `async-evaluations.md`.

## 6. Render results while work progresses

`GET /api/v1/evaluations/{evaluation_id}/result` can represent `pending`, `partial`, `final`, or `failed` availability. A frontend may render completed scenario/crop outcomes while an evaluation is partial, but it must label them as partial and must not imply missing executions are zero.

When final results are available:

- render each water regime as a separate scenario;
- use suitability summaries for per-crop detail;
- use `comparable_crops` for rankings;
- use common-support metadata to explain whether the ranking has shared valid spatial coverage;
- render `no_coverage` and failed outcomes as states, not numeric zeros.

## 7. Render scientific evidence and limitations

Use `/evidence` for safe trace metadata and `/limitations` for limiting-factor evidence. `affected_fraction` is a `0..1` fraction of valid analyzed area for that factor.

Do not expose or synthesize internal filesystem paths. The HTTP trace contract already publishes hashes and safe identifiers intended for the UI.

## 8. Retrieve knowledge and recommendations

Decision Support is scenario-specific: always send both `crop_id` and `water_regime` for knowledge, and the same pair when generating a recommendation.

Knowledge/recommendation context is only valid for a finalized scenario. Handle `409` as "not final yet" and `404` as "requested evaluation/scenario context does not exist". A provider outage is `503` and should be retryable without altering scientific results.

Normal generation uses cache/reuse semantics. Send `force_regenerate: false` for USER flows. Only an ADMIN who owns the evaluation may send `true`; USER receives `403`, and any foreign principal, including ADMIN, receives `404`.

For recommendation citations, keep `SOURCE_n` only as the join key. Match each recommendation item's `citation_ids` against `RecommendationRun.citations[].evidence_id` and render the citation's `organization`, `title`, pages, and section when present.
