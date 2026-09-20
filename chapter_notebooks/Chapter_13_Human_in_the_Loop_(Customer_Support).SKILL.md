---
name: human-in-the-loop
description: Pause for human judgment on high-stakes or ambiguous steps. Use before irreversible actions. Do NOT use to rubber-stamp every token.
role: [safety]
chapter: 13
token_cost_estimate: 234
chains_with: [guardrails-safety, exception-handling]
---

# Human-in-the-Loop

## When to use
- Irreversible, legal, medical, or financial actions
- Ambiguous cases after automated troubleshooting
- Approval, override, or personalization from a person

## When NOT to use
- High-volume, low-risk replies
- A deterministic policy filter is enough (load `guardrails-safety`)
- You only needed a retry (load `exception-handling`)

## Inputs
- Support/agent state (history, tier)
- `escalate_to_human` / approval gate
- Human response

## Outputs
- Ticket / handoff
- Action taken only after confirmation

## Failure modes
- Missing escalate tool
- HITL on every message
- Personalization callback returns non-None and aborts

## Minimal example
```python
# after troubleshoot/create_ticket, complex cases:
escalate_to_human(issue, context)
# Muse/Sentinel: never irreversible action without confirmation
```

## Next skills
- If the gate is automated policy: load `guardrails-safety`
- If the issue is a tool crash: load `exception-handling`
