# State of the repository: shinarugrok-a11y/Agentic-Design-Patterns

## Status update (maintained on `cursor/agent-standup-path-eada`)

This section is kept current. Everything under it, from "Read-only review" to the end, is the review as delivered (revision 2, 2026-10-06 00:11 UTC), except that two personal identifiers (an email address and a Colab user id) are replaced by placeholders. It was written against origin refs before any commit on this branch.

**Ordering deviation, stated plainly.** The owner asked for this review first, then the fixes. The fix work actually started earlier, in commits `0853b67` → `1a4d323`, before the review arrived. Some of those commits follow routes the review argues against:
- `STANDUP.md` as an entry point;
- "read the full `manifest.json`";
- trimming `AGENTS.md` to pass the gate.

Later commits on this branch correct those routes. They are listed per gap below.

Status as of the latest commit on this branch; a commit named only by subject is the one that introduced the change. "Branch" means fixed here, not on `main`; `main` changes only when the owner lands a PR.

| Gap | Status | By / note |
| --- | --- | --- |
| G1 README sends bots the wrong way | CLOSED (branch) | `0853b67` folded in the accurate README (no `book/` path, 458 pages). "Route correction" commit adds a first-screen "AI agents: start at AGENTS.md" line with the raw URL, which the validator checks |
| G2 main fails its validator | CLOSED (branch) | `0853b67` brought the keyword fix; `e5cafb9` brought the budget fix. `main` itself is unchanged until a PR lands |
| G3 runtime discovery | CLOSED (required scope) | "Route correction": `AGENTS.md` is the single entry (Codex and Claude Code read it natively; no `CLAUDE.md`, validator-enforced). `GEMINI.md` is a one-line pointer. `.agents/skills/<id>` symlinks for Codex skill scanning are generated and checked by the validator. Still OPEN: a `.claude/skills` mirror (Claude Code symlink handling not verified). UNVERIFIED: whether Cursor or Grok load `AGENTS.md` |
| G4 runtime / "who am I" step | CLOSED (branch) | `ba2b11d` added the runtime profiles. "Route correction" moves the runtime step and profile table into `AGENTS.md` boot steps 1–2, each with a Done: check, and deletes `STANDUP.md` |
| G5 provenance markers | CLOSED | `98674bc` added Provenance labels and GT:L citations in every deep-dive (`validation/skill-reaudit/LOG.md`); `8a14d56` makes the validator enforce a Provenance line per deep-dive code block |
| G6 slim index / gate measures wrong path | CLOSED (branch) | "Route correction" generates `skills/INDEX.md` (816 tokens) from `manifest.json`, and the validator checks it matches. The Step-7 gate now measures `AGENTS.md` + `skills/INDEX.md`: worst pair 2498/3000 (headroom 502; was 2996). Stand-up worst case is 3000/4000. The gate stays 3000. `deep-dive.md` remains on-demand and outside the gate |
| G7 source slices do not exist | CLOSED (branch) | "Route correction" generates `ground-truth/INDEX.md`: line ranges for chapters 1–21, appendices A–G, Glossary and Index of Terms. The validator checks it matches the text, and `AGENTS.md` step 5 points to it. Ranges spot-checked against the text (for example Ch 1 starts at GT:L696, Appendix A at 13596) |
| G8 appendices have no skills | OPEN | — |
| G9 duplicate notebook companions | OWNER-DECISION | — |
| G10 open security / review findings | OPEN | `eval` example, IDOR, validator path traversal, `ground-truth/README` output path |
| G11 behavioural stand-up test | OPEN | `8a14d56` adds a deterministic routing-table test only |
| G12 LICENSE | OWNER-DECISION | — |
| G13 validator honesty + fixtures | OPEN | — |
| G14 one gate policy | OPEN | — |
| G15 examples execute / fail open | OPEN (partial) | (a) HITL `send_email` is held as `pending_human` (`9329676`, re-checked); (b) the MCP `assert` was replaced by `PermissionError` (`1a4d323`, re-checked under `python -O`), but `tool_filter=[]` still exposes all tools; (c) the IDOR guard still fails open |
| G16 personal identifiers | OWNER-DECISION | Colab ids are in frozen notebooks. PR #4's README email is also on this branch's README (line 92) via the fold-in |

### Owner decisions (recorded, not acted on)

- **Landing PR #4.** Recommend removing the upstream author's personal email from its README (line ~88 on `ed7e205`) before landing. Do not merge PR #4 as is. This branch does not merge or modify PR #4.
- **LICENSE (G12).** No license file exists. Notebook headers cite an MIT file that is absent.
- **Colab `userId` / `displayName` in 7 notebooks (G16).** Notebooks are frozen by the standing rules. Stripping them needs an explicit exception, and they would remain in history.
- **The 56 duplicate `chapter_notebooks/Chapter_*.SKILL.md` companions (G9).** Keep (validator-synced), or delete.

---

Read-only review, written 2026-10-05 (UTC) from a fresh clone at `/tmp/review`. I made no commits, pushes, or PRs. Every number below comes from a command I ran in that clone unless a row says otherwise.

Labels used throughout:

- **SOURCE** means the book text (`ground-truth/agentic_design_patterns.txt`, cited as `GT:L<line>`) or a notebook in `chapter_notebooks/` says it. I re-located each one myself.
- **DERIVED** means our own interpretation, condensation, or new code. It may be good engineering, but the book does not say it.
- **UNVERIFIED** means a claim nobody in this repository has checked, or one that depends on something outside the repository (vendor facts, artifacts that were never supplied).

Commit messages, PR bodies, audit documents, and the saved plan are treated as claims, not as evidence.

