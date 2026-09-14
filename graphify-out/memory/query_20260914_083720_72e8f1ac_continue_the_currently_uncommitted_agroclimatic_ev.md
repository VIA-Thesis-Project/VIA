---
type: "query"
date: "2026-09-14T08:37:20.365216+00:00"
question: "Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment."
contributor: "graphify"
outcome: "useful"
source_nodes: ["Evaluation", "EvaluationRepository", "AgroclimaticEvaluationService", "EvaluationResult"]
---

# Q: Continue the currently uncommitted Agroclimatic Evaluation Query/Read API increment.

## Answer

Expanded from the request via graph vocabulary: [evaluation, result, public, contract, application, repository, evidence, execution, status, service]. The increment reuses EvaluationRepository.get through AgroclimaticEvaluationService, maps Evaluation into explicit status/result/evidence read models, and publishes an Application-owned FinalizedEvaluationResult contract only for succeeded evaluations. HTTP omits execution_reference and raw failure diagnostics; focused tests, Ruff, Pyright, and Import Linter pass.

## Outcome

- Signal: useful

## Source Nodes

- Evaluation
- EvaluationRepository
- AgroclimaticEvaluationService
- EvaluationResult