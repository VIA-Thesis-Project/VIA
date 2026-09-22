# syntax=docker/dockerfile:1

FROM python:3.11-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libexpat1 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/tmp \
    MPLCONFIGDIR=/tmp/matplotlib \
    VIA_CROPSUITE_ROOT=/opt/via/CropSuiteLite \
    VIA_CROPSUITE_PYTHON=/usr/local/bin/python \
    VIA_CROPSUITE_WORKSPACE=/var/lib/via/workspace \
    VIA_ARTIFACTS_ROOT=/var/lib/via/artifacts \
    VIA_CROPSUITE_INPUT_BINDINGS=/etc/via/input-bindings.json \
    VIA_ALEMBIC_CONFIG=/opt/via/backend/alembic.ini

WORKDIR /opt/via

# CropSuiteLite lists `tk`, but the VIA scientific path does not import tkinter.
# Exclude only that non-portable packaging artifact and keep every other
# scientific requirement and version exactly as declared by CropSuiteLite.
COPY CropSuiteLite/requirements.txt /tmp/cropsuite-requirements.txt
RUN grep -v -E '^[[:space:]]*tk[[:space:]]*$' \
        /tmp/cropsuite-requirements.txt \
        > /tmp/cropsuite-container-requirements.txt \
    && python -m pip install --no-cache-dir -r /tmp/cropsuite-container-requirements.txt \
    && rm /tmp/cropsuite-requirements.txt /tmp/cropsuite-container-requirements.txt

COPY backend /opt/via/backend
RUN python -m pip install --no-cache-dir /opt/via/backend \
    && python -m pip check

COPY CropSuiteLite /opt/via/CropSuiteLite
COPY data/huaura/boundary/huaura_province.geojson /opt/via/data/huaura/boundary/huaura_province.geojson
COPY data/huaura/boundary/metadata.json /opt/via/data/huaura/boundary/metadata.json

RUN groupadd --system via \
    && useradd --system --gid via --home-dir /nonexistent --shell /usr/sbin/nologin via \
    && mkdir -p /etc/via /mnt/via/sources /var/lib/via/workspace /var/lib/via/artifacts /var/lib/via/knowledge/sources \
    && chown -R via:via /var/lib/via/workspace /var/lib/via/artifacts \
    && chmod -R a+rX,a-w /opt/via/backend /opt/via/CropSuiteLite /opt/via/data /etc/via /mnt/via/sources /var/lib/via/knowledge/sources

USER via
WORKDIR /opt/via/backend

# Build-time smoke runs as the final non-root user. It verifies scientific
# imports, console scripts, pip consistency, and filesystem permissions without
# requiring PostgreSQL, datasets, bindings, credentials, or network access.
RUN python /opt/via/backend/scripts/verify_container_runtime.py --require-linux

CMD ["via-api"]
