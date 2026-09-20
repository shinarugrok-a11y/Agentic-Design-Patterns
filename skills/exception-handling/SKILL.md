---
name: exception-handling
description: Use when tools or agents can fail and need fallbacks or retries. Do not use to hide systematic errors that need fixing.
role: [safety]
chapter: 12
token_cost_estimate: 188
chains_with: [tool-use, guardrails]
---

# Exception Handling and Recovery

## When to use
- External tools can fail or time out
- Degraded answer beats no answer
- Errors are transient, not systematic

## When NOT to use
- Failure must surface loudly (billing, safety)
- Same error repeats (fix root cause)
- Fallback quality is unacceptable

## Inputs
- Primary handler + fallback chain
- Retry budget and timeouts

## Outputs
- Best available result + degraded flag
- Structured error for logging

## Failure modes
- Silent degradation — always flag fallback usage
- Retry storms — backoff + circuit breaker
- Catch-all — catch narrow, log full trace

## Minimal example
```python
try:
    loc = precise_lookup(addr)
except ToolError:
    loc = coarse_lookup(addr)  # flagged degraded
    log("fallback used", trace)
```

## Next skills
- If failures come from tools: load `tool-use`
- If need policy-level safety: load `guardrails`
