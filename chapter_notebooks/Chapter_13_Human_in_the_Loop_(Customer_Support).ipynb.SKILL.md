---
name: human-in-the-loop
description: Escalate to a human on low confidence or high stakes.
role: [safety]
chapter: 13
token_cost_estimate: 220
chains_with: [guardrails-safety, goal-setting]
---

# Human-in-the-Loop

## When to use
- Action is irreversible, costly, or policy-sensitive.
- Confidence is low or issue type is unknown.
- Ticket/approval trail is required.

## When NOT to use
- Low-risk reversible step; autonomy is faster.
- No human is actually available to respond.

## Inputs
- Escalation triggers
- Human channel: ticket, approval callback, handoff

## Outputs
- Human decision or approval + audit trail

## Failure modes
- Trigger threshold mis-tuned; everything or nothing escalates.
- Escalation without context forces humans to re-investigate.
- Blocked agent with no timeout while awaiting human.

## Minimal example
```python
if confidence < 0.7 or issue_type in ("billing", "legal"):
    escalate_to_human(issue)  # ticket + callback
else:
    auto_resolve(issue)
```

## Next skills
- If escalation policy must be enforced automatically: load `guardrails-safety`
- If human feedback becomes acceptance goals: load `goal-setting`
