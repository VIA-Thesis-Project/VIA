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

VIA now preserves the runtime scientific-source evidence accepted by the A5.4
integrity gate. The provenance chain is `EnvironmentalInputManifest` -> configured
A5.4 DatasetVersion-to-source binding -> CropSuiteLite `source_sha256` report ->
runtime integrity verification -> ordered, durable per-crop source fingerprints.
The exact tuple verified before result mapping is the tuple carried into the
application result, mapped into the domain trace, and persisted with the crop
outcome.

`source_reference` is opaque internal engine evidence. Current CropSuiteLite
values may be host-local absolute paths; VIA does not normalize them, interpret
them as `EnvironmentalInputSnapshot.storage_reference`, or expose them through
Decision Support or the HTTP evidence resource. The HTTP evidence projection
publishes only the ordered SHA-256 values. `DatasetVersion.checksum` remains a
separate opaque dataset-version checksum and is not treated as a per-file
CropSuiteLite SHA-256.

`source_files_unchanged` retains its original meaning as the post-run mutation
signal. Durable source fingerprints describe the actual pre-run source identities
reported by CropSuiteLite and accepted by the integrity verifier. Historical crop
outcomes created before A6 remain valid and hydrate with an empty fingerprint
tuple.

The PoC still does not provide a complete engine/dependency lock record or all
long-term audit evidence described by the target architecture.

## Source

Sections 5, 14, 18, and 20 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx) and [`CropSuiteLite/src/multicrop.py`](../../CropSuiteLite/src/multicrop.py).
