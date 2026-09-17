#!/usr/bin/env bash
set -Eeuo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
compose_file="${repository_root}/compose.digitalocean.yaml"
runtime_env="${VIA_RUNTIME_ENV_FILE:-/srv/via/config/runtime.env}"
config_dir="/srv/via/config"
sources_dir="/srv/via/sources"
artifacts_dir="/srv/via/artifacts"
backups_dir="/srv/via/backups"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command is unavailable: $1"
}

require_directory() {
  test -d "$1" || fail "Required production directory is missing: $1"
}

image_ref="${1:-${VIA_IMAGE:-}}"
test -n "${image_ref}" || fail "Pass VIA_IMAGE as the first argument or environment variable."
if [[ ! "${image_ref}" =~ ^ghcr\.io/[a-z0-9._/-]+(@sha256:[0-9a-f]{64}|:[0-9a-f]{40})$ ]]; then
  fail "VIA_IMAGE must be a GHCR digest or full 40-character git-SHA tag; latest is not accepted."
fi
export VIA_IMAGE="${image_ref}"

require_command docker
require_command find
require_command grep
require_command sudo
docker info >/dev/null 2>&1 || fail "Docker Engine is not available to the current user."
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required."

for directory in "${config_dir}" "${sources_dir}" "${artifacts_dir}" "${backups_dir}"; do
  require_directory "${directory}"
done

test -r "${runtime_env}" || fail "Production runtime environment file is missing or unreadable: ${runtime_env}"
if find "${runtime_env}" -perm /077 -print -quit | grep -q .; then
  fail "${runtime_env} must not be readable or writable by group/other users (use chmod 600)."
fi
test -r "${config_dir}/input-bindings.json" || fail "${config_dir}/input-bindings.json is required."
if ! find "${sources_dir}" -mindepth 1 -type f -print -quit | grep -q .; then
  fail "${sources_dir} must contain the operator-provided final scientific runtime sources."
fi

# runtime.env is an operator-owned shell-compatible dotenv file. It is sourced
# only to validate/interpolate deployment variables and is never printed.
set -a
# shellcheck disable=SC1090
. "${runtime_env}"
set +a

: "${VIA_POSTGRES_DB:?VIA_POSTGRES_DB is required in runtime.env}"
: "${VIA_POSTGRES_USER:?VIA_POSTGRES_USER is required in runtime.env}"
: "${VIA_POSTGRES_PASSWORD:?VIA_POSTGRES_PASSWORD is required in runtime.env}"
if [[ ! "${VIA_POSTGRES_PASSWORD}" =~ ^[-A-Za-z0-9._~]{24,}$ ]]; then
  fail "VIA_POSTGRES_PASSWORD must contain at least 24 URL-unreserved characters."
fi
export VIA_IMAGE="${image_ref}"

compose=(docker compose --env-file "${runtime_env}" -f "${compose_file}")

wait_for_health() {
  service="$1"
  attempts="$2"
  container_id="$("${compose[@]}" ps -q "${service}")"
  test -n "${container_id}" || fail "${service} container was not created."

  for attempt in $(seq 1 "${attempts}"); do
    state="$(docker inspect -f '{{.State.Status}}' "${container_id}")"
    health="$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{end}}' "${container_id}")"
    if [ "${health}" = "healthy" ]; then
      return 0
    fi
    if [ "${state}" != "running" ] || [ "${health}" = "unhealthy" ]; then
      "${compose[@]}" logs --no-color "${service}" >&2 || true
      fail "${service} stopped or became unhealthy during readiness verification."
    fi
    if [ "${attempt}" -eq "${attempts}" ]; then
      "${compose[@]}" logs --no-color "${service}" >&2 || true
      fail "${service} did not become healthy within the readiness window."
    fi
    sleep 1
  done
}

verify_worker_liveness() {
  worker_id="$("${compose[@]}" ps -q worker)"
  test -n "${worker_id}" || fail "worker container was not created."

  worker_poll_interval="${VIA_WORKER_POLL_INTERVAL_SECONDS:-5}"
  initial_restart_count="$(docker inspect -f '{{.RestartCount}}' "${worker_id}")" || {
    "${compose[@]}" logs --no-color worker >&2 || true
    fail "worker could not be inspected before liveness verification."
  }

  for observation in 1 2 3; do
    worker_running="$(docker inspect -f '{{.State.Running}}' "${worker_id}")" || {
      "${compose[@]}" logs --no-color worker >&2 || true
      fail "worker could not be inspected during liveness verification."
    }
    restart_count="$(docker inspect -f '{{.RestartCount}}' "${worker_id}")" || {
      "${compose[@]}" logs --no-color worker >&2 || true
      fail "worker restart count could not be inspected during liveness verification."
    }

    if [ "${worker_running}" != "true" ]; then
      "${compose[@]}" logs --no-color worker >&2 || true
      fail "worker stopped during liveness verification."
    fi
    if [ "${restart_count}" != "${initial_restart_count}" ]; then
      "${compose[@]}" logs --no-color worker >&2 || true
      fail "worker restarted during liveness verification."
    fi

    if [ "${observation}" -lt 3 ]; then
      if ! sleep "${worker_poll_interval}"; then
        "${compose[@]}" logs --no-color worker >&2 || true
        fail "VIA_WORKER_POLL_INTERVAL_SECONDS is not a usable sleep interval."
      fi
    fi
  done

  if ! worker_logs="$("${compose[@]}" logs --no-color worker 2>&1)"; then
    printf '%s\n' "${worker_logs}" >&2
    fail "worker logs could not be inspected after liveness verification."
  fi
  if grep -q "Traceback (most recent call last):" <<<"${worker_logs}"; then
    printf '%s\n' "${worker_logs}" >&2
    fail "worker emitted a fatal Python traceback during liveness verification."
  fi
}

echo "Pulling immutable VIA image ${VIA_IMAGE}"
docker pull "${VIA_IMAGE}"

via_uid="$(docker run --rm --entrypoint id "${VIA_IMAGE}" -u)"
via_gid="$(docker run --rm --entrypoint id "${VIA_IMAGE}" -g)"
sudo -n chown "${via_uid}:${via_gid}" "${artifacts_dir}"
sudo -n chmod 0770 "${artifacts_dir}"

docker run --rm \
  --entrypoint sh \
  -v "${config_dir}:/etc/via:ro" \
  -v "${sources_dir}:/mnt/via/sources:ro" \
  "${VIA_IMAGE}" \
  -c 'test -r /etc/via/input-bindings.json && test -x /mnt/via/sources && test ! -w /etc/via && test ! -w /mnt/via/sources'

echo "Starting durable PostgreSQL/PostGIS service"
"${compose[@]}" up -d db
wait_for_health db 60

echo "Applying one-shot schema migration"
"${compose[@]}" run --rm --no-deps migrate

echo "Updating API and worker only after migration success"
"${compose[@]}" up -d --no-deps api worker
wait_for_health api 60
verify_worker_liveness

expected_image_id="$(docker image inspect -f '{{.Id}}' "${VIA_IMAGE}")"
for service in api worker; do
  container_id="$("${compose[@]}" ps -q "${service}")"
  actual_image_id="$(docker inspect -f '{{.Image}}' "${container_id}")"
  test "${actual_image_id}" = "${expected_image_id}" || fail "${service} is not running the requested VIA_IMAGE."
done

echo "VIA deployment is healthy. API is bound to Droplet loopback for controlled smoke testing."
