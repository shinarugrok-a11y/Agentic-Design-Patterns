# Provenance audit for the Agent Academy design

Companion to [`DESIGN-ANALYSIS.md`](DESIGN-ANALYSIS.md). The labels ([C], [C-nb], [W], [D], [U], [X]) are defined there in §0.1.

## 1. Commits and sources

| Ref | SHA | Date | Role in this audit |
| --- | --- | --- | --- |
| `origin/cursor/repo-evidence-audit-1033` | `ed7e205` | 2026-09-23 | **Newest.** Only validation records (`validation/audit/`). Corrected README and validator. |
| `origin/main` | `ed9027e` | 2026-09-21 | Adds `ground-truth/agentic_design_patterns.txt` (via `92334d7`) and the AGENTS.md rule change (`a486c70`). |
| `cursor/agent-skill-library-eada` | `10ad49a` | 2026-09-20 | Base of this branch. Contains the skill library. No ground truth, no audit. |
| `…-b24b`, `…-6dc8`, `…-7680`, `…-3108` | various | 2026-09-20 | Older, superseded skill-library attempts. No directive-named artifacts. |
| `evoiz` upstream tip (per audit) | `e11e6fb` | 2026-07-24 | Original book repo: PDF + notebooks. |

Book text used: `ed9027e:ground-truth/agentic_design_patterns.txt`. It is byte-identical (checked with `cmp`) to the user's upload `agentic_design_patterns_ec92.txt`.

## 2. Directive-named artifacts

| Term | Exists? | Location / note |
| --- | --- | --- |
| canonical pattern records | No (only [D] summaries) | `manifest.json`, `skills/*/SKILL.md` |
| code-pattern records | No (only [D] notes mixing book and invented code) | `skills/*/references/*.md` |
| ROUTING-INDEX | **[X]** | — |
| EVALUATION-LAYER-MODEL | **[X]** | — |
| MANIFEST | Yes | `manifest.json` [D] |
| validation records | Yes, on `ed7e205` only | `validation/audit/01…10`, `evidence-claims.json`, `notebook-inventory.json` |
| conversion findings | **[X]** by name | Closest: `validation/audit/03-documentation-accuracy.md`, `04-correction-log.md` |
| contradictions | **[X]** by name | Closest: `validation/audit/09-consistency-report.md` (repo-internal only). New register: DESIGN-ANALYSIS §16. |
| extraction findings | **[X]** by name | Closest: `ground-truth/README.md`; audit evidence map (17-line Poppler delta) |
| failed routing fixtures | **[X]** | No fixtures or tests exist beyond `tools/validate.py` |
| schema history | **[X]** | Only git history of `manifest.json` |

Search method: `git grep -il <term> <ref>` over every remote ref (excluding `*.pdf` and `*.ipynb`), plus commit-message search. The terms searched were ROUTING-INDEX, ROUTING_INDEX, EVALUATION-LAYER, EVALUATION_LAYER, "schema history", "failed routing", fixture, contradiction, "conversion finding", "extraction finding", "validation record", JEV, and fly-inspired. "fixture" matched only an ordinary use of the word in one old branch's skill note. "contradiction" matched only book prose and one RAG note.

## 3. Evidence classes across the corpus

### 3.1 Canonical, verified in this analysis (book text located at a cited line)

Every `GT:L` citation in DESIGN-ANALYSIS was located by grep in the ground-truth text. That establishes that *the book says it*. It does not establish that the claim is true. The load-bearing ones:

