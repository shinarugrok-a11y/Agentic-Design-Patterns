---
name: human-in-the-loop
description: Human confirmation at high stakes. Use for irreversible or ambiguous actions. Not for routine volume.
role: [safety]
chapter: 13
token_cost_estimate: 231
chains_with: [guardrails, exception-handling]
---

# Human-in-the-Loop

## When to use
- Action is irreversible (payment, delete, send).
- Low confidence or unclear policy.
- Regulation requires sign-off.

## When NOT to use
- High-volume routine decisions.
- No human is available in time.

## Inputs
- Proposed action + context
- Escalation channel

## Outputs
- Approved or rejected action
- Audit record

## Failure modes
- Over-escalation fatigues reviewers.
- Context lost at hand-off.
- Approval assumed on timeout.

## Minimal example
```python
def escalate_to_human(issue_type: str) -> dict:
    """Escalate refunds, threats or unclear policy to a person."""
    return {"status": "escalated", "issue": issue_type}
agent = LlmAgent(name="support", tools=[troubleshoot, escalate_to_human],
    instruction="If unsure or asked for a refund, escalate.")
```

## Next skills
- If high stakes must be defined by policy: load `guardrails`
- If the non-escalated path must recover alone: load `exception-handling`
