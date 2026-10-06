# Skill re-audit log (branch `cursor/agent-standup-path-eada`)

Scope: all 21 skills (`SKILL.md`, `references/patterns.md`,
`references/deep-dive.md`, `examples/minimal.py`) plus the appendix
references. Ground truth is `ground-truth/agentic_design_patterns.txt` (GT)
and `chapter_notebooks/*.ipynb`. Earlier audit claims (including
`validation/audit/`) were treated as leads, not proof. Each item below was
re-checked against GT lines or notebook cells.

## Method

- GT line numbers come from `split("\n")`. The text has form feeds, and
  `splitlines()` shifts every number (Chapter 1 shows as 716 rather than
  696). Every `GT:Lx` citation in the repo uses `\n` numbering, which matches
  `grep -n` and `sed -n`.
- Chapter slices (start lines): Ch1 696, Ch2 1204, Ch3 1797, Ch4 2412,
  Ch5 2907, Ch6 3808, Ch7 4274, Ch8 4996, Ch9 5911, Ch10 6341, Ch11 7003,
  Ch12 7539, Ch13 7808, Ch14 8157, Ch15 8793, Ch16 9386, Ch17 10038,
  Ch18 11017, Ch19 11897, Ch20 12618, Ch21 13042, appendices 13596–17659.
- `tools/provenance_scan.py` normalises whitespace and quote style, then
  looks up every code line of 14+ characters in the GT chapter slice, the
  chapter's notebooks, and the other chapters. It also lists called names
  that appear in no GT slice or notebook. It shows where code came from but
  cannot prove a block is verbatim, so every flagged block was read by hand.
- Two throwaway checks found the blocks the line scan missed (reflowed book
  code):
  - a 5-word shingle overlap;
  - identifier overlap between DERIVED-labelled blocks and the chapter text.
  The same checks catch book code mislabelled as ours.
- Labels: every deep-dive now has a legend. Every code block is preceded by
  `Provenance: SOURCE | SOURCE (abridged) | DERIVED`, and section headings
  carry `(SOURCE, GT:L…)` or `(DERIVED)`. `tools/validate.py` enforces the
  Provenance line.

## Findings and fixes

