---
name: exception-handling
description: Detect, retry, fall back, escalate. Use around anything that can fail. Not for deterministic errors.
role: [safety]
chapter: 12
token_cost_estimate: 227
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
primary  = LlmAgent(name="primary", tools=[precise_location], output_key="loc")
fallback = LlmAgent(name="fallback", tools=[general_area],
    instruction="Only if {loc} is an error, call general_area")
root = SequentialAgent(sub_agents=[primary, fallback, responder])
```

## Next skills
- If recovery needs a person: load `human-in-the-loop`
- If bad inputs should be blocked first: load `guardrails`
