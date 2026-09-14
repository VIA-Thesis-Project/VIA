---
type: "query"
date: "2026-09-14T02:07:58.771538+00:00"
question: "Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors"
contributor: "graphify"
outcome: "useful"
source_nodes: ["AgroclimaticEvaluationExecutionService", "EvaluationResult", "ExecuteEvaluation", "ResourceConflictError", "Settings"]
---

# Q: Trace the worker executor result protocol and configuration typing relevant to the ten Pyright errors

## Answer

Expanded from the original request via graph vocab: [worker, evaluation, execute, execution, result, service, command, config, settings, recoverable]. The graph connected AgroclimaticEvaluationWorker to ExecuteEvaluation, EvaluationResult, AgroclimaticEvaluationExecutionService, ResourceConflictError, and Settings. This supported test-only fixes: the recording executor now returns EvaluationResult while production execution remains owned by the execution service, and the config validation cases use typed factories instead of a heterogeneous kwargs dictionary.

## Outcome

- Signal: useful

## Source Nodes

- AgroclimaticEvaluationExecutionService
- EvaluationResult
- ExecuteEvaluation
- ResourceConflictError
- Settings