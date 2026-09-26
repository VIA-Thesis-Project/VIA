# Route and security matrix

This matrix describes the live non-production schema and the production runtime behavior. `Bearer` means the short-lived access token in the `Authorization` header. Refresh tokens are accepted only through the rotating `HttpOnly` cookie.

| Route group | Operations | Authentication | Role/ownership | Cost protection |
| --- | --- | --- | --- | --- |
| `/health` | GET | public | none | none |
| `/api/v1/auth/login` | POST | public credentials | active user only | host + normalized-email rate limit; `429` + `Retry-After` |
| `/api/v1/auth/refresh` | POST | refresh cookie | trusted browser `Origin`; rotation/reuse protection | host rate limit; `429` + `Retry-After` |
| `/api/v1/auth/logout` | POST | refresh cookie optional | trusted browser `Origin` | none |
| `/api/v1/auth/me` | GET | Bearer | active session/user | none |
| `/projects` and nested parcel routes | GET/POST | Bearer | owner only; foreign Project/Parcel is `404` for USER and ADMIN | none |
| `/datasets` reads | GET | Bearer | USER or ADMIN | none |
| `/datasets` and `/versions` mutation | POST | Bearer | ADMIN; USER is `403` | none |
| dataset `/coverage` | POST | Bearer | USER or ADMIN | per-user rate limit; `429` + `Retry-After` |
| `/api/v1/evaluation-capabilities` | GET | Bearer | USER or ADMIN | none |
| `/api/v1/evaluations` | GET/POST | Bearer | owner-scoped; foreign ParcelVersion is `404` | evaluations are queued without a per-user quota |
| `/api/v1/evaluations/{id}` and result/evidence/limitations | GET | Bearer | owner only; foreign Evaluation is `404` for USER and ADMIN | none |
| Decision Support knowledge | GET | Bearer | evaluation owner only; foreign is `404` for USER and ADMIN | per-user rate limit; `429` + `Retry-After` |
| Decision Support recommendations list | GET | Bearer | evaluation owner only; foreign is `404` | none |
| Decision Support recommendation generation | POST | Bearer | owner; `force_regenerate=true` additionally requires ADMIN; foreign ADMIN is `404` | per-user rate limit; `429` + `Retry-After` |

## Status semantics

- `401` never reveals whether an opaque token existed. Missing, malformed, unknown, expired, revoked, reused-family, and disabled-user sessions are unauthenticated.
- `403` means identity is known but role or browser-origin policy denies the action.
- `404` is deliberately used for missing and foreign owned resources to prevent IDOR existence disclosure. ADMIN does not bypass ownership.
- `422` covers request/schema/domain validation, including client-supplied evaluation snapshot fields and parcel geometry outside/crossing the Huaura AOI.
- `429` always includes `Retry-After`.

## Production-only surface

Production exposes `/health` but disables `/docs`, `/redoc`, and `/openapi.json`. The committed `openapi.json` is generated offline from the live non-production application schema and checked for exact equality in tests.
