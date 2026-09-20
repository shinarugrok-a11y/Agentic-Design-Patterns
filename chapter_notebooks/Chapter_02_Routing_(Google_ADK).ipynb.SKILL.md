---
name: routing
description: Classify input then dispatch to a specialist.
role: [planner, executor]
chapter: 2
token_cost_estimate: 236
chains_with: [prompt-chaining, multi-agent]
---

# Routing

## When to use
- Inputs fall into distinct types needing different handlers.
- One entry point fronts booking/info/unclear-style specialists.
- You can write a fast classifier up front.

## When NOT to use
- Every input follows the same steps (use `prompt-chaining`).
- Subtasks run concurrently (use `parallelization`).

## Inputs
- Raw user request
- Route definitions: name -> handler + trigger description

## Outputs
- Chosen route + specialist response
- Fallback response for unclassifiable input

## Failure modes
- Misclassification sends requests to the wrong specialist.
- No fallback route leaves unclear inputs unhandled.
- Classifier prompt drifts as new request types appear.

## Minimal example
```python
route = llm("Classify as booking|info|unclear: {req}")
handlers = {"booking": booking_handler, "info": info_handler}
print(handlers.get(route, unclear_handler)(req))
```

## Next skills
- If a route needs multiple ordered steps: load `prompt-chaining`
- If specialists must collaborate, not just dispatch: load `multi-agent`
