# 9. Consistency report

Compared after the README and validator edits, against the tree on branch `cursor/repo-evidence-audit-1033`.

| Pair | Result |
| --- | --- |
| Root README ↔ directory names | The structure block lists `AGENTS.md`, `manifest.json`, the root PDF, `ground-truth/`, `skills/`, `models/`, `chapter_notebooks/`, `tools/validate.py`, and `validation/audit/`. Those paths exist. `book/`, `requirements.txt`, `LICENSE`, and `CONTRIBUTING.md` are described as absent, and they are absent. |
| Root README ↔ page count | README says 458 pages from `pdfinfo`. `pdfinfo` printed `Pages: 458`. |
| Root README ↔ ground truth | README says 17 of 17,659 lines differ from Poppler 24.02.0. That is the compare result (17,659 − 17 = 17,642 matching lines). |
| Root README ↔ remote | README names `shinarugrok-a11y/Agentic-Design-Patterns` and evoiz tip `e11e6fb`. `git remote` and `gh repo view` match. |
| Root README ↔ validator | README says structural checks and 21 examples pass, and the 3,000-token simulation fails. Re-run after the phrase fix is recorded below. |
| `chapter_notebooks/README.md` ↔ filenames | The per-chapter index was already a match and was not rewritten. The new counts (65, 56, 9, 7 placeholders, 56 `.SKILL.md`) match `notebook-inventory.json`. |
| `chapter_notebooks/README.md` ↔ root README | Both say there is no `requirements.txt`, Drive is not a setup step, and notebooks are snippets. |
| `AGENTS.md` ↔ `manifest.json` | Unchanged. Validator role-table check passes. |
| `AGENTS.md` ↔ `tools/validate.py` | The keyword check now looks for "Do not load the entire PDF", which is the sentence in `AGENTS.md`. |
| `tools/validate.py` ↔ notebooks and PDF | The guard still fails the build if `.ipynb` or `.pdf` bytes differ from `origin/main`. This audit did not change those bytes. |
| Skill cards ↔ `.SKILL.md` copies | Validator companion check: identical. |
| Docs ↔ live APIs | README does not claim notebooks were executed against providers. Evidence map marks those runs unverified. Consistent. |
| License sentences ↔ tree | README says no `LICENSE` file. GitHub `licenseInfo` is null. Notebook headers that cite `LICENSE` are described as pointing at a missing file. Consistent. |
| Pattern map ↔ ontology | The mapping file uses manifest ids and does not invent `APD-NN` labels. README does not claim the stubs are the book. Consistent. |

## Validator after the documentation fix

`python3 tools/validate.py` on this branch: 26 passed, 2 failed, exit code 1.

Failures, both expected:

- executor walk-through 3006 tokens (budget 3000)
- worst role pair 3014 tokens (`tool-use` + `multi-agent`, patterns ref `tool-use`)

PDF and notebook bytes still match `origin/main`. The `AGENTS.md` phrase check passes.

## Remaining tension (intentional)

Placeholder notebooks still tell a reader to use Google Drive. The READMEs say that text is historical and that Drive is not required. That tension is documented in the correction log so the notebook bytes can stay frozen.

`BUDGET = 3000` still fails. The README states the failure. The constant was not changed.
