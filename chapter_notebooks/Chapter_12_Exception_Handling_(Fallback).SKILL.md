---
name: exception-handling
description: Detect, retry, fall back, escalate. Use around anything that can fail. Not for deterministic errors.
role: [safety]
chapter: 12
token_cost_estimate: 230
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
out = primary_tool(args)              # expected failure -> {"status": "error"}
if out.get("status") == "error":
    out = fallback_tool(args)         # degrade instead of crashing
reply = respond(out) if out.get("status") != "error" else "Tried primary and fallback; both failed."
```

## Next skills
- If recovery needs a person: load `human-in-the-loop`
- If bad inputs should be blocked first: load `guardrails`
