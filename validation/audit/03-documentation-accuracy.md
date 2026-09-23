# 3. Documentation accuracy

Scope: root `README.md` (pre-audit text), `chapter_notebooks/README.md`, `AGENTS.md`, `ground-truth/README.md`, `models/*.md`, `tools/validate.py` docstring, notebook markdown and comments that give instructions. Classifications: `CORRECT`, `CORRECT BUT INCOMPLETE`, `STALE`, `INCORRECT`, `UNSUPPORTED`, `DEPRECATED`, `EXTERNAL/HISTORICAL CONTEXT`.

## Root README (text before this audit)

| Claim | Class | Evidence |
| --- | --- | --- |
| Book by Antonio Gulli; royalties to Save the Children | CORRECT | Title page region and acknowledgment line 112 of the extract |
| Repository contains the book PDF and notebooks | CORRECT BUT INCOMPLETE | PDF is at repo root, not `book/`. Notebooks are snippets, and seven appendices are placeholders. Skill library was undescribed |
| "Complete book (424 pages)" | INCORRECT | `pdfinfo` Pages: 458 |
| Part page counts 103 / 61 / 34 / 114 / 74 and appendices 74 | UNSUPPORTED | Not reproduced from this PDF. Printed numbers restart per chapter |
| TOC chapter titles and appendix letters | CORRECT BUT INCOMPLETE | Titles match chapter start lines in the extract. Appendix title wording in the PDF differs slightly (for example "Appendix B - AI Agentic Interactions") |
| `pip install -r requirements.txt` | INCORRECT | File does not exist |
| `pip install pandas numpy matplotlib openai langchain` as the install | UNSUPPORTED | Notebook imports are a wider, different set (`google.adk`, `langchain_openai`, `crewai`, …). Versions unpinned |
| Clone `evoiz/Agentic-Design-Patterns` | INCORRECT for this repo | `origin` is `shinarugrok-a11y/Agentic-Design-Patterns`. evoiz `main` is ancestor `e11e6fb` |
| `jupyter notebook Chapter_01_Prompt_Chaining.ipynb` | INCORRECT | Filename does not exist |
| `CONTRIBUTING.md` | INCORRECT | File does not exist |
| Code examples MIT, see `LICENSE` | INCORRECT | No `LICENSE`. GitHub `licenseInfo` is null. Individual notebook headers still say MIT |
| Google Drive folder as an official materials link | EXTERNAL/HISTORICAL CONTEXT | URL is the one embedded in placeholder notebooks. Not required to use the PDF or skills. Reachability not re-tested |
| Issues and Discussions on `evoiz/Agentic-Design-Patterns` | STALE | This repo has `has_issues: false` and `has_discussions: false`. evoiz issue state was not checked |
| Shields and star-history for `evoiz/agentic-design-patterns`, including a license badge | INCORRECT | Points at a different repository, and this repo has no license file |
| "Pre-order" the book | UNVERIFIED external status | Amazon URL kept as an external pointer. Current retail state was not checked on 2026-09-23 |
| Related frameworks (LangChain, AutoGPT, Assistants, AutoGen, CrewAI) | EXTERNAL/HISTORICAL CONTEXT | Some of those names appear in notebooks. They are not vendored. AutoGPT and Assistants are not imported by a repo entry point |

## `chapter_notebooks/README.md` (before this audit)

| Claim | Class | Evidence |
| --- | --- | --- |
| Filename index of chapter and appendix notebooks | CORRECT | Compared to `ls chapter_notebooks` |
| "58 notebooks" and "complete, runnable" | INCORRECT | 65 ipynb files; placeholders, syntax errors, stored tracebacks |
| `pip install pandas numpy matplotlib` | UNSUPPORTED | Same as root README |
| Google Doc TOC and Google Drive as sources | EXTERNAL/HISTORICAL CONTEXT | Not needed to list the files already present |

## `AGENTS.md`

| Claim | Class | Evidence |
| --- | --- | --- |
| 21 skills, lazy-load via `manifest.json` | CORRECT | Validator role table matches |
| "Do not load the entire PDF during normal execution" | CORRECT as a loading rule | The PDF is 18 MB. The validator used to look for a different sentence |
| Model names Fable 5.1, Grok 4.6, Muse | CORRECT BUT INCOMPLETE | Files exist. Their capability numbers are unverified |

## `models/*.md`

Context windows ("~1M", "~500K"), prices, and role ownership are **UNSUPPORTED** by any measurement in this repo. Treat them as guidance notes, not vendor facts.

## `ground-truth/README.md`

| Claim | Class | Evidence |
| --- | --- | --- |
| Extract command `pdftotext -layout` from the root PDF | CORRECT BUT INCOMPLETE | Re-extract matches except 17 emoji-wrap lines on Poppler 24.02.0 |
| Baseline commit `fede537` | CORRECT BUT INCOMPLETE | That commit is when the extract was added relative to the skill library. The PDF blob dates from `7ddebbc` and is unchanged since |
| "Do not claim that the PDF was verified from the binary alone" | CORRECT | This audit used `pdfinfo` plus text compare, not a visual proof |

## `tools/validate.py` docstring (before this audit)

| Claim | Class | Evidence |
| --- | --- | --- |
| Examples run offline | CORRECT | PASS |
| Combination stays under 3,000 tokens | INCORRECT as a description of current numbers | Measured 3,006 and 3,014. The check still enforces 3,000 and still fails |
| README and notebooks must be unmodified vs `origin/main` | STALE relative to an accuracy pass | The PDF and `.ipynb` guard remains. README edits are now allowed and logged |

## Notebook instructions

| Instruction | Class | Evidence |
| --- | --- | --- |
| "Log into Google Drive / replace this placeholder" in seven appendix notebooks | DEPRECATED as setup; EXTERNAL/HISTORICAL CONTEXT as provenance | Left in place inside the ipynb files |
| Comments that require `OPENAI_API_KEY`, `GOOGLE_API_KEY`, and similar | CORRECT BUT INCOMPLETE | Those names occur in the code. The repo does not document how to obtain each key, and it should not invent that procedure |
| `Chapter_02_Routing_(LangGraph).ipynb` header: see `LICENSE` | INCORRECT | No license file |
| `Chapter_06_Planning_(Deep_Research_API).ipynb` uses `api_key="YOUR_OPENAI_API_KEY"` and model `o3-deep-research-2025-06-26` | UNSUPPORTED | Stored output is a 401 from that placeholder. Whether that model id still exists was not checked |
| `Chapter_03_Parallelization_(Google_ADK).ipynb` points at `https://google.github.io/adk-docs/get-started/quickstart/` | EXTERNAL/HISTORICAL CONTEXT | URL not fetched. The cell also has a leading indent and does not parse |

## What was trustworthy without edits

- `manifest.json` skill ids, chapters, and roles (validator PASS)
- `chapter_notebooks/README.md` filename index
- Book acknowledgment text, including the royalties sentence and named code contributors
- `ground-truth/README.md` command, with the Poppler caveat above
