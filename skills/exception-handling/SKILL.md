---
name: exception-handling
description: Detect, fallback, degrade. Use whenever tools and networks can fail. Do NOT use as a substitute for fixing bad prompts.
role: [safety]
chapter: 12
token_cost_estimate: 237
chains_with: [tool-use, guardrails-safety]
---

# Exception Handling and Recovery

## When to use
- Tools, APIs, or networks can fail in production
- Need retries, timeouts, fallbacks, or graceful degradation
- Primary precise tool, then coarser fallback

## When NOT to use
- Failures are actually prompt/routing bugs
- Policy must *block* the call (load `guardrails-safety`)
- Human must decide after failure (load `human-in-the-loop`)

## Inputs
- Primary handler + tools
- State flag (e.g. `primary_location_failed`)
- Fallback handler + response formatter

## Outputs
- Best-effort result
- Logged error / degraded marker

## Failure modes
- Flag not set → fallback never runs
- Infinite retry
- User sees success on garbage data

## Minimal example
```python
robust = SequentialAgent(sub_agents=[primary_handler, fallback_handler, response_agent])
# fallback: if state["primary_location_failed"]: use general_area tool
```

## Next skills
- If the call is a tool: load `tool-use`
- If failure is a policy violation: load `guardrails-safety`
