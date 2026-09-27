# 6. Candidate pattern mappings

This repository's pattern vocabulary is the skill id list in `manifest.json` (chapters 1–21 of Gulli's book). There is no `APD-NN` ontology in the tree. The mappings below are proposals. They are not an acceptance of an external catalog.

`mapping_status` is `supported` only when this audit both read the symbols and observed them run. `candidate` means the filename, imports, or card text point at a pattern and runtime was not established. `disputed` means the file does not contain the pattern's behavior.

## Offline stubs (executed)

Validator result: all 21 `skills/<id>/examples/minimal.py` exit 0. The three below were read. The other 18 are `candidate` for fidelity to the chapter and `supported` only for "this file is the offline example the validator runs for that skill id."

### prompt-chaining

implementation:
  file: `skills/prompt-chaining/examples/minimal.py`
  symbols: `stage_extract`, `stage_transform`, `chain`, `llm`
candidate_pattern:
  pattern_id: `prompt-chaining`
evidence:
  - `chain` passes stage-1 text into stage-2
  - Stage prompts match the Chapter 1 card in `skills/prompt-chaining/SKILL.md`
  - Process exit 0 under `tools/validate.py`
mapping_status: supported
reasoning: The observable behavior is a two-step pipeline with a structured handoff, which is the pattern the card describes.
counterevidence:
  - `llm` is a regex stub, not a model call
  - The notebook `Chapter_01_Prompt_Chaining_(Code_Example).ipynb` was not executed

### tool-use

implementation:
  file: `skills/tool-use/examples/minimal.py`
  symbols: `tool_schemas`, `decide`, `run`, `get_stock_price`
candidate_pattern:
  pattern_id: `tool-use`
evidence:
  - Schemas are built from function signatures and docstrings
  - Unknown ticker returns a structured error rather than a raised string dumped as success
  - Exit 0
mapping_status: supported
reasoning: The file implements the card's "typed call, execute, return observation" loop.
counterevidence:
  - `decide` matches uppercase words; it does not call a model
  - Prices are constants

### mcp

implementation:
  file: `skills/mcp/examples/minimal.py`
  symbols: `ToyMCPServer.list_tools`, `ToyMCPServer.call_tool`, `MCPToolset`
candidate_pattern:
  pattern_id: `mcp`
evidence:
  - Tools are discovered from the server object
  - `tool_filter` hides `delete_everything`
  - Exit 0, stdout includes "blocked"
mapping_status: supported
reasoning: Discovery plus least-privilege filter is the behavior `skills/mcp/SKILL.md` describes.
counterevidence:
  - No MCP transport, no FastMCP process, no `localhost:8000`
  - `skills/mcp/references/deep-dive.md` shows a real server URL; that code was not run

## Notebooks (not executed against libraries)

For each chapter, the candidate pattern id is the manifest id for that chapter number. Evidence is the filename prefix `Chapter_NN_` plus imports where `ast.parse` succeeded. mapping_status: **candidate**. Counterevidence for the whole set: dependencies were not installed, and these files failed `ast.parse`:

| File | pattern_id | Why disputed as a running example |
| --- | --- | --- |
| `chapter_notebooks/Chapter_03_Parallelization_(Google_ADK).ipynb` | `parallelization` | Leading indent, `SyntaxError` |
| `chapter_notebooks/Chapter_14_Knowledge_Retrieval_(RAG_Google_Search).ipynb` | `rag` | `tools=[Google Search]` is invalid syntax |
| `chapter_notebooks/Chapter_15_Inter_Agent_(Sync_Streaming_Requests).ipynb` | `a2a` | JSON examples in a code cell, `SyntaxError` |
| `chapter_notebooks/Chapter_17_Reasoning_(CoT_Prompt).ipynb` | `reasoning-techniques` | Prompt prose, not Python |
| `chapter_notebooks/Chapter_17_Reasoning_(Self_Correction).ipynb` | `reasoning-techniques` | Prompt prose, not Python |
| `chapter_notebooks/Chapter_18_Guardrails_(LLM_as_Guardrail).ipynb` | `guardrails` | Prompt prose, not Python |
| `chapter_notebooks/Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb` | `exploration-discovery` | Excerpt does not parse |

Those seven remain **candidate** labels by filename and **disputed** as executable implementations.

`Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb` is a stronger candidate:

implementation:
  file: `chapter_notebooks/Chapter_19_Evaluation_(Basic_Response_Evaluation).ipynb`
  symbols: the single code cell (not split into named functions in-repo)
candidate_pattern:
  pattern_id: `evaluation-monitoring`
evidence:
  - Executed offline during this audit
  - Printed an accuracy line, a simulated latency, and token counts
mapping_status: candidate
reasoning: It performs local bookkeeping that resembles evaluation. The printed accuracy was 0.0. This audit did not compare the cell to the chapter's rubric.
counterevidence:
  - One successful exec is not a test suite
  - `skills/evaluation-monitoring/examples/minimal.py` is a different stub and was only covered by the validator's exit code

## Placeholders

implementation:
  file: `chapter_notebooks/Appendix_A_Advanced_Prompting_Techniques.ipynb` and the six sibling placeholders
  symbols: none (undefined `chapter_name`)
candidate_pattern:
  pattern_id: none
evidence:
  - Markdown says the notebook was not downloaded
  - Execution raises `NameError`
mapping_status: disputed
reasoning: There is no appendix implementation in these files. Appendix text is in the PDF.
counterevidence:
  - The Drive folder might still hold notebooks. That was not checked, and it would be external material.

## Generated copies

`chapter_notebooks/Chapter_*.SKILL.md` are not separate implementations. They are duplicates of `skills/<id>/SKILL.md`. Mapping them again would double-count the skill cards.
