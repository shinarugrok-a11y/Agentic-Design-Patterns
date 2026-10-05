# Reconciliation: user's design analysis vs this design analysis

Inputs compared:

- **U** — the user's "Agent Academy — First Design Analysis" (received 2026-09-27 04:49 UTC; coordinator condensation at `/tmp/academy/USER-ANALYSIS-2.md`, not committed).
- **A** — [`DESIGN-ANALYSIS.md`](DESIGN-ANALYSIS.md) (commit `0368663`).

Evidence base: the book text at `ground-truth/agentic_design_patterns.txt` (now merged into this branch from `origin/main`), and `validation/audit/` (merged from `ed7e205`). The user's corpus claims are registered one by one in [`PROVENANCE-AUDIT.md` §7](PROVENANCE-AUDIT.md#7-external-unverified-claims-register-user-analysis-2026-09-27).

Rule applied: the newest *commits* win for repository content. The user's analysis is newer than A, but it is an **argument, not a commit**. Where it asserts facts about the corpus, those facts were checked. Where it makes design proposals, they are judged on evidence and reasoning. They are not adopted because they are newer.

---

## 1. Summary of the outcome

| Category | Count | Items |
| --- | --- | --- |
| **Adopted** | 13 | Implementation vs teaching dependency · "Define Done" first · composition mission by Mission 5 · authority taught with tools · silent-success failure class · extended forensic timeline · no fake chain-of-thought · OUTCOME/PROCESS/GENERALIZATION · public / generated / private-held-out split · "Reflection fixes today, Learning fixes tomorrow" · "sometimes add nothing" · six primary IA surfaces incl. Benchmark Lab · human-scale graduation core + extra stressors |
| **Adopted with modification** | 5 | Provenance labels (merged scheme, §3) · ten-mission list (merged, §5) · disclosure tiers · Pattern Library fields · trace lifecycle |
| **Rejected / not adopted** | 6 | Governance taught after multi-agent (phase VII) · evaluation as phase VIII only · "01–04 more verified than 05–21" · "Reflection batch corrupted" · single-label classification · corpus vocabulary that does not exist (APD, controlling_topology, CompSD, Beowulf…) |
| **Corrections to A** | 6 | A missed the Ch 11 / Planning overlap · A's "Tool Use must precede Routing" was too strong · A lacked "silent success" as a distinct class · A's label scheme conflated synthesis with invention · A's F-15 overstated the book ("degradation must be declared" is DERIVED) · an off-by-three citation for F-28 (§6 items 10–11) |

## 2. Corpus claims in U

