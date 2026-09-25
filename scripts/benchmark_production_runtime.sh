#!/usr/bin/env bash
set -Eeuo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
base_compose="$repository_root/compose.production-smoke.yaml"
benchmark_compose="$repository_root/compose.benchmark.yaml"

fixture_path="${VIA_BENCHMARK_FIXTURE:-}"
source_dir="${VIA_BENCHMARK_SOURCE_DIR:-}"
extra_config_dir="${VIA_BENCHMARK_CONFIG_DIR:-}"
source_config="${VIA_BENCHMARK_SOURCE_CONFIG:-}"
catalog="${VIA_BENCHMARK_CATALOG:-}"
image="${VIA_IMAGE:-via:b6}"
result_path="${VIA_BENCHMARK_RESULT_PATH:-$repository_root/benchmark-results.json}"
requested_runs="${VIA_BENCHMARK_RUNS:-1}"
benchmark_cropsuite_max_workers="${VIA_BENCHMARK_CROPSUITE_MAX_WORKERS:-1}"
idle_seconds="${VIA_BENCHMARK_IDLE_SECONDS:-45}"
settle_seconds="${VIA_BENCHMARK_SETTLE_SECONDS:-15}"
evaluation_timeout_seconds="${VIA_BENCHMARK_EVALUATION_TIMEOUT_SECONDS:-7200}"
sample_interval_seconds=1

case "$benchmark_cropsuite_max_workers" in
  1|2) ;;
  *) fail_later="VIA_BENCHMARK_CROPSUITE_MAX_WORKERS must be 1 or 2 for the comparison benchmark." ;;
esac

runtime_root=""
runtime_config_dir=""
sample_root=""
compose_project="${VIA_BENCHMARK_COMPOSE_PROJECT:-via-b61-benchmark}"
compose=()

fail() {
  printf 'B6.1 benchmark: %s\n' "$*" >&2
  exit 1
}

[ -z "${fail_later:-}" ] || fail "$fail_later"

cleanup() {
  status=$?
  if [ "${#compose[@]}" -gt 0 ]; then
    "${compose[@]}" down -v --remove-orphans >/dev/null 2>&1 || true
  fi
  if [ -n "$runtime_root" ] && [ -d "$runtime_root" ]; then
    rm -rf "$runtime_root"
  fi
  exit "$status"
}
trap cleanup EXIT

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "required command '$1' is unavailable."
}

monotonic_ns() {
  python3 -c 'import time; print(time.monotonic_ns())'
}

database_size_bytes() {
  "${compose[@]}" exec -T db \
    psql -U via -d via -Atc 'SELECT pg_database_size(current_database());'
}

wait_for_api() {
  local deadline=$((SECONDS + 90))
  until curl --fail --silent http://127.0.0.1:18000/health >/dev/null 2>&1; do
    if (( SECONDS >= deadline )); then
      "${compose[@]}" logs api >&2 || true
      fail "API did not become healthy within 90 seconds."
    fi
    sleep 1
  done
}

post_json() {
  local url="$1"
  local body_path="$2"
  local output_path="$3"
  curl --fail-with-body --silent --show-error \
    -H 'Content-Type: application/json' \
    --data-binary "@$body_path" \
    "$url" >"$output_path"
}

record_stack_sample() {
  local output_path="$1"
  local sample_id="$2"
  local timestamp_ns
  timestamp_ns="$(monotonic_ns)"

  docker stats --no-stream \
    --format '{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}' \
    "$db_container" "$api_container" "$worker_container" |
    while IFS=$'\t' read -r container_name cpu_percent memory_usage; do
      local service=""
      case "$container_name" in
        "$db_name") service="db" ;;
        "$api_name") service="api" ;;
        "$worker_name") service="worker" ;;
        *) continue ;;
      esac
      printf '%s\t%s\t%s\t%s\t%s\n' \
        "$sample_id" "$timestamp_ns" "$service" "$cpu_percent" "$memory_usage" \
        >>"$output_path"
    done
}

workspace_bytes_for_evaluation() {
  local evaluation_id="$1"
  docker exec -e VIA_BENCHMARK_EVALUATION_ID="$evaluation_id" "$worker_container" \
    sh -c '
      set -- /var/lib/via/workspace/"${VIA_BENCHMARK_EVALUATION_ID}_"*
      if [ ! -e "$1" ]; then
        printf "0\n"
        exit 0
      fi
      du -sb "$@" 2>/dev/null | awk "{total += \$1} END {print total + 0}"
    '
}

