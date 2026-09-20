---
name: routing
description: Dynamic path selection. Classify an incoming request and dispatch it to the one handler, tool, or sub-agent that fits. Do not use when every request takes the same path or when all branches should run anyway.
role: [planner, executor]
chapter: 2
token_cost_estimate: 340
chains_with: [prompt-chaining, multi-agent, resource-aware-optimization]
---

# Routing

## When to use
- Requests fall into distinct categories (booking vs. info vs. support).
- Different inputs need different tools or specialist agents.
- You want a cheap/fast path for simple cases and a heavy path for hard ones.
- Triage must happen before any expensive work.

## When NOT to use
- All inputs follow one fixed pipeline: use `prompt-chaining`.
- Every branch must run regardless: use `parallelization`.
- Only 1 handler exists.

## Inputs
- User request or state
- Set of named handlers with descriptions
- Router (LLM, rules, or embeddings)

## Outputs
- Selected route label
- Handler result
- Fallback result when unclear

## Failure modes
- Misclassification sends the request to the wrong handler silently.
- No default/unclear branch: unhandled inputs crash or loop.
- Router output not normalised (`' booker\n'` != `'booker'`).
- Overlapping handler descriptions confuse LLM-driven delegation.

## Minimal example
```python
decision = llm("Output one word: booker|info|unclear. Request: {req}").strip()
handlers = {"booker": book, "info": lookup}
result = handlers.get(decision, handle_unclear)(req)
# ADK: Agent(name="Coordinator", sub_agents=[booker, info]) -> auto-delegation
```

## Next skills
- If a branch is itself multi-stage: load `prompt-chaining`
- If routes are full specialist agents: load `multi-agent`
- If routing by cost/complexity: load `resource-aware-optimization`