| Claim (paraphrase) | GT line(s) | PDF page (chapter start) |
| --- | --- | --- |
| Book extracts 21 patterns; chapters "ordered to build concepts progressively" | L311, L346 | intro |
| Agent levels 0–3 | L452, L462, L476, L523 | p.12ff |
| Context engineering definition; "short, focused, and powerful context" | L486–L497 | p.12ff |
| Level 3 limited by LLM reasoning | L548 | p.12ff |
| Hypothesis 5: architectural vs instructional modification | L646–L652 | p.12ff |
| Chaining What/Why/Rule; "easier to debug" | L1126–L1149 | p.21 |
| Four routing mechanisms (LLM, embedding, rule, trained classifier) | L1238–L1265 | p.34 |
| Routing summaries list three mechanisms | L1733, L1756 | p.34 |
| Parallelization needs independence; "substantial complexity and cost" | L2332–L2346, L2365–L2367 | p.48 |
| Reflection stopping condition; separate critic; cost/context/throttling | L2445, L2822–L2826, L2859–L2862 | p.63 |
| Tool Use What/Why | L3728–L3750 | p.77 |
| Multi-agent collaboration forms and topologies | L4303–L4330, L4405–L4450 | p.111 |
| Memory: two components; ADK scopes; state_delta; direct mutation "strongly discouraged"; memory types | L5229, L5303–L5336, L5410–L5418, L5649–L5670, L5817–L5822, L5867, L5875 | p.130 |
| Goal-setting caveat: same LLM writes and judges; "running forever" | L7405–L7418 | p.181 |
| Exception triad; reflective retry; retries | L7564, L7580–L7612 | p.194 |
| HITL lack of scalability; escalation policies; human-on-the-loop (policy) | L7882, L7945, L8125, L8128 | p.202 |
| RAG What/Why ("outdated") | L8685–L8700 | p.211 |
| A2A vs MCP distinction | Ch 15 Key Takeaways (~L9340) | p.229 |
| OpenRouter example located in Ch 16 | L9806 | p.244 |
| Resource-aware: Router Agent, Critique Agent, fallback/graceful degradation, contextual pruning | L9403–L9406, L9909, L9959–L9966 | p.244 |
| Thinking budget; Scaling Inference Law; ReAct as core loop | L10638, L10725, L10930 | p.260 |
| Engineering Reliable Agents: checkpoint/rollback, modularity, structured logging with confidence, least privilege, blast radius | L11765–L11810 | p.284 |
| Prompt injection mentioned only as a reference link | L11891 | p.284 |
| Evaluation method table; outcome and trajectory; trajectory matchers; test files and evalsets | L12306–L12372 | p.304 |
| "Does adding more agents improve performance?"; contractor model | L12400–L12470 | p.304 |
| Prioritization criteria; dynamic re-prioritization | L12975, L13002 | p.323 |
| Co-Scientist Elo tournament | L13109 | p.333 |
| App A context engineering; "richness" of context; structured output "absolute necessity" | L13838–L13900, L13851, L14676–L14680 | p.347 |
| App B agent-computer interfaces | L14737–L14760 | p.376 |
| App G primacy of context; no black-box retrieval; direct model access; personas; human "ultimate authority" | L16326–L16365 | p.417 |
| Conclusion 4-group taxonomy; composition example; human-on-the-loop (reporting); drift question | L16536–L16580, L16596, L16655–L16660, L16683 | after App G |
| Terms absent from the book: "idempot", "calibrat", System 1/2 (as dual-process), JEV, fly-inspired, recurrent | 0 hits | — |

### 3.2 Canonical but unverified

- **Notebook content** [C-nb]. Never diffed cell-by-cell against the book's printed code. Spot matches: Ch 11 `goals_met` (GT:L7207), Ch 12 state key (GT:L7687), OpenRouter (GT:L9806).
- **Chapter bodies not read in full**: Ch 5, 6, 9, 10, 14, 15, 17, 21 and App C–E. Summaries and targeted greps only.
- **External or time-sensitive book claims** [U]: market sizes (~L423–L427), "30% of code" (App G), model identifiers, A2A method names (`tasks/send`, `tasks/sendSubscribe`), the "Scaling Inference Law" label, and the Deloitte/Cloudera statistics.
- **Figures**: not viewed (text extract only).
- **Audit-branch facts** read but not re-run: `pdfinfo` 458 pages; the 17-line Poppler delta; the Colab metadata finding; the secret-pattern scan.

### 3.3 Derived

