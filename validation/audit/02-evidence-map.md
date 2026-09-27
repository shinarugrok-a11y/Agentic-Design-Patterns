# 2. Evidence map

Shape: repository → directory → file → symbol or command → behavior. Status values: `verified`, `partially_verified`, `unverified`, `contradicted`, `stale`, `broken`, `deprecated`.

`verified` is used only where a command or file inspection established the claim during this audit.

## Book bytes

claim: The book PDF in this repository has 458 pages.
evidence: `pdfinfo` (Poppler 24.02.0) printed `Pages: 458`. PDF objects: `/Type /Page` 459 minus `/Type /Pages` 1. `pdftotext` form-feed split: 459 segments, last empty.
file: `Agentic_Design_Patterns_Complete.pdf`
symbol: n/a
dependencies: Poppler
tests: `pdfinfo` during this audit
runtime_behavior: file opens as an unencrypted PDF 1.4, letter size, producer PyPDF2
confidence: high for page count of this file
status: verified

claim: The README figure "424 pages" and the part subtotals (103, 61, 34, 114, 74) describe this PDF.
evidence: 458 ≠ 424. Printed page numbers inside the extract restart per chapter (Chapter 1 starts at printed page 1 on PDF page 21), so those subtotals are not a single page sequence in the file.
file: `README.md` (pre-audit), `ground-truth/agentic_design_patterns.txt`
symbol: n/a
dependencies: none
tests: page index of chapter titles from the form-feed split (Chapter 1 PDF page 21, Chapter 8 page 130, Chapter 12 page 194, Chapter 15 page 229, Appendix A page 347, glossary page 431)
runtime_behavior: n/a
confidence: high that 424 is not the page count of this file; the origin of the number 424 was not found in the extract
status: contradicted

claim: `ground-truth/agentic_design_patterns.txt` is `pdftotext -layout` of the PDF.
evidence: Fresh `pdftotext -layout` with Poppler 24.02.0 produced 17,659 lines. 17 lines differ, in four clusters (lines 3078–3081, 7169–7173, 7304–7307, 7320–7323), all emoji glyph wrapping. Same line count. File sizes 882,642 (stored) vs 882,701 (fresh).
file: `ground-truth/agentic_design_patterns.txt`, `ground-truth/README.md`
symbol: n/a
dependencies: Poppler version
tests: byte compare during this audit
runtime_behavior: n/a
confidence: high that the file is that class of extract; the 17-line delta is version-sensitive layout
status: partially_verified

claim: Royalties are donated to Save the Children.
evidence: Extract line 112: "All my royalties are donated to Save the Children."
file: `ground-truth/agentic_design_patterns.txt`
symbol: n/a
dependencies: none
tests: search
runtime_behavior: n/a
confidence: high that the book text says this; payment records were not checked
status: verified as a statement in the book text

## Skill library

claim: There are 21 skills, chapters 1–21, each with SKILL.md, two reference files, and an offline example, and frontmatter matches `manifest.json`.
evidence: `python3 tools/validate.py` PASS lines for manifest, files, frontmatter, and "exactly 21 skill directories".
file: `tools/validate.py`, `manifest.json`, `skills/*`
symbol: `check()` results
dependencies: `tiktoken`
tests: validator, this audit
runtime_behavior: examples print and exit 0
confidence: high
status: verified

claim: `AGENTS.md` + `manifest.json` + any two same-role skills + one `patterns.md` stays under 3,000 cl100k tokens.
evidence: Validator output: base 2,159; executor walk-through `prompt-chaining` + `tool-use` + `tool-use` patterns = 3,006; worst pair 3,014 (`executor` `tool-use`+`multi-agent` ref=`tool-use`); 119 of 136 combinations under budget.
file: `tools/validate.py` (`BUDGET = 3000`)
symbol: simulation block
dependencies: `tiktoken` `cl100k_base`
tests: validator FAIL on both simulation checks
runtime_behavior: process exit 1
confidence: high
status: contradicted

claim: `AGENTS.md` contains the instruction "Do not read the PDF".
evidence: Current text is "Do not load the entire PDF during normal execution." The validator looked for the shorter phrase and failed before this audit. The check was updated to the current sentence.
file: `AGENTS.md`, `tools/validate.py`
symbol: keyword loop
dependencies: none
tests: validator FAIL before the correction; PASS for the updated phrase after
runtime_behavior: n/a
confidence: high
status: stale (corrected in the validator)

claim: `skills/prompt-chaining/examples/minimal.py` implements a two-stage extract-then-JSON pipeline offline.
evidence: File read. `chain()` calls `stage_extract` then `stage_transform`. Stub `llm()` branches on prompt prefix. Validator executed it with exit 0.
file: `skills/prompt-chaining/examples/minimal.py`
symbol: `chain`, `stage_extract`, `stage_transform`, `llm`
dependencies: `json`, `re`
tests: validator example run
runtime_behavior: deterministic regex extraction of a fixed laptop sentence into JSON keys `cpu`, `memory`, `storage`
confidence: high for this stub; it does not call a model
status: verified

