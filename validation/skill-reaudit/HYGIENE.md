# Hygiene pass (branch `cursor/agent-standup-path-eada`)

## Secret scan

These commands were run over every commit on this branch that is not on
`origin/main`, and over the working tree at HEAD.

```bash
git log -p origin/main..HEAD | grep -iE 'api[_-]?key|secret|token|password|BEGIN .*PRIVATE'
```
- 724 matching lines. 647 of them contain only "token", meaning token
  counts and budgets.
- The other 77 were reviewed by hand. All are one of: env-var names
  (`OPENAI_API_KEY`, `GOOGLE_API_KEY`, `GOOGLE_CLIENT_SECRET`, …), angle-bracket
  placeholders (`Bearer <OPENROUTER_API_KEY>`), the book's
  `"authentication": {"schemes": ["apiKey"]}`, function parameters
  (`client_secret=client_secret`), prose about secrets, or the earlier
  audit's notes on the notebook placeholders `YOUR_OPENAI_API_KEY` and
  `your_key_here`.
- No credential values found.

Key-shape regex, over added lines and the HEAD tree (PDF excluded):

```bash
RE='sk-[A-Za-z0-9_-]{20,}|sk-or-v1-[a-f0-9]{20,}|AIza[0-9A-Za-z_-]{35}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{20,}|xox[abprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}'
git log -p origin/main..HEAD | grep -E '^\+' | grep -oE "$RE"
git grep -nIE "$RE" HEAD -- . ':!*.pdf'
git log --name-only --format= origin/main..HEAD | grep -iE '(^|/)\.env|\.pem$|\.key$|credentials'
```
All three returned no matches. `.gitignore` now excludes `.env`,
`__pycache__/` and `*.pyc`.

## Credentials in examples

- None of the 21 `examples/minimal.py` files reads or embeds a credential.
  All run offline.
- Deep-dive code that needs a key or id reads it from the environment, or
  shows an angle-bracket placeholder with a warning. Examples: the OpenRouter
  `<OPENROUTER_API_KEY>` block in `resource-aware-optimization`, and
  `DATASTORE_ID` in `tool-use`.
- The `tool-use` block now checks `DATASTORE_ID` and exits with a clear
  message when it is unset. That mirrors the book (GT:L3607, L3688).

## Input validation and error leakage

- `tool-use/minimal.py`:
  - New `observe()` rejects unknown tools and malformed arguments.
  - `get_stock_price` validates the ticker.
  - Unexpected exceptions now return a generic message (previously
    unknown tools crashed with `KeyError`).
  - New asserts cover these paths.
- `mcp/minimal.py`:
  - The least-privilege check was an `assert`, which `python -O` removes.
    It now raises `PermissionError`, and the demo exits non-zero if the
    filtered tool runs.
  - `greet` validates its input.
- `a2a/minimal.py`:
  - `send_task` validates the text and the card URL.
  - `pick_skill` returns None on no match, instead of always delegating.
  - The `input-required` branch never fired: it was a substring check, and
    "forecast" contains "for". It now uses a word check.
  - The follow-up reply reuses the same task id, as the deep-dive says.
    Asserted.
- `guardrails/minimal.py`: `handle` rejects empty, non-string or oversized
  input.
- `human-in-the-loop/minimal.py`: covered earlier on this branch. It
  defaults to `pending_human`, denies on timeout, silence or non-APPROVE,
  and validates `Action` fields.

## Instructions that weaken safety

```bash
grep -rniE "skip (the )?(auth|confirm|guardrail)|bypass|disable (the )?(guardrail|safety|auth)|without (asking|confirm)|auto-?approve|--no-verify|dangerously" skills/ STANDUP.md models/ AGENTS.md README.md docs/
```
- Every hit either forbids skipping or describes an attack to defend
  against.
- One phrase could be misread: "sample-audit the auto-approved tail" in
  `human-in-the-loop/references/deep-dive.md`. It was rewritten to say that
  volume must never turn a required approval into an automatic one.
- AGENTS.md, STANDUP.md (self-check 3 and 4) and both new profiles say
  explicitly: never skip auth, confirmation or guardrails, and silence or a
  timeout means denied.
