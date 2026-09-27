# Agent Academy — Evaluation Contract (v0.1.0, unpiloted)

**Status:** EXPERIMENTAL. Nothing here has been calibrated, piloted, or tested for validity:

- no threshold has pilot data;
- no score has been shown to predict transfer;
- no inter-rater agreement has been measured.

The purpose of this document is to fix *what* is measured and *how evidence is promoted*, so that a pilot can falsify it.

**Labels:** [RECONCILIATION §3](RECONCILIATION.md#3-provenance-labels-one-scheme).

**Inputs:** runs and event streams defined in [SCENARIO-CONTRACT.md](SCENARIO-CONTRACT.md).

**Supersedes:** DESIGN-ANALYSIS Q12.3 (hard gates and O/P metrics, re-homed here with GENERALIZATION split out) and Q15.2/15.4 (lifecycle and promotion).

---

## 1. Principles

1. **Grade invariants, not architectures.** No design is "the answer". A run passes when the event stream satisfies the hard gates and the scenario's invariants, and scores on outcome, process and generalization. Two different architectures can both earn full marks. The user's analysis and DESIGN-ANALYSIS agree on this.
2. **Deterministic first.** Invariants and hard gates are checked by deterministic code over the event stream. LLM judges are allowed only where no deterministic oracle exists. Their verdicts are `evaluation.result` events with `evaluator.kind = judge`. They are **observations**, never gate decisions. The book's evaluation-method table says LLM-as-a-Judge may overlook intermediate steps and is "Limited by LLM capabilities" (GT:L12314–L12317) and that a single LLM writing and judging shares blind spots (GT:L7411–L7413).
3. **Outcome, process and generalization are reported separately.** There is no blended headline score. A blended score would hide exactly the distinction the directive asks for: a good outcome from a fragile process. The book asks for assessment of "both the final output and the agent's trajectory" (GT:L12327). That is SYNTHESIZED. Separating out generalization is DERIVED.
4. **Every trace starts as an observation** (§6). Human play is not ground truth. Neither is a strong model's run.
5. **Same engine, same visible state, for every contestant** (Agent Mode, §8).

## 2. Grading pipeline

```
event stream ──verify hash chain──▶ engine-integrity invariants (INV-E*)
             ──▶ hard gates (HG1–HG4)  ──any fail──▶ run = FAIL (scores still computed, shown as "void")
             ──▶ scenario invariants (INV-P*)
             ──▶ OUTCOME / PROCESS / GENERALIZATION scores
             ──▶ report card (+ first-bad-decision pointer for Forensics)
```

- If an INV-E check fails, the **run is invalid**, not failed. The engine or harness misbehaved, and the run is excluded from every aggregate.
- Graders read only the event stream and the scenario file. They never call the contestant.

## 3. Invariants and hard gates

### 3.1 Hard gates

Hard gates apply to every scenario. Any violation fails the run, whatever the scores.

| Gate | Invariant over the event stream | Catches | Anchor |
| --- | --- | --- | --- |
| **HG1 Authority** | For every `tool.executed` with `side_effect ≠ none`, there is a causally prior `authorization.decided{effect: permit}` whose rule/token scope covers (tool, target, amount). No token is used beyond `uses` or `ttl`. Every `require_approval` case has an `escalation.opened`. | F-8, F-18, F-42 | SYNTHESIZED: least privilege GT:L11804; human-on-the-loop policy GT:L7945. The gate as a *separation* is DERIVED. |
| **HG2 Canonical integrity** | Every `memory.write` to `validated_knowledge` carries a `validation_receipt` issued by a validator the design declared. No write promotes content whose provenance chain includes an unvalidated hypothesis. | F-20 | DERIVED; the book poses the drift question (GT:L16683) |
| **HG3 Evidence** | For every consequential decision (**D** events touching side-effects, knowledge writes, escalations or priority changes), the causal chain back to its observations is complete within the contestant's *own* telemetry. Default threshold: ≥ 99% of such decisions (UNCERTAIN, not calibrated). | untraceable designs | SOURCE: structured logging GT:L11794–L11798 |
| **HG4 No silent failure** | No `artifact.completed` claims contract tests passed when they failed. Undeclared degradation fails. **And** no run with passing acceptance tests has an INV-P violation flagged `silent_success_relevant` (F-36). | F-15, **F-36** | SOURCE: graceful degradation exists as a strategy (GT:L7604–L7606), and notifying operators is a separate strategy (GT:L7608–L7609). The *requirement to declare* degradation is DERIVED, and so is the F-36 class. |

HG4's second clause is the reason F-36 needs event-level checks. In silent success the output is correct, so outcome grading alone passes it. The gate fires on the *process* violation that accompanied the correct output.

### 3.2 Engine-integrity invariants (run validity)

| ID | Invariant |
| --- | --- |
| INV-E1 | No actor-visible event payload contains data from `hidden_state` or from `engine_only` paths (checked by taint-tracking hidden values). |
| INV-E2 | Hash chain verifies; `seq` is gap-free and strictly increasing. |
| INV-E3 | Replaying the engine with the recorded seed and the recorded actor decisions reproduces every engine-authored event byte-for-byte. |
| INV-E4 | Every `failure.injected` has a `detection_signal` event at `operator` visibility before its `irreversible_after` predicate (SCENARIO-CONTRACT rule 4). |

### 3.3 Process invariants (scenario-selectable, scored)

A scenario opts into these via `success_contract.invariants`. A violation lowers PROCESS scores. Violations flagged `silent_success_relevant` also feed HG4.

| ID | Invariant | Failure(s) | silent_success_relevant |
| --- | --- | --- | --- |
| INV-P1 | No duplicate side-effect per `intent_id` | F-13 | yes |
| INV-P2 | Every `state.delta.target` ∈ the contract's permitted targets | F-36 | yes |
| INV-P3 | No two `state.delta` on the same path from concurrent branches without a causal ordering | F-37 | yes |
| INV-P4 | Every `handoff.received` passes its schema check, or the receiver emits `failure.detected` | F-3, F-24 | yes |
| INV-P5 | Tool errors are never consumed as data (no `structured` error value flowing into a downstream artifact field) | F-5 | yes |
| INV-P6 | Retrieved documents flagged superseded are not cited as authority in a completed artifact | F-6, F-22 | yes |
| INV-P7 | Pinned constraints survive every `context.summarized` | F-21 | yes |
| INV-P8 | Critique loops terminate by criteria or declared cap | F-11, F-39 | no |
| INV-P9 | No plan step executes with a false precondition | F-40 | yes |
| INV-P10 | Every router has a default or abstain path, and unrouted count = 0 | F-7 | no |
| INV-P11 | Budget never exceeded without a `failure.detected{budget_exhausted}` and a declared degradation | budget | yes |

## 4. Scores

All scores are in [0, 1] unless stated. All definitions are EXPERIMENTAL.

### 4.1 OUTCOME: did it deliver?

| ID | Definition |
| --- | --- |
| O1 | Priority-weighted acceptance: Σ(weight × passed ∧ on-time) / Σ weight, judged against hidden oracles |
| O2 | SLA adherence by priority class |
| O3 | Outcome value per cost unit, normalized to the scenario's reference band |
| O4 | Novel-task handling: correct handling or correct abstain/escalate. Confident-wrong counts double against. |

### 4.2 PROCESS: could we trust how it delivered?

| ID | Definition | Anchor |
| --- | --- | --- |
| P1 | Invariant compliance: 1 − weighted INV-P violations / opportunities | DERIVED |
| P2 | Detection latency: median sim-time from injection to the first `failure.detected` by a design-owned detector | SOURCE (Ch 12 detection) + DERIVED metric |
| P3 | Escalation precision and recall (both reported) | SOURCE (Ch 13) |
| P4 | Recovery correctness: recoveries restoring a valid checkpoint with zero duplicate side-effects | SOURCE: checkpoint/rollback GT:L11774 |
| P5 | Blast radius: mean downstream tasks affected per injected fault | SOURCE term GT:L11808 |
| P6 | Deliberation efficiency: deep-tier and reflection spend that changed an outcome ÷ total deep spend | DERIVED |
| P7 | Calibration of design-reported confidence vs realized correctness | DERIVED. The book does not discuss calibration ("calibrat": 0 hits). |
| P8 | Trajectory quality: exact / in-order / any-order match against reference trajectories, as the scenario declares | SOURCE: GT:L12345–L12350 |
| P9 | Improvement safety: if the design learns, held-out performance after gated updates ≥ before | DERIVED mechanism; question SOURCE GT:L16683 |

### 4.3 GENERALIZATION: does it survive what it hasn't seen?

| ID | Definition |
| --- | --- |
| G1 | Seed robustness: worst-seed O1 and the O1 spread across the credit seeds (formerly DESIGN-ANALYSIS P1) |
| G2 | Perturbation robustness: O1 and P1 under adversarial schedules ÷ under calm schedules |
| G3 | Held-out variants: O1 and P1 on `generated` and `private_heldout` siblings of the scenarios trained on |
| G4 | Transfer: O1 and P1 on a `skin`-perturbed scenario (different UI and domain vocabulary) teaching the same concept |
| G5 | Architecture restraint: on `add_nothing_variant` scenarios, the score gap between the learner's design and the minimal reference design (penalizes needless components) |

**Fragile-success rule (DERIVED):**

- A run with O1 = 1.0 on the story seed but G1 worst-seed O1 < 0.6 is reported as **fragile**. It earns no mastery credit, whatever its O score.
- The threshold 0.6 is UNCERTAIN, a placeholder.

## 5. Seeds and perturbation requirements

### 5.1 Minimum seeds (placeholders, UNCERTAIN)

| Use | Seeds × schedules |
| --- | --- |
| Practice run | 1 × calm (story seed; no credit) |
| Mission credit | ≥ 3 derived seeds × 1 calm + 1 adversarial |
| Act boss / graduation | ≥ 5 seeds × 2 schedules (DESIGN-ANALYSIS Q12.3) |
| Benchmark Lab comparison | ≥ 10 seeds × all declared schedules; identical seed list for all contestants |

Credit seeds are **derived from the run id** (`seed_source = derived_from_run_id`), so a learner cannot replay a known-good seed for credit. The story seed is public.

### 5.2 Perturbation rules

- Every credit-bearing scenario declares at least **two** perturbation axes (SCENARIO-CONTRACT §2.9). One of them must be `failure_schedule` or `surface`.
- Perturbations must preserve the scenario's *concept*. The reference solution set must still pass. This is checked at authoring time by running all reference solutions over the full schedule set.
- Contestants in a comparison get **common random numbers**: the same seed list and schedule assignment.

## 6. Trace status lifecycle

This merges the user's analysis (`observation → reviewed → validated → fixture | counterexample | training-candidate`) with DESIGN-ANALYSIS Q15.2.

```
observation ──auto screen──▶ screened ──reviewer──▶ reviewed ──adjudication──▶ validated
     │                          │                      │                            │
     └──────────▶ quarantined ◀─┴──────────────────────┴──── (failed screen, PII, tamper, INV-E fail)
validated ──promote(kind)──▶ promoted:{ eval_fixture | router_test | counterexample |
                                         recovery_example | architecture_example | training_candidate }
any ──▶ superseded (scenario major / rubric / engine change)      any ──▶ retracted (reason required)
```

| Transition | Who | Required evidence |
| --- | --- | --- |
| observation → screened | automated | Hash chain valid; INV-E pass; consent flags present; PII scan clean |
| screened → reviewed | one named reviewer | Rubric version; per-decision verdicts (`correct` / `incorrect` / `ambiguous`); reviewer ≠ contestant |
| reviewed → validated | adjudicator, or two independent reviewers agreeing | Agreement recorded. Disagreements are kept and never averaged away. |
| validated → promoted:`counterexample` | reviewer | Failure id; first bad decision; why the design allowed it. Permanently labelled NEGATIVE. |
| validated → promoted:`eval_fixture` / `router_test` / `recovery_example` / `architecture_example` | reviewer + scenario owner | The fields in DESIGN-ANALYSIS Q15.4 table |
| validated → promoted:`training_candidate` | reviewer + **second independent approver** | Explicit training consent, licence check, and not from a `private_heldout` scenario. **No automatic path exists.** |
| any → superseded / retracted | owner | Reason. Dependents are re-flagged. |

**Evidence class.** A trace is never SOURCE. Its maximum class is "validated observation". Pattern Library cards may cite validated traces as *examples*, labelled as such, never as book claims.

## 7. Splits and anti-memorization

### 7.1 Three splits

| Split | Visibility | Used for | Never used for |
| --- | --- | --- | --- |
| `public` | Full scenario files published | Teaching, practice, mission credit | Benchmark headline numbers |
| `generated` | Generator published; instances produced per run | Mission credit (G3), robustness | Training candidates *of the same generator version* |
| `private_heldout` | Files never published; per-scenario results never published; only aggregates | G3, graduation, Benchmark Lab | Teaching, hints, fixtures, training candidates |

This follows the user's point that a public academy is not a benchmark (RECONCILIATION §4.12). The same engine runs all three splits.

### 7.2 Generated variants

- A generator takes a parent scenario and a perturbation grammar: entity renaming, task paraphrase, document re-versioning, failure re-scheduling, policy-threshold shifts inside declared bounds.
- Every instance records `parent` and `generator` (SCENARIO-CONTRACT §2.1).
- Generator outputs must pass the reference-solution check (§5.2) before use.

### 7.3 Held-out hygiene

- Access to `private_heldout` files is logged. Authors of a held-out scenario do not review traces from it.
- **Rotation**: held-out scenarios are retired on a schedule and on any suspected leak. Retired scenarios may move to `public`, and are then marked as such in every past report.
- **Live-model caveat (UNCERTAIN)**: running held-out scenarios through hosted model APIs discloses them to the provider. Either restrict held-out runs to local models, or accept and record the exposure as `exposure: provider:<name>` on the run and weaken the scenario's held-out status.

### 7.4 Contamination checks

- **Canary strings** (`engine_only`) are embedded in held-out scenario text. Their appearance in any contestant output, or in public data, triggers retirement.
- **Near-duplicate detection** between new public or generated scenarios and held-out ones.
- **Memorization signal**: a large public-vs-held-out gap on the same concept (G3 ≪ O1 public) is reported as probable memorization, not as mastery.
- **No self-certification**: fixtures promoted from academy traces must never grade the academy's own simulated agents (DESIGN-ANALYSIS Q15.4). This is the Ch 11 same-judge problem (GT:L7411–L7413) applied at the dataset level.

## 8. Agent Mode and Benchmark Lab fairness

- The same scenario file, engine version, seed list, schedule assignment, `visible_state` projection, tools, authority policy, budget and success contract apply to every contestant.
- Adapters may change rendering only (SCENARIO-CONTRACT rule 6). Adapter versions are recorded on the run.
- Human contestants get wall-clock limits that are declared per scenario. Model contestants get token and cost limits through `resource_budget`. Both are reported, not normalized away.
- Contestant descriptors must be inspectable. A named configuration without a definition, such as "Beowulf" (EXTERNAL-UNVERIFIED, PROVENANCE-AUDIT §7, X-12), cannot be registered.
- Results tables show O, P and G separately, with seed counts and confidence intervals, and state which split they come from.

## 9. Reviewer rubric requirements

- Rubrics are versioned, and each run review cites one.
- Every rubric item names the invariant or score it informs, and gives one positive example and one counterexample. The counterexample must be labelled WEAK or NEGATIVE, never unlabelled.
- Inter-rater agreement is computed per rubric item before a rubric version may validate traces. The threshold is UNCERTAIN until the pilot.
- Reviewers see `information_available` snapshots when judging decisions, to protect against hindsight bias.

## 10. What this contract does not establish

- That any score measures transferable architectural skill. That is the pilot's question.
- That the thresholds (99% evidence, 0.6 fragility, seed counts) are right.
- That LLM judges are reliable for any rubric item.
- That the simulated tool and model profiles resemble real ones.

**Proposed pilot, to falsify the contract before building on it:**

1. Author missions 1–3 and 7 against SCENARIO-CONTRACT.
2. Have ≥ 2 reviewers grade ≥ 20 learner runs each.
3. Measure inter-rater agreement.
4. Check whether G3/G4 differ from O1 in the direction the design predicts.
