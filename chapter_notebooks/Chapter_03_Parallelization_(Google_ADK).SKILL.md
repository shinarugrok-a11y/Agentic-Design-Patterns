---
name: parallelization
description: Concurrent independent work, then merge. Use when sub-tasks do not depend on each other. Do NOT use for strict sequential pipelines.
role: [executor]
chapter: 3
token_cost_estimate: 233
chains_with: [routing, prompt-chaining]
---

# Parallelization

## When to use
- Workers do not need each other's outputs
- Latency is dominated by APIs or multiple LLM views
- Research: summarize / questions / terms then merge

## When NOT to use
- Step B requires step A's result (load `prompt-chaining`)
- You only need one of several paths (load `routing`)
- Debug cost of concurrency exceeds the latency win

## Inputs
- Shared query/topic
- Independent worker agents or chains
- Merger instruction (grounded on worker outputs only)

## Outputs
- Per-worker artifacts (distinct state keys)
- Single grounded synthesis

## Failure modes
- Merger adds ungrounded facts
- Missing join: later steps see partial state
- Hidden coupling causes races

## Minimal example
```python
mapped = RunnableParallel(summary=sum_chain, questions=q_chain, key_terms=term_chain)
result = (mapped | synthesis_prompt | llm).invoke(topic)
```

## Next skills
- If only one worker should run: load `routing`
- If merge output must be staged further: load `prompt-chaining`
