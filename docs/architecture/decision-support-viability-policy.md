# Decision Support viability policy

The current global default is an immutable `ViabilityPolicySnapshot` selected by
`decision_support.default_viability_policy`. Migration `20260927_0018` seeds
`via-policy:1` with conditional 40 and viable 70 only if the pointer is absent.
It never replaces an existing pointer. A conflicting pre-existing `via-policy:1`
causes migration failure instead of silently using different baseline values.

An authenticated user can read the global default. Only an administrator can
replace it. The PUT request carries the identifier and version seen by the
client. The server checks that reference, validates thresholds in Domain,
generates a new version, and uses a compare-and-set pointer update. Unchanged
values return the current snapshot. A stale request returns HTTP 409.

Evaluation creation resolves its authorized parcel and validates the request,
then binds the new evaluation UUID to the current policy before persisting the
evaluation. The worker does not select the default. The binding is stored only
in Decision Support; its evaluation UUID is opaque, with no cross-context FK.
It is insert-only for evaluations that exist. A binding insert for the same
UUID and reference is idempotent; another reference is rejected.

The two writes are separate transactions to preserve bounded-context ownership.
Binding first prevents a persisted new evaluation without a policy. If
evaluation persistence fails, composition checks whether the evaluation exists
and removes the orphan binding only when it does not. If the process crashes
between these operations, an orphan binding can remain; it cannot change or
reclassify an evaluation, and an operator may safely clean it up after checking
that the evaluation UUID is absent. A future transaction coordinator could
remove this narrow orphan window.

Legacy evaluations receive no invented binding. The policy lookup returns
`policy_not_recorded` with a null policy. Classification of finalized
evaluations loads the bound snapshot, never the current default. It preserves
the scientific mean and rank and returns no classification when comparable
evidence is unavailable. Queued and running evaluations retain the binding
while scientific execution proceeds.
