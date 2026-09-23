# Agentic Design Patterns

Repository for the book **Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems** by Antonio Gulli, plus a derived agent skill library and an evidence audit of what this tree actually contains.

This checkout is [shinarugrok-a11y/Agentic-Design-Patterns](https://github.com/shinarugrok-a11y/Agentic-Design-Patterns). Git history through `e11e6fb` (2026-07-24, "Merge pull request #2 from 1040942669/fix-readme-typo") is the tip of [evoiz/Agentic-Design-Patterns](https://github.com/evoiz/Agentic-Design-Patterns). Later commits on this repository add the skill library, model profiles, and the pdftotext extract.

The book text states: "All my royalties are donated to Save the Children." That sentence is in `ground-truth/agentic_design_patterns.txt` (acknowledgment). Retail availability of the print edition was not re-checked for this audit. An external product page that previous READMEs linked is [Amazon, ISBN 3032014018](https://www.amazon.com/Agentic-Design-Patterns-Hands-Intelligent/dp/3032014018/).

## Current status

| Material | Where | Status in this repository |
| --- | --- | --- |
| Book PDF | `Agentic_Design_Patterns_Complete.pdf` | Present. Poppler `pdfinfo` reports **458 pages**, letter size, producer PyPDF2, not encrypted. |
| Text extract | `ground-truth/agentic_design_patterns.txt` | Present. A fresh `pdftotext -layout` (Poppler 24.02.0) matches 17,642 of 17,659 lines. The 17 differing lines are emoji wrap in four clusters. |
| Skill library | `skills/`, `manifest.json`, `AGENTS.md`, `models/` | Structure checks pass. All 21 `examples/minimal.py` files exit 0 offline. The validator's 3,000-token simulation **fails** (3,006 and 3,014). |
| Chapter notebooks | `chapter_notebooks/` | 65 notebooks. Illustrative snippets and fragments. Seven appendix files are Google Drive placeholders. Dependencies are not pinned. |
| Audit | `validation/audit/` | This evidence pass (2026-09-23). Independent of any Claude or Anthropic extraction. |

Verified here means a file, command, or test in this repository was inspected or run. It does not mean every sentence of the book was re-proofed, or that notebook snippets were executed against live model APIs.

## Repository structure

```
.
├── README.md
├── AGENTS.md                  # how an agent should load the skill library
├── manifest.json              # index of the 21 skills
├── Agentic_Design_Patterns_Complete.pdf   # book PDF (458 pages)
├── ground-truth/
│   ├── README.md              # how the text extract was produced
│   └── agentic_design_patterns.txt
├── skills/<id>/
│   ├── SKILL.md               # compact pattern card
│   ├── references/patterns.md
│   ├── references/deep-dive.md
│   └── examples/minimal.py    # offline stub; the examples that actually run here
├── models/                    # per-model loading notes (Fable 5.1, Grok 4.6, Muse)
├── chapter_notebooks/         # book-related notebooks and generated .SKILL.md copies
├── tools/validate.py          # skill-library checks; requires tiktoken
└── validation/audit/          # structural map, evidence, corrections, security notes
```

Nothing in this tree is a deployed service. There is no application server, database, or frontend.

## How to use it

### Read the book

Open `Agentic_Design_Patterns_Complete.pdf`, or search `ground-truth/agentic_design_patterns.txt`. The text file is the readable extract. Seventeen lines differ from a Poppler 24.02.0 re-extract; see `validation/audit/02-evidence-map.md`.

### Use the skill library

Follow `AGENTS.md`: read `manifest.json`, then load only the `skills/<id>/SKILL.md` files you need.

Check the library:

```bash
python3 -m pip install tiktoken
python3 tools/validate.py
```

On 2026-09-23 that command passed the structural checks and all 21 offline examples, and failed the two 3,000-token simulation checks. `tiktoken` is the validator's dependency. It is not declared in a requirements file because this repository has no `requirements.txt`.

`python3 tools/validate.py --sync` rewrites `token_cost_estimate` values and the `chapter_notebooks/Chapter_*.SKILL.md` copies. Run it only when you intend to regenerate those files.

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
- **Derived skill library.** `skills/`, `manifest.json`, `AGENTS.md`, and `models/` compress each chapter into an agent-loadable card and an offline stub. They are derived notes, not a second copy of the book.
- **Notebook mirror.** `chapter_notebooks/*.ipynb` arrived with the original repository commits by Elias Albittar / Elias Al-bittar (`evoiz963@gmail.com`). Some cells carry `Copyright (c) 2025 Marco Fago` and point at a `LICENSE` file that is not in the tree. The book text itself also contains those copyright headers inside code listings.
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
- Confirm the context-window and price figures in `models/*.md` against vendors
- Confirm that the Google Drive folder or the Google Docs table of contents is still reachable
- Confirm current retail status of the book
- Decide a license for snippets whose headers mention a missing `LICENSE` file
- Shrink the skill cards to satisfy the 3,000-token simulation, or raise that budget to hide the failure
- Compare this audit with any Claude or Anthropic extraction

Start with `validation/audit/README.md` for the evidence behind these statements.