artifact_bytes_for_evaluation() {
  local evaluation_id="$1"
  docker exec -e VIA_BENCHMARK_EVALUATION_ID="$evaluation_id" "$worker_container" \
    sh -c '
      path="/var/lib/via/artifacts/evaluations/${VIA_BENCHMARK_EVALUATION_ID}"
      if [ ! -e "$path" ]; then
        printf "0\n"
        exit 0
      fi
      du -sb "$path" | awk "{print \$1}"
    '
}

if [ "$(uname -s)" != "Linux" ]; then
  fail "this benchmark harness must run on Linux so Docker/cgroup measurements are comparable."
fi

for command_name in docker curl python3 git uname nproc; do
  require_command "$command_name"
done
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 is required."

[ -n "$fixture_path" ] || fail "set VIA_BENCHMARK_FIXTURE to a legitimate scientific benchmark fixture JSON."
[ -f "$fixture_path" ] || fail "fixture does not exist: $fixture_path"
[ -n "$source_dir" ] || fail "set VIA_BENCHMARK_SOURCE_DIR to the legitimate scientific source directory."
[ -d "$source_dir" ] || fail "scientific source directory does not exist: $source_dir"
[ -n "$(find "$source_dir" -mindepth 1 -print -quit 2>/dev/null)" ] || fail "scientific source directory is empty: $source_dir"
[[ "$requested_runs" == "1" || "$requested_runs" == "3" ]] || fail "VIA_BENCHMARK_RUNS must be 1 or 3."
[[ "$idle_seconds" =~ ^[0-9]+$ ]] || fail "VIA_BENCHMARK_IDLE_SECONDS must be an integer."
[[ "$settle_seconds" =~ ^[0-9]+$ ]] || fail "VIA_BENCHMARK_SETTLE_SECONDS must be an integer."
[[ "$evaluation_timeout_seconds" =~ ^[0-9]+$ ]] || fail "VIA_BENCHMARK_EVALUATION_TIMEOUT_SECONDS must be an integer."
(( idle_seconds >= 30 && idle_seconds <= 60 )) || fail "idle sampling must remain between 30 and 60 seconds."

docker image inspect "$image" >/dev/null 2>&1 || fail "VIA image '$image' is not available locally; build the normal B6 image first."

runtime_root="$(mktemp -d)"
runtime_config_dir="$runtime_root/config"
sample_root="$runtime_root/samples"
mkdir -p "$runtime_config_dir" "$sample_root"

if [ -n "$extra_config_dir" ]; then
  [ -d "$extra_config_dir" ] || fail "VIA_BENCHMARK_CONFIG_DIR does not exist: $extra_config_dir"
  cp -a "$extra_config_dir/." "$runtime_config_dir/"
fi

python3 - "$fixture_path" "$requested_runs" >"$runtime_root/fixture-validation.json" <<'PY'
import json
import re
import sys
from pathlib import Path

fixture_path = Path(sys.argv[1])
requested_runs = int(sys.argv[2])
fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

required_root = {"repeatable", "evaluation", "environmental_inputs"}
if set(fixture) != required_root:
    raise SystemExit(f"fixture root fields must be exactly {sorted(required_root)}")

repeatable = fixture["repeatable"]
if not isinstance(repeatable, bool):
    raise SystemExit("fixture.repeatable must be boolean")
if requested_runs == 3 and not repeatable:
    raise SystemExit("three sequential runs require fixture.repeatable=true")

evaluation = fixture["evaluation"]
if not isinstance(evaluation, dict) or set(evaluation) != {"parcel_snapshot", "requested_crops"}:
    raise SystemExit("fixture.evaluation must contain only parcel_snapshot and requested_crops")
if not isinstance(evaluation["requested_crops"], list) or not evaluation["requested_crops"]:
    raise SystemExit("fixture.evaluation.requested_crops must be a non-empty array")

inputs = fixture["environmental_inputs"]
if not isinstance(inputs, list) or not inputs:
    raise SystemExit("fixture.environmental_inputs must be a non-empty array")

