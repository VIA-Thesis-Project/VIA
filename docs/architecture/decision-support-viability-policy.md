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

Each authenticated user can read and save personal thresholds through
`/api/v1/decision-support/my-viability-policy`. The identity comes from the
session, never from a user identifier supplied in the request. Personal pointers
are stored in `decision_support.user_viability_policies`; the user UUID is opaque
and has no cross-context foreign key. Migration `20261001_0020` creates this table
without modifying existing defaults or historical evaluation bindings.

Before a user saves personal settings, their effective configuration falls back
to the global default. Saving creates or selects an immutable policy version and
updates only their pointer using optimistic concurrency. A stale reference or
concurrent first save returns HTTP 409. Saving values equal to the default also
records a personal selection, so later global changes do not alter saved settings.

Evaluation creation resolves its authorized parcel and validates the request,
then binds the new evaluation UUID to its owner's effective personal policy before
persisting the evaluation. The worker does not select the policy. The binding is stored only
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
evaluations loads the bound snapshot, never current personal or global settings. It preserves
the scientific mean and rank and returns no classification when comparable
evidence is unavailable. Queued and running evaluations retain the binding
while scientific execution proceeds.
