# ADR-007: Initial deployment

## Status

Accepted

## Context

The first public deployment needs to fit a thesis-scale budget while keeping short HTTP work separate from long calculations.

## Decision

Use one small VPS initially for the modular backend, queue, and worker in separate processes or containers, with low-cost or free supporting services where their terms and limits fit. A static frontend and managed PostgreSQL/PostGIS/authentication are planning options. This accepts the deployment shape and budget direction, not a particular provider or capacity.

## Consequences

Operations must include HTTPS, secret management, process restart, resource limits, logs, persistent storage, backups, and recovery tests. Capacity must be measured with uncached runs before selecting a server or worker count. Provider pricing, free-tier conditions, IPv4, taxes, retention, and transfer remain risks.

## Current implementation status

No public backend deployment or supporting service has been provisioned. The indicative budget is approximately USD 15–20 per month, subject to confirmation.

## Source

Sections 16 through 20 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx).
