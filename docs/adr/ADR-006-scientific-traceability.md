# ADR-006: Scientific traceability

## Status

Accepted

## Context

Parcels, inputs, parameters, engine code, and configurations can change. Historical results must remain interpretable and must not be silently reassigned to current geometry or current data.

## Decision

Preserve an immutable `ParcelSnapshot`, exact versions and checksums of inputs and crop parameters, effective scientific configuration, engine version or commit, relevant dependency versions, scenario, management, spatial and aggregation methods, attempts, timestamps, artifact checksums, and result evidence.

## Consequences

Storage and schemas must support versioned references and immutable historical interpretation. Audit data and scientific evidence remain distinct. Reuse is allowed only when a compatibility identity proves that all result-affecting inputs match.

## Current implementation status

The PoC already writes the parcel snapshot, source and engine hashes, configuration hashes, artifact hashes, method metadata, timestamps, and a source-unchanged check into local evaluation outputs. It does not provide application persistence, user audit, durable dataset records, or a complete dependency lock record.

## Source

Sections 5, 14, 18, and 20 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx) and [`CropSuiteLite/src/multicrop.py`](../../CropSuiteLite/src/multicrop.py).
