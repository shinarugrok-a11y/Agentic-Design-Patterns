---
name: parallelization
description: Fan out independent subtasks and join results.
role: [executor]
chapter: 3
token_cost_estimate: 209
chains_with: [routing, multi-agent]
---

# Parallelization

## When to use
- Subtasks are independent.
- Latency matters and calls can run concurrently.
- Results merge with a final join/synthesis step.

## When NOT to use
- Subtask B needs subtask A's output (use `prompt-chaining`).
- Tasks contend for one rate-limited resource.

## Inputs
- List of independent subtasks
- Join/synthesis prompt or reducer

## Outputs
- Per-task results + merged synthesis

## Failure modes
- One slow branch stalls the join; needs timeouts.
- Unbounded fan-out hits rate limits or cost spikes.
- Join step drops or garbles a branch result.

## Minimal example
```python
results = await asyncio.gather(*(research(t) for t in topics))
report = llm(f"Synthesize into one report: {results}")
```

## Next skills
- If branches need different specialist agents: load `multi-agent`
- If results must be ranked before use: load `prioritization`
