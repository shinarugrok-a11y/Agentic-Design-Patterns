---
name: exception-handling
description: Detect, retry, fall back, escalate. Use around anything that can fail. Not for deterministic errors.
role: [safety]
chapter: 12
token_cost_estimate: 233
chains_with: [human-in-the-loop, guardrails]
---

# Exception Handling and Recovery

## When to use
- Tools or APIs can time out or rate-limit.
- A fallback path exists.
- Failures must be reported.

## When NOT to use
- Error is deterministic (bad args): fix the call.
- Failure needs a human: use `human-in-the-loop`.

## Inputs
- Primary action
- Fallback + retry policy

## Outputs
- Result or fallback result
- Structured error report

## Failure modes
- Fallback runs even on success.
- Retrying a deterministic error.
- Error message returned as normal data.

## Minimal example
```python
primary  = Agent(name="primary", tools=[get_precise_location_info])
fallback = Agent(name="fallback", tools=[get_general_area_info],
    instruction='If state["primary_location_failed"]: get_general_area_info')
root = SequentialAgent(sub_agents=[primary, fallback, responder])
# the book never sets the flag; your tool must
```

## Next skills
- If recovery needs a person: load `human-in-the-loop`
- If bad inputs should be blocked first: load `guardrails`
