---
name: exception-handling
description: Detect failures and recover via retry, fallback, or degrade.
role: [safety]
chapter: 12
token_cost_estimate: 206
chains_with: [tool-use, guardrails-safety]
---

# Exception Handling and Recovery

## When to use
- Agent calls flaky models, tools, or networks.
- Define retry -> fallback agent -> degraded response order.
- Partial failure must not kill the whole workflow.

## When NOT to use
- Failure is deterministic.
- Silent fallback hides errors users must see.

## Inputs
- Primary path + fallback chain + retry policy
- Error taxonomy

## Outputs
- Recovered result or explicit degraded response

## Failure modes
- Retrying fatal errors wastes budget; classify first.
- Fallback silently returns worse answers unflagged.
- No circuit breaker; cascading retries overload services.

## Minimal example
```python
try:
    out = primary(q)
except TransientError:
    out = fallback_agent(q)  # SequentialAgent primary->fallback
flag_degraded(out)
```

## Next skills
- If failures come from tool calls: load `tool-use`
- If failures must be blocked by policy: load `guardrails-safety`