claim: `skills/tool-use/examples/minimal.py` runs a function-calling loop.
evidence: `decide()` is a keyword stub, not a model. `run()` executes `get_stock_price` and returns structured success or error. Validator exit 0.
file: `skills/tool-use/examples/minimal.py`
symbol: `decide`, `run`, `get_stock_price`
dependencies: stdlib
tests: validator
runtime_behavior: `AAPL` returns a hard-coded price; `ZZZZ` returns `status=error`
confidence: high for the stub
status: verified

claim: `skills/mcp/examples/minimal.py` speaks MCP to a server.
evidence: `ToyMCPServer` and `MCPToolset` are in-process classes. `tool_filter=["greet"]` blocks `delete_everything` via `AssertionError`. No socket.
file: `skills/mcp/examples/minimal.py`
symbol: `ToyMCPServer`, `MCPToolset`
dependencies: stdlib
tests: validator
runtime_behavior: prints discovered tools, greeting, then "blocked"
confidence: high that the stub runs; the MCP protocol itself is not on the wire
status: partially_verified

The other 18 `examples/minimal.py` files exited 0 in the same validator run. Their individual stdout was not transcribed in this map. Status for "they run offline": **verified**. Status for "they faithfully implement the book chapter": **unverified** beyond the three files read in full (`prompt-chaining`, `tool-use`, `mcp`).

## Notebooks

claim: All 21 chapters have complete, runnable notebooks (58 notebooks).
evidence: 56 chapter ipynb files + 9 appendix files = 65. Seven appendices are placeholders. Seven files fail `ast.parse`. Five files store error outputs. See [notebook-inventory.json](notebook-inventory.json).
file: `chapter_notebooks/`
symbol: n/a
dependencies: many third-party, unpinned
tests: `ast.parse`; stdlib execution attempt
runtime_behavior: placeholders raise `NameError: name 'chapter_name' is not defined`
confidence: high
status: contradicted

claim: `Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb` can run without third-party packages.
evidence: Executed in-process during the audit. Imports `time` only.
file: `chapter_notebooks/Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb`
symbol: notebook cells (single code cell)
dependencies: stdlib `time`
tests: direct `exec` of the cell
runtime_behavior: printed `Response accuracy: 0.0`, a simulated tool latency near 150 ms, and token-count lines. Metric correctness against the book was not judged.
confidence: high that it runs; medium that the printed accuracy is a meaningful score
status: partially_verified

claim: Chapter notebooks are safe to follow as setup instructions for Google Drive.
evidence: Placeholder markdown tells the reader to visit `https://drive.google.com/drive/u/0/folders/1Y3U3IrYCiJ3E45Z8okR5eCg7OPnWQtPV`, download a notebook, and replace the file. No download script exists in the repo. The appendix prose is already in the PDF. Drive access was not attempted.
file: `chapter_notebooks/Appendix_*.ipynb` (seven files)
symbol: markdown cell 0, code cell 1
dependencies: Google account, external folder
tests: execution raises `NameError`
runtime_behavior: local failure; no network call in the placeholder code
confidence: high that Drive is not required for the files that are already here
status: deprecated as an operational step; retained in the notebook files as historical text

## Identity of the git remote

claim: Contributors should clone `https://github.com/evoiz/Agentic-Design-Patterns.git` to get this tree.
evidence: This environment's `origin` is `github.com/shinarugrok-a11y/Agentic-Design-Patterns`. `gh repo view` shows evoiz `main` = `e11e6fb` (2026-07-24). This HEAD is `ed9027e`, which has that commit as an ancestor and adds `skills/`, `ground-truth/`, and later README edits.
file: `README.md` (pre-audit), `.git`
symbol: n/a
dependencies: GitHub
tests: `gh repo view`, `git log`
runtime_behavior: n/a
confidence: high
status: contradicted for this repository; the evoiz URL remains the historical upstream tip

## Trace example (documentation → code → test)

DOCUMENTATION CLAIM: skill examples run offline (`tools/validate.py` docstring).
IMPLEMENTATION LOCATION: `skills/*/examples/minimal.py`, invoked by `subprocess.run` in `tools/validate.py`.
DEPENDENCIES: Python standard library; validator itself needs `tiktoken`.
TEST COVERAGE: the validator is the test. There is no separate `tests/` tree.
OBSERVED BEHAVIOR: "all examples/minimal.py run offline with exit 0" PASS.
VERDICT: verified.

DOCUMENTATION CLAIM (pre-audit README): `pip install -r requirements.txt` then run `Chapter_01_Prompt_Chaining.ipynb`.
IMPLEMENTATION LOCATION: no `requirements.txt`. Chapter 1 files are `Chapter_01_Prompt_Chaining_(Code_Example).ipynb` (LangChain imports, not executed) and `Chapter_01_Prompt_Chaining_(JSON_Example).ipynb` (a JSON literal).
DEPENDENCIES: missing pin file; code example imports `langchain_openai`.
TEST COVERAGE: none for notebooks.
OBSERVED BEHAVIOR: JSON file exec produces no output. Code example was not run (third-party import).
VERDICT: contradicted.
