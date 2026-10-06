# Identity / profile (template)

DERIVED/operational, not from the book. Placeholders only: fill a copy in your own deployment, never in this repository. Runtime-class guidance lives in `models/`; this file is about the person or team the agent works for.

```yaml
agent_name: <agent name>
works_for: <role, e.g. "a small product team">   # no real names or emails here
runtime: <runtime and model, or "unknown">
profile: <one models/*.md file>
languages: [<language>]
timezone: <timezone>
approver: <who replies APPROVE for gate G2>        # a role, not a personal address
delivery_format: <e.g. "short bullet summary, then details">
escalate_when: [<condition>]
out_of_scope: [<task the agent must decline>]
```

Rules: gates in `templates/gates.md` override anything here. Unknown fields stay `<...>` and count as unknown.