| # | Skill / file | Finding | Fix | Evidence |
|---|---|---|---|---|
| 1 | gate | Step-7 budget failed at 3006/3014 (> 3000) | Trimmed AGENTS.md (now 301 tokens) and two cards; gate unchanged at 3000 | `python3 tools/validate.py` worst pair 2991 |
| 2 | routing/deep-dive | OpenRouter attributed to Ch2 | Moved to `resource-aware-optimization` as Pattern C; routing points there | OpenRouter code is Ch16 GT:L9808–L9836; Ch2 has none |
| 3 | routing (notebook filing) | `Chapter_02_Routing_(OpenRouter)` holds Ch16 material; `(LangGraph)` notebook has no LangGraph code | Recorded in both deep-dives; notebooks untouched | Notebook cells vs GT Ch2/Ch16; LangGraph conditional edges are in Ch17 GT:L10817 |
| 4 | resource-aware-optimization | Invented per-model prices in the cost sketch; an "Observed" output that was never run | Prices removed (`PRICE_PER_1M[model]` placeholder, ILLUSTRATIVE); "Observed" replaced with a not-executed note (UNCERTAIN) | No prices in GT Ch16 |
| 5 | resource-aware-optimization | Critic prompt labelled SOURCE (abridged), but the wording is ours | Relabelled DERIVED paraphrase | `CRITIC_SYSTEM_PROMPT` GT:L9572–L9590 (shingle overlap 0.10) |
| 6 | exception-handling | Invented code (`retry_with_backoff` etc.) shown as the book example; tool and state names did not match the book | Verbatim book block added; tool names and `primary_location_failed` aligned; remaining code labelled ILLUSTRATIVE; gaps in the book listed | GT:L7666–L7714 = notebook cell 0; the book never defines the tools or sets the flag (GT:L7718–L7728) |
| 7 | human-in-the-loop/minimal.py | Escalation auto-approved | Rewritten: `pending_human` by default; `denied` on timeout, None or non-APPROVE; executes only on explicit APPROVE through an injectable `approver` | `__main__` asserts six outcomes |
| 8 | human-in-the-loop/deep-dive | Book `escalate_to_human` presented as a working gate | Marked as a stub (returns success, no human); `personalization_callback` defined but never attached | GT:L7988–L8053 |
| 9 | prompt-chaining/deep-dive | Book JSON stage and prose uncited | Cited (rule GT:L1146–L1149, JSON GT:L784–L795, context engineering GT:L1068–L1080); framework mapping DERIVED | — |
| 10 | prompt-chaining/patterns | `llm.with_structured_output` listed as a Key API; not in book or notebooks | Replaced with "validate JSON with a schema (not a book API)" | `grep` GT/NB: 0 hits |
| 11 | parallelization/deep-dive | Aggregator block labelled DERIVED but is book code | Relabelled SOURCE (abridged) | GT:L2213–L2231 |
| 12 | reflection/deep-dive | `LoopAgent` reflection code presented as book code | Marked DERIVED: the book mentions the idea but gives no code; Pattern B noted as notebook-only | GT:L2796–L2797 |
| 13 | tool-use/deep-dive | One docstring spliced from two book tools | Split into `search_information` and `get_stock_price` | GT:L3086–L3091, GT:L3227–L3230 |
| 14 | planning/deep-dive | Deep Research model id given as fact | Model id marked UNCERTAIN; block cited abridged | GT:L4098–L4175 |
| 15 | multi-agent/deep-dive | CrewAI block mislabelled; claim about AgentTool input unsupported | CrewAI → SOURCE (abridged) GT:L4519–L4570; AgentTool claim UNCERTAIN | GT:L4906–L4907 |
| 16 | memory-management/deep-dive | Session, long-term and procedural blocks uncited | Cited abridged (GT:L5144–L5182, L5436–L5486, L5676–L5703); the procedural prompt template is labelled a paraphrase | — |
| 17 | learning-adaptation/patterns | `OpenEvolve(program_path, evaluator_path, config)`: wrong keyword names | Now `initial_program_path=, evaluation_file=, config_path=` | GT:L6225–L6229 |
| 18 | mcp/deep-dive | FastMCP server shown with notebook-only API (`from fastmcp import tool`, `@tool()`, `/tools.json`) as the book version | Replaced with the book listing; notebook variant noted as UNCERTAIN | GT:L6790–L6829 |
| 19 | mcp/patterns | `StreamableHTTPServerParams` not in book or notebooks | Now `HttpServerParameters(url=...)` | GT:L6845–L6881 |
| 20 | mcp/minimal.py | `tools/list` / `tools/call` presented as from the book | Docstring says they come from the MCP spec (EXTERNAL-UNVERIFIED) | GT/NB: 0 hits |
| 21 | goal-setting/deep-dive | Book loop labelled DERIVED | Relabelled SOURCE (abridged); helpers, goals and LangChain model cited; ADK note corrected (no ADK code; goals via instructions) | GT:L7292–L7335, L7144–L7148, L7512 |
| 22 | rag/deep-dive | `VSearchAgent` placed inside a Ch14 SOURCE block | Comment now says Ch5 (GT:L3616); re-ranker and query rewrite marked not-in-Ch14 | GT Ch14: no `VSearchAgent`, no re-rank |
| 23 | rag/patterns | `RecursiveCharacterTextSplitter`, `WeaviateVectorStore` not in book or notebooks | Now `CharacterTextSplitter(500, 50)`, `Weaviate.from_documents` | GT:L8562, L8571 |
| 24 | a2a/SKILL, patterns | `message/send`, `to_a2a`, `RemoteA2aAgent`, `securitySchemes` not in book or notebooks | Now book names `sendTask`, `A2AStarletteApplication`, `DefaultRequestHandler`, `authentication.schemes`; newer spec names UNVERIFIED | GT:L8988–L9026, L9227–L9231 |
| 25 | a2a/deep-dive | Book uses `sendTask` in examples and `tasks/send` in takeaways; unflagged | Inconsistency noted; current spec EXTERNAL-UNVERIFIED | GT:L8988, L9326 |
| 26 | reasoning-techniques/deep-dive | CoT, Self-Correction and PALM agent blocks labelled DERIVED, but they are book text | Relabelled SOURCE (abridged); "PAL" → "PALMs" (book term) | GT:L10137–L10170, L10297–L10330, L10406, L10422–L10455 |
| 27 | reasoning-techniques/deep-dive | Book passes `code_executor=[BuiltInCodeExecutor]` (a class in a list) | Flagged UNCERTAIN; not "fixed" | GT:L10448 vs Ch5 `BuiltInCodeExecutor()` GT:L3467 |
| 28 | guardrails/deep-dive | Guardrail prompt and `validate_tool_params` labelled DERIVED, but they are book code | Relabelled SOURCE (abridged); regex/PII marked DERIVED; `tool_filter` cited to Ch10 | GT:L11590–L11640, L11672–L11760, L6848 |
| 29 | evaluation-monitoring/deep-dive | `LEGAL_SURVEY_RUBRIC` labelled DERIVED; `.test.json` / `.evalset.json` stated as fact | Rubric → SOURCE (abridged); file extensions marked UNCERTAIN | GT:L12099–L12157, L12355–L12369 |
| 30 | evaluation-monitoring/patterns | Same `.evalset.json` claim | Now names `adk web` / pytest `AgentEvaluator.evaluate` / `adk eval` | GT:L12489–L12502 |
| 31 | evaluation-monitoring | Book's exact-match example scores 0.0 on a paraphrase | Kept and stated (the book's own point) | GT Ch19 basic snippet |
| 32 | prioritization/SKILL, patterns | Tool names `assign_priority`, `list_tasks` invented | Now `assign_priority_to_task`, `list_all_tasks`; formula marked DERIVED | GT:L12767, L12809 |
| 33 | prioritization/deep-dive | Weakness not stated: the book example only tags P0–P2, never ranks or re-prioritises | Weakness note added | GT:L12726–L12906 |
| 34 | exploration-discovery/deep-dive | Review template broken by a nested fence; a Provenance line ended up inside the code block | Rebuilt with a `~~~` fence; SOURCE (abridged) | GT:L13303–L13362 |
| 35 | exploration-discovery/deep-dive | Role prompts and Professor `sys_prompt` labelled DERIVED, but they are book code | Relabelled SOURCE; the Sakana "AI Scientist" credit is cited to the notebook cell 0 comment (not in GT) | GT:L13384–L13388, L13460–L13490 |
| 36 | all deep-dives | No provenance legend; "(book)" headings uncited | Legend added; headings cited or marked DERIVED | `tools/validate.py` provenance check |

