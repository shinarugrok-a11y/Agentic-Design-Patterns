# Agent Academy — Scenario Contract (v0.1.0, unpiloted)

**Status:** EXPERIMENTAL. This is a proposal. No engine implements it, no scenario has been authored against it, and no learner or agent has run it. Every field name, enum and default may change after the first pilot.

**Labels:** as in [RECONCILIATION §3](RECONCILIATION.md#3-provenance-labels-one-scheme). A field's *existence* is EXPERIMENTAL unless marked otherwise. Where a field encodes something the book says, the anchor is given as `GT:L…` into `ground-truth/agentic_design_patterns.txt`.

**Companion:** [EVALUATION-CONTRACT.md](EVALUATION-CONTRACT.md) says how runs of these scenarios are graded, and how their traces are reviewed and promoted.

**Supersedes:** DESIGN-ANALYSIS Q15.3 (trace schema). That trace schema is split here into a scenario definition (§2) and an event stream (§4). Its lifecycle and promotion rules moved to EVALUATION-CONTRACT §6.

---

## 1. Design rules

1. **The engine enforces governance from the first scenario** (implementation dependency, [RECONCILIATION §4.2](RECONCILIATION.md#42-dependencies-implementation-vs-teaching-u-2)). Policy gates, exception propagation, budget accounting and the event log exist in every scenario. The `disclosure_tier` controls only what the learner is *told*, never what the engine *does*.
2. **Three state partitions, no leakage.** `world_state` is the full simulated world. `visible_state` is what the actor may observe. `hidden_state` holds the ground truth and the injection schedule. A contestant, human or agent, can only reach `hidden_state` through the observations the engine emits. Engine code that leaks hidden state into an actor-visible channel is a contract violation (EVALUATION-CONTRACT INV-E1).
3. **Determinism.** Given `(scenario_id, version, engine_version, seed, perturbation_schedule)` and the same actor decisions, the engine emits the same event stream with the same hash chain. Live-model contestants are non-deterministic, so determinism applies to the *engine side* only. Model outputs are recorded, not replayed as predictions.
4. **No unobservable punishment.** Every injected failure must declare at least one `detection_signal` that is present at `operator` visibility before the failure's consequences become irreversible. A scenario that violates this fails authoring validation. This carries forward DESIGN-ANALYSIS Q7's rule.
5. **No fake chain-of-thought.** The engine never shows or stores an "inner monologue". Decisions carry `structured_rationale` (reason codes plus evidence references). Text a live model produces about its own reasoning is stored as `model_stated_explanation`, labelled as model output, never as mechanism. This follows App F's caution (DESIGN-ANALYSIS W-13; GT:L16127). It is reconciled with Ch 18's "its reasoning for the next step" logging advice (GT:L11796–L11797) in [RECONCILIATION §4.7](RECONCILIATION.md#47-what-the-player-sees-forensics-u-89).
6. **One scenario, many contestants.** The same scenario file runs for human learners, simulated agents and live-model contestants ("Agent Mode"). Contestant-specific adapters may change the *rendering* of `visible_state` (UI vs text/JSON). They may not change its *content*.
7. **Provenance travels with content.** Any book-derived text the scenario shows the actor, such as a Pattern Library card or a hint, is referenced by claim id and label, not pasted untraceably.

## 2. Scenario schema

Types are informal: `str`, `int`, `enum{…}`, `[T]` for a list, `{…}` for an object, `?` for optional.

### 2.1 Identity and versioning

| Field | Type | Meaning |
| --- | --- | --- |
| `scenario_id` | str | Stable id, e.g. `m07-something-broke`. Never reused. |
| `version` | semver str | Change rules in §6. |
| `schema_version` | semver str | Version of *this contract* the file conforms to (`0.1.0`). |
| `engine_min_version` | semver str | Oldest engine that can run it faithfully. |
| `corpus_commit` | git SHA | Corpus content version (Pattern Library claims, citations) the scenario was authored against. |
| `split` | enum{`public`, `generated`, `private_heldout`} | See EVALUATION-CONTRACT §7. |
| `parent` | {`scenario_id`, `version`}? | Required when `split = generated`: the public or held-out scenario it was derived from. |
| `generator` | {`id`, `version`, `params`}? | Required when `split = generated`. |
| `authors`, `reviewed_by` | [str] | `reviewed_by` must be non-empty before the scenario may be used for credit. |
| `labels` | [enum{SOURCE, SYNTHESIZED, DERIVED, EXPERIMENTAL}] | Class of the scenario's *premise*. Almost always includes EXPERIMENTAL. |

### 2.2 Randomness

| Field | Type | Meaning |
| --- | --- | --- |
| `seed` | int | Default seed, used for the public "story" run. |
| `seed_policy` | {`credit_seeds`: int, `seed_source`: enum{`fixed_list`, `derived_from_run_id`}, `fixed_list`?: [int]} | How many seeds a run needs for credit, and where they come from. Minimums are set in EVALUATION-CONTRACT §5. |
| `perturbation_axes` | [{`axis`, `range`, `distribution`}] | What may vary across seeds. See §2.9 and EVALUATION-CONTRACT §5.2. |
| `perturbation_schedules` | [{`id`, `assignments`}] | Named bundles of axis values, e.g. `P1` (calm) and `P2` (adversarial). |

### 2.3 World, visible and hidden state

| Field | Type | Meaning |
| --- | --- | --- |
| `world_state` | {`entities`, `documents`, `queues`, `clocks`, `external_services`} | Initial full world. Documents carry `doc_id`, `version`, `valid_from`, `superseded_by?` so staleness is representable (F-6, F-22). |
| `visible_state` | {`projection`: [rule], `tier_overrides`: {tier → [rule]}} | A **projection** of `world_state`, not a copy. Each rule selects paths, can redact or transform them, and names the UI panel or text channel that shows them. |
| `hidden_state` | {`ground_truth`, `injection_schedule_ref`, `reference_trajectories?`, `acceptance_oracles`} | Never projected to an actor. `reference_trajectories` feed trajectory matchers (GT:L12345–L12350). |
| `disclosure_tier` | enum{`beginner`, `intermediate`, `advanced`, `expert`} | Tier names from the user's analysis. Tiers change `visible_state.tier_overrides` and explanation text only (rule 1). Unlocks are earned by *installing* a mechanism, not by level (RECONCILIATION §4.7). |

### 2.4 Capabilities

| Field | Type | Meaning |
| --- | --- | --- |
| `tools` | [Tool] | See below. |
| `model_tiers` | [{`id`, `price_per_unit`, `latency_dist`, `accuracy_profile`, `context_limit`}] | Simulated models. Profiles are authored, not measured (EXPERIMENTAL). Ch 16's fast/cheap vs powerful framing is SOURCE (GT:L9959–L9966). |
| `agents` | [{`agent_id`, `role_text`, `model_tier`, `tool_grants`, `memory_scopes`}]? | Pre-placed agents. In design missions the learner creates these. |
| `memory_layers` | [{`layer`: enum{`context`, `working_state`, `validated_knowledge`, `history`}, `capacity`, `write_policy`}] | The 4-layer model is DERIVED (RECONCILIATION §3). The book's short-term/long-term split is SOURCE (GT:L5818–L5821). |
| `protocols` | [enum{`direct_tool`, `mcp`, `a2a`}] | Which interop surfaces exist. MCP vs function calling: GT:L6393. |

**Tool** object:

| Field | Meaning |
| --- | --- |
| `tool_id`, `schema` | Name and argument/result JSON schema. The engine rejects calls to unknown tools or with unknown arguments and emits `failure.detected{kind: tool_hallucination}` (F-38). |
| `side_effect` | enum{`none`, `reversible`, `irreversible`}. |
| `idempotent` | bool. If false and `side_effect ≠ none`, the engine tracks `intent_id` to detect duplicate effects (F-13). |
| `required_authority` | Policy rule id(s) that must yield `permit` before execution (§2.5). |
| `latency_dist`, `cost` | Per call. |
| `failure_profile` | [{`mode`: enum{`timeout`, `timeout_after_commit`, `http_5xx`, `rate_limit`, `malformed_output`, `stale_data`, `wrong_target`}, `prob`, `schedule_ref?`}]. The book names malformed tool outputs and API errors as the first things to detect (GT:L7592). |
| `returns_error_as` | enum{`structured`, `string`}. `string` deliberately reproduces the "error as data" trap (F-5). |

### 2.5 Authority policy

| Field | Type | Meaning |
| --- | --- | --- |
| `authority_policy.rules` | [{`rule_id`, `applies_to` (tool / action class / data class), `condition`, `effect`: enum{`permit`, `deny`, `require_approval`}, `approver_role?`}] | Evaluated by a **deterministic** engine component, never by a model. The six-stage chain *predict → recommend → policy-check → authorize → execute → record* is DERIVED (RECONCILIATION §4.1). Least privilege per agent is SOURCE (GT:L11804–L11808). |
| `authority_policy.tokens` | [{`token_type`, `scope` (tool, target, max_amount), `issued_by`, `uses`: int, `ttl_sim`}] | Authority tokens from the user's analysis. A token is **consumed** on execution. Scope mismatch leads to `deny`. |
| `approvers` | [{`role`, `capacity_per_sim_hour`, `latency_dist`, `fatigue_model?`}] | Human-gate capacity. HITL scalability limits are SOURCE (GT:L8128). The fatigue model is EXPERIMENTAL. |
| `human_on_the_loop` | {`policy_editable_by`: [role]}? | Humans set policy; the AI acts within it (GT:L7945). |

### 2.6 Success contract

| Field | Type | Meaning |
| --- | --- | --- |
| `goal_text` | str | What the actor is shown. In "Define Done" missions the learner *writes* part of the contract. That text is stored as `learner_contract`, and the run is graded against both. |
| `acceptance_tests` | [{`test_id`, `oracle_ref`, `weight`}] | Outcome checks against `hidden_state.acceptance_oracles`. |
| `required_artifacts` | [{`artifact_type`, `schema`}] | Structured output requirements (App A, GT:L14676–L14680). |
| `invariants` | [invariant_id] | Process invariants from the EVALUATION-CONTRACT §3 catalog that apply. Hard gates apply to **every** scenario whether listed or not. |
| `degradation_allowed` | {`allowed`: bool, `must_declare`: bool} | Graceful degradation is SOURCE (GT:L7574). Undeclared partial delivery triggers F-15 / HG4. |
| `smart_check` | bool | Whether the scenario checks the learner's contract for SMART properties (GT:L7506). EXPERIMENTAL as a grading device. |

### 2.7 Resource budget

`resource_budget`: {`cost_units`, `sim_time_ms`, `tokens?`, `human_minutes`, `reflection_rounds_max?`, `parallel_slots`}. Every charge emits `budget.charged`. Exhausting a budget emits `failure.detected{kind: budget_exhausted}` and never silently truncates work. Resource-aware operation is SOURCE (Ch 16, GT:L9388–L9390). The specific budget dimensions are EXPERIMENTAL.

### 2.8 Injected failures

`injected_failures`: [InjectedFailure]

| Field | Meaning |
| --- | --- |
| `failure_id` | From the catalog (§5): `F-1`…`F-42`. |
| `trigger` | {`at_sim_ms`} or {`on_event`: type + predicate} or {`prob_per_opportunity`} |
| `target` | Tool, agent, document, queue or artifact id. |
| `effect` | Engine-level mutation, e.g. `tool.failure_mode = timeout_after_commit`. |
| `detection_signals` | [{`signal`, `visibility`: `operator`, `earliest_sim_ms`}]. At least one is required (rule 4). |
| `irreversible_after` | Event predicate after which the harm cannot be undone. Authoring validation checks that `detection_signals.earliest_sim_ms < irreversible_after`. |
| `teaching_ref` | Mission and concept id. |

Injections are logged as `failure.injected` with `visibility: postmortem`, so the actor cannot see them during the run.

### 2.9 Perturbation axes (catalog)

| Axis | Examples | Why |
| --- | --- | --- |
| `timing` | Arrival times, tool latency draws | Breaks timing-memorized solutions |
| `failure_schedule` | Which call fails, and when | Prevents "the 3rd call always fails" memorization |
| `surface` | Paraphrased requests, renamed entities, reordered documents | Forces routing on meaning, not on string memory |
| `distribution` | Task-mix proportions, drift onset | Tests adaptation (Ch 19 drift, GT:L12512–L12521) |
| `knowledge` | Which documents are superseded; retrieval noise | Stale grounding (F-6) |
| `authority` | Which approver is saturated; token scopes | Tests escalation design, not escalation habits |
| `skin` | UI theme and domain vocabulary (transfer missions) | The user's transfer requirement (RECONCILIATION §4.12) |

### 2.10 Teaching metadata (not graded)

`teaching`: {`mission_no?`, `concepts`: [concept_id], `confused_with`: [concept_id], `pattern_library_claims`: [{`claim_id`, `label`, `anchor`}], `add_nothing_variant`: bool}.

`add_nothing_variant = true` marks scenarios where the best-scoring design adds no new component (RECONCILIATION §4.8). Authors must register it, so graders can verify the claim against the reference solution set.

## 3. Visibility model

Every event (§4) and every state path carries a `visibility`:

| Value | Who sees it, when | Examples |
| --- | --- | --- |
| `operator` | The actor, live, within its disclosure tier | Tool results, route decisions, budget, approval-queue length |
| `postmortem` | The actor and reviewers after the run ends | `failure.injected`, hidden ground truth, reference trajectories |
| `engine_only` | Engine and auditors only; never shown to actors | RNG state, held-out oracle internals, canary strings (EVALUATION-CONTRACT §7.4) |

Decision events carry `information_available_ref`, a hash-addressed snapshot of the `operator`-visible state at the moment of decision. This implements DESIGN-ANALYSIS Q15.1 principle 2 (hindsight-bias protection).

## 4. Event schema (append-only)

### 4.1 Envelope

| Field | Type | Meaning |
| --- | --- | --- |
| `event_id` | str (ULID) | Unique id. |
| `run_id` | str | One run = one scenario × one seed × one perturbation schedule × one contestant. |
| `seq` | int | Strictly increasing within a run; no gaps. |
| `t_sim_ms` | int | Simulated time. `t_wall` is recorded separately and never used for grading. |
| `actor` | {`kind`: enum{`engine`, `learner`, `agent`, `model`, `human_approver`, `reviewer`}, `id`} | Who caused the event. |
| `type` | enum (§4.2) | |
| `causal_parents` | [event_id] | The events this one depends on. Forensics builds the causal DAG from these. |
| `payload` | object | Type-specific (§4.2). |
| `visibility` | enum (§3) | |
| `cost` | {`units`, `tokens_in?`, `tokens_out?`, `human_minutes?`}? | Mirrored into `budget.charged`. |
| `latency_ms` | int? | |
| `structured_rationale` | {`reason_codes`: [code], `evidence_refs`: [event_id or artifact_id]}? | Required on decision-type events (marked **D** below). Optional human rationale tags from the user's analysis go here as `reason_codes`. |
| `model_stated_explanation` | {`text`, `label`: "model output, not mechanism"}? | Live-model contestants only. |
| `prev_hash`, `hash` | str | `hash = H(prev_hash ‖ canonical(event without hash))`. Tampering breaks the chain (EVALUATION-CONTRACT INV-E2). |

**Append-only.** Events are never edited or deleted. A correction is a new event of type `annotation.correction` that references the corrected `event_id`. Redaction for privacy replaces the payload with a hash and emits `annotation.redaction`. The chain stays verifiable.

### 4.2 Event types

**D** = decision event: requires `structured_rationale` and `information_available_ref`.

| Type | Key payload fields | Forensic stage |
| --- | --- | --- |
| `run.started` / `run.ended` | scenario ref, seed, schedule, engine version / terminal status | — |
| `observation.presented` | what was shown, panel/channel, `info_snapshot_ref` | OBSERVATION |
| `artifact.read` | artifact id, version | OBSERVATION |
| `task.created` | task id, priority, source | OBSERVATION |
| `task.split` / `task.joined` | parent, children / children, join policy, missing children | ROUTE |
| `route.proposed` | router id, candidates with scores | DECISION |
| `route.decided` **D** | chosen route, `default_used`, `abstained` | ROUTE |
| `decision.made` **D** | `decision_type`, `candidate_actions`, `selected_action` (for non-route decisions) | DECISION |
| `stage.entered` / `stage.exited` | stage id, input/output artifact ids, schema check result | ROUTE / RESULT |
| `critique.round` | round no, critic id, criteria ids, verdict, delta size | EVALUATION |
| `context.loaded` / `context.evicted` / `context.summarized` | items, layer, tokens; for summaries, `dropped_constraint_ids` (engine-computed, postmortem) | CONTEXT SELECTED |
| `memory.read` / `memory.write` | layer, key, version, `validation_receipt?` | CONTEXT SELECTED / STATE CHANGE |
| `retrieval.result` | query, doc ids with versions, `superseded` flags (postmortem) | CONTEXT SELECTED |
| `action.requested` **D** | tool id, args hash, `intent_id`, requesting agent | ACTION REQUEST |
| `authorization.decided` | rule ids evaluated, effect, token consumed, approver | AUTHORIZATION |
| `tool.executed` | tool id, `intent_id`, result or structured error, `side_effect_committed`, `target` | EXECUTION → RESULT |
| `state.delta` | paths changed, before/after hashes, `target_project` / owner | STATE CHANGE |
| `handoff.sent` / `handoff.received` | from/to, artifact, schema check, missing fields | ROUTE |
| `escalation.opened` **D** / `escalation.resolved` | reason, queue, approver / decision, latency | AUTHORIZATION |
| `failure.injected` (postmortem) | failure id, target | — |
| `failure.detected` | kind, detector id (engine or actor-built), linked injection (postmortem) | EVALUATION |
| `recovery.action` **D** | retry / fallback / rollback / degrade / escalate, target | DECISION |
| `checkpoint.created` / `rollback.applied` | checkpoint id, state hash / to-checkpoint, valid, duplicate side-effects | STATE CHANGE |
| `priority.changed` | task, old → new, reason | DECISION |
| `budget.charged` | dimension, amount, remaining | — |
| `agent.spawned` / `agent.terminated` | agent id, grants / reason, lost working state | — |
| `evaluation.result` | evaluator id (engine / actor-built / judge), subject, verdict, score | EVALUATION |
| `artifact.completed` | artifact id, contract tests claimed passed, `declared_degradation?` | RESULT |
| `annotation.correction` / `annotation.redaction` | target event id, reason | — |

**Mapping from the user's event field list.** The user's fields map to envelope fields or event types as follows:

- `timestamp` → `t_sim_ms`
- `observation` → `observation.presented`
- `artifact_read` → `artifact.read`
- `memory_read` → `memory.read`
- `retrieval_result` → `retrieval.result`
- `decision_type`, `candidate_actions`, `selected_action` → `decision.made` / `route.decided`
- `tool_request` → `action.requested`
- `authorization_result` → `authorization.decided`
- `tool_result` → `tool.executed`
- `state_delta` → `state.delta`
- `memory_write` → `memory.write`
- `human_escalation` → `escalation.*`
- `cost`, `latency` → envelope fields
- `error` → `failure.detected`
- `recovery_action` → `recovery.action`
- `evaluation_result` → `evaluation.result`

Nothing from the user's list is dropped.

### 4.3 Forensic timeline

The Forensics surface renders the causal DAG in the user's ten stages: OBSERVATION → DECISION → ROUTE → CONTEXT SELECTED → ACTION REQUEST → AUTHORIZATION → EXECUTION → RESULT → STATE CHANGE → EVALUATION. The "Forensic stage" column above is that mapping.

A consequential action whose chain lacks an `authorization.decided` event between `action.requested` and `tool.executed` is, by construction, an HG1 violation.

## 5. Failure catalog

F-1…F-35 are defined in DESIGN-ANALYSIS Q7 with their anchors, and are incorporated here by reference. Additions from the reconciliation:

| ID | Failure | Engine realization | Detection (invariant or signal) | Class |
| --- | --- | --- | --- | --- |
| **F-36** | **Silent success**: acceptance tests pass, but a process invariant was violated, or a side-effect hit the wrong target (e.g., the correct file written to the wrong project) | `tool.failure_mode = wrong_target`, or a scenario where a shortcut passes the oracle while breaking an invariant | Invariants on the event stream: `state.delta.target` ∉ contract's permitted targets, or any HG violation alongside passing acceptance tests | DERIVED (the class); SOURCE ingredients: blast radius GT:L11808 |
| F-37 | Unsafe parallel mutation: parallel branches write the same state | Shared-state targets across fan-out children | Two `state.delta` on the same path with no ordering or causal edge between them | DERIVED; book: state-mutation concurrency concern GT:L5410–L5413 |
| F-38 | Tool hallucination: a call to a non-existent tool or with invalid arguments | Engine rejects against `tools[].schema` | `failure.detected{kind: tool_hallucination}` | DERIVED |
| F-39 | Non-convergent reflection: critique rounds oscillate or never meet the criteria | Critic profile with oscillating verdicts | `critique.round` count reaches the max with no criteria met, or the delta sign flips ≥ 2 times | SOURCE: stopping condition GT:L2445; cost GT:L2859–L2862 |
| F-40 | Obsolete plan: the world changes after planning and the plan is executed unchanged | World event invalidates a plan precondition | Plan step executed whose precondition is false at execution time | SOURCE: Ch 6 adaptivity; DERIVED specifics |
| F-41 | Metric gaming: the design optimizes a visible proxy metric while hidden outcome quality falls | Visible metric diverges from the hidden oracle | Visible metric ↑ while held-out oracle score ↓ across seeds | DERIVED |
| F-42 | Unsafe escalation avoidance: the design avoids asking because asking is costly | Escalation priced; a required-approval case is present | `require_approval` case with no `escalation.opened` (feeds HG1) | DERIVED (pair of F-17 over-escalation) |

## 6. Versioning and compatibility

- **Patch** (`x.y.Z`): text or typo fixes with no effect on any event, oracle or score. Past runs remain comparable.
- **Minor** (`x.Y.0`): new optional fields, new perturbation schedule, or new teaching metadata. Past runs remain comparable *for unchanged schedules*.
- **Major** (`X.0.0`): anything that changes the world, oracles, capabilities, policy, budget or injections. Past runs are **not** comparable. Traces tied to the old major are marked `superseded` (EVALUATION-CONTRACT §6).
- `corpus_commit` changes are at least minor if they change shown claims, and major if a shown claim flips its label (e.g., SOURCE → DERIVED).
- A private held-out scenario that leaks is retired, never "patched" (EVALUATION-CONTRACT §7.3).

## 7. Illustrative skeleton (Mission 7, "Something Broke")

Illustrative only. Values are placeholders and have not been tuned.

```jsonc
{
  "scenario_id": "m07-something-broke",
  "version": "0.1.0", "schema_version": "0.1.0", "engine_min_version": "0.1.0",
  "corpus_commit": "<sha>", "split": "public",
  "labels": ["SOURCE", "EXPERIMENTAL"],            // Ch 12 recovery is SOURCE; the mission is ours
  "seed": 7001,
  "seed_policy": {"credit_seeds": 3, "seed_source": "derived_from_run_id"},
  "perturbation_axes": [{"axis": "failure_schedule", "range": "call 1..6", "distribution": "uniform"}],
  "world_state": {"entities": {"orders": "<12 refund requests>"}, "documents": [], "queues": {"inbox": 12}},
  "visible_state": {"projection": ["queues.inbox", "tools.*.schema", "budget", "receipts"]},
  "hidden_state": {"acceptance_oracles": {"refunds": "<expected ledger>"}},
  "disclosure_tier": "beginner",
  "tools": [{
    "tool_id": "refund.create", "side_effect": "irreversible", "idempotent": false,
    "required_authority": ["POL-refund-under-100"],
    "failure_profile": [{"mode": "timeout_after_commit", "prob": 0.0, "schedule_ref": "inj-1"}],
    "returns_error_as": "structured"
  }],
  "authority_policy": {"rules": [{"rule_id": "POL-refund-under-100", "applies_to": "refund.create",
                                  "condition": "amount < 100", "effect": "permit"}]},
  "success_contract": {"acceptance_tests": [{"test_id": "ledger-matches", "oracle_ref": "refunds"}],
                       "invariants": ["INV-P1-no-duplicate-side-effect"],
                       "degradation_allowed": {"allowed": true, "must_declare": true}},
  "resource_budget": {"cost_units": 50, "sim_time_ms": 600000, "human_minutes": 0, "parallel_slots": 1},
  "injected_failures": [{
    "failure_id": "F-13", "trigger": {"on_event": "tool.executed#3"}, "target": "refund.create",
    "effect": "timeout_after_commit",
    "detection_signals": [{"signal": "receipt_present_for_intent", "visibility": "operator", "earliest_sim_ms": 0}],
    "irreversible_after": "second tool.executed with same intent_id"
  }, {
    "failure_id": "F-36", "trigger": {"prob_per_opportunity": 0.0}, "target": "refund.create",
    "effect": "wrong_target on retry path without intent_id",
    "detection_signals": [{"signal": "state.delta.target shown in ledger", "visibility": "operator", "earliest_sim_ms": 0}],
    "irreversible_after": "run.ended"
  }],
  "teaching": {"mission_no": 7, "concepts": ["detect-handle-recover", "idempotency", "checkpoint"],
               "confused_with": ["guardrails"], "add_nothing_variant": false,
               "pattern_library_claims": [{"claim_id": "ch12-retries", "label": "SOURCE", "anchor": "GT:L7601"},
                                          {"claim_id": "idempotency", "label": "DERIVED", "anchor": null}]}
}
```

## 8. Open questions (UNCERTAIN)

- Whether one projection language can express both UI panels and text/JSON channels without the adapters diverging (rule 6).
- Whether `information_available_ref` snapshots are affordable at graduation volume. The fallback is snapshot-on-decision with delta encoding.
- How to author `acceptance_oracles` for open-ended artifacts (drafts, research) without an LLM judge. Where a judge is used, its output is an observation, and EVALUATION-CONTRACT §2 applies.
- Whether `unit_of_application` and `controlling_topology` (user terms, EXTERNAL-UNVERIFIED; RECONCILIATION §4.13) should become fields. They are not included until the user defines them.
