---
name: human-in-the-loop
description: Human confirmation at high stakes. Use for irreversible or ambiguous actions. Not for routine volume.
role: [safety]
chapter: 13
token_cost_estimate: 215
chains_with: [guardrails, exception-handling]
---

# Human-in-the-Loop

## When to use
- Action is irreversible (payment, delete, send).
- Low confidence or unclear policy.
- Regulation requires sign-off.

## When NOT to use
- High-volume routine decisions: set policy up front.
- Reversible, low-risk, in-policy actions.

## Inputs
- Proposed action + context
- Escalation channel

## Outputs
- Approved or rejected action
- Audit record

## Failure modes
- Over-escalation fatigues reviewers.
- Context lost at hand-off.
- Approval assumed on timeout or silence.

## Minimal example
```python
def escalate_to_human(issue_type: str) -> dict:
    return {"status": "pending_human", "issue": issue_type}
# act only on explicit APPROVE; silence/timeout -> denied (templates/gates.md G2)
```

## Next skills
- If high stakes must be defined by policy: load `guardrails`
- If the non-escalated path must recover alone: load `exception-handling`