sha_re = re.compile(r"^[0-9a-f]{64}$")
for index, item in enumerate(inputs):
    if not isinstance(item, dict) or set(item) != {"input_key", "dataset", "version", "source_sha256"}:
        raise SystemExit(f"environmental_inputs[{index}] has unsupported or missing fields")
    dataset = item["dataset"]
    if not isinstance(dataset, dict) or set(dataset) != {"name", "source", "variable", "unit"}:
        raise SystemExit(f"environmental_inputs[{index}].dataset has invalid fields")
    version = item["version"]
    version_fields = {
        "version_identifier", "crs", "resolution", "extent", "valid_from", "valid_to",
        "scenario", "checksum", "storage_reference",
    }
    if not isinstance(version, dict) or set(version) != version_fields:
        raise SystemExit(f"environmental_inputs[{index}].version has invalid fields")
    storage_reference = version["storage_reference"]
    if not isinstance(storage_reference, str) or not (
        storage_reference == "/mnt/via/sources" or storage_reference.startswith("/mnt/via/sources/")
    ):
        raise SystemExit(f"environmental_inputs[{index}].version.storage_reference must be under /mnt/via/sources")
    if version["checksum"] == "smoke-only:bindings-loader-fixture":
        raise SystemExit("the B6 startup-only bindings fixture cannot be used for B6.1")
    hashes = item["source_sha256"]
    if not isinstance(hashes, list) or not hashes or len(hashes) != len(set(hashes)):
        raise SystemExit(f"environmental_inputs[{index}].source_sha256 must be a non-empty unique array")
    for value in hashes:
        if not isinstance(value, str) or sha_re.fullmatch(value) is None:
            raise SystemExit(f"environmental_inputs[{index}].source_sha256 contains an invalid SHA-256")
        if value == "a" * 64:
            raise SystemExit("the B6 startup-only source hash cannot be used for B6.1")

print(json.dumps({
    "repeatable": repeatable,
    "requested_crops": evaluation["requested_crops"],
    "environmental_input_count": len(inputs),
}))
PY

export VIA_IMAGE="$image"
export VIA_BENCHMARK_SOURCE_DIR="$(cd "$source_dir" && pwd)"
export VIA_BENCHMARK_RUNTIME_CONFIG_DIR="$runtime_config_dir"
export VIA_BENCHMARK_SOURCE_CONFIG="$source_config"
export VIA_BENCHMARK_CATALOG="$catalog"
export COMPOSE_PROJECT_NAME="$compose_project"
compose=(docker compose -f "$base_compose" -f "$benchmark_compose")

"${compose[@]}" config --quiet
"${compose[@]}" up -d db migrate api
wait_for_api

python3 - "$fixture_path" "$runtime_root" <<'PY'
import json
import sys
from pathlib import Path

fixture = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
runtime = Path(sys.argv[2])
for index, item in enumerate(fixture["environmental_inputs"]):
    (runtime / f"dataset-{index}.json").write_text(json.dumps(item["dataset"]), encoding="utf-8")
    (runtime / f"version-{index}.json").write_text(json.dumps(item["version"]), encoding="utf-8")
PY

input_count="$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1], encoding="utf-8"))["environmental_inputs"]))' "$fixture_path")"
bindings_json="$runtime_config_dir/input-bindings.json"
evaluation_request_json="$runtime_root/evaluation-request.json"
printf '{"bindings":[]}\n' >"$bindings_json"

for ((index = 0; index < input_count; index++)); do
  dataset_response="$runtime_root/dataset-response-$index.json"
  version_response="$runtime_root/version-response-$index.json"
  post_json "http://127.0.0.1:18000/datasets" "$runtime_root/dataset-$index.json" "$dataset_response"
  dataset_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["id"])' "$dataset_response")"
  post_json "http://127.0.0.1:18000/datasets/$dataset_id/versions" "$runtime_root/version-$index.json" "$version_response"
done

python3 - "$fixture_path" "$runtime_root" "$bindings_json" "$evaluation_request_json" <<'PY'
import json
import sys
from pathlib import Path

fixture = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
runtime = Path(sys.argv[2])
bindings_path = Path(sys.argv[3])
request_path = Path(sys.argv[4])

bindings = []
references = []
for index, item in enumerate(fixture["environmental_inputs"]):
    dataset = json.loads((runtime / f"dataset-response-{index}.json").read_text(encoding="utf-8"))
    version = json.loads((runtime / f"version-response-{index}.json").read_text(encoding="utf-8"))
    bindings.append({
        "dataset_id": dataset["id"],
        "dataset_version_id": version["id"],
        "storage_reference": version["storage_reference"],
        "checksum": version["checksum"],
        "source_sha256": item["source_sha256"],
    })
    references.append({
        "input_key": item["input_key"],
        "dataset_id": dataset["id"],
        "dataset_version_id": version["id"],
    })

