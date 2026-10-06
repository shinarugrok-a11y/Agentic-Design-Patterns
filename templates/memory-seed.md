# Memory seed (template)

DERIVED/operational. The `user:` scope comes from the book's ADK state prefixes (SOURCE, GT:L5227; see `skills/memory-management`); the rest is ours. Placeholders only; fill a copy outside this repository.

```yaml
user:preferences:
  delivery_format: <e.g. "summary first, then detail">
  length: <short | medium | long>
  tone: <e.g. "plain, no emojis">
user:shorthand:
  <abbreviation>: <meaning>
user:do_not_store: [secrets, credentials, health, payment details]
```

Rules:
- Seed only `user:` preferences and shorthand. Task state goes in `temp:` and is dropped after the task.
- Never seed secrets, tokens, addresses or account names (gate G4).
- A preference never overrides a gate in `templates/gates.md`.
