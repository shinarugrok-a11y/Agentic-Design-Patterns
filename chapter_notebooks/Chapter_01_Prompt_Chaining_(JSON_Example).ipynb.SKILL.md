---
name: prompt-chaining
description: Sequential task decomposition.
role: [executor]
chapter: 1
token_cost_estimate: 225
chains_with: [routing, tool-use]
---

# Prompt Chaining

## When to use
- Task splits into ordered stages.
- Each stage needs its own focused prompt and output schema.
- Intermediate outputs must be inspectable or validated.

## When NOT to use
- Subtasks are independent (use `parallelization`).
- Route depends on input type (use `routing`).

## Inputs
- Ordered stage list with per-stage prompt template
- Input payload; output schema per stage

## Outputs
- Final stage output
- Intermediate outputs for debugging

## Failure modes
- Error in an early stage cascades silently downstream.
- Over-long chains drift off-goal without checkpoints.
- Rigid sequence breaks on inputs needing a different order.

## Minimal example
```python
extract = llm("Extract specs from: {text}")
table = llm(f"Format as JSON table: {extract}")
report = llm(f"Summarize for execs: {table}")
```

## Next skills
- If branching depends on input type: load `routing`
- If a stage needs external data or actions: load `tool-use`
