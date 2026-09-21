#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${1:-${API_BASE_URL:-http://localhost:8000}}"
EVALUATION_ID="${2:-}"
BASE="${API_BASE_URL%/}"

check_get() {
  local label="$1"
  local path="$2"
  local accepted="${3:-200}"
  local status

  status="$(curl --silent --show-error --output /dev/null --write-out '%{http_code}' "$BASE$path")"
  if [[ ",${accepted}," != *",${status},"* ]]; then
    echo "FAIL $label returned HTTP $status" >&2
    exit 1
  fi
  echo "OK  $label ($status)"
}

check_get "health" "/health"
check_get "openapi" "/openapi.json"
check_get "projects list" "/projects"
check_get "datasets list" "/datasets"
check_get "evaluations list" "/api/v1/evaluations"
check_get "evaluation capabilities" "/api/v1/evaluation-capabilities" "200,503"

if [[ -n "$EVALUATION_ID" ]]; then
  check_get "evaluation status" "/api/v1/evaluations/$EVALUATION_ID"
  check_get "evaluation result" "/api/v1/evaluations/$EVALUATION_ID/result"
  check_get "evaluation evidence" "/api/v1/evaluations/$EVALUATION_ID/evidence"
  check_get "evaluation limitations" "/api/v1/evaluations/$EVALUATION_ID/limitations"
fi

echo "Frontend API smoke checks completed. No evaluation was created."
