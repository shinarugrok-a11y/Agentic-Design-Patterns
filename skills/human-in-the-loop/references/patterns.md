# Human-in-the-Loop — patterns (Ch 13)

## Pattern
1. Define escalation triggers (refund, threat, low confidence).
2. Expose escalation as a tool the agent can call.
3. Hand off full context; status `pending_human` until a reply.
4. Execute only on explicit APPROVE; anything else denies.

## Prompt template
```
You are a support agent. Try to resolve the issue with troubleshoot_issue.
If the user asks for a refund, threatens to cancel, or policy is unclear,
call escalate_to_human with the issue type and stop.
```

## Key APIs
- ADK (book): `Agent(tools=[troubleshoot_issue, create_ticket, escalate_to_human])`, rules in `instruction`.
- The book's `escalate_to_human` is a stub: no human gate.
- Confirmation gate: `propose -> pending_human -> APPROVE -> execute`.

## Pitfalls -> fixes
- Over-escalation -> tighten triggers, sample audits.
- Lost context -> include transcript in the handoff.
- Timeout = approval -> default to deny.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_13_*`.
