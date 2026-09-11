# Proposed bounded contexts

The contexts below are the current modeling hypothesis for the VIA modular monolith. They organize language, rules, and data ownership, not deployment units. Use cases and business events may refine these boundaries before implementation.

## Identity and Access

**Responsibility.** Identify users and administer memberships, roles, and authorization for projects and resources.

**Owned model and data.** User identity references, memberships, roles, and access permissions.

**Public collaboration.** Supplies authenticated identity and authorization decisions to Farm Management and other entry points that operate on protected resources.

**Must not access directly.** Parcel internals, environmental datasets, evaluation aggregates, scientific artifacts, or decision-support rules. It must not authorize by querying another context's tables directly.

## Farm Management

**Responsibility.** Manage agricultural projects and parcels, including immutable geometry versions.

**Owned model and data.** Project, Parcel, ParcelVersion, geometry, and parcel metadata.

**Public collaboration.** Uses Identity and Access authorization. Publishes an authorized parcel description and exact version to Agroclimatic Evaluation, which creates its own `ParcelSnapshot`.

**Must not access directly.** Evaluation repositories, CropSuiteLite, environmental storage paths, or recommendation internals. It must not rewrite historical evaluation snapshots when a parcel changes.

## Environmental Information

**Responsibility.** Catalog geoenvironmental inputs and determine their coverage, quality, version, and compatibility.

**Owned model and data.** Dataset, DatasetVersion, layer metadata, source, variable, unit, CRS, resolution, extent, validity mask, time period, scenario, checksum, and storage reference.

**Public collaboration.** Provides stable coverage and compatible-input descriptions. Agroclimatic Evaluation consumes these through its own port and anti-corruption adapter, for example as an `EnvironmentalInputManifest`.

**Must not access directly.** Evaluation aggregates, parcel repositories, user-role tables, or Decision Support rules. It must not decide suitability or recommendations.

## Agroclimatic Evaluation

**Responsibility.** Manage evaluation requests, execution, results, status transitions, and reproducible scientific evidence.

**Owned model and data.** Evaluation, exact `ParcelSnapshot`, execution or `ScientificRun`, per-crop result, evidence, artifact references, attempts, timestamps, and state.

**Public collaboration.** Obtains an authorized parcel version from Farm Management and compatible dataset versions from Environmental Information. Uses `ICropSuitabilityEngine`; Infrastructure supplies `CropSuiteAdapter`. Publishes completed results and evidence to Decision Support through stable contracts or an idempotent integration event.

**Must not access directly.** Another context's entities, repositories, or tables. Domain must not depend on CropSuiteLite, HTTP, a queue, an ORM, or filesystem paths.

## Decision Support

**Responsibility.** Compare compatible alternatives and, when sufficient evidence and explicit criteria exist, provide explanations or recommendations.

**Owned model and data.** Comparison criteria, decision-support views, explanations, and any future recommendation rules and provenance.

**Public collaboration.** Consumes finalized evaluation results, factors, coverage, and evidence. It may react to an `EvaluationCompleted`-style integration event and retrieve the authorized details it needs.

**Must not access directly.** CropSuiteLite, raw evaluation tables, parcel internals, environmental repositories, or identity tables. It must not silently modify scientific scores or present suitability as profitability.

## Collaboration rules

- A context changes its state only through its own use cases and repositories.
- Collaboration uses stable public contracts; sharing PostgreSQL does not make models public.
- Local interfaces are sufficient inside the monolith. Events are useful only when deferred reaction is needed.
- Cross-context reactions must tolerate duplicates and retries.
- If two contexts repeatedly require shared entities and atomic changes, revisit the boundary before adding coordination machinery.
- Technical names such as Jobs, Reports, or Repositories do not by themselves define bounded contexts.

## Open modeling questions

The exact boundaries remain subject to use-case modeling. In particular, Experiments is not initially required merely to store hashes; it becomes a candidate if hypotheses, study designs, trial sets, and scientific comparisons gain an independent lifecycle. Organizations, campaigns, and varieties are possible later concepts, not first-increment requirements.

## Source

See sections 4, 5, and 10 of [`Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx`](../Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx).