bindings_path.write_text(json.dumps({"bindings": bindings}, indent=2) + "\n", encoding="utf-8")
request_path.write_text(json.dumps({
    "parcel_snapshot": fixture["evaluation"]["parcel_snapshot"],
    "requested_crops": fixture["evaluation"]["requested_crops"],
    "environmental_inputs": references,
}, indent=2) + "\n", encoding="utf-8")
PY

"${compose[@]}" up -d worker

db_container="$("${compose[@]}" ps -q db)"
api_container="$("${compose[@]}" ps -q api)"
worker_container="$("${compose[@]}" ps -q worker)"
[ -n "$db_container" ] && [ -n "$api_container" ] && [ -n "$worker_container" ] || fail "could not resolve benchmark containers."
db_name="$(docker inspect -f '{{.Name}}' "$db_container" | sed 's#^/##')"
api_name="$(docker inspect -f '{{.Name}}' "$api_container" | sed 's#^/##')"
worker_name="$(docker inspect -f '{{.Name}}' "$worker_container" | sed 's#^/##')"

sleep "$settle_seconds"
if [ "$(docker inspect -f '{{.State.Running}}' "$worker_container")" != "true" ]; then
  "${compose[@]}" logs worker >&2 || true
  fail "worker stopped before idle measurement; inspect scientific configuration."
fi

idle_samples="$sample_root/idle.tsv"
: >"$idle_samples"
idle_started_ns="$(monotonic_ns)"
sample_id=0
while true; do
  now_ns="$(monotonic_ns)"
  elapsed_whole_seconds=$(( (now_ns - idle_started_ns) / 1000000000 ))
  (( elapsed_whole_seconds >= idle_seconds )) && break
  record_stack_sample "$idle_samples" "$sample_id"
  sample_id=$((sample_id + 1))
done
idle_finished_ns="$(monotonic_ns)"

run_records="$runtime_root/run-records.jsonl"
: >"$run_records"
all_runs_succeeded=true

for ((run_number = 1; run_number <= requested_runs; run_number++)); do
  db_before="$(database_size_bytes)"
  response_path="$runtime_root/evaluation-response-$run_number.json"
  started_ns="$(monotonic_ns)"
  post_json "http://127.0.0.1:18000/api/v1/evaluations" "$evaluation_request_json" "$response_path"
  evaluation_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["id"])' "$response_path")"

  evaluation_samples="$sample_root/evaluation-$run_number.tsv"
  workspace_samples="$sample_root/workspace-$run_number.tsv"
  : >"$evaluation_samples"
  : >"$workspace_samples"
  sample_id=0
  terminal_status=""

  while true; do
    record_stack_sample "$evaluation_samples" "$sample_id"
    workspace_bytes="$(workspace_bytes_for_evaluation "$evaluation_id")"
    printf '%s\t%s\t%s\n' "$sample_id" "$(monotonic_ns)" "$workspace_bytes" >>"$workspace_samples"

    status_response="$runtime_root/evaluation-status-$run_number.json"
    curl --fail-with-body --silent --show-error \
      "http://127.0.0.1:18000/api/v1/evaluations/$evaluation_id" >"$status_response"
    current_status="$(python3 -c 'import json,sys; print(str(json.load(open(sys.argv[1], encoding="utf-8"))["status"]).lower())' "$status_response")"
    case "$current_status" in
      succeeded|failed|cancelled)
        terminal_status="$current_status"
        break
        ;;
    esac

    now_ns="$(monotonic_ns)"
    if (( (now_ns - started_ns) / 1000000000 >= evaluation_timeout_seconds )); then
      terminal_status="timeout"
      break
    fi
    sample_id=$((sample_id + 1))
  done

  finished_ns="$(monotonic_ns)"
  db_after="$(database_size_bytes)"
  artifact_bytes="$(artifact_bytes_for_evaluation "$evaluation_id")"

  python3 - \
    "$run_number" "$evaluation_id" "$terminal_status" "$started_ns" "$finished_ns" \
    "$db_before" "$db_after" "$artifact_bytes" "$evaluation_samples" "$workspace_samples" \
    >>"$run_records" <<'PY'
import json
import math
import statistics
import sys
from pathlib import Path

