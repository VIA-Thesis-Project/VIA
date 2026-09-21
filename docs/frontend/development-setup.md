# Frontend development setup

## Backend origin

Copy `frontend.env.example` into the frontend project's local environment mechanism and expose the value according to that framework. The example uses `API_BASE_URL=http://localhost:8000` as a framework-neutral name.

The backend must allow the browser origin explicitly. Set, for example:

```text
VIA_CORS_ALLOWED_ORIGINS=http://localhost:5173
```

Multiple origins are comma-separated. Duplicates and `*` are rejected. Each entry must start with `http://` or `https://`. Credentials are disabled; allowed methods are `GET`, `POST`, and `OPTIONS`, and allowed request headers are `Content-Type` and `Authorization`.

## OpenAPI

`docs/frontend/openapi.json` is a reproducible snapshot generated from the FastAPI application with a fake database composition during generation. Creating the schema must not contact production, execute CropSuite, or call OpenAI.

Use the snapshot for client generation and CI diffing. Regenerate it when an HTTP contract changes, then review the diff with the corresponding backend tests.

## Smoke scripts

From the repository root:

```powershell
.\scripts\smoke_frontend_api.ps1 -API_BASE_URL http://localhost:8000
```

or:

```bash
bash scripts/smoke_frontend_api.sh http://localhost:8000
```

The default smoke checks are read-only/lightweight: health, OpenAPI availability, list endpoints, and capability discovery. They do not create an evaluation or invoke scientific execution. Capability `503` is reported as unavailable rather than causing the script to fabricate fallback data.

Optional resource IDs can be supplied to extend read-only checks when a developer has suitable test data; the scripts do not embed production IDs.
