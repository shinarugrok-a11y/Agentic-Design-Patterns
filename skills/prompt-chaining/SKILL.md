---
name: prompt-chaining
description: Use when a task has clear sequential stages where each step's output feeds the next. Do not use for independent tasks that could run in parallel.
role: [executor]
chapter: 1
token_cost_estimate: 217
chains_with: [routing, tool-use]
---

# Prompt Chaining

## When to use
- Task splits into ordered stages (extract -> transform -> summarize)
- Each stage needs a different prompt or model setting
- Intermediate output must be validated before continuing

## When NOT to use
- Stages are independent (use parallelization)
- Single-step task with no decomposition benefit
- Latency budget forbids sequential calls

## Inputs
- Ordered stage list with per-stage prompt
- Input data plus stage output schemas

## Outputs
- Validated output per stage
- Final result with stage trace

## Failure modes
- No validation between stages lets errors compound
- Over-long chains drift off-goal; cap at 3-5 stages
- One slow stage blocks the whole chain

## Minimal example
```python
extract = run("Extract entities: {text}")
check = run(f"Validate JSON: {extract}")
answer = run(f"Summarize for execs: {check}")
return answer  # 3 stages, validated
```

## Next skills
- If output must branch by type: load `routing`
- If a stage needs search, code, or APIs: load `tool-use`