(
    run_number, evaluation_id, status, started_ns, finished_ns, db_before,
    db_after, artifact_bytes, stack_path, workspace_path,
) = sys.argv[1:]

UNITS = {
    "B": 1,
    "kB": 1000,
    "MB": 1000 ** 2,
    "GB": 1000 ** 3,
    "TB": 1000 ** 4,
    "KiB": 1024,
    "MiB": 1024 ** 2,
    "GiB": 1024 ** 3,
    "TiB": 1024 ** 4,
}

def memory_bytes(value: str) -> int:
    amount = value.split("/", 1)[0].strip()
    for unit in sorted(UNITS, key=len, reverse=True):
        if amount.endswith(unit):
            return int(round(float(amount[:-len(unit)].strip()) * UNITS[unit]))
    raise ValueError(f"unsupported Docker memory value: {value!r}")

def summarize(values):
    if not values:
        return {"average": None, "peak": None}
    return {"average": statistics.fmean(values), "peak": max(values)}

samples = {}
for line in Path(stack_path).read_text(encoding="utf-8").splitlines():
    sample_id, timestamp_ns, service, cpu, memory = line.split("\t", 4)
    item = samples.setdefault(sample_id, {"timestamp_ns": int(timestamp_ns), "services": {}})
    item["services"][service] = {
        "cpu": float(cpu.rstrip("%")),
        "memory": memory_bytes(memory),
    }

services = {name: {"memory": [], "cpu": []} for name in ("db", "api", "worker")}
total_memory = []
total_cpu = []
for sample in samples.values():
    if set(sample["services"]) != set(services):
        continue
    for name in services:
        services[name]["memory"].append(sample["services"][name]["memory"])
        services[name]["cpu"].append(sample["services"][name]["cpu"])
    total_memory.append(sum(sample["services"][name]["memory"] for name in services))
    total_cpu.append(sum(sample["services"][name]["cpu"] for name in services))

workspace_values = []
for line in Path(workspace_path).read_text(encoding="utf-8").splitlines():
    _, _, value = line.split("\t", 2)
    workspace_values.append(int(value))

elapsed_seconds = (int(finished_ns) - int(started_ns)) / 1_000_000_000
worker_cpu_average = statistics.fmean(services["worker"]["cpu"]) if services["worker"]["cpu"] else None
record = {
    "run": int(run_number),
    "evaluation_id": evaluation_id,
    "terminal_status": status,
    "elapsed_seconds": elapsed_seconds,
    "sample_count": len(total_memory),
    "db_memory_average_bytes": statistics.fmean(services["db"]["memory"]) if services["db"]["memory"] else None,
    "db_memory_peak_bytes": max(services["db"]["memory"]) if services["db"]["memory"] else None,
    "api_memory_average_bytes": statistics.fmean(services["api"]["memory"]) if services["api"]["memory"] else None,
    "api_memory_peak_bytes": max(services["api"]["memory"]) if services["api"]["memory"] else None,
    "worker_memory_average_bytes": statistics.fmean(services["worker"]["memory"]) if services["worker"]["memory"] else None,
    "worker_memory_peak_bytes": max(services["worker"]["memory"]) if services["worker"]["memory"] else None,
    "total_memory_average_bytes": statistics.fmean(total_memory) if total_memory else None,
    "total_memory_peak_bytes": max(total_memory) if total_memory else None,
    "worker_cpu_average_percent": worker_cpu_average,
    "worker_cpu_peak_percent": max(services["worker"]["cpu"]) if services["worker"]["cpu"] else None,
    "worker_cpu_seconds_approx": elapsed_seconds * worker_cpu_average / 100 if worker_cpu_average is not None else None,
    "total_cpu_average_percent": statistics.fmean(total_cpu) if total_cpu else None,
    "total_cpu_peak_percent": max(total_cpu) if total_cpu else None,
    "workspace_peak_bytes": max(workspace_values) if workspace_values else 0,
    "artifact_bytes": int(artifact_bytes),
    "database_size_before_bytes": int(db_before),
    "database_size_after_bytes": int(db_after),
    "database_growth_bytes": int(db_after) - int(db_before),
}
print(json.dumps(record, separators=(",", ":")))
PY

  if [ "$terminal_status" != "succeeded" ]; then
    all_runs_succeeded=false
    "${compose[@]}" logs worker >&2 || true
    break
  fi
done

