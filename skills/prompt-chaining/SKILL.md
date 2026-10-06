---
name: prompt-chaining
description: Sequential task decomposition. Use when each stage's output feeds the next. Not for independent sub-tasks.
role: [executor]
chapter: 1
token_cost_estimate: 246
chains_with: [routing, tool-use]
---

# Prompt Chaining

## When to use
- Task has distinct stages (extract -> transform -> format).
- One prompt drops constraints or drifts.
- A tool call or check is needed between steps.

## When NOT to use
- Sub-tasks are independent: use `parallelization`.
- Step order depends on input: use `routing`.

## Inputs
- Raw input
- Ordered stage prompts (+ optional schema)

## Outputs
- Final artifact
- Intermediate outputs for debugging

## Failure modes
- Ambiguous or free-text handoff makes the next step fail (GT:L771-L774); use JSON.
- No check between steps lets bad output flow on.
- Chaining a task one prompt handles adds calls and latency.

## Minimal example
```python
specs = llm(f"Extract specs: {raw}")
data = json.loads(llm(f"Specs -> JSON with cpu, memory, storage: {specs}"))
assert {"cpu", "memory", "storage"} <= data.keys()    # check before the next step
```

## Next skills
- If stage order depends on input: load `routing`
- If a stage must call an API: load `tool-use`