| Item | Why it is [D] |
| --- | --- |
| `skills/*` (84 files), `manifest.json`, `chapter_notebooks/*.SKILL.md` | Written by us. `failure_modes`, `when_not_to_use` and `chains_with` are mostly our inferences, with no per-field citation. |
| `skills/*/examples/minimal.py` | Offline simulations with keyword/regex stubs standing in for models. They show that a mechanism runs, not that it matches the book. |
| `skills/*/references/deep-dive.md` | Mix book code and invented code. 17 of 21 contain no marker such as "derived", "sketch" or "illustrative". |
| `AGENTS.md` role map (planner/executor/critic/memory/safety) | From the user's earlier spec. The book has no role taxonomy. |
| `models/*.md` (Fable 5.1, Grok 4.6, Muse) | Model names, context windows and costs are unverified. None appear in the book. |
| `tools/validate.py` token budget (3,000) | A product constraint, not a book claim. |
| `validation/audit/*` | An independent audit, but an interpretation of the repo, not of the book's claims. |
| The academy's ontology, JUDGMENT≠AUTHORITY, 4-layer memory, System-1/System-2 / deliberation budget, outcome vs process, trace lifecycle, missions, thresholds | This design. See DESIGN-ANALYSIS Q14. |

### 3.4 Missing or nonexistent

The [X] rows in §2 above, plus: no `tests/`, no `requirements.txt`, no `LICENSE` (notebook headers cite an MIT `LICENSE` that does not exist, per the audit), and no pinned dependency versions for any notebook.

## 4. Notebook inventory with verified weaknesses

"Parses" and "Stored errors" come from the audit's `notebook-inventory.json` and were re-derived here from the ipynb JSON. The flags are regex name matches on code (for example, `AgentExecutor`) and are [U] with respect to current library versions. The semantic notes were verified by reading the code.

