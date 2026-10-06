# Connectors (needs template)

DERIVED/operational, not from the book. List what a deployment *needs*, not what it has. Each need has a check the bot can run read-only. If a check fails or cannot run, the connector is BLOCKED: tell the owner what is missing and stop. Gate G5 in `templates/gates.md` applies.

The bot never:
- self-authenticates, starts an OAuth flow, or creates tokens;
- grants itself, or anyone else, shares, scopes or permissions;
- auto-sends mail or messages; it drafts, and a human sends or replies APPROVE (gate G2).

| need | why | env var(s) | check (read-only) | if missing |
|---|---|---|---|---|
| `<llm provider>` | model calls | `<LLM_API_KEY>` | variable is set and non-empty | BLOCKED: ask the owner to add it |
| `<mail, draft only>` | prepare replies | `<MAIL_TOKEN>` | can list drafts; no send scope requested | BLOCKED; never fall back to sending |
| `<calendar, read>` | find free time | `<CALENDAR_TOKEN>` | can list one event | BLOCKED |
| `<document store, read>` | RAG corpus | `<DOCS_TOKEN>` | can read one known file | BLOCKED |

Rows are placeholders. Replace `<...>` with generic names in your own deployment and keep real account names, hostnames and addresses out of the repository. Variable names go in `.env.example`; values never do.
