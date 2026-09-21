# Known frontend gaps

These are limitations of the current published contract, not tasks for the frontend to guess around.

1. **Scientific binding discovery does not guarantee runtime integrity.** Capabilities returns `input_key_discovery: "arbitrary_unique"` and publishes `scientifically_bound_dataset_versions`, but a configured binding can still fail later integrity checks during scientific execution.
2. **Capabilities depend on scientific runtime configuration.** `VIA_CROPSUITE_CATALOG` and `VIA_CROPSUITE_INPUT_BINDINGS` must both be configured and readable. Missing, invalid, or empty discovery sources can make capability discovery return `503`.
3. **Mixed route versioning.** Projects/datasets are unversioned while evaluation and Decision Support routes use `/api/v1`.
4. **Polling only.** There is no websocket/SSE evaluation progress contract and no server-provided retry interval.
5. **Irrigation feasibility is outside the scientific scenario contract.** The backend can evaluate an irrigated scientific scenario but does not establish real water/infrastructure availability.
6. **Decision Support requires durable PostgreSQL composition.** Its router is present when the application has database sessions; provider/configuration failures can still return `503`.
7. **No frontend authentication/session contract is defined here.** CORS allows the `Authorization` header, but this handoff does not define an auth flow.
8. **No bulk endpoint for full evaluation presentation.** Status, result, evidence, limitations, knowledge, and recommendations are separate resources and should be cached independently.
9. **`completed_crop_count` is outcome-count based today.** With more than one water regime it is not a unique-crop progress counter. Use `requested_execution_count` / `completed_execution_count` for progress UI.

Do not solve these gaps by changing scientific units, masks, interpolation, scoring, no-data semantics, or by hardcoding runtime-specific bindings into shared frontend code.