**Revision 2 (2026-10-06 00:11 UTC).** Added §9 (external input from the owner's Pepper bot) and §10 (runtime and Codex facts checked against vendor sources). Merged the relevant items into §7 and §8. Corrected §4.6 and gap G3: Claude Code now reads `AGENTS.md` natively, and adding a `CLAUDE.md` that does not import it would *stop* `AGENTS.md` loading.

---

## 1. Snapshot

| Item | Value |
| --- | --- |
| Review date | 2026-10-05 |
| Clone | `gh repo clone shinarugrok-a11y/Agentic-Design-Patterns` with all `refs/heads/*` fetched |
| Newest commit (all refs) | `a62aaed40b35217485fa5797cd51d4902fbafa46`, 2026-09-27 05:11 UTC, Cursor Agent, "Add revision note to DESIGN-ANALYSIS linking the reconciliation" (branch `cursor/agent-academy-design-eada`) |
| `main` | `ed9027ebba8018fbf18fad1493f32288d1eeab35`, 2026-09-21 (merge of PR #3) |
| `upstream/main` (evoiz) | `e11e6fbd9d3d1d747edbf1f151d32f58480b55fc`, 2026-07-24. This is an ancestor of `main` and predates all skill-library work. |
| Not on the remote | `cursor/agent-standup-path-eada`, which another agent is working on in `/workspace`. `git ls-remote` shows no such branch. I did not inspect it. |
| Issues | Disabled on this repository (`gh issue list` returns "repository has disabled issues"). |
| Tooling used | Python 3, `tiktoken` 0.14.0, Poppler `pdftotext`/`pdfinfo` 24.02.0 (installed for this review) |

Refs examined:

| Ref | SHA | Last commit date |
| --- | --- | --- |
| origin/main | `ed9027e` | 2026-09-21 |
| origin/cursor/agent-academy-design-eada | `a62aaed` | 2026-09-27 |
| origin/cursor/repo-evidence-audit-1033 | `ed7e205` | 2026-09-23 |
| origin/cursor/add-pdftotext-ground-truth-84c8 | `92334d7` | 2026-09-21 |
| origin/cursor/agent-skill-library-eada | `10ad49a` | 2026-09-20 07:23 |
| origin/cursor/agent-skill-library-b24b | `37c98da` | 2026-09-20 06:38 |
| origin/cursor/skill-library-6dc8 | `21ec79f` | 2026-09-20 06:22 |
| origin/cursor/agentic-skill-library-3108 | `1a5b04c` | 2026-09-20 06:17 |
| origin/cursor/skill-library-7680 | `573b7d1` | 2026-09-20 06:15 |

Authors in the whole history (`git log --all`): Cursor Agent (31 commits), shinarugrok-a11y (4: the two PR merges plus `a486c70` and `ed9027e`), Elias Al-bittar / Elias Albittar (6, the upstream book materials), 1040942669 (1, upstream README typo fix).

---

## 2. Branch and PR ledger

### 2.1 PRs on shinarugrok-a11y/Agentic-Design-Patterns

The default `gh` remote resolves to the evoiz upstream repository, which has its own unrelated PRs #1–#3. Every PR command has to pass `-R shinarugrok-a11y/Agentic-Design-Patterns`. The PRs below are the owner's.

| PR | Head branch | State | Created / merged | What it contributed | Discussion and review |
| --- | --- | --- | --- | --- | --- |
| [#1](https://github.com/shinarugrok-a11y/Agentic-Design-Patterns/pull/1) | `cursor/agent-skill-library-b24b` | MERGED (squash `fb89422`, tree identical to `37c98da`) | 2026-09-20 06:44 / 06:47 | First library: long ids (`multi-agent-collaboration`, `knowledge-retrieval-rag`, `guardrails-safety`, ...), 21 `chapter_notebooks/Chapter_NN_<Title>.SKILL.md`, ~1000-token `patterns.md`, `tools/validate_skills.py`. Budget handled with a `jq` role slice of the manifest instead of reading the whole file. | Codex review hit its usage limit. No human review. Merged 3 minutes after it was opened. |
| [#2](https://github.com/shinarugrok-a11y/Agentic-Design-Patterns/pull/2) | `cursor/agent-skill-library-eada` | MERGED (squash `fede537`, tree identical to `10ad49a`) | 2026-09-20 07:18 / 08:03 | Replaced PR #1 almost entirely: short ids, 22-line `AGENTS.md`, two-tier references (`patterns.md` ~250 tokens plus `deep-dive.md` built from PR #1's content), 56 per-notebook `.SKILL.md` copies, `tools/validate.py`. Deleted PR #1's folders, companions, and validator. | Three MEDIUM findings from Cursor Security Review: (1) `skills/reasoning-techniques/examples/minimal.py:8` uses `eval(expr, {"__builtins__": {}})`, which is not a sandbox; (2) the IDOR guard at `skills/guardrails/examples/minimal.py:28` lets a call through when `user_id` is missing; (3) path traversal through manifest ids in `tools/validate.py` `sync()` (line 77ff.). **None of the three has been fixed on any branch** (I checked `main`). No reply on the PR. |
| [#3](https://github.com/shinarugrok-a11y/Agentic-Design-Patterns/pull/3) | `cursor/add-pdftotext-ground-truth-84c8` | MERGED (`ed9027e`) | 2026-09-21 20:30 / 20:36 | `ground-truth/agentic_design_patterns.txt` and `ground-truth/README.md` | Codex P2: the documented command writes `./agentic_design_patterns.txt` instead of `ground-truth/...`. **Not fixed.** `ground-truth/README.md:5` still has the bare output path. |
| [#4](https://github.com/shinarugrok-a11y/Agentic-Design-Patterns/pull/4) | `cursor/repo-evidence-audit-1033` | **OPEN** | 2026-09-23 01:01 | `validation/audit/*` (13 files), an accurate root README rewrite, a `chapter_notebooks/README.md` rewrite, and a validator update (keyword fixed to "Do not load the entire PDF"; README edits allowed) | PR body: "Do not merge to `main` until a human reviews the audit." No comments. |
| none | `cursor/agent-academy-design-eada` | Branch only, **no PR exists** | 2026-09-27 | `docs/academy/*` (6 design documents for an "Agent Academy" teaching product), plus merges of `main` and PR #4 | The saved plan says "PR registered as draft (user must open it)". The PR list shows no such PR. |

### 2.2 Branch ledger, including the four old competing skill-library branches

All five skill-library branches were created between 06:11 and 06:57 UTC on 2026-09-20 from the same base (`e11e6fb`). That looks like parallel best-of-N attempts at one prompt. Only `eada` survives in content.

| Branch | Head | Ahead / behind main | Merged? | Ids and naming | Validator | Superseded by |
| --- | --- | --- | --- | --- | --- | --- |
| `cursor/skill-library-7680` | `573b7d1` | 1 / 5 | No, never PR'd | Same ids as main except `resource-optimization`. 56 `<nb>.SKILL.md` | None in tree. The commit message claims "executor sim 2743, worst 2852" with no validator present, so that claim is **UNVERIFIED**. | PR #2 |
| `cursor/agentic-skill-library-3108` | `1a5b04c` | 2 / 5 | No, never PR'd | `guardrails-safety`, `learning-and-adaptation`. 56 `<nb>.SKILL.md` | None | PR #2 |
| `cursor/skill-library-6dc8` | `21ec79f` | 1 / 5 | No, never PR'd | `inter-agent-a2a`, `knowledge-retrieval`, `resource-optimization`, `guardrails-safety`. 56 `<nb>.ipynb.SKILL.md` | None | PR #2 |
| `cursor/agent-skill-library-b24b` | `37c98da` | 10 / 5 | Yes, as PR #1, then removed by PR #2 | Long ids. 21 `Chapter_NN_<Title>.SKILL.md` | `tools/validate_skills.py`. I re-ran it: **PASS**, worst role 2743 under its own role-slice model | PR #2. Its references became `deep-dive.md`. |
| `cursor/agent-skill-library-eada` | `10ad49a` | 8 / 4 | Yes, as PR #2 | Current ids. 56 `<nb>.SKILL.md` | `tools/validate.py`: now **27 pass / 1 fail** (see §6) | Live on main |
| `cursor/add-pdftotext-ground-truth-84c8` | `92334d7` | 0 / 1 | Yes, as PR #3 | n/a | n/a | Live on main |
| `cursor/repo-evidence-audit-1033` | `ed7e205` | 1 / 0 | **No**. PR #4 is open. Merged into the academy branch only. | n/a | 26 / 2 | Not superseded |
| `cursor/agent-academy-design-eada` | `a62aaed` | 16 / 0 | **No**, and no PR | n/a | 26 / 2 (same as the audit branch) | Not superseded. Separate product. |

Direct commit on main: `a486c70` (owner, 2026-09-21) rewrote the `AGENTS.md` PDF rule. This one-line change pushed `AGENTS.md` from 279 to 311 tokens and broke the validator on `main`. Details in §5 and §6.

---

## 3. What exists now, by area

### 3.1 `main` (`ed9027e`)

| Area | Files | Notes |
| --- | --- | --- |
| Book | `Agentic_Design_Patterns_Complete.pdf` (unchanged since `7ddebbc`) | `pdfinfo`: 458 pages, producer PyPDF2, not encrypted (re-checked) |
| Ground truth | `ground-truth/agentic_design_patterns.txt` (17,658 lines by `wc -l`), `ground-truth/README.md` | A fresh `pdftotext -layout` differs on 12 lines of the fresh output, all emoji line-wrap around GT:L3078, 7168, 7304, 7320. The audit said 17 of 17,659. The two counts measure differently, but the conclusion holds: the extract is faithful. |
| Agent entry | `AGENTS.md` (22 lines, 311 cl100k tokens) | Role table plus four rules. It does not say where to start if you don't know your role. |
| Index | `manifest.json` (version "1.0", 21 records, 8,387 bytes, 1,848 tokens) | Every record repeats SKILL.md frontmatter fields. The validator checks that the two agree. |
| Skills | `skills/<id>/{SKILL.md, references/patterns.md, references/deep-dive.md, examples/minimal.py}` for 21 ids | SKILL.md bodies 188–234 tokens. `patterns.md` 209–282. `deep-dive.md` about 1,300–2,000 tokens each, 2,912 lines in total. |
| Models | `models/fable-5-1.md`, `models/grok-4-6.md`, `models/muse.md` | These describe a three-model team topology (planner, executor, personal agent behind a "Sentinel gate"). Context and cost figures are **UNVERIFIED** (audit 10-unresolved #8). There are no profiles for Claude Code, Codex, Cursor, Gemini CLI, or a generic chat assistant. |
| Notebooks | 65 `.ipynb` (56 chapter, 9 appendix) plus 56 `.SKILL.md` copies | The copies are byte-identical duplicates of 21 cards, so some cards appear up to 4 times (`Chapter_02_*` has 3, for example). |
| Tooling | `tools/validate.py` | Fails on main (§6) |
| README | Upstream marketing README (253 lines) | Points to a nonexistent `book/` folder, says "424 pages", and gives an evoiz clone URL. **It never mentions `AGENTS.md`, `skills/`, or `manifest.json`.** |
| Absent | No `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/`, `.claude/skills/`, `.github/`, `llms.txt`, `LICENSE`, `requirements.txt`, `.gitignore` on **any** branch | Checked with `git ls-tree` on all 9 refs |

### 3.2 `cursor/repo-evidence-audit-1033` (adds to main)

- `validation/audit/01..10-*.md`, `README.md`, `evidence-claims.json`, `notebook-inventory.json` (1,033 lines)
- Accurate root `README.md`: 458 pages, root PDF path, status table, "verified means..." definition. It mentions `AGENTS.md` in the tree diagram only, not as a "bots start here" line.
- `chapter_notebooks/README.md`: counts, parse failures, placeholder appendices, no `requirements.txt`
- `tools/validate.py`: keyword now "Do not load the entire PDF". README edits allowed. A docstring says not to raise `BUDGET`.

### 3.3 `cursor/agent-academy-design-eada` (adds to the audit branch)

- `docs/academy/DESIGN-ANALYSIS.md` (1,005 lines), `PROVENANCE-AUDIT.md` (283), `RECONCILIATION.md` (276), `SCENARIO-CONTRACT.md` (312), `EVALUATION-CONTRACT.md` (226), `ART-DIRECTION.md` (185)
- This is a design for a teaching game or simulation ("Agent Academy", missions, Mission Control UI, 3D art direction). It is **not** part of the stand-up path, and it contains no code.

### 3.4 Old branches

Their content is fully superseded. PR #1's reference material survives as `deep-dive.md`. No unique content on 3108, 6dc8, or 7680 needs keeping, other than 2aa6779's "chapter notebook pattern reference" on 3108, which `deep-dive.md` covers.

---

## 4. Verified vs unverified

### 4.1 Re-checked myself, with results

| Claim | Status | My evidence |
| --- | --- | --- |
| PDF is 458 pages, not 424 | **SOURCE-verified** | `pdfinfo`: `Pages: 458` |
| Ground-truth text is a faithful extract | **Verified** | Fresh pdftotext vs the committed file: only emoji-wrap lines differ |
| Chapter locations | **Verified** | Ch1 GT:L696, Ch2 L1204, Ch12 L7539, Ch13 L7808, Ch14 L8157, Ch16 L9386, Ch17 L10038, Ch18 L11017, Ch21 L13042. Appendix A L13596, E L15451, G L16292. |
| 7 of 65 notebooks do not parse | **Verified** | `ast.parse`: Ch03 ADK (L5 indent), Ch14 RAG Google Search, Ch15 Sync/Streaming, Ch17 CoT, Ch17 Self-Correction, Ch18 LLM-as-Guardrail, Ch21 Agent Laboratory. "Reflection notebooks corrupted" is false; all three Ch04 notebooks parse. |
| All 21 `examples/minimal.py` exit 0 offline | **Verified** | Validator check passes on all four branches I ran |
| No secrets in tree or history | **Verified (shape scan only)** | `rg` for `sk-…`, `AIza…`, `AKIA…`, `ghp_…`, `xox[bp]-`, private-key headers: 0 hits in tree, 0 in `git log --all -p`. Colab `userId` `<colab-user-id>` and `displayName` appear in 7 notebooks, which matches audit finding S1. |
| 7 of the academy's GT:L citations | 6 exact, 1 off by 2 | L2885, L7564, L7945, L8128, L7687, L3737 match. L9806 points 2 lines before the OpenRouter heading (L9808). |

### 4.2 The three known weak items, re-checked

**(a) Routing deep-dive misattributes OpenRouter.** Confirmed. The deep-dive itself is DERIVED and wrong on this point.

- The book's only OpenRouter material is GT:L9808–L9880, "Hands-On Code Example (OpenRouter)". That falls inside Chapter 16 Resource-Aware Optimization (L9386–L10038). The string "openrouter" never appears inside Chapter 2 (L1204–L1797).
- The notebook is misfiled upstream as `chapter_notebooks/Chapter_02_Routing_(Openrouter).ipynb`. It has one cell: a single `requests.post` to a fixed `"model": "openai/gpt-4o"`, so it does no routing.
- Our files repeat the misfiling as fact:
  - `skills/routing/references/deep-dive.md:4` lists it as a Chapter 2 source.
  - Line 108 says "(the chapter's OpenRouter example)".
  - Line 132 files it under "CrewAI / other".
  - `skills/routing/references/patterns.md:20` says "route by cost/quality tier".
- `skills/resource-aware-optimization/references/deep-dive.md:133` correctly mentions `openrouter/auto` (which is SOURCE, GT:L9857), but the Ch16 skill does not claim the example.
- Fix: move the OpenRouter example to `resource-aware-optimization` with a GT:L9808 citation, and add a note in routing that the notebook filename is misleading.

**(b) Exception-handling deep-dive has invented code.** Confirmed, and it is unlabeled.

- `skills/exception-handling/references/deep-dive.md:25–52` (the ADK `SequentialAgent` with primary, fallback, and response agents) is **SOURCE**. It matches the notebook `Chapter_12_Exception_Handling_(Fallback).ipynb` and GT:L7666–L7714.
- The following are **DERIVED/invented**, all under a header that says only "Source: Chapter 12 + notebook":
  - The inline comment at line 34, "tool sets state["primary_location_failed"] on error".
  - "Why it works" at line 55.
  - **The whole `get_precise_location_info` implementation at lines 61–70**, which uses `geocode`, `ServiceUnavailable`, and `ToolContext`.
  - "Retry policy sketch" at lines 74–84, which raises a nonexistent `EscalateToHuman`.
  - "Degradation ladder" at line 86.
- Neither the book nor the notebook ever defines `get_precise_location_info` or `get_general_area_info`. The state key appears only inside the agent instruction (GT:L7687), and the book's description (GT:L7718–L7728) never says the tool sets it. The book example cannot run as written. Our deep-dive quietly fills that gap and presents the result as the explanation.

**(c) Human-in-the-loop "successful escalation with no human".** Partly confirmed. The issue is in a different place than the brief says.

- The prior finding (DESIGN-ANALYSIS F-16 and C-14) is about the **Ch13 notebook**. There, `escalate_to_human` returns `{"status": "success", ...}` and no human is involved. That is SOURCE (GT:L7997–L8000).
- `skills/human-in-the-loop/references/deep-dive.md:34–36` reproduces the stub verbatim, which is correct as a quote. Line 53 then adds a DERIVED overclaim: "the handoff is an auditable tool call". Nothing in the stub is auditable.
- `skills/human-in-the-loop/examples/minimal.py` is DERIVED and its logic is sound: a timeout is never treated as approval, and running it prints "no-op: awaiting human decision (reply='TIMEOUT')". However:
  - Line 50 passes a hard-coded `scripted_reply="APPROVE"`, and the output then reads `executed refund on order-42 (human approved)` when no human approved anything.
  - Line 44 prints "case logged" when nothing is logged.
- Fix: label the stub WEAK in the deep-dive, remove the "auditable" claim, and change the example's output to say "(scripted approval)" and actually append to a log list.

### 4.3 Spot-checks of other skills against the book

| Skill | Claim in SKILL.md | Finding | Label |
| --- | --- | --- | --- |
| prompt-chaining | Failure modes "error propagates downstream" and "early context lost" | The book lists *error propagation* and *contextual drift* as problems of a **monolithic single prompt**, which chaining is meant to solve (GT:L738–L742). The card presents them as failure modes **of chaining**. That is a reasonable engineering view, but it inverts the book's framing. | DERIVED, uncited |
| reflection | "Same model as producer and critic: shared blind spots" | The book supports separating producer and critic to avoid the "cognitive bias" of self-review (GT:L2469–L2471). The "same model" wording is our extension. | SOURCE-adjacent, partly DERIVED |
| memory-management | "State mutated directly instead of via events" | GT:L5231–L5235 says state should be updated through `session_service.append_event()`, and GT:L5411 says direct modification "is strongly discouraged as it bypasses the standard event processing". | SOURCE |
| mcp | "Relative server path fails outside notebooks"; "No tool_filter: dangerous tools exposed" | GT:L6635, L6645, and L6674 ("MUST be an absolute path"). `tool_filter` restriction at GT:L6848. | SOURCE |
| guardrails | IDOR guard pattern (deep-dive :79–81; example :28) | The book's own `validate_tool_params` has the same short-circuit flaw (GT:L11607–L11611, `if actual_user_id_in_args and ...`). The PR #2 security finding is therefore a **book defect copied faithfully**, still unlabeled, and our `minimal.py` makes it runnable. "Injection bypasses a single layer" is DERIVED; the book only links to prompt injection at GT:L11891. | SOURCE flaw plus DERIVED |
| prioritization | "Everything is P0" | The book uses `P0, P1, P2` labels in code (GT:L12730). The failure mode itself is DERIVED. | DERIVED, grounded |
| rag | "Bad chunking splits facts"; "Stale index" | Chunking at GT:L8250–L8263. Up-to-date and periodic reconciliation at GT:L8179 and L8309. | SOURCE |

### 4.4 Provenance across all 21 deep-dives (mechanical)

I took every line of 20 or more characters inside a code block in `patterns.md` and `deep-dive.md`, ignoring comment lines, and searched for it in the book and the notebooks after removing all whitespace.

- 1,045 lines in total. **487 are verbatim in the book, 21 are only in notebooks, and 537 (51%) match neither.**
- Per-skill traceability of `deep-dive.md` ranges from 22% (guardrails) to 75% (mcp). The lowest after guardrails are exploration-discovery (27%), evaluation-monitoring (28%), reasoning-techniques (31%), planning (35%), and learning-adaptation (35%).
- Nearly every non-matching line in `patterns.md` is a condensed paraphrase.
- Caveat: a non-match can be reformatting (joined arguments) rather than invention. Treat this as a triage list, not a verdict.
- Only 2 of 21 deep-dives contain any word like "derived", "invented", "illustrative", or "sketch". The other 17 or more have nothing marking new material. Each file starts with "Source: Chapter N + <notebook>", which implies everything below it is sourced.
- Full table: `/tmp/state/provenance.txt` (scratch, not committed).

### 4.5 DERIVED by construction

These were written by agents, not taken from the book. None of them carries per-section provenance today.

- Every `SKILL.md` "When to use / NOT / Inputs / Outputs / Failure modes" block
- Every `examples/minimal.py` (they are offline stubs with a scripted `think()` or `llm()`)
- `manifest.json` `role` assignments and `chains_with`
- The five-role scheme (planner, executor, critic, memory, safety)
- All `models/*.md` content
- All of `docs/academy/*`

### 4.6 UNVERIFIED or external

| Item | Status |
| --- | --- |
| "Fable 5.1", "Grok 4.6", "Muse": context windows, costs, "Sentinel gate" | UNVERIFIED. Not checked against any vendor. The book mentions "Grok 3" only, at GT:L15885. |
| The 3000-token BUDGET and "Step 7 gate" | Rationale UNVERIFIED. "Step 7" refers to a prompt that is not in the repository. No file explains why 3000 or why this particular walk. |
| APD-01..21, MANIFEST `pattern_index`, schema 2.1/2.2, conversion log, D4 correction, routing fixtures, ROUTING-INDEX, EVALUATION-LAYER-MODEL, `controlling_topology`, `unit_of_application`, CompSD, Beowulf | **Nonexistent.** I found none of them in any tree or in history (`git log --all -p` search for `APD-`, `pattern_index`, `ROUTING-INDEX`, `controlling_topology` turned up mentions only inside `docs/academy` and `validation/audit`, which say they are absent). `manifest.json` is version "1.0" with keys `version`, `source`, `skills`. |
| The 7680 commit's validation numbers | UNVERIFIED. No validator exists on that branch. |
| PR #2 body "28/28 pass" | Not reproducible now: 27/1 at the same SHA, because the "unmodified vs origin/main" check compares against a ref that has since moved (§6). It was plausibly true at the time. |
| Notebook code fidelity to the book's code listings | Not diffed one-to-one (audit 10-unresolved #2). Not done here either, beyond the Ch02, Ch12, and Ch13 spot-checks. |
| Third-party framework snippets (ADK, LangChain, CrewAI, FastMCP...) actually running | UNVERIFIED. Never executed by anyone. |
| Which files each runtime auto-loads | **Superseded by §10.** Codex, Claude Code, and Gemini CLI were checked against vendor documentation on 2026-10-06. Cursor and Grok are still UNVERIFIED. The book does not mention any of these files; Appendix E (GT:L15451ff.) discusses Claude CLI, Gemini CLI, and Aider at a high level only. |

---

## 5. Overlaps and conflicts

1. **The `AGENTS.md` PDF rule has three versions, and main is inconsistent with itself.**
   - PR #2 wrote "Do not read the PDF. It is for humans."
   - Owner commit `a486c70` on main replaced it with "Do not load the entire PDF during normal execution... consult canonical PDF-derived source slices..." (`AGENTS.md:19`).
   - `tools/validate.py:175` on main still checks for "Do not read the PDF", so main fails its own check.
   - The audit branch updated only the validator keyword.
   - The rule points to **"canonical PDF-derived source slices", which do not exist.** There is only the whole 17,658-line text file, with no chapter index or line-range map.
2. **The saved plan misattributes the token failure.** `/cursor/stores/self/agent-academy-next-steps.md` says the failure was "introduced by the audit-branch AGENTS.md rule wording". It was introduced on `main` by `a486c70` (279 to 311 tokens). The audit branch changed only the validator. This matters because "fix it on the audit branch" is the wrong mental model: main is broken today.
3. **Id schemes.** Five branches use four different schemes (§2.2). Main has one. Nothing on main references the old ids, so the risk is only stale branches.
4. **Companion naming.** There are three conventions across branches (`Chapter_NN_<Title>.SKILL.md` x21, `<nb>.SKILL.md` x56, `<nb>.ipynb.SKILL.md` x56). Main keeps 56 byte copies, which duplicates every card into the notebook directory. Any agent that greps or indexes the repo sees each pattern 2–5 times.
5. **Validators.** `validate_skills.py` (PR #1) was deleted by PR #2. Their budgeting models differ:
   - PR #1: role slice of the manifest plus richer ~1000-token references. Passes at 2743.
   - PR #2: read the whole manifest at 1848 tokens plus thin ~250-token references. Fails at 3014 on main.
   - PR #2's design spends 62% of the cold-start budget on an index that repeats the SKILL.md frontmatter.
6. **Manifest and SKILL.md duplication.** `name`, `role`, `chapter`, `chains_with`, `token_cost_estimate`, and when/when-not exist in both places and are kept in sync by validator and `--sync`. The owner's step (b) would add a "when to use which pattern" routing table as a third copy unless it is generated.
7. **The "originals untouched" check fights the audit.** Main's validator forbids README edits relative to `origin/main`. PR #4 rewrites both READMEs and relaxes the check. Those two must land together.
8. **The academy plan and the stand-up goal pull in different directions.** The saved plan's steps 5–7 (contracts, Mission 1 paper prototype, 3D art spike) are about a teaching product. The owner's current goal is a bot stand-up path. `docs/academy` should not sit in the bot's load path. If it merges, it needs to stay fenced under `docs/` and unmentioned in `AGENTS.md`.
9. **Brief vs evidence on HITL.** The task brief says "human-in-the-loop `minimal.py` reports successful escalation with no human". The audit's finding was about the notebook stub, reproduced in the deep-dive. Both have real issues, but they are different ones (§4.2c).
10. **Open review findings conflict with "ready to point a bot at".** The PR #2 security findings (`eval` sandbox, IDOR, validator path traversal) and the PR #3 Codex finding (wrong output path) have had no response and no fix. The IDOR is a book defect that our library promotes to a runnable example with no WEAK label.

---

## 6. Validator results per branch (`python3 tools/validate.py`, tiktoken 0.14.0)

| Branch @ SHA | Result | Failures |
| --- | --- | --- |
| main @ `ed9027e` | **25 pass / 3 fail**, exit 1 | `AGENTS.md contains 'Do not read the PDF'`; executor walk-through 311+1848+284+281+282 = **3006**; worst pair **3014** (executor, tool-use + multi-agent, ref tool-use). 17 of 136 combinations are over budget (119 under). |
| cursor/repo-evidence-audit-1033 @ `ed7e205` | 26 / 2, exit 1 | 3006 and 3014 |
| cursor/agent-academy-design-eada @ `a62aaed` | 26 / 2, exit 1 | 3006 and 3014 |
| cursor/agent-skill-library-eada @ `10ad49a` | 27 / 1, exit 1 | "PDF, notebooks and READMEs unmodified vs origin/main": `D ground-truth/README.md`. This is an artifact of the moving `origin/main`. The simulation passes at 2974 / 2982 with the old 279-token `AGENTS.md`. |
| cursor/agent-skill-library-b24b @ `37c98da` | `tools/validate_skills.py`: PASS | Role-slice model, worst 2743 |
| 3108, 6dc8, 7680 | No validator in tree | n/a |

Design observations about the validator itself:

- **The "unmodified vs origin/main" check is unreliable.** It diffs against whatever `origin/main` points to locally. On `main` it compares main to itself and always passes. On an old branch it fails because main moved. In a fork or a fresh clone it measures something else. Pinning SHA-256 hashes for the PDF and the 65 notebooks would make it deterministic.
- **The "simulation" only sums token counts.** No agent behavior is simulated. It also never counts `deep-dive.md`, which is where the real code lives and which the model profiles tell executors to open (`models/grok-4-6.md`).
- Running the validator executes every `examples/*.py` through `subprocess`. Combined with unvalidated manifest ids in `sync()`, this is the PR #2 path-traversal finding (low risk in practice, unfixed).

**Revision 2: how `tools/validate.py` behaves when it cannot know the answer.** I tested this on main's validator, using copies of the tree with no `.git` directory. Several cases treat "unknown" as "passed":

| Situation | What happens | Unknown treated as passed? |
| --- | --- | --- |
| No git metadata (for example a `git archive` or zip download) | `git diff` returns empty output, and the validator prints **`PASS  PDF, notebooks and READMEs unmodified vs origin/main`** | **Yes.** It certifies files it never compared. |
| No `origin/main` ref (fork, or `--single-branch` clone) | Same code path: empty diff, PASS | **Yes** (same mechanism) |
| One `examples/minimal.py` deleted | The structure check FAILs, but **`PASS  all examples/minimal.py run offline with exit 0`** still prints, because the loop skips missing files (`continue` at `tools/validate.py:154–155`) | **Yes**, for that check |
| One `SKILL.md` deleted | Uncaught `FileNotFoundError` traceback at `read()` (line 43). Exit 1, but no per-check report. | No, it blocks. But there is no evidence trail. |
| `tiktoken` not installed | `ModuleNotFoundError` at import (line 23). Exit 1, no checks run. | No, but there is no readable "blocked: dependency missing" message, and it is not offline-friendly. |
| An example hangs past 60 s | `subprocess.TimeoutExpired` is not caught, so the validator crashes | No, but it gives no report |
| "Offline" | Nothing enforces it. Examples could open sockets, and the check would still say "offline". | Claimed, not checked |
| Expected-FAIL fixtures | **None exist.** No test shows the validator actually fails on a known-bad pack. | n/a |
| Idempotent | Check mode makes no writes. `--sync` rewrites `SKILL.md`, `manifest.json`, and 56 companions; I did not test whether running it twice is stable. | Unknown |

---

## 7. Gap list for "point a bot at the URL and it stands up"

Ordered by impact on that goal.

**Revised priority order (revision 2):**

| Tier | Gaps |
| --- | --- |
| Blockers | G1 (README), G2 (main red), G15 (examples that execute or fail open), G10 (open security findings), G16 (README email) |
| Stand-up core | G4 (runtime step), G3 (discovery), G6 (slim index), G14 (one gate policy), G13 (validator honesty plus fixtures) |
| Trust | G5 (provenance markers), G7 (source slices) |
| Later | G11 (behavioral test), G9 (duplicates), G8 (appendices), G12 (license, owner decision) |

The G-numbers are stable ids, not ranks.

| # | Gap | Evidence | Size of fix |
| --- | --- | --- | --- |
| G1 | **The README on main sends bots the wrong way.** GitHub renders README first, and URL-only agents (chat assistants with browsing) usually fetch it first. It never mentions `AGENTS.md` or `skills/`, and it lists a nonexistent `book/` path and "424 pages". | `git show origin/main:README.md` lines 30–31, 114. The accurate README is stuck in open PR #4. | Small: land PR #4's README, then add a first-screen "For AI agents: start at AGENTS.md" line with absolute raw URLs |
| G2 | **Main fails its own validator (3 checks).** | §6 | Small: keyword fix from PR #4, plus the token fix (G6) |
| G3 (revised) | **Runtime discovery is only partly covered.** `AGENTS.md` is read natively by Codex and by Claude Code v2.1.277+ (both verified, §10). Gemini CLI reads `GEMINI.md` by default and only reads `AGENTS.md` if `context.fileName` is configured. **Skills are not auto-discovered by any runtime**: Codex scans `.agents/skills/`, Claude Code scans `.claude/skills/`, and this repo uses `skills/`. | §10 | Small. Do **not** add a `CLAUDE.md` unless it imports `@AGENTS.md`: Claude Code reads `CLAUDE.md` *instead of* `AGENTS.md` when both exist (§10). Add a project `.gemini/settings.json` with `context.fileName` that includes `AGENTS.md`, or a `GEMINI.md` that points to it. Optionally add generated or symlinked `.agents/skills/` and `.claude/skills/` mirrors (Codex follows symlinks per its docs). Weigh that against G9. |
| G4 | **No "who am I / what do I do first" step.** `AGENTS.md` says "Pick the skills that match your role", but a single Claude Code or Codex session holds every role. The `models/` profiles name three unverified models in a team topology and say nothing about the runtimes the owner listed. | `AGENTS.md:7–15`; `models/*.md` | Medium: a runtime-class step in `AGENTS.md` (coding CLI agent / IDE agent / chat-or-desktop assistant / URL-only reader) with per-class profiles. Appendix E and G are a SOURCE basis for the coding-agent profile (GT:L15451ff., L16292ff., "Primacy of Context" at GT:L16336–L16337). |
| G5 | **Provenance is not marked inside skills.** About 51% of code lines are not traceable, 17 or more deep-dives have no derived marker, and the three named defects (OpenRouter, invented Ch12 code, HITL overclaims) are confirmed. The book's own IDOR flaw is shipped as a runnable example without a WEAK label. | §4.2, §4.4 | Medium: a SOURCE/DERIVED/WEAK marker per section with GT:L citations, plus a validator rule that every code block in `deep-dive.md` either cites GT:L or notebook, or is labeled DERIVED |
| G6 | **The token gate fails, and it measures the wrong path.** It spends 1848 of 3000 tokens on a full manifest that duplicates SKILL.md frontmatter, and it ignores `deep-dive.md`. An id/role/when index is about 482 tokens (measured), which frees about 1,360 tokens. | §6; tiktoken measurement | Small: emit a slim index (in `AGENTS.md` or a generated `skills/INDEX.md`) and tell bots to read that. Keep `manifest.json` for tooling. Re-base the gate on the documented stand-up path. |
| G7 | **The rule references "PDF-derived source slices" that do not exist.** A bot told to consult the source for fidelity has to load a 17,658-line file. | `AGENTS.md:19`; `ground-truth/` contains only the whole file | Small: add `chapter_start_line` and `chapter_end_line` (GT:L) to the manifest, or a `ground-truth/INDEX.md`, so a bot can read just Chapter N's line range. Chapter offsets are in §4.1. |
| G8 | **Book appendices A–G have no skills.** That is book lines 13596–~17000, about 20% of the text. A (advanced prompting), E (CLI agents), and G (coding agents) are the most relevant to the stand-up goal. | `grep Appendix manifest.json skills/*/SKILL.md` returns 0 | Medium: either compact appendix cards or an explicit "out of scope" note. The owner's step (a) says "re-audit all 21 skills **and appendices**", but there is nothing for appendices to audit yet. |
| G9 | **Duplication noise.** 56 notebook copies of 21 cards, plus manifest/frontmatter duplication. A grepping bot sees the same pattern 2–5 times, and every new entry file adds another copy. | §3.1, §5.4–5.6 | Small: decide on one canonical location and generate the rest, or delete the 56 copies, which are not needed by any runtime |
| G10 | **Open security and review findings.** The `eval` sandbox, IDOR (book defect), validator path traversal, and the `ground-truth/README` output path are all unfixed. | §2.1 | Small |
| G11 | **No behavioral test of stand-up.** The only "simulation" is token arithmetic. | §6 | Medium (see §8c) |
| G12 | **No `LICENSE`.** Notebook headers cite an MIT file that does not exist. A bot asked "can I reuse this code" has no answer. | audit 10-unresolved #9; re-checked absent | Owner decision, not agent work |
| G13 (new, from Pepper) | **The validator treats some unknowns as passed and has no expected-FAIL fixtures.** No git data gives a false "unmodified" PASS. A missing example still gives "all examples run" PASS. A missing file or missing `tiktoken` crashes instead of reporting "blocked". | §6 revision-2 table | Medium. Use a tri-state result per check (PASS / FAIL / BLOCKED with evidence) where BLOCKED fails the run. Add `fixtures/pass/` and `fixtures/fail/` mini-packs. Pin file hashes instead of diffing against git. Fall back to a character count, or report BLOCKED, when `tiktoken` is absent. |
| G14 (new, from Pepper) | **There is no single gate or policy, and the four places that state the irreversible-action rule disagree.** `human-in-the-loop` SKILL.md:13 says payment, delete, send. `models/muse.md:21` adds share, publish, schedule. `models/grok-4-6.md:31` lets "the plan" (another agent) authorise irreversible actions with no human. `models/fable-5-1.md:31` only requires a gate "when the user is absent". There is no ship checklist, no secrets rule, and no "don't mutate the owner's machine" rule anywhere. | `rg` across the files named | Medium. One DERIVED `gates` policy template with placeholders, which the profiles reference instead of restating. See §9. |
| G15 (new, from Pepper) | **Examples execute where they should only draft, or fail open.** (a) `skills/human-in-the-loop/examples/minimal.py:49` auto-executes `send_email` marked `irreversible=False`, contradicting the skill's own rule that "send" is irreversible (SKILL.md:13). (b) `skills/mcp/examples/minimal.py:47–51`: under `python -O` the `assert` guard is stripped and `delete_everything` runs (verified). An empty `tool_filter=[]` exposes every tool, including `delete_everything` (verified). (c) The guardrails IDOR guard (G10) allows a call when `user_id` is absent. | Commands in §9.3 | Small. Make the guards fail closed with explicit `raise`, treat `[]` as "deny all", and make send default to draft-then-confirm. |
| G16 (new, privacy) | **Personal identifiers.** The Colab `userId` `<colab-user-id>` and `displayName` appear in 7 notebooks and in history. Notebooks are frozen by the standing rules, so this needs an owner decision: leave as is, or strip it with a documented one-time exception (it would still be in history). Separately, **PR #4's new README (line 88) writes the upstream author's personal email `<upstream-author-email>` into prose.** It is public in git metadata, but Pepper's "no real personal emails in repo" rule argues for removing it before PR #4 lands. | §4.1; `README.md:88` on `ed7e205` | Small edit for the README. Owner decision for the notebooks. |

---

## 8. Route assessment

The owner's proposed route:

- (a) Fix the 2 token failures and the 3 weak skills, and re-audit all 21 skills and appendices.
- (b) Add a single entry point (STANDUP.md or an AGENTS.md section) that tells a bot to identify its runtime, load a `models/` profile (adding coding-cli-agent and desktop-assistant-agent), read `manifest.json`, lazy-load skills through a routing table, and run a self-check.
- (c) Build a fixture simulation of a fresh agent doing 3–5 tasks, wired into the validator.
- (d) Run a secrets and hygiene scan.
- (e) Open a draft PR to main.

**Verdict: the direction is right, but the order is wrong, one piece is missing, and two parts would make things worse if done as written.**

### What is right

- Identifying the runtime first and loading a runtime profile is the most important missing step (G4). The current `models/` files describe a fictional three-model team, not the runtimes the owner listed.
- Fixing the three weak skills is necessary. All three are confirmed (§4.2).
- A secrets scan is cheap. I already ran one, and the tree and history are clean for common key shapes. The only exposure is the 7 Colab user ids, and notebooks are frozen by the standing rules.
- A draft PR to main is the right delivery mechanism.

### What I would change, and why

1. **Fix main and land PR #4 first, before any new feature.** Main fails its own validator today (3 checks). Its README, the file every URL-only bot sees first, sends bots to a nonexistent `book/` folder and never mentions `AGENTS.md` (G1, G2). PR #4 already fixes most of that. Building a stand-up path on top of a broken main means the draft PR in step (e) will carry the audit, the validator fix, and the stand-up change together, which makes it hard to review. Sequence instead: PR #4 (or its README plus validator keyword), then security and hygiene fixes, then the stand-up work.

2. **Do not create STANDUP.md as the entry point. Put the procedure in `AGENTS.md`.** Revised with the vendor checks in §10. No runtime auto-loads a file called STANDUP.md. `AGENTS.md` is auto-read by Codex and by Claude Code v2.1.277+ (verified), by Cursor (UNVERIFIED), and by Gemini CLI only when configured. A STANDUP.md would add a hop that some bots never take. Pepper's "ONE entry file with ordered boot steps and a done-check per step" is compatible with this, provided that one file **is** `AGENTS.md`. The design:
   - The ordered boot steps, each with a done-check, live in `AGENTS.md`.
   - **No `CLAUDE.md`**, or one that only contains `@AGENTS.md`. Claude Code reads `CLAUDE.md` *instead of* `AGENTS.md` when both exist.
   - A Gemini pointer (`.gemini/settings.json` `context.fileName` including `AGENTS.md`, or a one-line `GEMINI.md`).
   - The validator checks that every pointer resolves to `AGENTS.md`.
   - README gets a first-screen "AI agents: read AGENTS.md" line with absolute raw.githubusercontent URLs for agents that cannot clone.

3. **Do not tell the bot to "read manifest.json". Give it a slim generated index.** Reading the whole manifest costs 1848 tokens and repeats the SKILL.md frontmatter. It is also the reason the gate fails. Trimming 6–14 tokens from `AGENTS.md` would turn the check green while leaving that design in place. An id/role/when index is about 482 tokens. Generate the "when to use which pattern" routing table from `manifest.json` (`when_to_use`, `when_not_to_use`, `chains_with`) instead of hand-writing a third copy (§5.6). Keep the manifest for tools.

4. **Treat the 3000-token gate as a design choice, not a law, and measure the path you actually ship.** The 3000 number has no recorded rationale ("Step 7" refers to a prompt not in the repo). Every runtime the owner listed has context windows far larger than 3000 tokens, so the real risk is a bot loading the wrong skill or trusting invented code, not running out of space. A small cold start is still worth keeping. It matches the book's own resource-aware and context-curation guidance (Ch16; Appendix G "Primacy of Context"). But the gate should count the documented stand-up path (entry, runtime profile, index, 1–2 cards, and optionally one `patterns.md`) and report the cost of opening `deep-dive.md` separately, instead of pretending deep-dives are never loaded.

5. **Make the re-audit in step (a) mechanical, and fix provenance across the whole library, not only the three files.** Re-auditing 21 skills by hand will drift again. The problem is systemic: about half the code lines are untraceable, and almost no deep-dive marks what is derived (§4.4). Add a per-section SOURCE/DERIVED/WEAK marker convention with GT:L citations, plus a validator rule that enforces it (the line-matching script in §4.4 is a starting point). Then hand-check the lowest-traceability files first: guardrails, exploration-discovery, evaluation-monitoring, reasoning-techniques, planning, learning-adaptation. "Appendices" in step (a) needs a decision first: there are no appendix skills to audit (G8).

6. **Step (c) has to be honest about what it tests.** A scripted "fresh agent" inside `validate.py` cannot test whether a real bot follows the path. It would be a second version of the token arithmetic. Two realistic layers:
   - **Deterministic, in the validator:** a fixture file of 5–10 task prompts, each with the expected skill ids. The check asserts that the generated routing table and index contain the trigger terms needed to pick those ids, that each expected id's SKILL.md exists, and that the path stays under budget. Label it "static routing fixture", not "simulation".
   - **Behavioral, outside the validator:** a documented manual or CI-optional script that runs a real headless agent from a clean clone (for example `claude -p`, `codex exec`, or `gemini -p`) with the same prompts and records which files it opened and which pattern it applied. It needs credentials and is non-deterministic, so it should not gate `validate.py`.

7. **Add three things the plan does not mention:**
   - The source-slice index (G7). The `AGENTS.md` rule currently points bots at slices that do not exist, and this is the cheapest way to let a bot consult the book without loading it whole.
   - A decision on the 56 duplicate cards (G9).
   - The license question (G12), which only the owner can answer.

8. **Keep the Agent Academy separate.** It is a different product (§5.8). Merging `docs/academy` is fine only if `AGENTS.md` never routes bots into it.

### Suggested order

1. Land PR #4, or cherry-pick its README, `chapter_notebooks/README.md`, and validator keyword fix. Add the "agents start here" line to README.
2. Hygiene: fix the `eval` example, label the IDOR as a book defect in the guardrails skill and make the example fail closed, validate manifest ids before `sync()`, fix the `ground-truth/README` command, and pin file hashes instead of diffing against `origin/main`.
3. Fix the three weak skills, and add the provenance-marker convention and validator rule.
4. Stand-up path in `AGENTS.md` as ordered boot steps, each with a done-check:
   - identify the runtime;
   - load the runtime-class profile;
   - read the slim generated index;
   - read `templates/gates.md` (§9);
   - pick 1–2 cards;
   - use source slices by line range only when needed;
   - run the self-check.

   Also: add the Gemini pointer (no bare `CLAUDE.md`), runtime-class profiles, and optional `.agents/skills` and `.claude/skills` mirrors. Re-base the token gate on this path.
5. Validator honesty (G13): PASS/FAIL/BLOCKED with evidence per check, expected-PASS and expected-FAIL fixture packs, plus the static routing fixture. Keep the behavioral test outside the validator.
6. DERIVED operational templates (§9): gates/policy, connectors-as-needs plus `.env.example`, identity and memory-seed, bounded routines, and one `ship-security-checklist` skill. All placeholders, no personal data.
7. Draft PR to main, with the checklist and a review. Then a provenance pass over the remaining skills, ordered by the §4.4 triage list, and an appendix decision.

**Revision 2 verdict change:** the core verdict stands (fix main first, `AGENTS.md` as the one entry, slim index, honest tests). Two things change:

- The Claude Code fact means "add `CLAUDE.md`" would have been harmful. It is now "don't, or import `@AGENTS.md`".
- Pepper's input adds a missing **operational-safety layer** (G13–G15, the §9 templates). I now rank the fail-open examples and the conflicting irreversible-action rules as blockers, ahead of the stand-up work. A bot that stands up cleanly and then auto-sends mail is a worse outcome than one that never stands up.

---

## 9. External input: Pepper bot (UNVERIFIED)

The source is `/tmp/state/PEPPER-INPUT.md`, received 2026-10-06 00:03 UTC and forwarded by the owner. Pepper labels its own items UNVERIFIED. I checked every factual claim in it against the repository or vendor sources. **None of Pepper's items is book-sourced.**

- Some have a SOURCE *anchor* in the book: human approval (Ch 13), guardrails and least privilege (Ch 18), goal checks (Ch 11), evaluation (Ch 19), and context curation (Appendix G).
- Everything added for them is **DERIVED/operational** and must be labelled that way.

Pepper says this too (PEPPER-INPUT.md:21).

### 9.1 Item-by-item assessment

| # | Pepper item | Fits goal / existing design? | Book status | Conflicts with repo or owner plan | Verdict |
| --- | --- | --- | --- | --- | --- |
| P1 | ONE entry file with ordered boot steps and a done-check per step | Yes, and it is what §8 already recommends. The done-check per step is a real improvement over the current `AGENTS.md`, which has no checks. | DERIVED. Anchors: Ch 11 goal and monitoring checks (SOURCE), Appendix G context curation (SOURCE). | Conflicts with the owner's option "STANDUP.md". It does not conflict if the one file is `AGENTS.md`. | **ADAPT.** The one entry file is `AGENTS.md`. Native pointers (Gemini; Claude only via `@AGENTS.md`) are discovery shims, not second entry files. Each boot step gets an observable done-check, for example "you can name your runtime class", "you read `index` and chose ≤2 ids", "self-check printed PASS". |
| P2 | Skills as folder/SKILL.md with name plus a "use this when…" intent description, no frozen tool schemas | Mostly already true: all 21 `SKILL.md` have `name` and an intent `description` of the form "X. Use … Not …". This matches the Codex and Claude skill formats (§10). | DERIVED convention | Partial conflict with current content. **11/21 `SKILL.md` name framework APIs** in their body or minimal example (counts: multi-agent 4, memory-management 4, planning 3, exception-handling 3, tool-use 2, parallelization 2, mcp 2, rag/prompt-chaining/HITL/guardrails 1). **21/21 `patterns.md` have a "Key APIs" section** (16 name framework APIs). **19/21 `deep-dive.md`** do too. Dated model ids appear in references, for example `gemini-2.0-flash-exp` (multi-agent ×5, exception-handling ×3) and `gpt-4o` (resource-aware ×5). | **ADAPT.** Keep `SKILL.md` framework-neutral: move the 11 framework-specific minimal examples to pseudocode, and put the ADK/LangChain calls in `references/`. Keep book code in `references/` as **SOURCE quotes with an "as of the book" label**, not as schemas to call. Don't strip it: the book's value is partly that code. |
| P3 | Gates/policy TEMPLATE with placeholders: ship=NO until checklist passes; human AUTH before consequential actions; never mutate owner's machine without permission; no secrets in repo; reserved-ports placeholder; no real personal data | Strong fit. It fills G14: there is no policy file today, and four profile/skill files state conflicting irreversible-action rules. | Human approval is SOURCE (Ch 13: GT:L7945 human-on-the-loop; escalation in Key Takeaways). Least privilege and screening are SOURCE (Ch 18). "ship=NO", "owner's machine", and "reserved ports" are DERIVED/operational. | Fixes the conflict between `models/grok-4-6.md:31` ("unless the plan explicitly authorises") and `models/muse.md:21` / HITL. Choose "a human authorises, never a plan". | **ADOPT** as `templates/gates.md` (DERIVED, placeholders only, for example `<RESERVED_PORTS>`). Profiles and the three safety skills link to it instead of restating it. Validator: the file exists, contains no real emails, IPs, or hostnames, and every profile references it. |
| P4 | Connectors as "needs" with a check each; no self-auth or self-grant; no auto-send mail; only `.env.example` | Fits. The repo has no connectors today, but the notebooks expect `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `GOOGLE_CSE_ID`, and others (per `chapter_notebooks/README.md` on `ed7e205`), and there is no `.env.example`. | DERIVED/operational. Anchors: Ch 18 least privilege, Ch 10 MCP `tool_filter` (GT:L6848). | The current HITL example auto-sends email (G15a), which conflicts directly with "never auto-send". | **ADOPT.** `templates/connectors.md` lists each need, how to check it, and who grants it (always the human). Add a root `.env.example` with the variable names the notebooks read and empty values, plus a `.gitignore` that covers `.env`. Fix G15a. |
| P5 | Routine templates: bounded cron; self-expiring watches | Weak fit for a *pattern library*. It is useful for a personal-agent deployment (Muse-like), but it is not needed to "stand up and apply the patterns". | DERIVED/operational. Loose anchors: Ch 11 monitoring, Ch 16 resource bounds. No book text on cron. | Scope creep relative to the owner's plan (a)–(e). | **ADAPT, low priority.** One optional `templates/routines.md` with a hard max-runs, an expiry date, and an owner placeholder. Not in the boot path. |
| P6 | Offline validator: expected-PASS and expected-FAIL fixtures, one command, idempotent, "Unknown = blocked, not passed", evidence per check | Strong fit. The current validator violates it in several cases (§6 revision-2 table). | DERIVED. Anchor: Ch 19 evaluation (SOURCE). | Overlaps the owner's step (c). Pepper's version is the more honest one. | **ADOPT** (G13). Tri-state result per check with an evidence string. `fixtures/pass/` and `fixtures/fail/` mini-packs, with a meta-test that each fail-fixture fails for the stated reason. Hash pins instead of `git diff`. A `tiktoken`-absent path that reports BLOCKED. Catch timeouts. Make `python3 tools/validate.py` the one command. |
| P7 | Identity/profile template plus memory-seed template (preferences, shorthand, delivery format) | Partial fit. A runtime-class profile is G4 (needed). A personal identity and memory seed is for the owner's own deployment, not for a public pattern repo. | DERIVED. Anchor: Ch 8 memory (`user:` prefix GT:L5227, SOURCE). | Risk of personal data landing in a public repo, which Pepper itself forbids. | **ADAPT.** Ship `templates/profile.md` and `templates/memory-seed.md` with placeholders only, and have the validator check for personal data. Keep runtime-class profiles in `models/` and personal ones out of the repo. |
| P8 | ONE consolidated ship-security checklist skill, not near-duplicates | Fit. No such skill exists. Gate *skills* are not duplicated today: guardrails, HITL, and exception-handling are distinct book chapters that cross-link (`chains_with`). The **rules** are duplicated and inconsistent across `models/*.md` (G14). | DERIVED/operational. It assembles Ch 12, 13, 18, and 19. | Must not replace or merge the three chapter skills, which are SOURCE-anchored patterns. | **ADOPT** as a 22nd, explicitly DERIVED skill (for example `ship-security-checklist`, chapter `null`, role `safety`), or as `templates/ship-checklist.md`. It needs a manifest schema change: `chapter` currently has to be 1..21 (validator "manifest chapters are exactly 1..21"). It references the gate template and the three chapter skills rather than copying them. |
| P9 | Optional "teacher review" skill: structured quality review before merge | Fits the critic role, and matches the owner's "do not take 'I verified it' on trust" rule. | DERIVED. Anchors: Ch 4 reflection producer/critic (GT:L2462–L2471), Ch 19 LLM-as-judge (SOURCE). | Overlaps `reflection` and `evaluation-monitoring`. It could become a near-duplicate. | **ADAPT.** Make it a checklist inside the ship-checklist or `CONTRIBUTING`, citing `reflection` and `evaluation-monitoring`, rather than a 23rd skill. Revisit if a separate one proves needed. |
| W1 | Don't wire Codex as an MCP server; prefer a packet file plus `codex exec --json` | Claim **verified** (§10): `codex mcp-server` was deprecated on 2026-08-20 and removed on 2026-09-05, first absent in release `rust-v0.154.0`. `codex exec --json` exists. | Not book content. The book's MCP chapter predates this. | No repo file wires Codex as an MCP server (grep: none). | **ADOPT** as a note in the coding-cli profile. Don't overstate it: `codex mcp` (managing *external* MCP servers that Codex uses as a client) still exists. |
| W2 | Don't let any tool execute where it should only read or draft | Fit. There are real instances (G15): HITL auto-send, MCP `assert`/empty-filter fail-open, IDOR guard. | Ch 18 least privilege (SOURCE). Fixes are DERIVED. | None | **ADOPT.** Fix the instances, and add a validator check that every example's guard uses `raise` rather than `assert`. |
| W3 | No mega-skill | Already satisfied. The largest `SKILL.md` is 45 lines (`tool-use`); bodies are ≤234 tokens. The largest `deep-dive.md` is about 2,000 tokens. | n/a | Watch it when adding the ship-checklist skill, so it doesn't absorb gates, connectors, and routines. | **ADOPT** as a constraint (already enforced by the 400-token cap) |
| W4 | No duplicated gate skills | Gate skills are not duplicated. Gate *rules* are (G14), and the 56 notebook `.SKILL.md` copies triplicate the cards (G9). | n/a | n/a | **ADOPT.** Point to one policy file, and generate rather than copy. |
| W5 | No merge without checklist plus review; PR only, no merge | Fits the standing rules and the owner's step (e). Note that PRs #1 and #2 were merged with no human review (merged 3 and 45 minutes after opening, with the Codex review rate-limited). | DERIVED/process | None | **ADOPT** |

### 9.2 Is there a "mega-skill" or duplicated gate skill now?

No mega-skill exists (W3). No duplicated gate skill exists. The problem is three slightly different irreversible-action policies in `models/` plus the HITL card (G14), and no ship checklist at all.

### 9.3 Re-verified "executes where it should only draft"

| File | Observed |
| --- | --- |
| `skills/human-in-the-loop/examples/minimal.py:49` | `Action("send_email", ..., irreversible=False, confidence=0.95)` prints `executed send_email on jane@example.com`, with no confirmation |
| `skills/mcp/examples/minimal.py:50` | `python3 -O` run: `delete_everything` is called and the "blocked:" line never prints. `MCPToolset(server, tool_filter=[])` exposes `['greet', 'delete_everything']`. |
| `skills/guardrails/examples/minimal.py:28` | Allows the call when `user_id` is absent (book defect, GT:L11610) |
| `skills/reasoning-techniques/examples/minimal.py:8` | `eval` on model-chosen input |
| `tools/validate.py --sync` | Writes 78 files. That is intended, but the ids feeding the paths are not validated first. |

---

## 10. Runtime and Codex facts, checked 2026-10-06 against vendor sources

| Claim | Result | Source (fetched 2026-10-06) |
| --- | --- | --- |
| `codex mcp-server` removed | **VERIFIED.** Deprecation warning added in PR #39657 (merged 2026-08-20): "deprecated and will be removed in a future release". Removed in PR #42993 (merged 2026-09-05): "Remove the `codex mcp-server` subcommand and the standalone `codex-mcp-server` crate". The release notes for `rust-v0.154.0` (published 2026-09-09) say "The deprecated `codex mcp-server` entry point is no longer available. (#42993)". The GitHub compare shows `rust-v0.153.4` does **not** contain the removal commit and `rust-v0.154.0` does. At HEAD `685270a` (2026-10-05) the CLI `Subcommand` enum in `codex-rs/cli/src/main.rs` has no McpServer variant, and `codex-rs/` has no `mcp-server` crate. | [openai/codex#39657](https://github.com/openai/codex/pull/39657), [openai/codex#42993](https://github.com/openai/codex/pull/42993), [release rust-v0.154.0](https://github.com/openai/codex/releases/tag/rust-v0.154.0), `codex-rs/cli/src/main.rs` @ `685270a` |
| `codex mcp` still exists | **VERIFIED.** "Manage external MCP servers for Codex", where Codex is the client. Pepper's warning is about Codex *as a server* only. | `codex-rs/cli/src/main.rs` @ `685270a`, `Mcp(McpCli)` |
| `codex exec --json` exists | **VERIFIED.** `codex-rs/exec/src/cli.rs`: `#[arg(long = "json", alias = "experimental-json")]`, "Print events to stdout as JSONL". The docs page shows `codex exec --json "summarize the repo structure" \| jq` with events `thread.started`, `turn.started`, `turn.completed`, `turn.failed`, `item.*`, `error`. | `codex-rs/exec/src/cli.rs` @ `685270a`; [developers.openai.com/codex/noninteractive](https://developers.openai.com/codex/noninteractive) |
| Codex reads `AGENTS.md` | **VERIFIED.** It walks from the project root down to the CWD, checking `AGENTS.override.md`, then `AGENTS.md`, then fallbacks. Combined cap `project_doc_max_bytes` is 32 KiB by default. | [developers.openai.com/codex/guides/agents-md](https://developers.openai.com/codex/guides/agents-md) (.md variant) |
| Codex skill discovery | **VERIFIED.** It scans `.agents/skills` from CWD up to the repo root, plus `$HOME/.agents/skills` and `/etc/codex/skills`. A skill is a folder with a `SKILL.md` that has `name` and `description`. Symlinks are followed. The initial skill list uses at most 2% of context or 8,000 characters. **Our `skills/` is not scanned.** | [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills) |
| Claude Code reads `AGENTS.md` | **VERIFIED, with a trap.** It reads `AGENTS.md` natively from v2.1.277, but **only when there is no `CLAUDE.md`/`.claude/CLAUDE.md`/`CLAUDE.local.md` in the CWD or above**. If a `CLAUDE.md` exists, Claude reads that *instead*, unless it imports `@AGENTS.md`. | [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) ("AGENTS.md" section) |
| Claude Code skill discovery | **VERIFIED:** `.claude/skills/<name>/SKILL.md` | [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) |
| Gemini CLI | **VERIFIED:** the default context file is `GEMINI.md`. Settings `context.fileName` can list `["AGENTS.md", "CONTEXT.md", "GEMINI.md"]`. | [gemini-cli docs/cli/gemini-md.md](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/gemini-md.md) (main branch, fetched 2026-10-06) |
| Cursor reads `AGENTS.md`; Grok conventions | **UNVERIFIED** (not checked this session) | n/a |

Consequence for the design: one `AGENTS.md` now reaches Codex and Claude Code with no extra files. Gemini needs one pointer. Skills need either the boot steps in `AGENTS.md` ("read `skills/INDEX`") or mirrors in `.agents/skills/` and `.claude/skills/` to be discovered natively. Mirrors raise the duplication count (G9), so generate them, or symlink them if the platforms you care about allow it.

---

### Reproduction notes

- Validator logs: `/tmp/state/val-*.txt`. Provenance table: `/tmp/state/provenance.txt`. PR dumps: `/tmp/state/prs.txt`. These are scratch files and are not committed.
- Every PR and API command needs `-R shinarugrok-a11y/Agentic-Design-Patterns`, because the clone's default `gh` repo resolves to evoiz upstream, which has unrelated PRs #1–#3.
