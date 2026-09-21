# Frontend API reference

All paths below are relative to the configured backend origin. Operation IDs are explicit and unique in the generated OpenAPI document.

| Area | Method | Path | Operation ID | Success |
| --- | --- | --- | --- | --- |
| Health | GET | `/health` | `get_health` | 200 |
| Projects | GET | `/projects` | `list_projects` | 200 |
| Projects | POST | `/projects` | `create_project` | 201 |
| Projects | GET | `/projects/{project_id}` | `get_project` | 200 |
| Parcels | POST | `/projects/{project_id}/parcels` | `create_parcel` | 201 |
| Parcels | GET | `/projects/{project_id}/parcels` | `list_parcels` | 200 |
| Parcels | GET | `/projects/{project_id}/parcels/{parcel_id}` | `get_parcel` | 200 |
| Parcels | POST | `/projects/{project_id}/parcels/{parcel_id}/versions` | `create_parcel_version` | 201 |
| Datasets | GET | `/datasets` | `list_datasets` | 200 |
| Datasets | POST | `/datasets` | `create_dataset` | 201 |
| Datasets | GET | `/datasets/{dataset_id}` | `get_dataset` | 200 |
| Dataset versions | POST | `/datasets/{dataset_id}/versions` | `create_dataset_version` | 201 |
| Dataset versions | GET | `/datasets/{dataset_id}/versions` | `list_dataset_versions` | 200 |
| Dataset versions | GET | `/datasets/{dataset_id}/versions/{version_id}` | `get_dataset_version` | 200 |
| Dataset coverage | POST | `/datasets/{dataset_id}/versions/{version_id}/coverage` | `check_dataset_coverage` | 200 |
| Capabilities | GET | `/api/v1/evaluation-capabilities` | `get_evaluation_capabilities` | 200 |
| Evaluations | POST | `/api/v1/evaluations` | `request_evaluation` | 201 |
| Evaluations | GET | `/api/v1/evaluations` | `list_evaluations` | 200 |
| Evaluations | GET | `/api/v1/evaluations/{evaluation_id}` | `get_evaluation` | 200 |
| Results | GET | `/api/v1/evaluations/{evaluation_id}/result` | `get_evaluation_result` | 200 |
| Evidence | GET | `/api/v1/evaluations/{evaluation_id}/evidence` | `get_evaluation_evidence` | 200 |
| Limitations | GET | `/api/v1/evaluations/{evaluation_id}/limitations` | `get_evaluation_limitations` | 200 |
| Knowledge | GET | `/api/v1/decision-support/evaluations/{evaluation_id}/knowledge` | `get_evaluation_knowledge` | 200 |
| Recommendations | POST | `/api/v1/decision-support/evaluations/{evaluation_id}/recommendations` | `create_evaluation_recommendation` | 200 |
| Recommendations | GET | `/api/v1/decision-support/evaluations/{evaluation_id}/recommendations` | `list_evaluation_recommendations` | 200 |

## Capability discovery

`GET /api/v1/evaluation-capabilities` returns the deployment-selected crop catalog and currently enforceable input constraints. The successful contract is:

```json
{
  "status": "partial",
  "crops": [
    {
      "crop_id": "...",
      "display_name": "...",
      "water_regimes": ["rainfed", "irrigated"]
    }
  ],
  "environmental_inputs": {
    "minimum_count": 1,
    "maximum_input_key_length": 120,
    "input_keys": [],
    "input_key_discovery": "arbitrary_unique",
    "requires_registered_dataset_version": true,
    "requires_scientific_binding": true,
    "scientifically_bound_dataset_versions": [
      {
        "dataset_id": "...",
        "dataset_version_id": "..."
      }
    ]
  },
  "limitations": ["..."]
}
```

The endpoint returns `503` with `{ "detail": "..." }` if the scientific catalog is not configured, cannot be read, or is empty. A frontend must not manufacture crop options if discovery is unavailable.

## Evaluation request

`POST /api/v1/evaluations` queues an evaluation. Its request has three parts:

- `parcel_snapshot`: exact project, parcel, parcel version, geometry, CRS, and capture time.
- `requested_crops`: one or more crop identifiers obtained from capabilities.
- `water_regimes`: one or more of `rainfed`, `irrigated`; default is rainfed when omitted.
- `environmental_inputs`: one or more exact dataset-version references. Each entry contains `input_key`, `dataset_id`, and `dataset_version_id`.

The current API validates that environmental input keys are unique/non-empty and bounded, but it does not publish canonical keys. See `known-gaps.md`.

## Decision Support request shapes

Knowledge retrieval is a GET with query parameters:

```text
/api/v1/decision-support/evaluations/{evaluation_id}/knowledge?crop_id=maize&water_regime=rainfed
```

Recommendation generation is a POST:

```json
{
  "crop_id": "maize",
  "water_regime": "rainfed",
  "force_regenerate": false
}
```

Listing recommendations performs no provider call and supports optional `crop_id` and `water_regime` query filters.

For exact field schemas, enum values, validation limits, and nullable properties, use `openapi.json` as the machine-readable source of truth.