| Notebook | Code chars | Parses | Stored errors | Flags (name-matched) | Verified semantic note |
| --- | ---: | --- | --- | --- | --- |
| `Appendix_A_Advanced_Prompting_Techniques.ipynb` | 83 | yes | — | — | Google-Drive placeholder; raises NameError. |
| `Appendix_B_AI_Agentic_From_GUI_to_Real_world_environment.ipynb` | 83 | yes | — | — | Google-Drive placeholder; raises NameError. |
| `Appendix_C_(Code).ipynb` | 2534 | yes | NameError | exp/old model id | Stored NameError; first cell says not runnable. |
| `Appendix_C_Quick_overview_of_Agentic_Frameworks.ipynb` | 83 | yes | — | — | Google-Drive placeholder; raises NameError. |
| `Appendix_D_Building_an_Agent_with_AgentSpace.ipynb` | 83 | yes | — | — | Google-Drive placeholder; raises NameError. |
| `Appendix_E_AI_Agents_on_the_CLI.ipynb` | 83 | yes | — | — | Google-Drive placeholder; raises NameError. |
| `Appendix_F_Under_the_Hood_Reasoning_Engines.ipynb` | 83 | yes | — | — | Google-Drive placeholder; raises NameError. |
| `Appendix_G_Coding_agents.ipynb` | 83 | yes | — | — | Google-Drive placeholder; raises NameError. |
| `Appendix_Pydantic.ipynb` | 1819 | yes | — | — | Needs pydantic (not installed in audit env). |
| `Chapter_01_Prompt_Chaining_(Code_Example).ipynb` | 1559 | yes | — | — |  |
| `Chapter_01_Prompt_Chaining_(JSON_Example).ipynb` | 450 | yes | — | — | A JSON literal, not a program. |
| `Chapter_02_Routing_(Google_ADK).ipynb` | 5310 | yes | — | — |  |
| `Chapter_02_Routing_(LangGraph).ipynb` | 4361 | yes | — | — |  |
| `Chapter_02_Routing_(Openrouter).ipynb` | 539 | yes | — | placeholder | Misfiled: code is Ch 16 (GT:L9806). Single fixed-model call; no routing. |
| `Chapter_03_Parallelization_(Google_ADK).ipynb` | 5266 | no | — | — | Leading indent -> SyntaxError. |
| `Chapter_03_Parallelization_(LangChain).ipynb` | 3458 | yes | — | — |  |
| `Chapter_04_Reflection_(ADK).ipynb` | 1466 | yes | — | — |  |
| `Chapter_04_Reflection_(Iterative_Loop).ipynb` | 4243 | yes | — | — |  |
| `Chapter_04_Reflection_(LangChain).ipynb` | 3334 | yes | — | — |  |
| `Chapter_05_Tool_Use_(CrewAI).ipynb` | 4040 | yes | — | placeholder |  |
| `Chapter_05_Tool_Use_(Executing_Code).ipynb` | 3972 | yes | — | — |  |
| `Chapter_05_Tool_Use_(Google_Search).ipynb` | 1543 | yes | — | exp/old model id |  |
| `Chapter_05_Tool_Use_(LangChain).ipynb` | 7102 | yes | — | AgentExecutor |  |
| `Chapter_05_Tool_Use_(Vertex_AI_Search).ipynb` | 3534 | yes | — | exp/old model id, placeholder |  |
| `Chapter_06_Planning_(Code_Example).ipynb` | 1787 | yes | — | — |  |
| `Chapter_06_Planning_(Deep_Research_API).ipynb` | 2874 | yes | AuthenticationError | placeholder | Stored 401 from placeholder key; model id time-specific [U]. |
| `Chapter_07_Multi_Agent_(ADK_Gemini_AgentTool).ipynb` | 2923 | yes | — | — |  |
| `Chapter_07_Multi_Agent_(ADK_Gemini_Coordinator).ipynb` | 1809 | yes | — | exp/old model id |  |
| `Chapter_07_Multi_Agent_(ADK_Gemini_Loop).ipynb` | 1875 | yes | — | exp/old model id |  |
| `Chapter_07_Multi_Agent_(ADK_Gemini_Parallel).ipynb` | 1841 | yes | — | exp/old model id |  |
| `Chapter_07_Multi_Agent_(ADK_Gemini_Sequential).ipynb` | 699 | yes | — | — |  |
| `Chapter_07_Multi_Agent_(CrewAI_Gemini).ipynb` | 2803 | yes | — | — |  |
| `Chapter_08_Memory_(ADK_Explicit_State_Update).ipynb` | 2423 | yes | — | — |  |
| `Chapter_08_Memory_(ADK_LlmAgent_output_key).ipynb` | 1400 | yes | — | — |  |
| `Chapter_08_Memory_(ADK_MemoryService_InMemory).ipynb` | 1346 | yes | — | — |  |
| `Chapter_08_Memory_(ADK_SessionService).ipynb` | 1898 | yes | — | — |  |
| `Chapter_08_Memory_(LangChain_LangGraph).ipynb` | 4950 | yes | ModuleNotFoundError, NameError | LLMChain, ConversationBufferMemory | Stored ModuleNotFound/NameError; deprecated memory APIs. |
| `Chapter_09_Adaptation_(OpenEvolve).ipynb` | 405 | yes | — | placeholder | 405 chars; path/to/ placeholders; top-level await. Thinnest chapter code. |
| `Chapter_10_MCP_(ADK_FastMCP_Server).ipynb` | 898 | yes | — | — |  |
| `Chapter_10_MCP_(FastMCP_Client_Agent_init).ipynb` | 74 | yes | — | — | `from . import agent` fragment. |
| `Chapter_10_MCP_(FastMCP_Server_Example).ipynb` | 1507 | yes | — | — |  |
| `Chapter_10_MCP_(Filesystem_Example_agent).ipynb` | 2024 | yes | ModuleNotFoundError | — | Stored ModuleNotFoundError. |
| `Chapter_10_MCP_(Filesystem_Example_init).ipynb` | 63 | yes | — | — | `from . import agent` fragment. |
| `Chapter_11_Goal_Setting_(Iteration).ipynb` | 7854 | yes | — | — | Same LLM writes and judges (book caveat GT:L7405-L7418); max_iterations=5. |
| `Chapter_12_Exception_Handling_(Fallback).ipynb` | 1540 | yes | — | exp/old model id | Tools undefined; nothing sets state["primary_location_failed"]; fallback decided by LLM instruction. |
| `Chapter_13_Human_in_the_Loop_(Customer_Support).ipynb` | 2811 | yes | — | exp/old model id | escalate_to_human stub returns success; no human gate; inserts role="system" content [U]. |
| `Chapter_14_Knowledge_Retrieval_(RAG_Google_Search).ipynb` | 284 | no | — | exp/old model id | `tools=[Google Search]` invalid syntax; 284 chars. |
| `Chapter_14_Knowledge_Retrieval_(RAG_LangChain).ipynb` | 4057 | yes | — | exp/old model id, placeholder |  |
| `Chapter_14_Knowledge_Retrieval_(RAG_VertexAI).ipynb` | 1222 | yes | — | — |  |
| `Chapter_15_Inter_Agent_(A2A).ipynb` | 3263 | yes | ModuleNotFoundError | AgentExecutor | Stored ModuleNotFoundError. |
| `Chapter_15_Inter_Agent_(A2A_AgentCard_WeatherBot).ipynb` | 1311 | yes | — | — |  |
| `Chapter_15_Inter_Agent_(Sync_Streaming_Requests).ipynb` | 830 | no | — | — | JSON protocol examples in a code cell. |
| `Chapter_16_Resource_Optimization_(Code_Snippets).ipynb` | 3303 | yes | — | — | Self-declared "not runnable"; routes by word count <20; AsyncGenerator not imported. |
| `Chapter_16_Resource_Optimization_(OI_Google_Search).ipynb` | 4739 | yes | — | — | LLM classifier (simple/reasoning/internet_search); needs OpenAI + Google CSE keys. |
| `Chapter_17_Reasoning_(CoT_Prompt).ipynb` | 4069 | no | — | — | Prompt prose in a code cell. |
| `Chapter_17_Reasoning_(Executing_Code).ipynb` | 741 | yes | — | — |  |
| `Chapter_17_Reasoning_(Google_DeepSearch).ipynb` | 954 | yes | — | — |  |
| `Chapter_17_Reasoning_(Self_Correction).ipynb` | 3744 | no | — | — | Prompt prose in a code cell. |
| `Chapter_18_Guardrails_(ADK_Validate_Tool).ipynb` | 1667 | yes | — | exp/old model id |  |
| `Chapter_18_Guardrails_(LLM_as_Guardrail).ipynb` | 3658 | no | — | — | Prompt prose in a code cell. |
| `Chapter_18_Guardrails_(Practical_Examples).ipynb` | 13747 | yes | — | — |  |
| `Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb` | 2338 | yes | — | — | Runs offline; exact match scores correct paraphrase 0.0; tokens via split(). |
| `Chapter_19_Evaluation_(LLM_as_Judge).ipynb` | 6973 | yes | — | google.generativeai, exp/old model id, placeholder | Uses deprecated google.generativeai SDK [U]. |
| `Chapter_20_Prioritization_(SuperSimplePM).ipynb` | 7446 | yes | — | AgentExecutor, ConversationBufferMemory | Tags P0/P1/P2 only; no ranking or re-prioritization; silent P1 default. |
| `Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb` | 7130 | no | — | — | External excerpt (AgentLaboratory); does not parse; 3 reviewers = 1 model, 3 prompts. |

