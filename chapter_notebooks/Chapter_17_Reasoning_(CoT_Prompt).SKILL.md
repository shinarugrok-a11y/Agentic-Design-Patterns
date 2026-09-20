---
name: reasoning-techniques
description: Explicit reasoning: CoT, ToT, ReAct, self-correction. Use for multi-step logic. Not for lookups or formatting.
role: [critic]
chapter: 17
token_cost_estimate: 188
chains_with: [reflection, tool-use]
---

# Reasoning Techniques

## When to use
- Multi-step logic or math.
- Answer must be auditable.
- Search over alternatives helps (ToT).

## When NOT to use
- Simple lookups or formatting.
- Hard latency budget.

## Inputs
- Problem statement
- Technique choice + budget

## Outputs
- Reasoning trace
- Final answer

## Failure modes
- Confident wrong chain.
- ToT cost explosion.
- Trace leaks into user-facing output.

## Minimal example
```python
# ReAct loop
for _ in range(max_steps):
    thought, action = llm(f"Think, then choose an action.\n{history}")
    if action == "FINISH": break
    history += observe(run(action))
```

## Next skills
- If the chain needs self-critique: load `reflection`
- If reasoning must trigger actions: load `tool-use`
