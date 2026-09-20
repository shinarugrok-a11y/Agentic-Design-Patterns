---
name: exception-handling-and-recovery
description: Detect, retry, fall back, escalate. Detect tool and API failures, then retry, fall back, degrade, or escalate under an explicit policy. Skip it for pure in-context reasoning with no external calls or side effects.
role: [safety]
chapter: 12
token_cost_estimate: 360
chains_with: [human-in-the-loop, tool-use, resource-aware-optimization]
---

# Exception Handling and Recovery

## When to use
- Agent calls tools, APIs, or networks
- Partial failure must not abort the run
- Reliability is an explicit requirement

## When NOT to use
- Pure in-context reasoning with no side effects
- Failure is cheap, visible, and acceptable
- The error is non-transient - do not retry it

## Inputs
- operation to guard
- retry and timeout policy
- fallback path or escalation target

## Outputs
- result or typed error
- recovery action taken
- diagnostic log entry

## Failure modes
- Retrying non-transient errors such as invalid input or insufficient funds
- Swallowing errors so failures look like successes
- Retry storms without backoff or a cap
- Fallback path is itself untested and also fails

## Minimal example
```python
for attempt in range(3):
    try:
        return tool(args, timeout=10)
    except Transient as e:
        sleep(2 ** attempt)               # backoff, capped retries
    except Permanent as e:
        log(e); return fallback(args)     # never retry invalid input
escalate("tool unavailable after retries")
```

## Next skills
- If recovery needs a person: load `human-in-the-loop`
- If the failing call is a tool: load `tool-use`
- If fallback means a cheaper model: load `resource-aware-optimization`