Totals: 65 notebooks (56 chapter + 9 appendix). 7 do not parse. 7 are placeholders. 5 have stored error outputs. Per the audit, only `Chapter_19_Evaluation_(Basic_Response_Evaluation)` runs offline.

## 5. Skill-library findings relevant to teaching

| Skill | Finding | Class |
| --- | --- | --- |
| `routing` | deep-dive calls OpenRouter "the chapter's" example (it is Ch 16's); cites the misfiled notebook as a routing source | contradiction |
| `exception-handling` | deep-dive invents `get_precise_location_info` that sets the fallback flag, then explains "Why it works". The book defines no such tool (the key appears only in the instruction, GT:L7687). | damaged → positive promotion |
| `human-in-the-loop` | patterns/deep-dive present the notebook's stub escalation (`escalate_to_human` returning success) as the "default and cheapest variant" without noting that no human gate exists | weak example promoted |
| `prioritization` | deep-dive reproduces the SuperSimplePM tagging code; the chapter's dynamic re-prioritization claim is not demonstrated | weak example |
| `evaluation-monitoring` | correctly flags exact match as brittle | good |
| `memory-management` | SKILL.md failure mode ("direct state mutation") sits beside an example that writes `tool_context.state` (legitimate per book L5328) | ambiguous |
| all | no entries for context engineering, structured output, checkpoint/rollback, least privilege, contracts, human-on-the-loop, agent levels, trajectory matchers | coverage gap |

These are recorded, not fixed. The existing skill files were not modified by this work, per instruction.

## 6. Validator status by commit

| Commit | Result | Failing checks |
| --- | --- | --- |
| `10ad49a` (this branch's base; run here with `tiktoken` installed) | 27 pass / 1 fail | "PDF, notebooks and READMEs unmodified vs origin/main" — fails only because `origin/main` gained `ground-truth/README.md`. Token simulation passes: walk-through 2,974, worst pair 2,982. |
| `ed7e205` (newest; per `validation/audit/09-consistency-report.md`) | 26 pass / 2 fail | Token simulation 3,006 and 3,014 over the 3,000 budget, after the longer AGENTS.md rule from `a486c70`. |
| `8d15ae3` (this branch after merging `origin/main` and `ed7e205`; re-run here) | 26 pass / 2 fail | Same two: "simulation: executor walk-through < 3000" (3,006 tokens) and "every role pair + one patterns.md < 3000" (worst 3,014). Reported, not fixed; no skill file was edited. |

Conclusion: "validated" is branch-dependent and structural only. No check tests whether any skill claim matches the book.

## 7. EXTERNAL-UNVERIFIED claims register (user analysis 2026-09-27)

Source of the claims: the user's "Agent Academy — First Design Analysis", condensed by the coordinator. Reconciled in [`RECONCILIATION.md`](RECONCILIATION.md).

Method:

- `git grep -i` across every local and remote ref, excluding `docs/academy/`.
- `git log --all -S` for pickaxe history.
- `ast.parse` over the code cells of all 65 notebooks, with `!`/`%` magics stripped.
- Direct reads of `ground-truth/agentic_design_patterns.txt`.

Run on `8d15ae3`.

Status values:

- **NOT FOUND**: the artifact or term is absent from every ref and from history. It is labelled EXTERNAL-UNVERIFIED and may not be relied on.
- **FALSE**: the repository contradicts the claim.
- **UNSUPPORTED**: nothing in the repository bears on the claim either way.
- **VERIFIED** / **PARTIAL**: checked against the book text.

### 7.1 Claims about corpus artifacts

| # | User claim | Status | Evidence |
| --- | --- | --- | --- |
| X-1 | APD-01..APD-04 have structured extraction records | NOT FOUND | No `APD-` string in any ref or in history. `validation/audit/06-candidate-pattern-mappings.md:3`: "There is no `APD-NN` ontology in the tree." |
| X-2 | Those records are marked `status: unverified` | NOT FOUND | The string occurs only in `validation/audit/04-correction-log.md:117` and `10-unresolved.md:3`, both about this repo's own README claims, not about pattern records. |
| X-3 | APD-05..21 have not undergone extraction/verification | NOT FOUND (vacuous) | No APD records exist at all. |
| X-4 | MANIFEST `pattern_index` lists APD-01/02 at schema 2.1 while records are 2.2 | NOT FOUND | `manifest.json` has `version: "1.0"` and keys `version`, `source`, `skills` only. No `pattern_index` in any ref or in history. There are no schema versions 2.1 or 2.2. |
| X-5 | A "conversion log" shows syntax-breaking PDF damage across examples | NOT FOUND | No conversion log exists. The notebooks are not PDF conversions. They are the book's companion `.ipynb` files, and their parse failures are authoring defects (7.2). |
| X-6 | "The D4 correction demonstrates internal consistency improvement" of a router | NOT FOUND | No D4 correction, router, or routing fixture exists. `validation/audit/04-correction-log.md` records README/validator corrections only. |
| X-7 | "Relationship decomposition fixed a real synthetic routing failure" | NOT FOUND | There are no routing fixtures and no such term. |
| X-8 | `controlling_topology`, `unit_of_application`, "secondary local pattern" | NOT FOUND | None exists in any ref or in history. |
| X-9 | "System-1/System-2 decision bus" | NOT FOUND | Absent from the repo. The book has no System 1/System 2 dual-process framing (0 hits). |
| X-10 | "CompSD-style external durable state" | NOT FOUND | Absent. |
| X-11 | "Pattern retrieval as a compilation process" | NOT FOUND | Absent. |
| X-12 | "Beowulf configuration" | NOT FOUND | Absent. Not registrable as a Benchmark Lab contestant until defined. |
| X-13 | ROUTING-INDEX, EVALUATION-LAYER-MODEL (as corpus artifacts) | NOT FOUND | Absent. |
| X-14 | "Reflection batch contains particularly severe corruption" | **FALSE** | All three `Chapter_04_Reflection_*` notebooks (ADK, Iterative_Loop, LangChain) parse. The Ch 4 book text (GT:L2445–L2890) is clean prose and code. See 7.2 for the actual failures. |
| X-15 | Extracted code "can't serve as canonical implementation" | PARTIAL | True for the 7 non-parsing notebooks and for the placeholders (§4). It is not true corpus-wide. 58 of 65 parse, though parsing is not the same as running: only `Chapter_19_Evaluation_(Basic_Response_Evaluation)` runs offline. Notebooks stay SOURCE-CODE, never SOURCE. |
| X-16 | Chapters 01–04 are further verified than 05–21 ("05–21 source-only provisional") | UNSUPPORTED | Nothing in this repo treats 01–04 differently: not the skills, the manifest, `validation/audit/`, or the notebooks. |

### 7.2 Correction to X-14: the seven actual parse failures

Re-run on `8d15ae3`. The results match §4 and `validation/audit/notebook-inventory.json`.

| Notebook | Python error | Cause (read from the code) |
| --- | --- | --- |
| `Chapter_03_Parallelization_(Google_ADK).ipynb` | unexpected indent (line 5) | Leading indentation in the first code cell |
| `Chapter_14_Knowledge_Retrieval_(RAG_Google_Search).ipynb` | invalid syntax (line 1) | `import Google Search` / `tools=[Google Search]`, a product name typed as code |
| `Chapter_15_Inter_Agent_(Sync_Streaming_Requests).ipynb` | unexpected indent (line 25) | JSON protocol examples pasted into a code cell |
| `Chapter_17_Reasoning_(CoT_Prompt).ipynb` | unterminated string literal (line 1) | Prompt prose in a code cell |
| `Chapter_17_Reasoning_(Self_Correction).ipynb` | unterminated string literal (line 3) | Prompt prose in a code cell |
| `Chapter_18_Guardrails_(LLM_as_Guardrail).ipynb` | unterminated string literal (line 7) | Markdown/prompt prose in a code cell |
| `Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb` | expected `except` or `finally` (line 68) | Truncated `try:` block in an excerpt |

None is in Chapter 4. None is attributable to PDF extraction: these are the original authors' notebook files. All seven carry the WEAK flag and are never positive examples.

### 7.3 Claims about the book

All are checked against the book text. Pages are PDF chapter-start pages (§1). "VERIFIED" means the book says it. It does not mean the claim is true of agents in general.

| # | User claim | Status | Evidence |
| --- | --- | --- | --- |
| B-1 | Ch 6 Planning reasons from initial to goal state and distinguishes discovering *how* from a predetermined workflow | VERIFIED | p98. GT:L3813, L3821, L3839 ("does the 'how' need to be discovered"), L3860 |
| B-2 | Ch 11 opens on objectives, but its overview re-explains planning | VERIFIED | p181. GT:L7012–L7025 (trip analogy, initial/goal state, step sequence). Recorded as C-30. Authorial intent is UNCERTAIN. |
| B-3 | Ch 8 distinguishes short-lived context from persistent memory | VERIFIED | p130. GT:L5007–L5018 (short-term = context window); L5818–L5821 (short-term vs long-term, external stores) |
| B-4 | Ch 5: execution happens in an orchestration layer after the model proposes a structured call | VERIFIED | p77. GT:L3737–L3742 ("An orchestration layer executes this function call") |
| B-5 | Ch 16 distinguishes action sequencing from computational/temporal/financial resource decisions | VERIFIED | p244. GT:L9388–L9390 ("differs from simple planning, which primarily focuses on action sequencing") |
| B-6 | Ch 19 emphasizes trajectories, latency, resources, effectiveness and compliance, and distinguishes itself from Ch 11 | VERIFIED | p304. GT:L11900–L11903 ("While Chapter 11 outlines goal setting and monitoring… this chapter focuses on…"); trajectories GT:L12325–L12328 |
| B-7 | Ch 7 frames multi-agent as decomposition among specialized agents | VERIFIED | p111. GT:L4278 |
| B-8 | Ch 10 MCP is a standardized client/server interface for resources, prompts and tools | VERIFIED | p165. GT:L6354, L6960–L6963; MCP vs function-calling table GT:L6393 |
| B-9 | Ch 14 RAG supplies external/current knowledge | VERIFIED | p211. GT:L8161–L8176 |
| B-10 | Ch 15 A2A is an open protocol across frameworks | VERIFIED | p229. GT:L8807, L9277, L9286 |
| B-11 | Ch 17 uses more inference-time compute and multiple solution paths | VERIFIED | p260. GT:L10047, L10058 |
| B-12 | Ch 12 covers retries, fallback, graceful degradation, rollback, diagnosis and escalation | VERIFIED | p194. GT:L7574–L7578, L7613–L7617 |
| B-13 | Ch 13 is for oversight in complex, ambiguous or high-risk settings | VERIFIED | p202. GT:L7818–L7819 ("complexity, ambiguity, or significant risk") |
| B-14 | Ch 18 covers input validation, output filtering, behavioral constraints, tool restrictions and human oversight | VERIFIED (subset) | p284. GT:L11022–L11028 lists six stages. The user's list omits "External Moderation APIs". |
| B-15 | Ch 20 criteria: urgency, importance, dependencies, resources | VERIFIED | p323. GT:L12638, L12975 |
| B-16 | Ch 9 is about changing thinking/action/knowledge from experience | VERIFIED (paraphrase) | p152. GT:L5912–L5916, L6273–L6276 ("behavior or knowledge"). "Thinking" is the user's word. |
| B-17 | Ch 21 targets unfamiliar solution spaces | VERIFIED | p333. GT:L13044–L13047 ("unfamiliar territories", "unknown unknowns") |
| B-18 | Reflection "is source-supported as a behavior that can operate across another workflow" | PARTIAL | p63/p194. The book supports *combinable*: GT:L2884–L2886 ("can be integrated with other foundational patterns") and GT:L7564 (Ch 12 "may sometimes be used with reflection"). "Cross-cutting dimension" is DERIVED, both in the user's analysis and in DESIGN-ANALYSIS. |

### 7.4 Rule going forward

Rows X-1..X-13 stay EXTERNAL-UNVERIFIED until the user supplies the artifacts, as files committed to this repository or an inspectable link. Until then, no academy contract, mission, fixture or score may depend on them. RECONCILIATION §4.13 holds two of the terms (`unit_of_application`, `controlling_topology`) as EXPERIMENTAL candidates only.