## Appendices

No skill cites appendix content. The appendix slice (GT:L13596–L17659) was
included in the "other chapter" scan. The only appendix hit was a generic
fragment in the RAO critic prompt (GT:L14927), not a misattribution. Seven
appendix notebooks are Google Drive placeholders (see
`chapter_notebooks/README.md`). Their content was not checked against Drive.

## Follow-up fixes (cursor/agent-standup-path-eada, after the review)

- prompt-chaining: the card listed error propagation and lost context as chaining
  risks. The book gives them as limits of a single prompt (GT:L736–L740). The
  card now cites the chain risk the book does name, an ambiguous handoff
  (GT:L771–L774).
- guardrails: the book's IDOR check (GT:L11607–L11611) fails open on a missing
  or empty id; the example now fails closed, and the deep-dive marks the defect.
- Ten framework-bound cards (exception-handling, guardrails, mcp,
  memory-management, multi-agent, parallelization, planning, prompt-chaining,
  rag, tool-use) now show framework-neutral pseudo-code. The framework forms
  were already in each `references/patterns.md` with "(book)" labels, so no
  detail moved. Card code stays DERIVED.

## Still unverified

- Notebook-only code that is not in GT. Examples: the MCP FastMCP variant, and
  reflection Pattern B. It is marked, but was not executed.
- No example that calls a real provider was run. Model ids from the book
  (e.g. `gemini-2.0-flash-exp`, `gemini-1.5-flash-latest`) may be retired.
  UNCERTAIN.
- The A2A and MCP method names in the current specs are EXTERNAL-UNVERIFIED.
- Profile specs in `models/` (context sizes, gates) do not come from the book.
  They are marked unverified there.
