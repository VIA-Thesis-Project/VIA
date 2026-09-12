## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- For implementation tasks that touch multiple files or module boundaries,
  query Graphify before broad source browsing. Use the returned subgraph to
  decide which source files and ADRs need to be read; do not read the whole
  repository unless necessary.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

# VIA Architecture Guardrails

- `docs/Arquitectura_y_backend_CropSuiteLite_Huaura_v2.docx` is the original architecture design source. Do not modify it when maintaining repository-native guidance.
- `docs/architecture/` and `docs/adr/` are the repository-native architecture guidance. Preserve the decision status and open questions recorded there.
- `CropSuiteLite/` is the existing scientific engine. Do not rewrite it as part of backend restructuring.
- Respect bounded-context ownership; collaborate through public contracts rather than another context's entities, repositories, or tables.
- Domain must not depend on Infrastructure or HTTP concerns.
- REST controllers must not call CropSuiteLite directly.
- Access CropSuiteLite through the `ICropSuitabilityEngine` application port and the infrastructure `CropSuiteAdapter`.
- Run long calculations outside the HTTP request process, using a recoverable background worker flow.
- Historical evaluations must retain the exact `ParcelSnapshot` and versions used for calculation.
- Nodata means unavailable information; it is not suitability zero.
- Do not change scientific parameters, units, masks, interpolation, scoring, or other scientific rules merely to satisfy software tests.
- Before architecture-impacting changes, query Graphify and inspect the relevant ADRs.
- After architecture-impacting changes, run the relevant tests and update Graphify.

## Backend verification workflow

For backend implementation tasks:

- Use Graphify first to identify the relevant architecture, symbols, and files.
- Prefer focused source inspection based on the Graphify subgraph instead of broad repository browsing.
- Use `rg` for exact symbol/import searches after Graphify has narrowed the scope.
- During implementation, run focused pytest tests for the affected module rather than repeatedly running the full suite.
- Use Ruff for mechanical lint/import issues.
- Use Pyright for static type verification.
- Use Import Linter for architectural dependency contracts.
- Run the full backend verification suite only near the end of an increment.
- After code changes, update Graphify incrementally.

Preferred order:

1. Graphify query
2. Inspect selected files
3. Implement
4. Focused pytest
5. Ruff
6. Pyright
7. Import Linter
8. Full pytest
9. Graphify update
10. Git diff review

- Do not repeatedly run the full test suite while iterating on a local change when focused tests are sufficient.
- Do not broadly read the repository after Graphify has already identified the relevant subgraph unless the task requires broader context.
- When verification commands may take noticeable time or produce large output, prefer asking the user to run them manually and return the results.
