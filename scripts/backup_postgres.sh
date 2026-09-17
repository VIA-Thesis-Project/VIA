#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

backup_dir="${VIA_POSTGRES_BACKUP_DIR:-/srv/via/backups/postgres}"
test -d "${backup_dir}" || {
  echo "ERROR: backup directory does not exist: ${backup_dir}" >&2
  exit 1
}

mapfile -t db_containers < <(
  docker ps \
    --filter 'label=com.docker.compose.project=via' \
    --filter 'label=com.docker.compose.service=db' \
    --format '{{.ID}}'
)
if [ "${#db_containers[@]}" -ne 1 ]; then
  echo "ERROR: expected exactly one running VIA db container; found ${#db_containers[@]}." >&2
  exit 1
fi

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup_name="via-${timestamp}.dump"
backup_path="${backup_dir}/${backup_name}"
temporary_path="${backup_path}.tmp"
trap 'rm -f "${temporary_path}"' EXIT

docker exec "${db_containers[0]}" sh -ec \
  'exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=custom --no-owner --no-privileges' \
  > "${temporary_path}"
test -s "${temporary_path}"
mv "${temporary_path}" "${backup_path}"
(
  cd "${backup_dir}"
  sha256sum "${backup_name}" > "${backup_name}.sha256"
)

if [ -n "${VIA_BACKUP_RETENTION_DAYS:-}" ]; then
  [[ "${VIA_BACKUP_RETENTION_DAYS}" =~ ^[0-9]+$ ]] || {
    echo "ERROR: VIA_BACKUP_RETENTION_DAYS must be a non-negative integer." >&2
    exit 1
  }
  find "${backup_dir}" -type f \
    \( -name 'via-*.dump' -o -name 'via-*.dump.sha256' \) \
    -mtime "+${VIA_BACKUP_RETENTION_DAYS}" -delete
fi

echo "PostgreSQL backup created: ${backup_path}"
