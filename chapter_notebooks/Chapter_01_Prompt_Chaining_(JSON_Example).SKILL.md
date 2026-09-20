---
name: prompt-chaining
description: Sequential task decomposition. Split a task with clear stages into focused prompts where each output feeds the next. Do not use for independent sub-tasks that can run in parallel or for tasks one prompt already handles.
role: [executor]
chapter: 1
token_cost_estimate: 310
chains_with: [routing, tool-use, reflection]
---

# Prompt Chaining

## When to use
- Task has distinct stages (extract -> transform -> format).
- A single prompt overloads the model and drops constraints.
- You need a tool call or validation between steps.
- Intermediate outputs should be inspectable or structured (JSON).

## When NOT to use
- Sub-tasks are independent: use `parallelization`.
- The task fits one focused prompt already.
- Step order depends on input: use `routing`.

## Inputs
- Raw input text or data
- Ordered list of stage prompts
- Optional schema per stage output

## Outputs
- Final artifact
- Intermediate stage outputs (for debugging)

## Failure modes
- Error in step N propagates to all later steps.
- Context from step 1 is lost by step 4 unless passed explicitly.
- Latency and cost grow linearly with chain length.
- Unstructured handoff (free text) breaks the next prompt's parser.

## Minimal example
```python
extract = prompt("Extract specs from: {text}") | llm | str
to_json = prompt("Turn specs into JSON {cpu,memory,storage}: {specs}") | llm | str
chain = {"specs": extract} | to_json
result = chain.invoke({"text": raw_text})
```

## Next skills
- If stage order depends on input: load `routing`
- If a stage must call an API or run code: load `tool-use`
- If output quality must be checked before passing on: load `reflection`