The details are in [PROVENANCE-AUDIT §7](PROVENANCE-AUDIT.md#7-external-unverified-claims-register-user-analysis-2026-09-27). In short:

- **Not found anywhere** (all branches, all history): APD-01..21 records, `status: unverified` on APD records, MANIFEST `pattern_index`, schema 2.1/2.2, the conversion log, the D4 correction, routing fixtures, "relationship decomposition", `controlling_topology`, `unit_of_application`, "secondary local pattern", "System-1/System-2 decision bus", CompSD, the Beowulf configuration, ROUTING-INDEX, EVALUATION-LAYER-MODEL. `validation/audit/06-candidate-pattern-mappings.md:3` says literally: "There is no `APD-NN` ontology in the tree." `manifest.json` is `version: "1.0"` with keys `version`, `source`, `skills` only. These are labelled **EXTERNAL-UNVERIFIED**. They probably come from another project. Nothing in the academy may depend on them until that project's artifacts are supplied.
- **False**: "the Reflection batch contains particularly severe corruption". All three `Chapter_04_*` notebooks parse, and the Ch 4 text is clean. The seven actual parse failures are in Ch 3, 14, 15, 17 (two), 18 and 21. They are the original authors' notebook defects, not PDF-extraction damage.
- **Unsupported**: treating chapters 01–04 as more verified than 05–21. Nothing in this repo distinguishes them.
- **Verified**: every *book* claim in U that the fact-check covered, with two partials. U's claim that Reflection is "source-supported as a behavior that can operate across another workflow" is **partial**. The book supports *combinable*: Reflection "can be integrated with other foundational patterns" (GT:L2885, Ch 4), and Exception Handling "may sometimes be used with reflection" (GT:L7564). "Cross-cutting dimension" is our derived framing, in U as in A. U labels Reflection "cross-cutting" in its table and "source-supported" in its claims, so U contradicts itself. The same correction applies to A (§3.2 below).

## 3. Provenance labels: one scheme

U proposes SOURCE / SYNTHESIZED / DERIVED / EXPERIMENTAL. A used [C] / [C-nb] / [W] / [D] / [U] / [X]. U's scheme is better on one point that matters: A's [D] lumped together two very different things.

1. Statements *assembled* from cited source parts.
2. Statements that *add* content the source does not contain.

A's scheme is better on another: it had explicit markers for weak examples and nonexistent artifacts, which U's lacks.

**Adopted scheme (all academy docs from now on):**

| Class (one per claim) | Meaning | Replaces |
| --- | --- | --- |
| **SOURCE** | Stated in the book text; cite `GT:L…` / PDF page | [C] |
| **SOURCE-CODE** | Present in the book's companion notebooks; fidelity to the printed code unverified unless stated | [C-nb] |
| **SYNTHESIZED** | A conjunction of SOURCE statements, each cited, that adds no new mechanism. Example: "the book provides human-on-the-loop policy-setting (GT:L7945) *and* least privilege (GT:L11804)." | part of [D] |
| **DERIVED** | Our interpretation, which adds structure, mechanism or claims not in the source. Examples: JUDGMENT≠AUTHORITY as a principle, 4-layer memory, cross-cutting axis, the ontology. | rest of [D] |
| **EXPERIMENTAL** | A design hypothesis whose value must be shown by pilot data: missions, thresholds, mechanics' teaching efficacy, the visual direction | A's "thresholds [U]" |
| **EXTERNAL-UNVERIFIED** | A claim attributed to material outside this repository that cannot be inspected here | new |

**Orthogonal flags** (combinable with any class): `WEAK` (damaged or poor example; never a positive), `UNCERTAIN`, `NONEXISTENT` (named artifact absent).

Mapping for reading A: [C]→SOURCE, [C-nb]→SOURCE-CODE, [W]→SOURCE-CODE+WEAK, [D]→SYNTHESIZED or DERIVED (A's Q14 table's "nearest canonical anchor" column says which), [U]→flag UNCERTAIN, [X]→flag NONEXISTENT. Re-classifications of A's key [D] items:

| Item | Class | Why |
| --- | --- | --- |
| "Book provides policy-setting humans + least privilege + tool restrictions" | SYNTHESIZED | Each part cited |
| JUDGMENT≠AUTHORITY *as a separation principle* (prediction / recommendation / policy / authorization / execution) | DERIVED | The book's own routers dispatch directly with no policy layer |
| "Reflection is combinable with other patterns" | SYNTHESIZED | GT:L2885, GT:L7564 |
| "Reflection is a cross-cutting dimension" | DERIVED | Correction for both U and A |
| 4-layer CONTEXT/MEMORY/KNOWLEDGE/HISTORY | DERIVED | Re-cut of book's 2 components × 3 types |
| Deliberation-budget axis (System-1/System-2 framing) | DERIVED | Ingredients SOURCE (Ch 2, 16, 17); framing ours |
| Outcome vs process scoring | SYNTHESIZED (the idea) + DERIVED (the "fragile success scores lower" rule) | GT:L12327 |
| All missions, thresholds, graduation rule, visual direction | EXPERIMENTAL | Unpiloted |

## 4. Point-by-point comparison

### 4.1 Graduation outcomes (U: A–J; A: G1–G10)

**Agreement: substantial.** Both have:

- task ≠ pattern;
- control flow ≠ behavior;
- judgment ≠ authority;
- the 4-layer memory model (both label it derived);
- failures as architectural evidence;
- "more intelligence isn't always the answer" (A's G7 deliberation allocation);
- outcome ≠ architecture;
- survival under novelty.

**U adds**, and we adopt:

- (C) "goals and success criteria precede autonomy" as an explicit outcome. A had it only as the criteria-lite thread.
- (F) "tools don't make agents safe."

**A adds**, and we keep:

- G9 epistemic hygiene: learning without corrupting validated knowledge. The book poses the question at GT:L16683.
- G10 protocol choice (MCP vs direct tools vs A2A).

U's judgment≠authority is finer-grained (prediction / recommendation / policy / authorization / execution) than A's four-way split (propose / permit / verify / record). **Adopt U's five stages plus A's *record***, as six stages: *predict → recommend → policy-check → authorize → execute → record*. The forensic timeline in §4.7 encodes them. Class: DERIVED.

### 4.2 Dependencies: implementation vs teaching (U §2)

**Adopted.** This is U's best structural idea, and A lacked it. A's spiral threads were an informal version of it.

- **Implementation dependency**: what the simulator must enforce for a mission to be coherent. Policy gates, exception propagation, budget accounting and event logging exist in the engine **from Mission 1**, whether or not they are taught.
- **Teaching dependency**: what the learner must understand before a concept makes sense.

Consequence: in early missions guardrails and gates *act* (blocking with a plain-language message), but they are not yet *explained*. The learner meets authority as a constraint before designing it.

**Graph disagreements.**

| U's edge / placement | A's position | Resolution |
| --- | --- | --- |
| Goal → Decomposition → topologies | A: agent loop / structured output / criteria → chaining | **Converge**: Goal/criteria first (adopt U), with structured output folded into the chaining mission. |
| Topologies before Tools | A: "Tool Use should precede Routing" (tool selection is a routing juncture, GT:L1262) | **A corrected.** Routing among *fixed handlers* does not need tools; that is the teaching dependency. Tool-selection routing returns in the tools mission. A's claim was an implementation-graph claim presented as a teaching claim. |
| Evaluation, Exception, HITL, Guardrails, Resource as a "cross-cutting" cluster applied late | A: evaluation and authority are threads from Act I; governance is taught before multi-agent | **A kept** (argued in §4.3). |
| Reflection after Planning | A: Reflection before Planning | Both workable. The merged list puts Reflection before Planning because Reflection needs only criteria, and Planning needs world change *plus* a revise loop (Reflection at the plan level). |

### 4.3 Teaching order: U's 10 phases vs A's 6 acts

U's phases: I purpose & observable execution → II topology (+composition) → III tools → authority → MCP → IV context → memory → RAG → provenance → V planning → reflection → reasoning → VI multi-agent → contracts → A2A → **VII exception → HITL → guardrails** → **VIII evaluation → resource → prioritization** → IX learning → X exploration.

**Agreements:** reject chapter order; purpose first; composition early; learning only after evaluation; exploration last ("exploration in an ungoverned novice system is backwards", which A also argued via Act VI); MCP right after tools, as its standardization.

**Disagreement 1: governance (VII) after multi-agent (VI).** A keeps governance before multi-agent.

- **U's own first ten missions contradict U's phase order.** Mission 6 teaches judgment≠authority with tools (phase III). Mission 8 "Something Broke" teaches exceptions and checkpoints (phase VII). Mission 9 teaches reflection (phase V). Mission 10 teaches memory (phase IV). In U's own concrete sequence, exceptions and authority come *before* multi-agent.
- **Multi-agent multiplies authority surfaces.** Every added agent is another holder of tool permissions and another handoff that can drop context. The book's own reliability section makes least privilege and "blast radius" a property of *each* agent (GT:L11804–L11810) and ties modularity to fault isolation (GT:L11785–L11792). Teaching an organization before permissions teaches learners to build unbounded organizations first and retrofit limits later. That is the failure the directive's graduation criteria punish.
- **Tools fail as soon as they exist.** Exception handling is a teaching dependency of Tool Use: the book's error detection starts with "invalid or malformed tool outputs" (GT:L7592). Deferring it to phase VII means five phases of tools that never fail, or fail untaught.
- **What U gets right here:** HITL as a *human-capacity* problem (queues, fatigue, scalability, GT:L8128) needs volume to matter, so HITL at full depth can sit with or after multi-agent. **Resolution:** exception and authority basics come with tools (Act I). Guardrails/HITL depth stays in Act III, before multi-agent. HITL-at-scale returns in Act IV.

**Disagreement 2: evaluation only at phase VIII.** U itself puts "Define Done" at Mission 1 and makes OUTCOME/PROCESS scoring pervasive, so U is internally inconsistent here too. Reflection "against predefined criteria" (GT:L2816) and goal monitoring are evaluation. **Resolution:** evaluation remains a thread from Act I (A). *Evaluation engineering* (trajectory matchers, judges, drift, evalsets: GT:L12306–L12372) is the Act V deep dive.

**Merged act structure** (supersedes A §3 and §22.1 where they differ):

| Act | Learner role (U ∪ A) | Contents |
| --- | --- | --- |
| I Operator | worker | Define Done · Chaining (+schema) · Routing · Parallelization · **Composition** · Tools + authority basics · Exceptions basics |
| II Workflow designer | agent operator | Reflection · Context/Memory/Knowledge/RAG · Planning (+ReAct) · Reflection-vs-Reasoning |
| III Supervisor | workflow designer | Guardrails & least privilege · HITL & human-on-the-loop · Checkpoints/recovery depth · Goal monitoring & contracts |
| IV System designer | system architect | Multi-agent topologies & handoff contracts · MCP depth · A2A · Prioritization · HITL at scale |
| V Diagnostician | — | Evaluation engineering · postmortem gauntlet · **"Reflection fixes today, Learning fixes tomorrow"** · Learning & adaptation |
| VI Organization optimizer | organization designer | Resource-aware + deliberation lab · Exploration · Graduation |

### 4.4 Classification / ontology (U §4 vs A §4)

**Agreement** on most primary labels: 01–03 topology; 05 capability boundary; 10 and 15 as *interoperability protocols* (A's axis P; U says the same thing); 13 and 18 governance; 19 evaluation/observability; 20 scheduling; 17 deliberation; 16 resource control. U names "mission control" for Ch 11 and "resilience" for Ch 12. We adopt both names as axis labels.

**Disagreements.**

- U assigns one label per chapter ("at least eleven dimensions"). A assigns multiple axes per pattern. **A kept.** Reflection alone is a loop topology (producer–critic, GT:L2815), combinable with any node (GT:L2885), and a local evaluation. Single labels force a choice the source does not make. U effectively concedes this by calling Reflection both cross-cutting and a behavior "across another workflow".
- U marks 05–21 "source-only provisional" and implies 01–04 are further along. **Rejected.** There is no evidence for this (§2).

**U surfaced a real book overlap that A missed; adopted as new contradiction C-30.** Ch 11 "Goal Setting and Monitoring Pattern Overview" (GT:L7012–L7025) is a planning explanation: the trip analogy, initial and goal state, sequence of steps. It never discusses monitoring in that overview. Ch 6 already covers the same ground: "does the 'how' need to be discovered" (GT:L3839). Meanwhile Ch 19 explicitly distinguishes itself from Ch 11 (GT:L11900). Teaching consequence: separate *defining done / monitoring progress* (Ch 11's name and its At-a-Glance, GT:L7467ff) from *generating the plan* (Ch 6). Treat the Ch 11 overview as editorial overlap [SOURCE, flagged UNCERTAIN as to authorial intent].

U's boundary pairs (Planning/Goal, Tool/MCP, Multi-Agent/A2A, Memory/RAG, Reflection/Reasoning, Goal Monitoring/Evaluation, Recovery/Guardrails, Resource/Prioritization, Learning/Reflection) are **adopted as "confused-with" fields** in the Pattern Library (§4.9). Each becomes a discrimination exercise.

### 4.5 Mechanics and simulations (U §5–6)

**Agreement: near-total.** U adds three things, all adopted.

1. **Mechanics must interact.** Reflection everywhere bankrupts latency. Parallelizing everything causes races and duplicate mutations. Storing everything poisons retrieval. This is a design invariant: every mechanic has at least one cost coupling to another.
2. **Authority tokens** as a mechanic. This is sharper than A's permission matrix alone: a token is consumed on execution and is scoped. A keeps the matrix as the policy view.
3. **Planning needs real simulation because the world changes after the plan.** A had planning only as a later mission.

A adds, and keeps: receipts ledger; confidence-vs-accuracy reliability plot (U's "reliability meter from observed metrics" is the same idea); checkpoint pins; seed ensembles.

### 4.6 Engineered failures (U §7)

**Adopted as new class: SILENT SUCCESS.** The outcome check passes, but a process invariant was violated or a side-effect hit the wrong target (U's example: correct file written to the wrong project). This differs from A's F-15 (partial result *reported* as success). In silent success the result *is* correct, which is why outcome-only grading cannot catch it. It is registered as F-36 in the scenario contract's failure catalog. Detection requires invariant checks on the event stream, not on outputs ([EVALUATION-CONTRACT §3](EVALUATION-CONTRACT.md)).

Also adopted from U: unsafe parallel mutation; tool hallucination (calling a non-existent tool or arguments); non-convergent reflection; obsolete plan; metric gaming; **unsafe escalation avoidance** (the agent avoids asking because asking is scored as a cost), which pairs with A's over-escalation; and "successful outcome through unsafe process" (the parent category of silent success).

### 4.7 What the player sees; forensics (U §8–9)

**Adopt U's forensic timeline**, which is strictly better than the directive's and A's: OBSERVATION → DECISION → ROUTE → CONTEXT SELECTED → **ACTION REQUEST → AUTHORIZATION → EXECUTION** → RESULT → **STATE CHANGE → EVALUATION**. It encodes judgment≠authority directly in the timeline.

**Adopt "do not fake inspectable chain-of-thought".** It is consistent with A's Appendix F finding: model self-reports of reasoning are not evidence of mechanism (W-13).

This creates one tension with the source. Ch 18 asks structured logs to capture "its reasoning for the next step" (GT:L11796–L11797). **Resolution:** log *structured rationales* (reason codes plus evidence references). For live models, store any model-produced explanation as `model_stated_explanation`, labelled as output text, never as the internal computation.

**Disclosure tiers:** U's Beginner / Intermediate / Advanced / Expert tiers map onto A's unlock-by-mechanic model. **Adopt the tier names**, keeping A's rule that unlocks are earned by installing the mechanism, not by level. U's "then remove visual assistance" at Expert matches A's visibility-reversal principle (Q9).

### 4.8 Difficulty; "sometimes add nothing" (U §10)

**Adopted.** A had fragments: the no-AI route in M6, and graduation rewarding fewer agents. U makes "uncertainty about the architecture itself" the final difficulty axis. That is an axis A lacked, and it is added. Every act includes at least one mission where the best-scoring design **adds no new component**.

### 4.9 IA (U: six surfaces; A: nine routes)

**Adopt U's six as primary navigation.** A's three extra surfaces become secondary, reached from within the six.

| Primary surface (U) | A's equivalent | Secondary surfaces attached |
| --- | --- | --- |
| Academy (campaign map by competencies) | Campus map | — |
| Mission Control (world \| workflow; timeline/cost/status) | Mission workspace | Context tray, memory, router, permissions drawers |
| Architecture Lab (sandbox) | /lab | Deliberation lab |
| Forensics (replay/scrub) | Postmortem room | Evidence locker (own traces) |
| Pattern Library | Codex | **Sources** browser (book at cited lines; notebook status) |
| **Benchmark Lab** (compare human / agent traces) | — (new) | **Review** queue (reviewer role) |

**Pattern Library entry fields** merge U's list with A's four panes: problem · failure it prevents · cost · composes-with · **confused-with** · SOURCE evidence (cited) · SOURCE-CODE status badges · SYNTHESIZED/DERIVED interpretation (labelled) · counterexamples (WEAK) · missions experienced.

**Benchmark Lab conditions** (A adds, EXPERIMENTAL):

- Every contestant (human, Claude, Codex, local models, others) runs on the same engine with the same `visible_state`, tools, permissions and success contract ("Agent Mode").
- Results on **private held-out** scenarios are never published per-scenario.
- "Beowulf configuration" is EXTERNAL-UNVERIFIED. It may be registered as a contestant only once its definition is supplied.

### 4.10 Graduation (U §12 vs A Q12)

U: 12–20 consequential tasks, 4–6 agents. A: about 2,000 tasks over 30 simulated days. **Adopt U's scale for the core** (human-reviewable, every task consequential). Keep A's volume as an **automated background load** handled only by the routers and gates the learner designed. Volume tests System-1 design; the core tests judgment.

Adopt U's additional injections:

- "tempting unauthorized action";
- "reflection-wasting task";
- "deep-reasoning task";
- **"deterministic-code-superior task"**, where the best answer is a plain function and not a model.

U evaluates invariants, not a prescribed architecture. A agrees, and the evaluation contract formalizes this.

### 4.11 Instrumentation (U §15)

**Adopted**: U's scenario fields (`scenario_id, version, seed, world_state, visible_state, hidden_state, capabilities, authority_policy, success_contract, resource_budget, injected_failures`) and U's event field list. Both are merged with A's trace schema in [SCENARIO-CONTRACT.md](SCENARIO-CONTRACT.md).

**Adopted**: OUTCOME / PROCESS / GENERALIZATION. A's O and P scores map onto the first two. A's seed-ensemble robustness (P1) moves into GENERALIZATION, alongside held-out variants and transfer domains.

**Lifecycle**: U's `observation → reviewed → validated → fixture | counterexample | training-candidate` is merged with A's `screened`, `quarantined`, `superseded` and `retracted` states ([EVALUATION-CONTRACT §6](EVALUATION-CONTRACT.md)).

### 4.12 Assumptions U tries to falsify

All seven are **adopted**. A had four already: human traces aren't labels; visibility ≠ understanding; one optimal solution; success ≠ mastery. New from U:

- transfer missions with a different UI skin and domain;
- no "patterns unlock one by one" (composition by Mission 5);
- "public academy ≠ benchmark", which motivates the three-way split.

### 4.13 Derived vocabulary in U not adopted

`controlling_topology`, `unit_of_application`, "secondary local pattern", "relationship decomposition", "pattern retrieval as compilation", "System-1/System-2 decision bus", "CompSD-style durable state", Beowulf.

- **None has a definition in this repository.**
- Two look useful as ideas. `unit_of_application` (what a pattern is applied to: a node, an edge, a subgraph, or the whole workflow) overlaps A's cross-cutting axis. `controlling_topology` (which topology governs when patterns nest) overlaps A's composition missions.
- These two are held as **EXPERIMENTAL candidates** pending the user's definitions. They are not used in the contracts.
- The decision-bus idea is covered architecture-neutrally by the deliberation lab. No named architecture is preferred, per the directive.

## 5. Merged first ten missions (supersedes A §Q11 table ordering)

| # | Mission | From | Core concept | Key engineered failure | Class |
| --- | --- | --- | --- | --- | --- |
| 1 | **Define Done, then Do It** | U1 + A-M1 | Success contract before execution; the monolith fails *against the learner's own contract* | F-1 buried constraint; learner's contract turns out ambiguous | SOURCE (Ch 11 SMART GT:L7506; contracts GT:L12406) + EXPERIMENTAL |
| 2 | **Break the Monolith** | U2 + A-M2/M3 | Chaining with typed, schema-checked edges; localized recovery | F-2 corrupted Verify; F-3 prose-for-number | SOURCE (Ch 1; App A GT:L14676) |
| 3 | **Choose One Door** | U3 + A-M6 | Routing among fixed handlers: rules → embeddings → classifier; default/abstain; the no-AI route | F-7 misroute, no default | SOURCE (GT:L1238–L1265) |
| 4 | **Race the Clock** | U4 + A-M8 | Real vs apparent independence | F-9 hidden dependency; F-10 throttling / partial join; unsafe parallel mutation | SOURCE (Ch 3) + DERIVED |
| 5 | **The Mixed Workflow** | U5 | **Composition**: chain + route + fan-out in one design; one variant where the best answer adds nothing | Seams: router output schema ≠ chain input; a parallel branch needing a routed result | EXPERIMENTAL |
| 6 | **Hands Outside the Brain** | U6 + A-M4 + A-M7 | Tools; model *requests*, orchestrator *executes* (GT:L3735–L3743); authority tokens; policy gate on consequential actions | F-4 stale self-knowledge; F-5 error-as-data; F-8 confident request for an unauthorized action; tool hallucination | SOURCE + SYNTHESIZED + DERIVED (the principle) |
| 7 | **Something Broke** | U8 + A-M10 | Detect → handle → recover; checkpoints; idempotency; first full forensic replay | F-13 double side-effect; F-14 fallback never fires; **F-36 silent success** | SOURCE (Ch 12; GT:L11774) + DERIVED (idempotency) |
| 8 | **The Critic's Tax** | U9 + A-M9 | Reflection: criteria, stopping condition, separate critic; conditional use | F-11 reflect-everywhere; F-12 shared blind spot; non-convergent critique | SOURCE (Ch 4) + DERIVED (conditionality framing) |
| 9 | **What Should We Remember?** | U10 + A-M5 | Context vs working state vs validated knowledge vs history; retrieval grounding and staleness | F-6 grounded-but-stale; F-20 hypothesis → fact; F-21 summary drops constraint | SOURCE (Ch 8, 14) + DERIVED (4 layers) |
| 10 | **Script or Strategize?** | U7 | Fixed workflow vs plan discovery (GT:L3839); world changes after the plan | Obsolete plan; over-planning a fixed task | SOURCE (Ch 6) |

**Why this order and not U's:**

- Exceptions (7) move before Reflection and Memory because tools (6) fail immediately.
- Planning (10) moves after Reflection and Memory because re-planning uses both: a plan-level critique, and state that records what changed.

U's order puts Planning (7) before Exceptions (8), so its plans would meet failures the learner has not yet learned to handle. The trade-off is accepted: Mission 10 then doubles as the Act I→II boss.

## 6. Changes this implies to A

Recorded here; A is not rewritten, so its history stays auditable.

1. A §0.1 labels → read through the mapping in §3.
2. A §3 / §22 acts → superseded by §4.3's merged act table.
3. A §Q11 → superseded by §5. A's missions M3, M5, M6 and M7 are folded in, as shown.
4. A §16 → add **C-30** (Ch 11 overview duplicates planning; Ch 19 distinguishes itself from Ch 11, GT:L11900).
5. A §Q7 → add **F-36 silent success**, unsafe parallel mutation, tool hallucination, non-convergent reflection, obsolete plan, metric gaming, unsafe escalation avoidance.
6. A §Q12 → human-scale core + background load; four added injections.
7. A §Q15 → superseded by [SCENARIO-CONTRACT.md](SCENARIO-CONTRACT.md) and [EVALUATION-CONTRACT.md](EVALUATION-CONTRACT.md).
8. A §21 → six primary surfaces (§4.9).
9. A §Q3 claim "Tool Use should precede Routing" → withdrawn as a *teaching* claim (§4.2).
10. A §Q7 F-15 anchor → **overstated**; the correction was found while writing the contracts. A labels "graceful degradation must be *declared*" as canonical (GT:L7604–L7606). The book describes graceful degradation as keeping partial functionality, and lists notification as a separate strategy (GT:L7608–L7609). It does not require declaring the degradation. Reclassified: graceful degradation is SOURCE; "must be declared" is DERIVED. EVALUATION-CONTRACT HG4 carries the corrected label.
11. A §Q7 F-28 citation → the LLM-as-a-Judge row of the evaluation-method table is GT:L12314–L12317, not L12311–L12314. The content is unchanged.
