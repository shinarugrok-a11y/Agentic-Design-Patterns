---
name: human-in-the-loop
description: Escalate, confirm or collect feedback from a human at defined points. Insert a human checkpoint when an action is high-stakes, ambiguous, irreversible or outside the agent's confidence. Do not use for high-volume routine decisions where human review cannot scale.
role: [safety]
chapter: 13
token_cost_estimate: 340
chains_with: [guardrails, exception-handling, evaluation-monitoring]
---

# Human-in-the-Loop

## When to use
- Irreversible actions (payments, deletes, sends).
- Low-confidence or emotionally charged cases.
- Policy requires human sign-off (legal, medical, finance).
- Human labels/feedback improve the agent later.

## When NOT to use
- Thousands of routine decisions per minute.
- Human has no more context than the agent.
- Automated fallback suffices: use `exception-handling`.

## Inputs
- Escalation policy (when to hand off)
- Escalation tool/channel
- Customer/context state for the human

## Outputs
- Escalated case with context
- Human decision fed back
- Audit trail

## Failure modes
- Escalation criteria too broad: everything is escalated.
- Handoff loses context; human restarts from zero.
- No timeout; agent blocks forever waiting.
- Confirmation prompt is ambiguous; user approves the wrong action.

## Minimal example
```python
def escalate_to_human(issue_type: str) -> dict:
    return {"status": "success", "message": f"Escalated {issue_type}"}
support = Agent(instruction="""Troubleshoot -> create_ticket if unresolved.
For complex issues beyond basic steps: escalate_to_human.""",
    tools=[troubleshoot_issue, create_ticket, escalate_to_human])
# before_model_callback can inject state["customer_info"] for personalisation
```

## Next skills
- If inputs must be screened before the agent acts: load `guardrails`
- If failure can be handled automatically: load `exception-handling`
- If human feedback should be measured: load `evaluation-monitoring`
