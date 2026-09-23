# 5. Dependency and dead-material report

Classifications: `ACTIVE`, `REFERENCE`, `HISTORICAL`, `GENERATED`, `DUPLICATE`, `ORPHANED`, `DEPRECATED`, `CANDIDATE_FOR_REMOVAL`.

Nothing was deleted.

## Runtime dependencies that are real

| Dependency | Where | Class | Notes |
| --- | --- | --- | --- |
| Python 3 standard library | `skills/*/examples/minimal.py` | ACTIVE | Sufficient for the 21 examples. Observed exit 0. |
| `tiktoken` | `tools/validate.py` | ACTIVE | Imported at runtime. Not pinned. Audit environment had 0.14.0. |
| `git` | `tools/validate.py` originals check | ACTIVE | Compares PDF and notebooks to `origin/main`. |
| Poppler `pdfinfo` / `pdftotext` | not a repo dependency | REFERENCE | Used by this audit and named in `ground-truth/README.md`. Not required to import skills. |

## Notebook imports (unpinned, not installed here)

Third-party roots seen by `ast.parse` across notebooks include: `langchain_openai`, `langchain_core`, `langchain`, `langchain_google_genai`, `langchain_community`, `langgraph`, `google` (`google.adk`, `google.genai`, `google.generativeai`), `crewai`, `openai`, `dotenv`, `fastmcp`, `openevolve`, `pydantic`, `requests`, `nest_asyncio`.

Class: `REFERENCE`. They are required only if someone chooses to execute that notebook. No version was verified. No `requirements.txt` was added.

`pandas`, `numpy`, and `matplotlib` were named by the old READMEs and were not the import set. Class of that instruction: removed from the docs. The packages themselves are not in the tree.

## Environment variables named in notebooks

`OPENAI_API_KEY`, `OPENAI_MODEL_NAME`, `GOOGLE_API_KEY`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_GENAI_USE_VERTEXAI`, `DATASTORE_ID`, `GOOGLE_CSE_ID`, `GOOGLE_CUSTOM_SEARCH_API_KEY`.

Class: `REFERENCE`. No values are stored, except the literal placeholders `YOUR_OPENAI_API_KEY` and `your_key_here`.

## File classes

| Item | Class | Why it stays |
| --- | --- | --- |
| `skills/**` | ACTIVE | Validator and `AGENTS.md` load them. Examples run. |
| `manifest.json`, `AGENTS.md`, `models/*` | ACTIVE | Navigation and checks. Model numbers are unverified. |
| PDF and `ground-truth/` | REFERENCE (canonical source) | Book bytes and extract. |
| `chapter_notebooks/Chapter_*.ipynb` | REFERENCE | Book-related snippets. Several are fragments or syntactically broken. Still the historical code mirror. |
| `chapter_notebooks/Chapter_*.SKILL.md` | GENERATED, DUPLICATE | Byte copies of skill cards. Validator requires them. `--sync` rewrites them. |
| Seven appendix placeholder ipynb files | HISTORICAL, DEPRECATED as instructions | Not the appendix text. `CANDIDATE_FOR_REMOVAL` only if a later decision accepts losing the acquisition note. Not removed here. |
| `Appendix_C_(Code).ipynb` | REFERENCE | Stored `NameError` outputs. The first cell says it is not runnable. |
| `Appendix_Pydantic.ipynb` | REFERENCE | Needs `pydantic`, which was not installed. |
| `chapter_notebooks/Chapter_01_Prompt_Chaining_(JSON_Example).ipynb` | REFERENCE | JSON literal, not a program. |
| `Chapter_10_MCP_*_init.ipynb` | REFERENCE | `from . import agent` fragments. Fail outside a package. |
| `Chapter_09_Adaptation_(OpenEvolve).ipynb` | REFERENCE | `path/to/` placeholders and top-level `await`. |
| Root README and chapter README | ACTIVE | Updated to match the tree. |
| `validation/audit/**` | ACTIVE | This audit. |

## Broken internal links (pre-audit, now removed from the root README)

- `CONTRIBUTING.md`
- `LICENSE`
- `book/Agentic_Design_Patterns_Complete.pdf`
- `requirements.txt`
- `chapter_notebooks/Chapter_01_Prompt_Chaining.ipynb`

No markdown link checker beyond path existence and the GitHub API was run. Skill files link to sibling `deep-dive.md` and `chapter_notebooks/Chapter_NN_*` globs; those globs match real files.

## Unreachable code

There is no application package with an import graph. "Unreachable" applies to notebook fragments that cannot run as scripts:

- Leading-indent ADK parallelization snippet
- `tools=[Google Search]` (invalid syntax)
- Prompt text stored in code cells (chapters 17 and 18)
- Agent Laboratory excerpt with a syntax error
- JSON-RPC examples stored in a Python code cell (chapter 15 sync/streaming)

Class: `REFERENCE` fragments, not dead modules. They were not deleted.

## Orphans

No source file was unreferenced after the README update. The placeholder notebooks are referenced from `chapter_notebooks/README.md` and this audit. `models/*.md` are referenced from `AGENTS.md`.

## Conflicting setup instructions

Before this audit the root README, the chapter README, and the notebooks disagreed (requirements file vs pandas vs per-notebook secrets vs Google Drive). The two READMEs now agree: no requirements file, no Drive step, skills are the offline executable path, notebooks are optional snippets. The placeholder notebooks still contain the old Drive text on purpose.
