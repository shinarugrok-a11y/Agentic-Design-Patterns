---
name: routing
description: Dynamic path selection. Classify the incoming request and dispatch it to one specialized handler, tool, or sub-agent. Skip it when there is exactly one valid handler or the path is fixed in advance.
role: [planner, executor]
chapter: 2
token_cost_estimate: 350
chains_with: [prompt-chaining, tool-use, resource-aware-optimization]
---

# Routing

## When to use
- Two or more distinct handlers, tools, or sub-agents exist
- Intent must be classified before work starts
- Requests need triage by type, topic, or urgency

## When NOT to use
- Only one valid handler exists
- The path is already fixed by prior state
- Misroute cost exceeds the cost of running all paths

## Inputs
- user request or state
- route catalog with descriptions
- default fallback route

## Outputs
- selected route id
- routing rationale
- arguments for the handler

## Failure modes
- Overlapping route descriptions make selection non-deterministic
- No fallback route, so unmatched inputs dead-end
- Router hallucinates a route id that does not exist
- One misroute derails the whole downstream workflow

## Minimal example
```python
ROUTES = {"billing": billing_agent, "tech": tech_agent, "other": human_handoff}
choice = llm.invoke(ROUTER_PROMPT.format(query=q, routes=list(ROUTES)))
ROUTES.get(choice.strip(), ROUTES["other"])(q)  # fallback is mandatory
```

## Next skills
- If the route is multi-stage: load `prompt-chaining`
- If the route calls an API: load `tool-use`
- If routing on cost: load `resource-aware-optimization`
