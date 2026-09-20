---
name: parallelization
description: Use when subtasks are independent and can run concurrently before merging. Do not use when subtasks depend on each other's outputs.
role: [executor]
chapter: 3
token_cost_estimate: 185
chains_with: [prompt-chaining, multi-agent]
---

# Parallelization

## When to use
- Subtasks are independent (research 3 topics)
- Latency matters — run branches concurrently
- Results merge into one synthesis step

## When NOT to use
- Subtasks depend on each other (use prompt-chaining)
- Only one task — no fan-out benefit
- Merge step is undefined or ambiguous

## Inputs
- List of independent subtasks
- Merge prompt or reduce function

## Outputs
- Per-branch results
- Single synthesized answer

## Failure modes
- Hidden dependencies — verify independence before fanning out
- Straggler branch blocks join — set per-branch timeouts
- Unbounded fan-out — cap concurrency (3-8 branches)

## Minimal example
```python
results = gather(run("Research solar"),
               run("Research wind"),
               run("Research hydro"))
return run(f"Synthesize comparison: {results}")
```

## Next skills
- If branches need sequential steps: load `prompt-chaining`
- If branches need specialist agents: load `multi-agent`
