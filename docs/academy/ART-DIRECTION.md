# Agent Academy — Art Direction (design analysis, no code, no mockups)

**Status:** EXPERIMENTAL. This translates the user's visual directive (quoted verbatim in the appendix) into rules that bind visuals to the simulation. Nothing has been prototyped or tested with learners. No visual choice here has evidence that it teaches better than a plain 2D schematic. That is the first thing a pilot must test (§7).

**Labels:** [RECONCILIATION §3](RECONCILIATION.md#3-provenance-labels-one-scheme). Every visual element is a *rendering* of entities and events defined in [SCENARIO-CONTRACT.md](SCENARIO-CONTRACT.md). The book says nothing about visual design, so this entire document is EXPERIMENTAL, apart from the SOURCE anchors of the concepts being drawn.

---

## 1. The governing rule: the world is a view of the event stream

The directive's strongest line is "every window should represent an actual architectural responsibility and every animation should communicate meaningful state rather than decoration." It is adopted as a hard rule, and made checkable:

1. **Every persistent space** maps to a responsibility named in the scenario schema: a tool, a memory layer, a router, a policy, an agent, a queue or an evaluator.
2. **Every semantic animation** is triggered by a specific event type (SCENARIO-CONTRACT §4.2) and parameterized only by that event's fields. If no event fired, nothing semantic moves.
3. **Ambient motion** (atmosphere, parallax, idle particles) is allowed but must be *visibly non-semantic*: uniform, low-contrast, never directional between two spaces, and disabled under reduced motion. It may never resemble a semantic animation. This is where "decoration" is permitted, and it is fenced off.
4. **The renderer sees only `operator`-visible events during a run.** It never animates `failure.injected` or hidden state live. Doing so would leak ground truth (EVALUATION-CONTRACT INV-E1) and defeat the missions. The postmortem replay may render `postmortem` events, clearly styled as "revealed after the fact".
5. **Time is simulated time.** Animations play at a declared time-scale, and the scale is always on screen. "Real time" in the directive means *live with respect to the simulation*, not wall-clock parity.

A consequence the directive may not intend: a silent failure (F-36) produces **no** collision during the run, because nothing detected it. The learner sees a clean run and only meets the collision in Forensics. This is the intended lesson. It is also the strongest argument that the visuals must be event-driven and not scripted.

## 2. Spatial map: space = architectural responsibility

Layout principle: **depth encodes scope.**

- Near spaces are what one actor touches.
- Middle spaces are the shared infrastructure.
- Far and overhead spaces are governance and evaluation, which apply to everything beneath them.

Adjacency encodes the common data paths, so the camera's travel between neighbours follows real event flows.

| Space | Responsibility (schema entity) | Driving events | Placement | Concept class |
| --- | --- | --- | --- | --- |
| **Agent terminal** | One actor's decision point | `observation.presented`, `decision.made`, `route.decided` | Foreground, eye level | — |
| **Context tray** | The actor's current context (layer `context`); visible capacity | `context.loaded/evicted/summarized` | Attached to the terminal; physically small, and fills up | SOURCE (short-term memory, GT:L5007–L5018) |
| **Workflow floor with stations** | Chain stages with typed edges | `stage.entered/exited` | Floor plane leading away from the terminal | SOURCE (Ch 1) |
| **Router junction** | Routers and their default/abstain exits | `route.proposed/decided` | Branch points on the floor | SOURCE (Ch 2) |
| **Fan-out hall and join gate** | Parallel branches, parallel slots, join policy | `task.split/joined` | Widening of the floor; join gate has one socket per child | SOURCE (Ch 3) |
| **Critique chamber** | Reflection loop with a separate critic | `critique.round` | Side chamber off a station, with a visible round counter | SOURCE (Ch 4) |
| **Authorization gate** | Deterministic policy check between request and tool | `action.requested`, `authorization.decided` | Physically **in front of** the tool bay; the only way in | DERIVED principle; SOURCE ingredients (GT:L7945, L11804) |
| **Tool bay** | Tools, with their schemas, side-effect class and failure profile | `tool.executed` | Behind the gate. Irreversible tools styled distinctly from read-only ones. | SOURCE (Ch 5: model requests, orchestration layer executes, GT:L3737–L3742) |
| **World horizon** | External services and the world the tools change | `state.delta` | Beyond the tool bay; effects land on named targets | — |
| **Protocol ports** | MCP port on the tool bay; A2A dock to external agents | `tool.executed` via MCP; `handoff.*` to A2A partners | Tool-bay wall; outer dock | SOURCE (Ch 10, Ch 15) |
| **Working-state vault** | Layer `working_state` | `memory.read/write` | Mid-ground, shared by agents | DERIVED (4-layer cut) |
| **Knowledge archive** | Layer `validated_knowledge`; writes need a validation receipt | `memory.write` + receipt; `retrieval.result` | Mid-ground, sealed; separate from the vault | DERIVED; RAG SOURCE (Ch 14) |
| **History ledger** | Append-only event history | every event (hash chain) | A continuous strip along the floor edge | SOURCE (session history, GT:L5410); hash chain EXPERIMENTAL |
| **Approval desk** | Human approvers and their queue capacity | `escalation.opened/resolved` | Beside the gate; queue physically visible | SOURCE (Ch 13; scalability GT:L8128) |
| **Team floors** | Agents, their grants and memory scopes; handoff conduits | `agent.spawned/terminated`, `handoff.*` | Parallel floors at mid-depth | SOURCE (Ch 7) |
| **Intake conveyor** | Task queue and priorities | `task.created`, `priority.changed` | Entering from one side of the organization | SOURCE (Ch 20) |
| **Policy lattice** | Authority rules and tokens | rule edits; `authorization.decided` references | Overhead structure spanning every gate | DERIVED |
| **Evaluation deck** | Evaluators, invariant monitors, scores | `evaluation.result`, `failure.detected` | Overhead observation level | SOURCE (Ch 19) |
| **Forensics room** | Replay of a finished run's causal DAG | all, including `postmortem` | Separate space entered only after a run | — |
| **Budget gauges** | Resource budget dimensions | `budget.charged` | Fixed reference instruments, same place in every space | SOURCE (Ch 16) |

**Windows that expand.** The directive asks for windows that expand into mission interfaces and collapse back. Each space above has exactly one expanded form, its drawer or console in Mission Control (RECONCILIATION §4.9). Expanding a space never changes what it *is*: the expanded view shows the same entity's fields in full.

## 3. Animation → event mapping

| # | Animation (directive wording) | Trigger event(s) | Fields that drive it | End state | Must **not** imply |
| --- | --- | --- | --- | --- | --- |
| 1 | Task **splits** when parallelized | `task.split` | `children` (one fragment each); `parallel_slots` (fragments beyond the slot count wait visibly) | Fragments travel to branch lanes; `task.joined` later fills the join sockets. Missing children leave empty sockets. | That branches are simultaneous when the engine serialized them, or that splitting is free (each fragment charges budget) |
| 2 | Chooses different **illuminated pathways** when routed | `route.proposed` → `route.decided` | Candidates shown as **ranked** outlets; the chosen path lights; `default_used` / `abstained` use distinct styles | Task enters the chosen lane | That router scores are calibrated probabilities. Brightness must not scale with the score. Ranks only, unless the scenario declares calibration. |
| 3 | Moves **sequentially through stations** when chained | `stage.entered` / `stage.exited` | Input/output artifact ids; schema check result at each station exit | Artifact is carried as an object between stations; a failed schema check stops it at the exit | That a stage "understands" its input. A station transforms an artifact; its internals stay closed unless the learner built them. |
| 4 | **Loops through critique chambers** during reflection | `critique.round` | Round number (ring counter), criteria met / unmet, delta size; `budget.charged` drains visibly each round | Leaves the loop on "criteria met" or "cap reached" (different exits). Oscillation (F-39) is visible as a flip-flopping delta marker. | That more rounds mean better quality. The book warns about cost and latency (GT:L2859–L2862). |
| 5 | **Enters and leaves memory structures** | `memory.write` (entry); `memory.read`, `retrieval.result` (exit); `context.*` for the tray | `layer` picks the structure; `validation_receipt` present or absent (archive entry is blocked without one); document `version` tag is always visible | Item placed in the vault or archive with its version tag; retrieved copies carry that tag out | That memory lives inside the model, or that retrieval changes the model. A document's staleness is shown **only** through its version and date metadata during the run. The "superseded" highlight is postmortem-only. |
| 6 | **Crosses authorization gates** before tools can act | `action.requested` → `authorization.decided` → `tool.executed` | `effect`: permit (gate opens, **token visibly consumed**), deny (request returns to the requester), require_approval (diverts to the approval desk as `escalation.opened`) | Tool executes only after "permit". There is no path around the gate. | That the model executes tools itself. The model sends a *request*; the orchestration layer executes (GT:L3737–L3742). |
| 7 | **Branches toward specialized agents** | `agent.spawned`; `handoff.sent` / `handoff.received` | Target agent; the handoff artifact's fields (missing fields drawn as gaps); schema check at receipt | Artifact docks at the receiving team floor | That agents are persistent beings with continuous awareness. An agent exists as its grants, scopes and the calls made to it. |
| 8 | **Collides with simulated failures** | `failure.detected` (live); `failure.injected` (replay only) | `kind`, `detector` (engine vs learner-built), location = the event's target | Impact at the point of **detection**, not of injection. In replay, a dotted line connects injection to detection, showing the latency (P2). | That the failure was visible before anything detected it (rule 4). Undetected failures produce no collision live. |
| 9 | **Reroutes** during recovery | `recovery.action`; `checkpoint.created`; `rollback.applied` | Action type (retry / fallback / rollback / degrade / escalate); checkpoint pins; duplicate side-effects drawn as double marks on the world horizon | Task continues on the recovery path, or rewinds to a pin | That rollback undoes the world. Irreversible `state.delta` marks **stay** after a rollback, because only internal state rewinds. |
| 10 | **Converges into completed artifacts** | `task.joined`, `artifact.completed` | `declared_degradation` (an incomplete artifact is visibly incomplete); "claimed passed" vs oracle verdict | During the run, the artifact is marked *claimed*. Oracle verification appears only at run end. | That completion means correctness. "Claimed" and "verified" must look different (HG4, F-36). |

Supporting non-mission animations, all event-driven:

- the intake conveyor (`task.created`, `priority.changed`);
- the budget drain (`budget.charged`);
- the approval-queue length (`escalation.*`);
- the history-ledger tick for every event.

**Peripheral processes** ("distant processes continue operating visibly in peripheral space") are the scenario's real background load. They are rendered at reduced fidelity: glyphs, not full animations. They are never scripted filler.

## 4. Zoom-out progression mapped to the acts

The directive's order is terminal → workflows → teams → memory and knowledge → policy and evaluation → organism. The merged act structure ([RECONCILIATION §4.3](RECONCILIATION.md#43-teaching-order-us-10-phases-vs-as-6-acts)) teaches memory in Act II and governance in Act III, both **before** multi-agent teams in Act IV. The reasons are argued there: governance before multi-agent, and exceptions with tools.

The zoom therefore follows the acts, not the directive's literal order. This is a **deliberate deviation**, recorded here so it is not mistaken for an oversight.

| Act | Camera scope | Newly revealed spaces | What stays hidden or abstracted |
| --- | --- | --- | --- |
| I Operator | One agent terminal, then its workflow floor | Terminal, context tray, stations, router junction, fan-out hall, authorization gate + tool bay (the gate is *present and acting* but unexplained: implementation dependency), history ledger (thin) | Policy lattice (the gate just says "not permitted: rule POL-x"), memory layers beyond the tray |
| II Workflow designer | The workflow plus its infrastructure | Critique chamber, working-state vault, knowledge archive, retrieval paths | Team floors; the overhead levels |
| III Supervisor | Upward: the governance layer above the workflow | Policy lattice, approval desk + queue, checkpoint pins | Other teams |
| IV System designer | Outward: several team floors, protocol ports, intake conveyor | Team floors, handoff conduits, MCP port, A2A dock, priority conveyor | — |
| V Diagnostician | The evaluation deck and the Forensics room | Invariant monitors, evaluator outputs, replay of the causal DAG. At Expert tier, visual assistance is **removed**: the 2D schematic or text timeline only, per the visibility-reversal principle (DESIGN-ANALYSIS Q9). | — |
| VI Organization optimizer | The whole academy as one organization | Budget flows across all floors; background load at full scale | — |

**The "computational organism" final view** is allowed as a *composition* of real spaces. It is the organization's topology drawn at a distance. It may not introduce new visual vocabulary (see §5 on organic metaphors).

## 5. Metaphor-disclaimer rule

Visual metaphors teach mechanisms whether we intend it or not. The rules:

1. **No fake neural conduits.** The directive's "neural-like conduits" are **not adopted** as drawn. Channels between spaces are *message channels*: discrete packets along `causal_parents` edges. They must not use neuron, synapse, dendrite or brain-tissue imagery. That imagery implies weights, learning-in-transit, or that the system is a neural network at the architecture level. Models are sealed units, drawn as closed instruments. Nothing is drawn inside a model, because the scenario has no data about its insides. App F cautions against treating model self-descriptions as mechanism (DESIGN-ANALYSIS W-13; GT:L16127).
2. **Discrete, not fluid.** Information travels as countable packets tied to events, not as continuous streams or liquids. Request/response is discrete. A continuous "flow" would teach the wrong model of how agents call tools and models.
3. **No learning without an update event.** Nothing visibly "grows", "strengthens" or "glows brighter with experience" unless a learning-mechanism event (a gated update, Ch 9) fired. In-context use is never drawn as a lasting change.
4. **No anthropomorphic agents.** No faces or avatars that suggest persistent awareness. Agents are workstations with role labels, grants and scopes.
5. **Speed is not intelligence.** Packet speed reflects simulated latency only, never capability or "effort".
6. **"Organism" is a figure of speech.** The final zoom may be *called* an organism in text. The rendering stays architectural: stations, gates, archives, lattices. It never becomes biological.
7. **Every metaphor has a legend.** A persistent "What am I looking at?" legend maps each visual element to its schema entity and gives a one-line "this is **not**…" caption. The Pattern Library entry for each concept includes a "how it's drawn, and what the drawing does not mean" note.
8. **Mystery never hides the curriculum.** The directive's "mysterious" is allowed for atmosphere and for yet-unlocked spaces seen at a distance. It is never allowed for a mechanism the current mission teaches. Anything the learner is graded on must be inspectable.

## 6. Palette: HEX / PulseChain branding

- **This is a user-requested branding choice.** HEX magenta/violet and PulseChain cyan/purple give the academy its visual identity. **It implies no crypto integration**: no wallets, tokens, chains, prices, on-chain records or crypto terminology anywhere in the academy. Nothing in this repository or in the book relates to either project.
- **Authority tokens must not look like crypto tokens.** The "authority token" mechanic (SCENARIO-CONTRACT §2.5) plus this palette invites the misreading "tokens = cryptocurrency". Render authority tokens as badges or keycards, never coins, and never use the word "mint". The hash chain on the event log (SCENARIO-CONTRACT §4.1) is a tamper-evidence technique. It must not be marketed or drawn as a blockchain.
- **Exact colour values are UNCERTAIN.** We have not verified official brand colour codes, and none are asserted here. Whether using the brand names or their exact palettes needs permission is also UNCERTAIN, and is for the user to resolve.
- **Semantic colours sit outside the brand palette.** Magenta, violet, cyan and purple are *identity* colours for spaces and ambient light. Failure, deny and irreversible side-effects need a separate, reserved warning hue (e.g., an amber/red family) that the brand colours never use. That keeps "danger" unambiguous.
- **Colour is never the only channel.** Every state encoded in colour is also encoded in shape, pattern, label or position (WCAG 1.4.1). Magenta vs violet vs purple is a poor distinction for many colour-vision types, so no two *semantic* states may differ only by those hues.
- **Restrained neon on dark** (per the directive) must still meet text-contrast minimums (WCAG 1.4.3 / 1.4.11). Glow effects may not be the only boundary of an interactive element.

## 7. Honest risks

### 7.1 Accessibility

- **Reduced motion.** Honour the OS setting (`prefers-reduced-motion`) and provide an in-app toggle. Under reduced motion:
  - semantic animations become state changes: cuts, with the changed element marked;
  - ambient motion and parallax stop;
  - camera travel becomes instant transitions.
- **Pause and flashes.** Any auto-playing motion must be pausable (WCAG 2.2.2). No flashing above three per second (2.3.1). Motion caused by interaction must be disableable (2.3.3).
- **Vestibular risk.** Free 3D camera travel and parallax can cause motion sickness. The camera is never scroll-hijacked inside missions. Scroll-driven travel is limited to the campus overview and is optional.
- **Screen readers.** A 3D canvas is opaque to assistive technology. The **event stream rendered as a text timeline** is therefore a primary view, not an afterthought:
  - every semantic animation has a text equivalent generated from the same event;
  - every space has an accessible name and a structured summary (queue length, budget, last decision);
  - keyboard navigation moves between spaces in the §2 adjacency order.
- **2D fallback.** A schematic 2D graph view with **identical semantics**: same entities, same event-driven changes. It is the Expert-tier view (§4), the low-end view (§7.2), and the reference view for any learner who prefers it. If a concept can only be understood in the 3D view, that is a defect.

### 7.2 Low-end devices and performance

- "Photorealistic", "extremely high-detail" and "volumetric atmosphere" conflict with running on school laptops, phones and integrated GPUs.
- Tiered rendering:
  - capability detection at load;
  - on lower tiers, remove volumetrics, reflections and particles *first*, and semantic animations *never*;
  - a frame-time budget with automatic downgrade.
- Loading. Large 3D assets delay the first mission. Budget for a fast first interaction: the terminal and the first workflow floor must be usable before distant spaces load.
- Battery and thermal limits on mobile. Peripheral processes are throttled when off-screen.
- UNCERTAIN: whether the full-fidelity tier is worth its cost at all. The pilot should compare learning outcomes between the 3D and 2D views.

### 7.3 Cognitive overload vs progressive disclosure

- The directive's "continuously shows those abilities happening around them" conflicts with progressive disclosure and with the attention limits of a novice. A learner who sees ten mechanisms moving at once in Mission 1 learns none of them.
- Resolution: only spaces **revealed by the current act** (§4) animate at full salience. Background load appears as low-salience glyphs. Anything not yet revealed is a dim silhouette with no semantic motion.
- A salience budget: at most one foreground semantic animation plays at a time at normal speed. Others queue briefly or appear in the history ledger. Forensics can replay them in order.
- Engineered failures must be detectable (SCENARIO-CONTRACT rule 4). A detection signal lost in visual noise is effectively unobservable. Authoring validation should include a "signal salience" review for each injected failure.

### 7.4 Spectacle teaching false mechanistic models

- This is the risk that matters most for an academy. A beautiful system of glowing conduits can convince learners that agents work the way they look. The possible false beliefs:
  - continuous thought;
  - neural wiring between components;
  - agents as beings;
  - memory inside models;
  - speed as capability;
  - "completed" as "correct".
- §5 guards against these by rule. The rules are not evidence that the guards work.
- Proposed pilot probe: after a mission, ask learners to *predict* system behaviour in a changed situation (for example, "the tool times out after committing; what happens on retry?"). Compare the 3D group, the 2D group and a text-only group. If the 3D group predicts worse, the visuals are teaching the wrong model, and they lose to the schematic regardless of their appeal.
- The directive's "the website itself is the agent architecture" is true only in a narrow sense: the website renders a simulated architecture's event stream. The academy must say so plainly, somewhere a learner will read it. The simulation is not a live agent system, and the simulated models are not real models.

### 7.5 Other tensions noted, not resolved

- "Premium, realistic" vs "technically credible". Photorealism for things that have no physical form, such as policies, contexts and routers, is itself a metaphor. It must obey §5 like any other.
- "Unlike a normal SaaS dashboard": the Mission Control drawers (context, memory, router, permissions) are dashboards by nature. Their *entry* can be spatial, but their contents should be plain, legible panels. Legibility wins over style inside any interactive console.

## Appendix: the user's visual directive (verbatim)

Source: the user's design message of 2026-09-27, as preserved verbatim in the coordinator's condensation. It is reproduced so that every deviation above can be checked against it.

> Design the Agent Academy as a **cinematic, spatial 3D digital world rather than a conventional website**: the learner should feel as though they have physically entered a living AI system, standing inside a dark, photorealistic HEX/PulseChain command environment where translucent glass workspaces, agent terminals, memory vaults, tool interfaces, browser windows, code environments, knowledge stores, and simulation chambers exist as distinct floating architectural spaces arranged beside and behind one another in depth; as the user scrolls or moves through the experience, the camera should travel naturally between these adjacent spaces while luminous HEX magenta/violet and PulseChain cyan/purple streams of information visibly travel through cables, light paths, neural-like conduits, and airborne data channels from one system to another—tasks should physically split when parallelized, choose different illuminated pathways when routed, move sequentially through stations when chained, loop visibly through critique chambers during reflection, enter and leave memory structures, cross authorization gates before tools can act, branch toward specialized agents, collide with simulated failures, reroute during recovery, and ultimately converge into completed artifacts—so instead of **telling** visitors that agents can plan, browse, code, retrieve knowledge, use tools, collaborate, remember, evaluate, recover, and operate simultaneously, the environment continuously **shows those abilities happening around them in real time**; every window should represent an actual architectural responsibility and every animation should communicate meaningful state rather than decoration, with windows capable of expanding into interactive mission interfaces and collapsing back into the surrounding system, while distant processes continue operating visibly in peripheral space; progressively zoom the learner outward from controlling one agent terminal to seeing workflows, then teams of agents, then memory and knowledge infrastructure, then policy and evaluation layers, until the final perspective reveals the entire academy as one enormous interconnected computational organism—premium, realistic, mysterious, technically credible, extremely high-detail, and visually unlike a normal SaaS dashboard, landing page, or collection of floating cards, using cinematic depth, volumetric atmosphere, reflective dark materials, restrained neon illumination, flowing information particles, parallax, physically coherent transitions, and seamless spatial continuity to create the feeling that **the website itself is the agent architecture and the visitor is walking through it while it operates**.

**Deviations from the directive, summarized:**

1. The zoom order follows the acts, so policy comes before teams (§4).
2. "Neural-like conduits" are replaced by discrete message channels (§5.1).
3. "Streams" of information become countable packets (§5.2).
4. "Organism" is kept as a word only (§5.6).
5. "Continuously shows" is bounded by a salience budget (§7.3).
6. "Mysterious" never applies to taught mechanisms (§5.8).
7. Crypto associations are excluded (§6).
