#!/usr/bin/env bash
set -Eeuo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
compose_file="${repository_root}/compose.production-smoke.yaml"
project_name="via-b6-${GITHUB_RUN_ID:-local}-${GITHUB_RUN_ATTEMPT:-0}-$$"
compose=(docker compose -p "${project_name}" -f "${compose_file}")

cleanup() {
  status=$?
  trap - EXIT
  if [ "${status}" -ne 0 ]; then
    echo "B6 production-like Compose smoke failed; collecting diagnostics."
    "${compose[@]}" ps -a || true
    "${compose[@]}" logs --no-color || true
  fi
  "${compose[@]}" down -v --remove-orphans >/dev/null 2>&1 || true
  exit "${status}"
}
trap cleanup EXIT

container_id() {
  service="$1"
  "${compose[@]}" ps -a -q "${service}"
}

assert_running() {
  service="$1"
  id="$(container_id "${service}")"
  test -n "${id}"
  test "$(docker inspect -f '{{.State.Running}}' "${id}")" = "true"
}

assert_worker_liveness() {
  worker_id="$(container_id worker)"
  test -n "${worker_id}"
  for observation in 1 2 3; do
    test "$(docker inspect -f '{{.State.Running}}' "${worker_id}")" = "true"
    if [ "${observation}" -lt 3 ]; then
      sleep 6
    fi
  done
  worker_logs="$("${compose[@]}" logs --no-color worker 2>&1)"
  printf '%s\n' "${worker_logs}"
  if grep -q "Traceback (most recent call last):" <<<"${worker_logs}"; then
    echo "Worker emitted a fatal traceback while expected to remain idle."
    return 1
  fi
}

cd "${repository_root}"

"${compose[@]}" config --quiet
test "$("${compose[@]}" config --services | sort | tr '\n' ' ')" = "api db migrate worker "

"${compose[@]}" up -d

db_id="$(container_id db)"
migrate_id="$(container_id migrate)"
api_id="$(container_id api)"
worker_id="$(container_id worker)"
test -n "${db_id}"
test -n "${migrate_id}"
test -n "${api_id}"
test -n "${worker_id}"

test "$(docker inspect -f '{{.State.Health.Status}}' "${db_id}")" = "healthy"
test "$(docker inspect -f '{{.State.Status}}' "${migrate_id}")" = "exited"
test "$(docker inspect -f '{{.State.ExitCode}}' "${migrate_id}")" -eq 0

for attempt in $(seq 1 30); do
  if [ "$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{end}}' "${api_id}")" = "healthy" ]; then
    break
  fi
  if [ "$(docker inspect -f '{{.State.Running}}' "${api_id}")" != "true" ]; then
    echo "API stopped before becoming healthy."
    exit 1
  fi
  if [ "${attempt}" -eq 30 ]; then
    echo "API did not become healthy within the readiness window."
    exit 1
  fi
  sleep 1
done

health_json="$(curl --fail --silent http://127.0.0.1:18000/health)"
grep -q '"status":"ok"' <<<"${health_json}"
projects_status="$(
  curl \
    --silent \
    --output /dev/null \
    --write-out '%{http_code}' \
    http://127.0.0.1:18000/projects
)"
test "${projects_status}" = "401"

"${compose[@]}" run --rm --no-deps -T migrate python - <<'PY'
import os

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text

config = Config(os.environ["VIA_ALEMBIC_CONFIG"])
heads = ScriptDirectory.from_config(config).get_heads()
if len(heads) != 1:
    raise SystemExit(f"Expected exactly one Alembic head, found {heads!r}")

engine = create_engine(os.environ["VIA_DATABASE_URL"])
try:
    with engine.connect() as connection:
        current = connection.execute(text("SELECT version_num FROM alembic_version")).scalars().all()
finally:
    engine.dispose()

if current != heads:
    raise SystemExit(f"Database revision {current!r} does not equal repository head {heads!r}")
print(f"Database revision matches repository Alembic head: {heads[0]}")
PY

migrate_image_id="$(docker inspect -f '{{.Image}}' "${migrate_id}")"
api_image_id="$(docker inspect -f '{{.Image}}' "${api_id}")"
worker_image_id="$(docker inspect -f '{{.Image}}' "${worker_id}")"
test "${migrate_image_id}" = "${api_image_id}"
test "${migrate_image_id}" = "${worker_image_id}"

"${compose[@]}" exec -T worker sh -c '
  test -r /etc/via/input-bindings.json &&
  test -x /mnt/via/sources &&
  test -r /mnt/via/sources/.gitkeep &&
  test ! -w /etc/via &&
  test ! -w /mnt/via/sources &&
  test ! -w /opt/via/CropSuiteLite
'

assert_worker_liveness

marker="${GITHUB_RUN_ID:-local}-${GITHUB_RUN_ATTEMPT:-0}-${GITHUB_SHA:-manual}-$$"
"${compose[@]}" exec -T -e B6_MARKER="${marker}" worker sh -c '
  printf "%s" "$B6_MARKER" > /var/lib/via/artifacts/b6-marker.txt
  printf "%s" "$B6_MARKER" > /var/lib/via/workspace/b6-marker.txt
'

"${compose[@]}" up -d --force-recreate --no-deps worker
worker_id="$(container_id worker)"
assert_worker_liveness
"${compose[@]}" exec -T -e B6_MARKER="${marker}" worker sh -c '
  test "$(cat /var/lib/via/artifacts/b6-marker.txt)" = "$B6_MARKER" &&
  test ! -e /var/lib/via/workspace/b6-marker.txt
'

"${compose[@]}" stop -t 10 api worker
api_id="$(container_id api)"
worker_id="$(container_id worker)"
test "$(docker inspect -f '{{.State.Running}}' "${api_id}")" = "false"
test "$(docker inspect -f '{{.State.ExitCode}}' "${api_id}")" -eq 0
test "$(docker inspect -f '{{.State.Running}}' "${worker_id}")" = "false"
test "$(docker inspect -f '{{.State.ExitCode}}' "${worker_id}")" -eq 0

echo "B6 production-like Docker Compose smoke passed."