architecture="$(uname -m)"
cpu_count="$(nproc)"
host_memory_bytes="$(awk '/MemTotal:/ {printf "%.0f\n", $2 * 1024}' /proc/meminfo)"
docker_version="$(docker version --format '{{.Server.Version}}')"
image_id="$(docker image inspect "$image" --format '{{.Id}}')"
git_sha="$(git -C "$repository_root" rev-parse HEAD)"

python3 - \
  "$fixture_path" "$source_dir" "$image" "$architecture" "$cpu_count" "$host_memory_bytes" \
  "$docker_version" "$image_id" "$git_sha" "$idle_started_ns" "$idle_finished_ns" \
  "$idle_samples" "$run_records" "$result_path" "$sample_interval_seconds" \
  "$requested_runs" "$all_runs_succeeded" "$benchmark_cropsuite_max_workers" <<'PY'
import json
import statistics
import sys
from pathlib import Path

(
    fixture_path, source_dir, image, architecture, cpu_count, host_memory_bytes,
    docker_version, image_id, git_sha, idle_started_ns, idle_finished_ns,
    idle_path, run_records_path, result_path, sample_interval, requested_runs,
    all_runs_succeeded, cropsuite_max_workers,
) = sys.argv[1:]

UNITS = {
    "B": 1, "kB": 1000, "MB": 1000 ** 2, "GB": 1000 ** 3, "TB": 1000 ** 4,
    "KiB": 1024, "MiB": 1024 ** 2, "GiB": 1024 ** 3, "TiB": 1024 ** 4,
}

def memory_bytes(value: str) -> int:
    amount = value.split("/", 1)[0].strip()
    for unit in sorted(UNITS, key=len, reverse=True):
        if amount.endswith(unit):
            return int(round(float(amount[:-len(unit)].strip()) * UNITS[unit]))
    raise ValueError(f"unsupported Docker memory value: {value!r}")

def metric(values):
    return {
        "average": statistics.fmean(values) if values else None,
        "peak": max(values) if values else None,
    }

def min_median_max(values):
    values = [value for value in values if value is not None]
    if not values:
        return {"min": None, "median": None, "max": None}
    return {"min": min(values), "median": statistics.median(values), "max": max(values)}

idle_samples = {}
for line in Path(idle_path).read_text(encoding="utf-8").splitlines():
    sample_id, timestamp_ns, service, cpu, memory = line.split("\t", 4)
    sample = idle_samples.setdefault(sample_id, {"timestamp_ns": int(timestamp_ns), "services": {}})
    sample["services"][service] = {
        "cpu": float(cpu.rstrip("%")),
        "memory": memory_bytes(memory),
    }

idle_by_service = {name: {"memory": [], "cpu": []} for name in ("db", "api", "worker")}
idle_total_memory = []
idle_total_cpu = []
for sample in idle_samples.values():
    if set(sample["services"]) != set(idle_by_service):
        continue
    for name in idle_by_service:
        idle_by_service[name]["memory"].append(sample["services"][name]["memory"])
        idle_by_service[name]["cpu"].append(sample["services"][name]["cpu"])
    idle_total_memory.append(sum(sample["services"][name]["memory"] for name in idle_by_service))
    idle_total_cpu.append(sum(sample["services"][name]["cpu"] for name in idle_by_service))

idle = {
    "duration_seconds": (int(idle_finished_ns) - int(idle_started_ns)) / 1_000_000_000,
    "sample_count": len(idle_total_memory),
}
for name in idle_by_service:
    idle[f"{name}_memory_average_bytes"] = statistics.fmean(idle_by_service[name]["memory"]) if idle_by_service[name]["memory"] else None
    idle[f"{name}_memory_peak_bytes"] = max(idle_by_service[name]["memory"]) if idle_by_service[name]["memory"] else None
    idle[f"{name}_cpu_average_percent"] = statistics.fmean(idle_by_service[name]["cpu"]) if idle_by_service[name]["cpu"] else None
    idle[f"{name}_cpu_peak_percent"] = max(idle_by_service[name]["cpu"]) if idle_by_service[name]["cpu"] else None
idle["total_memory_average_bytes"] = statistics.fmean(idle_total_memory) if idle_total_memory else None
idle["total_memory_peak_bytes"] = max(idle_total_memory) if idle_total_memory else None
idle["total_cpu_average_percent"] = statistics.fmean(idle_total_cpu) if idle_total_cpu else None
idle["total_cpu_peak_percent"] = max(idle_total_cpu) if idle_total_cpu else None

