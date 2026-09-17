# syntax=docker/dockerfile:1

FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIA_CROPSUITE_ROOT=/opt/via/CropSuiteLite \
    VIA_CROPSUITE_PYTHON=/usr/local/bin/python \
    VIA_CROPSUITE_WORKSPACE=/var/lib/via/workspace \
    VIA_ARTIFACTS_ROOT=/var/lib/via/artifacts

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

RUN groupadd --system via \
    && useradd --system --gid via --home-dir /nonexistent --shell /usr/sbin/nologin via \
    && mkdir -p /etc/via /var/lib/via/workspace /var/lib/via/artifacts \
    && chown -R via:via /var/lib/via/workspace /var/lib/via/artifacts \
    && chmod -R a+rX,a-w /opt/via/backend /opt/via/CropSuiteLite

USER via
WORKDIR /opt/via/backend

# Build-time smoke runs as the final non-root user. It verifies scientific
# imports, console scripts, pip consistency, and filesystem permissions without
# requiring PostgreSQL, datasets, bindings, credentials, or network access.
RUN python /opt/via/backend/scripts/verify_container_runtime.py --require-linux

# B3 owns production API/worker process commands and orchestration. Intentionally
# inherit the base image's neutral Python command in B2.
