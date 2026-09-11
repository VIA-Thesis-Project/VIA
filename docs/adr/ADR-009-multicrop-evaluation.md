# ADR-009: Multicrop evaluation

## Status

Implemented in PoC

## Context

Users need to evaluate one parcel against multiple selected crops while retaining the outcome and evidence of every alternative. A failure or lack of coverage for one crop must not erase successful outcomes for others.

## Decision

Treat one parcel plus a unique non-empty list of crop identifiers as one multicrop request. Preserve independent per-crop status, results, logs, and artifacts. Summarize each crop on valid parcel-intersection area and rank only on common valid support; report failures and exclusions explicitly.

## Consequences

Consumers must inspect both request and per-crop outcomes. Nodata is excluded, while a valid zero participates in summaries and ranking. No common coverage means no ranking. A higher rank is not proof of profitability or agronomic validation.

## Current implementation status

Implemented in [`CropSuiteLite/src/multicrop.py`](../../CropSuiteLite/src/multicrop.py), exposed through [`CropSuiteLite/evaluate.py`](../../CropSuiteLite/evaluate.py), and tested in [`CropSuiteLite/tests/test_multicrop.py`](../../CropSuiteLite/tests/test_multicrop.py). The real engine flow was technically checked with maize, potato, and rice; this does not validate every catalog entry or establish field agronomy.

## Source

Sections 2, 13, 15, 18, 20, and 22 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx) and the PoC files cited above.
