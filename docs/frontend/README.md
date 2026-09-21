# VIA frontend handoff

This directory is the frontend-facing contract for the current VIA backend. It documents the HTTP surface as implemented today and keeps scientific semantics explicit so UI code does not infer meanings that the backend does not provide.

Start with:

- `api-reference.md` for endpoint paths and operation IDs.
- `integration-flows.md` for the end-to-end user flow.
- `async-evaluations.md` for polling and lifecycle handling.
- `scientific-result-semantics.md` before rendering suitability, coverage, rankings, or limitations.
- `error-handling.md` for status-code handling.
- `development-setup.md` for local CORS and smoke checks.
- `sample-data.md` and `fixtures/` for illustrative payloads.
- `known-gaps.md` for current contract limitations.
- `openapi.json` for generated client tooling. It is generated from the FastAPI app rather than edited by hand.

## Base URL and route prefixes

Configure one backend origin, for example `http://localhost:8000`. Append the paths exactly as documented. The current API does not use one uniform version prefix:

- `/health`, `/projects`, and `/datasets` are currently unversioned.
- `/api/v1/evaluations`, `/api/v1/evaluation-capabilities`, and `/api/v1/decision-support/...` use `/api/v1`.

Do not silently prepend `/api/v1` to every route in a frontend API wrapper.

## Frontend rules that should be treated as invariants

1. Evaluations are asynchronous. Creating one returns `201`; the scientific calculation is completed by the worker outside the HTTP request.
2. A suitability value of `0` is a valid scientific value. It is different from no-data, `no_coverage`, or a `null` suitability summary.
3. `coverage_fraction`, `common_coverage_fraction`, and limitation `affected_fraction` are fractions in `0..1`, not percentages in `0..100`.
4. Use `comparable_crops` for cross-crop rankings. Raw per-crop means can be based on different valid spatial support.
5. Rainfed and irrigated are separate scientific scenarios. An irrigated result does not assert that irrigation water or infrastructure is available in the real parcel.
6. Crop and scientific-binding discovery comes from `GET /api/v1/evaluation-capabilities`. Environmental `input_key` values are caller-defined unique logical identifiers; use `scientifically_bound_dataset_versions` to choose versions configured with scientific bindings.
7. Keep the exact parcel version and dataset-version identifiers used in an evaluation visible in application state. Historical evaluations are versioned evidence, not a live view of mutable inputs.
