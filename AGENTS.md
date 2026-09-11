## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
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
