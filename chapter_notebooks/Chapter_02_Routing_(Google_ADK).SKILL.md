---
name: routing
description: Dynamic path selection. Use to classify a request and dispatch one handler. Not when every request takes the same path.
role: [planner, executor]
chapter: 2
token_cost_estimate: 219
chains_with: [multi-agent, resource-aware-optimization]
---

# Routing

## When to use
- Requests fall into distinct categories.
- Cheap path for easy cases, heavy path for hard ones.
- Triage must precede expensive work.

## When NOT to use
- One fixed pipeline: use `prompt-chaining`.
- Every branch must run: use `parallelization`.

## Inputs
- Request or state
- Named handlers with descriptions

## Outputs
- Route label
- Handler result (or fallback)

## Failure modes
- Silent misroute to the wrong handler.
- No default branch for unclear input.
- Router output not normalised (`' booker\n'`).

## Minimal example
```python
route = llm("One word: booker|info|unclear. Request: {req}").strip()
handlers = {"booker": book, "info": lookup}
result = handlers.get(route, handle_unclear)(req)
```

## Next skills
- If routes are full specialist agents: load `multi-agent`
- If routing is by cost tier: load `resource-aware-optimization`
