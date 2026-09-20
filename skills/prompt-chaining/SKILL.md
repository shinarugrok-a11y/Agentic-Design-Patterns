---
name: prompt-chaining
description: Sequential task decomposition. Use when each stage's output feeds the next. Not for independent sub-tasks.
role: [executor]
chapter: 1
token_cost_estimate: 227
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
- Step-N error propagates downstream.
- Early context lost unless passed explicitly.
- Free-text handoff breaks the next parser.

## Minimal example
```python
extract = prompt("Extract specs: {text}") | llm | str
to_json = prompt("Specs -> JSON {cpu,memory,storage}: {specs}") | llm | str
result = ({"specs": extract} | to_json).invoke({"text": raw})
```

## Next skills
- If stage order depends on input: load `routing`
- If a stage must call an API: load `tool-use`
