# Agentic Design Patterns

**AI agents: start at [AGENTS.md](AGENTS.md)** (raw: `https://raw.githubusercontent.com/shinarugrok-a11y/Agentic-Design-Patterns/main/AGENTS.md`). It is the single entry point; read nothing else first.

Repository for the book **Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems** by Antonio Gulli, plus a derived agent skill library and an evidence audit of what this tree actually contains.

This checkout is [shinarugrok-a11y/Agentic-Design-Patterns](https://github.com/shinarugrok-a11y/Agentic-Design-Patterns). Git history through `e11e6fb` (2026-07-24, "Merge pull request #2 from 1040942669/fix-readme-typo") is the tip of [evoiz/Agentic-Design-Patterns](https://github.com/evoiz/Agentic-Design-Patterns). Later commits on this repository add the skill library, model profiles, and the pdftotext extract.

The book text states: "All my royalties are donated to Save the Children." That sentence is in `ground-truth/agentic_design_patterns.txt` (acknowledgment). Retail availability of the print edition was not re-checked for this audit. An external product page that previous READMEs linked is [Amazon, ISBN 3032014018](https://www.amazon.com/Agentic-Design-Patterns-Hands-Intelligent/dp/3032014018/).

## Current status

| Material | Where | Status in this repository |
| --- | --- | --- |
| Book PDF | `Agentic_Design_Patterns_Complete.pdf` | Present. Poppler `pdfinfo` reports **458 pages**, letter size, producer PyPDF2, not encrypted. |
| Text extract | `ground-truth/agentic_design_patterns.txt` | Present. A fresh `pdftotext -layout` (Poppler 24.02.0) matches 17,642 of 17,659 lines. The 17 differing lines are emoji wrap in four clusters. |
| Skill library | `AGENTS.md`, `skills/`, `skills/INDEX.md`, `manifest.json`, `models/` | `python3 tools/validate.py` passes, including the 3,000-token simulation (worst pair 2,498, measured on `AGENTS.md` + `skills/INDEX.md`) and the stand-up fixtures (worst case 3,000 of 4,000). All 21 `examples/minimal.py` files exit 0 offline. Re-audit log: `validation/skill-reaudit/LOG.md`. |
| Chapter notebooks | `chapter_notebooks/` | 65 notebooks. Illustrative snippets and fragments. Seven appendix files are Google Drive placeholders. Dependencies are not pinned. |
| Audit | `validation/audit/` | This evidence pass (2026-09-23). Independent of any Claude or Anthropic extraction. |

Verified here means a file, command, or test in this repository was inspected or run. It does not mean every sentence of the book was re-proofed, or that notebook snippets were executed against live model APIs.

## Repository structure

```
.
├── README.md
├── AGENTS.md                  # single agent entry point: boot steps, profile table, role table
├── GEMINI.md                  # one-line pointer to AGENTS.md for Gemini CLI
├── manifest.json              # full record of the 21 skills (for tools)
├── .agents/skills/<id>        # symlinks to skills/<id> for Codex skill discovery
├── Agentic_Design_Patterns_Complete.pdf   # book PDF (458 pages)
├── ground-truth/
│   ├── README.md              # how the text extract was produced
│   ├── INDEX.md               # generated chapter/appendix line ranges
│   └── agentic_design_patterns.txt
├── skills/INDEX.md            # generated slim index + routing signals; agents read this, not manifest.json
├── skills/<id>/
│   ├── SKILL.md               # compact pattern card
│   ├── references/patterns.md
│   ├── references/deep-dive.md
│   └── examples/minimal.py    # offline stub; the examples that actually run here
├── models/                    # runtime profiles (Fable 5.1, Grok 4.6, Muse, coding CLI, desktop assistant)
├── chapter_notebooks/         # book-related notebooks and generated .SKILL.md copies
├── tools/validate.py          # skill-library checks; requires tiktoken
├── tools/standup_sim.py       # deterministic routing-table test of the boot path on tests/fixtures/standup_tasks.json
├── tools/provenance_scan.py   # where each skill code line comes from (book, notebook, none)
├── tests/fixtures/            # stand-up task fixtures
└── validation/                # audit/ evidence pass; skill-reaudit/ per-skill fixes
```

Nothing in this tree is a deployed service. There is no application server, database, or frontend.

## How to use it

### Read the book

Open `Agentic_Design_Patterns_Complete.pdf`, or search `ground-truth/agentic_design_patterns.txt`. The text file is the readable extract. Seventeen lines differ from a Poppler 24.02.0 re-extract; see `validation/audit/02-evidence-map.md`.

### Use the skill library

A fresh agent follows the boot steps in [AGENTS.md](AGENTS.md): name the runtime, load one `models/` profile, read the generated `skills/INDEX.md`, then load at most three `skills/<id>/SKILL.md` chosen by its pick rule. `manifest.json` is the full record for tools. `STANDUP.md` was folded into `AGENTS.md`. Whether Cursor or Grok load `AGENTS.md` automatically is UNVERIFIED.

Check the library:

```bash
python3 -m pip install tiktoken
python3 tools/validate.py
```

On 2026-09-23 that command failed the two 3,000-token simulation checks (3,006 and 3,014). Card trims on this branch fixed them without raising the budget; see `validation/skill-reaudit/LOG.md`. `python3 tools/standup_sim.py` runs only the stand-up fixtures. It is a deterministic test of the routing tables, not of real agent behaviour. `tiktoken` is the validator's dependency. It is not declared in a requirements file because this repository has no `requirements.txt`.

`python3 tools/validate.py --sync` rewrites `token_cost_estimate` values, the `chapter_notebooks/Chapter_*.SKILL.md` copies, `skills/INDEX.md`, `ground-truth/INDEX.md` and the `.agents/skills` symlinks. Run it only when you intend to regenerate those files.

### Notebooks

Notebook setup that this repository supports is: install Jupyter yourself, open a file under `chapter_notebooks/`, and install whatever that file imports. Provide your own API keys. Details and the file index are in `chapter_notebooks/README.md`.

These paths and commands are absent, and the README used to imply them:

- `book/Agentic_Design_Patterns_Complete.pdf` — the PDF is at the repository root
- `requirements.txt` — no such file
- `CONTRIBUTING.md` — no such file
- `LICENSE` — no such file; GitHub reports `licenseInfo: null` for this repository
- `pip install pandas numpy matplotlib` as the common notebook stack — those packages are not what the notebooks import
- `jupyter notebook Chapter_01_Prompt_Chaining.ipynb` — the Chapter 1 files are `Chapter_01_Prompt_Chaining_(Code_Example).ipynb` and `Chapter_01_Prompt_Chaining_(JSON_Example).ipynb`
- Logging into Google Drive — seven placeholder notebooks mention a Drive folder; the rest of the repository does not use it

Clone this repository from `https://github.com/shinarugrok-a11y/Agentic-Design-Patterns`. Cloning `evoiz/Agentic-Design-Patterns` yields the 2026-07-24 tree, which stops before `skills/`, `ground-truth/`, and `validation/`.

GitHub Issues and Discussions are disabled on this repository (`has_issues: false`, `has_discussions: false` as of 2026-09-23).

## Provenance

- **Authoritative book text.** `Agentic_Design_Patterns_Complete.pdf` and the pdftotext extract under `ground-truth/`. The acknowledgment names Antonio Gulli as the author, thanks Springer, and credits Marco Fago (code, diagrams, review) and Mahtab Syed (coding), among others.
- **Derived skill library.** `skills/`, `manifest.json`, `AGENTS.md`, the generated indexes, and `models/` compress each chapter into an agent-loadable card and an offline stub. They are derived notes, not a second copy of the book.
- **Notebook mirror.** `chapter_notebooks/*.ipynb` arrived with the original repository commits by Elias Albittar / Elias Al-bittar (contact details omitted here; see git history). Some cells carry `Copyright (c) 2025 Marco Fago` and point at a `LICENSE` file that is not in the tree. The book text itself also contains those copyright headers inside code listings.
- **Generated duplicates.** `chapter_notebooks/Chapter_*.SKILL.md` copies of `skills/<id>/SKILL.md`, maintained by `tools/validate.py`.
- **Audit record.** `validation/audit/` is the 2026-09-23 evidence pass: what was checked, what was corrected, and what is still uncertain.

## Attribution

Thank you to **Antonio Gulli**, author of *Agentic Design Patterns*, whose book is the source foundation of this repository, and who directed royalties to Save the Children.

Thank you to the people named in the book's acknowledgment, including Marco Fago and Mahtab Syed for code that the notebooks and the book listings attribute.

Thank you to the repository contributors recorded in git history:

- Elias Albittar / Elias Al-bittar — added the PDF, the chapter notebooks, and the original README
- 1040942669 — README typo fix on the evoiz history
- shinarugrok-a11y — skill-library and ground-truth merges on this repository
- Cursor Agent — skill-library and pdftotext commits recorded in that history

This repository does not claim authorship of the book. Book content remains the author's, as stated in the PDF. No `LICENSE` file in this tree grants the notebook code. Where a notebook header says MIT, that header refers to a license file that is not present.

## Limitations

The 2026-09-23 audit did not:

- Re-proof the book prose against a print edition
- Execute notebooks that import Google ADK, LangChain, CrewAI, OpenAI, FastMCP, or OpenEvolve, or that call live APIs
- Confirm the context-window and price figures in `models/*.md` against vendors (they are marked UNVERIFIED)
- Confirm that the Google Drive folder or the Google Docs table of contents is still reachable
- Confirm current retail status of the book
- Decide a license for snippets whose headers mention a missing `LICENSE` file
- Shrink the skill cards to satisfy the 3,000-token simulation (done later on this branch, budget unchanged)
- Compare this audit with any Claude or Anthropic extraction

Start with `validation/audit/README.md` for the evidence behind these statements.
