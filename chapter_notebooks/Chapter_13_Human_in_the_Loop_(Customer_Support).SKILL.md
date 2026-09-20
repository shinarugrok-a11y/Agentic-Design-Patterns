---
name: human-in-the-loop
description: Use when actions are irreversible or need human judgment before proceeding. Do not use for low-risk reversible routine steps.
role: [safety]
chapter: 13
token_cost_estimate: 166
chains_with: [guardrails, exception-handling]
---

# Human-in-the-Loop

## When to use
- Irreversible actions (refunds, deletes, sends)
- Low-confidence or high-stakes decisions
- Policy requires human sign-off

## When NOT to use
- Low-risk reversible steps
- Latency forbids waiting
- Decision is fully audited automation

## Inputs
- Action proposal with diff/preview
- Approver + timeout policy

## Outputs
- Approved/rejected/blocked verdict
- Audit record

## Failure modes
- Rubber-stamping — show diff + risk, not just 'approve?'
- Stuck queues — set timeouts + escalation path
- No audit — log who approved what, when

## Minimal example
```python
ticket = propose(action, risk="high", preview=diff)
if approve(ticket, approver, timeout="10m"):
    execute(ticket)
else: escalate_or_block(ticket)
```

## Next skills
- If need automated policy gates too: load `guardrails`
- If need failure fallbacks: load `exception-handling`
