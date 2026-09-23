# 4. Correction log

Each row is a substantive change or an explicit decision to leave a false claim in its original file.

## Corrected in the root README

original_claim: The PDF lives at `book/Agentic_Design_Patterns_Complete.pdf` and is 424 pages, with part lengths 103, 61, 34, 114, and 74.
location: `README.md` (pre-audit structure and table of contents)
classification: INCORRECT
evidence: PDF is at repository root. `pdfinfo` Pages: 458. Part lengths were not reproduced.
action: corrected
replacement: Root path and 458-page `pdfinfo` result. Part marketing lengths removed.
reason: The public contract has to name the file that exists and the page count that was measured.

original_claim: `pip install -r requirements.txt` and `pip install pandas numpy matplotlib openai langchain`, then open `Chapter_01_Prompt_Chaining.ipynb`.
location: `README.md` Getting Started
classification: INCORRECT
evidence: Those paths and that dependency set are absent. Chapter 1 filenames differ.
action: corrected
replacement: Install `tiktoken` to run `tools/validate.py`. Notebook use points at `chapter_notebooks/README.md` and does not invent pins.
reason: A requirements file was not created, because the correct pin set cannot be established from the snippets.

original_claim: Clone `https://github.com/evoiz/Agentic-Design-Patterns.git`. File issues and discussions there. Shields use that repo name. Code is MIT via `LICENSE`. See `CONTRIBUTING.md`.
location: `README.md`
classification: INCORRECT for this repository
evidence: `origin` is `shinarugrok-a11y/Agentic-Design-Patterns`. evoiz `main` is `e11e6fb`. `has_issues` and `has_discussions` are false here. `licenseInfo` is null. `CONTRIBUTING.md` is absent.
action: corrected
replacement: Clone URL for this repository. evoiz described as the historical tip at `e11e6fb`. License and contributing files described as absent. Issues/discussions described as disabled.
reason: Setup and license statements were operationally false.

original_claim: Google Drive is an official way to get the materials, and the repository is the complete runnable companion.
location: `README.md` resources and "About"
classification: EXTERNAL/HISTORICAL CONTEXT mixed with over-claim
evidence: Drive URL exists only as a pointer from placeholder notebooks. Skills and the PDF are already in git.
action: corrected
replacement: Drive is named as a historical pointer, not a setup step. Status table separates PDF, extract, skills, notebooks, and audit.
reason: Readers were being sent off-repo for files the PDF already contains, and told the notebooks were complete.

## Corrected in `chapter_notebooks/README.md`

original_claim: "All 21 chapters have complete, runnable code examples — 58 notebooks."
location: `chapter_notebooks/README.md` About
classification: INCORRECT
evidence: 65 ipynb, 7 placeholders, 7 syntax failures, stored error outputs. Inventory in `notebook-inventory.json`.
action: corrected
replacement: Counts, placeholder behavior (`NameError` on `chapter_name`), syntax-invalid file list, and the one notebook executed offline (Chapter 19 basic evaluation).
reason: The filename index was already accurate and was kept. The summary sentence was not.

original_claim: Common dependencies are pandas, numpy, and matplotlib. Google Drive and a Google Doc are the sources to use.
location: `chapter_notebooks/README.md` Requirements and Sources
classification: UNSUPPORTED and EXTERNAL/HISTORICAL CONTEXT
evidence: Import set in the inventory. No requirements file.
action: corrected
replacement: Jupyter optional. Per-notebook imports. Drive and the Google Doc labeled as external pointers, not setup.
reason: Same as the root README. No pin file was invented.

## Corrected in `tools/validate.py`

original_claim: `AGENTS.md` must contain the substring "Do not read the PDF".
location: `tools/validate.py` keyword loop
classification: STALE
evidence: `AGENTS.md` says "Do not load the entire PDF during normal execution." Validator FAIL before the edit.
action: corrected
replacement: The check looks for "Do not load the entire PDF".
reason: The test disagreed with the current agent guide. The guide was left as written.

original_claim: Any README change versus `origin/main` fails validation, together with PDF and notebook changes.
location: `tools/validate.py` "originals untouched"
classification: STALE once README accuracy is required
evidence: This audit's task is to correct the README. PDF and `.ipynb` bytes were not edited.
action: corrected
replacement: The guard is "PDF and notebooks unmodified vs origin/main".
reason: Freezing the README would make the accuracy pass fail a check that was meant to protect book artifacts.

original_claim: The docstring stated the 3,000-token gate as what the tool guarantees.
location: `tools/validate.py` module docstring
classification: INCORRECT as a description of measured results
evidence: Walk-through 3,006; worst pair 3,014.
action: corrected
replacement: Docstring states the measured overrun and says not to raise `BUDGET` to hide it. `BUDGET` remains 3000, so the two simulation checks still fail.
reason: Silencing the gate would hide a contradicted invariant. Shrinking skill text to pass it was not justified by a book defect.

## Retained as historical (not edited)

original_claim: Visit the Google Drive folder, download the notebook, replace this file.
location: seven `chapter_notebooks/Appendix_*.ipynb` files
classification: DEPRECATED as instructions; historical as provenance
evidence: Placeholder body; `NameError` on execution; appendix text exists in the PDF.
action: retained_as_historical
replacement: Called out in both READMEs and in this log. Notebook bytes unchanged so the acquisition note stays with the file.
reason: Deleting them would hide how those files entered the tree. Editing ipynb JSON was avoided because `tools/validate.py` treats notebook bytes as frozen.

original_claim: `Copyright (c) 2025 Marco Fago` / MIT / see `LICENSE`.
location: `Chapter_02_Routing_(Google_ADK).ipynb`, `Chapter_02_Routing_(LangGraph).ipynb`, `Chapter_18_Guardrails_(Practical_Examples).ipynb`, and the same headers inside the book extract
classification: The header is a claim; the license file is INCORRECT / absent
evidence: No `LICENSE` in git. GitHub license API is null. The book acknowledgment thanks Marco Fago for code.
action: retained_as_historical
replacement: README states that no license file exists and that those headers point at a missing file. No `LICENSE` was added.
reason: Adding MIT text would invent a legal grant that is not in the repository.

original_claim: Colab `executionInfo.user` display names and numeric user ids, and a cell output that lists `.env`.
location: seven notebooks listed in `07-security-findings.md`
classification: security finding, not a false technical claim
evidence: JSON metadata in the ipynb files
action: retained_as_historical
replacement: Recorded as a finding. Not stripped, because the values are already in git history and the notebook guard forbids silent ipynb edits.
reason: Redaction in the working tree would not remove history, and would touch frozen notebooks.

## Not corrected because the right replacement is unknown

original_claim: Model profiles' context windows and costs.
location: `models/fable-5-1.md`, `models/grok-4-6.md`, `models/muse.md`
classification: UNSUPPORTED
evidence: No measurement in the repo.
action: retained
replacement: none
reason: status: unverified. README limitations say so.

original_claim: 3,000-token budget should pass.
location: `tools/validate.py` `BUDGET`
classification: contradicted by measurement
evidence: 3,006 and 3,014
action: retained as a failing check
replacement: none
reason: Whether to edit skill prose or change the budget is a product decision, not an established fact.
