# 7. Security findings

No release, deploy, or push to `main` was done as part of the audit. Findings are for human review.

The repository has no application server, so many checklist items have no code to inspect.

| Check | Result |
| --- | --- |
| API keys in the tree | No live keys found. Placeholders only: `YOUR_OPENAI_API_KEY` in `Chapter_06_Planning_(Deep_Research_API).ipynb` (stored 401 output redacts it as `YOUR_OPE*******_KEY`) and `your_key_here` in `Chapter_19_Evaluation_(LLM_as_Judge).ipynb`. |
| `.env` exposure | No `.env` file in the tree or in `git log` filenames. `Chapter_11_Goal_Setting_(Iteration).ipynb` stores stdout `.env` from a commented `!ls .env` cell, so a Colab session once had a file by that name. The contents are not in git. |
| Hardcoded secrets | Working-tree scan for `sk-` + 20 alphanumerics, `AIza` keys, `AKIA` keys, and PEM private keys: no matches. `git log -S 'sk-'` hits the ground-truth add because the book text contains the letters `sk-` as a substring, not a key. |
| Authentication | No login implementation. Notebooks read provider keys from the environment when someone runs them. |
| Server-side authorization, user-id trust, data isolation, database rules | No server, database, Firebase, or Supabase. |
| Admin routes, debug mode, security headers, CORS | None. |
| Input validation, sanitization, uploads, injection, rate limits | No request handler. Skill examples accept in-process strings and return strings. |
| Frontend-provided user ids | No frontend. Notebooks use example ids such as `user_123` in source comments. |
| Git history secrets | No committed `.env`. Full binary PDF was not scanned for embedded secrets beyond `pdfinfo` (Encrypted: no, JavaScript: no). |
| Production error leakage | Notebook outputs store tracebacks (`ModuleNotFoundError`, `NameError`, OpenAI 401). Those are local files, not a service. |

## Finding S1 — Colab account metadata committed

Severity: low (identity metadata, not a credential).

Seven notebooks contain Colab `executionInfo.user.displayName` and numeric `userId` values:

- `chapter_notebooks/Appendix_C_(Code).ipynb`
- `chapter_notebooks/Chapter_05_Tool_Use_(LangChain).ipynb`
- `chapter_notebooks/Chapter_06_Planning_(Deep_Research_API).ipynb`
- `chapter_notebooks/Chapter_08_Memory_(LangChain_LangGraph).ipynb`
- `chapter_notebooks/Chapter_10_MCP_(Filesystem_Example_agent).ipynb`
- `chapter_notebooks/Chapter_11_Goal_Setting_(Iteration).ipynb`
- `chapter_notebooks/Chapter_15_Inter_Agent_(A2A).ipynb`

Display names observed: Antonio Gulli (11 occurrences) and Mahtab Syed (2). Both names also appear in the book's acknowledgment, so the names are already public in the PDF. The numeric Colab user ids are not in the acknowledgment. This audit does not repeat those numbers. They remain in the ipynb JSON and in git history. Notebooks were not rewritten.

## Finding S2 — Filesystem MCP sample creates a directory from `__file__`

Severity: informational.

`Chapter_10_MCP_(Filesystem_Example_agent).ipynb` sets `TARGET_FOLDER_PATH` from `os.path.dirname(os.path.abspath(__file__))` and calls `os.makedirs`. In a notebook `__file__` is often unset. The stored output is `ModuleNotFoundError: No module named 'google.adk'`, so this audit did not observe a directory being created. If the imports were installed, the snippet would create `mcp_managed_files` beside the process. It is a sample, not a service.

## Finding S3 — Placeholder key was sent to a provider in a past session

Severity: informational.

`Chapter_06_Planning_(Deep_Research_API).ipynb` stores an OpenAI `AuthenticationError` for the placeholder key. That shows a past run contacted `api.openai.com` with a non-secret placeholder. This audit did not repeat that call.

## Finding S4 — No license file beside code that tells readers to look for one

Severity: legal/process, not a secret.

Headers in three notebooks say the code is MIT and cite `LICENSE`. The file is absent. See the correction log. Do not treat the header as a grant stored in this repository.

## Items with nothing to flag

No admin backdoor, no CORS configuration, no SQL string, no upload endpoint, and no rate-limiter gap, because those components are not in the repository.