runs = [json.loads(line) for line in Path(run_records_path).read_text(encoding="utf-8").splitlines() if line]
successful = [run for run in runs if run["terminal_status"] == "succeeded"]
aggregate = {
    "successful_runs": len(successful),
    "elapsed_seconds": min_median_max([run["elapsed_seconds"] for run in successful]),
    "worker_memory_peak_bytes": min_median_max([run["worker_memory_peak_bytes"] for run in successful]),
    "total_memory_peak_bytes": min_median_max([run["total_memory_peak_bytes"] for run in successful]),
    "workspace_peak_bytes": min_median_max([run["workspace_peak_bytes"] for run in successful]),
    "artifact_bytes": min_median_max([run["artifact_bytes"] for run in successful]),
}

observed_peak = max(
    [value for value in [idle.get("total_memory_peak_bytes")] + [run.get("total_memory_peak_bytes") for run in successful] if value is not None],
    default=None,
)
headroom = {
    "observed_total_stack_peak_bytes": observed_peak,
    "plus_30_percent_bytes": int(round(observed_peak * 1.30)) if observed_peak is not None else None,
    "plus_50_percent_bytes": int(round(observed_peak * 1.50)) if observed_peak is not None else None,
}

fixture = json.loads(Path(fixture_path).read_text(encoding="utf-8"))
result = {
    "schema_version": 1,
    "valid_scientific_benchmark": all_runs_succeeded == "true" and len(successful) == int(requested_runs),
    "environment": {
        "architecture": architecture,
        "cpu_count": int(cpu_count),
        "host_memory_bytes": int(host_memory_bytes),
        "docker_version": docker_version,
        "image": image,
        "image_id": image_id,
        "git_sha": git_sha,
        "cropsuite_max_workers": int(cropsuite_max_workers),
    },
    "fixture": {
        "fixture_path": str(Path(fixture_path).resolve()),
        "scientific_source_directory": str(Path(source_dir).resolve()),
        "repeatable": fixture["repeatable"],
        "requested_crops": fixture["evaluation"]["requested_crops"],
        "environmental_input_count": len(fixture["environmental_inputs"]),
    },
    "measurement": {
        "sampling_interval_seconds_target": float(sample_interval),
        "memory_definition": "Docker-reported container MemUsage current usage for db/api/worker; total is their observed sum per sample.",
        "cpu_definition": "Docker-reported CPUPerc; 100% is approximately one fully utilized host CPU core and values can exceed 100% on multicore hosts.",
        "workspace_definition": "Peak du -sb bytes for /var/lib/via/workspace entries prefixed by the evaluation id while the evaluation is active.",
        "artifact_definition": "du -sb bytes below /var/lib/via/artifacts/evaluations/<evaluation_id> after terminal state.",
        "database_definition": "pg_database_size(current_database()) immediately before and after each evaluation; growth is after minus before.",
        "elapsed_definition": "Python time.monotonic_ns() from evaluation POST start through observed terminal status.",
    },
    "idle": idle,
    "evaluation_runs": runs,
    "aggregate": aggregate,
    "ram_headroom": headroom,
}

output = Path(result_path)
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

def mib(value):
    return "n/a" if value is None else f"{value / (1024 ** 2):.1f} MiB"

print("B6.1 resource benchmark")
print(f"  valid scientific benchmark: {result['valid_scientific_benchmark']}")
print(f"  host: {architecture}, {cpu_count} CPUs, {mib(int(host_memory_bytes))} RAM")
print(f"  idle samples: {idle['sample_count']}, total peak: {mib(idle['total_memory_peak_bytes'])}")
for run in runs:
    print(
        f"  run {run['run']}: status={run['terminal_status']} elapsed={run['elapsed_seconds']:.2f}s "
        f"worker_peak={mib(run['worker_memory_peak_bytes'])} total_peak={mib(run['total_memory_peak_bytes'])} "
        f"workspace_peak={mib(run['workspace_peak_bytes'])} artifact_bytes={run['artifact_bytes']} "
        f"db_growth_bytes={run['database_growth_bytes']}"
    )
print(f"  result: {output}")
PY

if [ "$all_runs_succeeded" != "true" ]; then
  fail "at least one scientific evaluation did not reach SUCCEEDED; the JSON is diagnostic and must not be used for VPS sizing."
fi
