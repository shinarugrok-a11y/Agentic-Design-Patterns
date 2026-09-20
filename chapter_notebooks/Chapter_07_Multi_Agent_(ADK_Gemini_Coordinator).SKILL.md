---
name: multi-agent
description: Use when specialists with distinct roles must cooperate on one goal. Do not use when a single agent with tools can do the job.
role: [planner, executor]
chapter: 7
token_cost_estimate: 183
chains_with: [planning, parallelization]
---

# Multi-Agent Collaboration

## When to use
- Task needs distinct specialists (researcher + writer)
- Work splits by topology (sequential/parallel/loop)
- Single agent context would overflow

## When NOT to use
- Single agent with tools suffices
- Only 2 trivial steps (use prompt-chaining)
- No clear role boundaries exist

## Inputs
- Role cards (name, model, instruction)
- Topology: sequential, parallel, loop, coordinator

## Outputs
- Coordinated final output
- Handoff trace

## Failure modes
- State drift — share via explicit keys (output_key/state)
- Deadlock loops — cap loop iterations with exit check
- Overhead — default to fewer, broader roles

## Minimal example
```python
pipe = SequentialAgent([fetch, summarize])
team = ParallelAgent([weather, news])
loop = LoopAgent([worker, checker], max_iter=3)
```

## Next skills
- If need the overall plan first: load `planning`
- If need concurrent specialists: load `parallelization`
