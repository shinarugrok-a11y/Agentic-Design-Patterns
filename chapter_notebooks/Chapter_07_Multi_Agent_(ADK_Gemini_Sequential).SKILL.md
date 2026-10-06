---
name: multi-agent
description: Specialist agents plus a coordination model. Use when roles differ. Not when one agent suffices.
role: [planner, executor]
chapter: 7
token_cost_estimate: 217
chains_with: [a2a, routing]
---

# Multi-Agent Collaboration

## When to use
- Distinct roles (researcher, writer, reviewer).
- Specialists need different tools.

## When NOT to use
- One agent with tools suffices.
- Coordination costs more than the task.

## Inputs
- Role definitions + tools
- Coordination model

## Outputs
- Combined result
- Shared state keys

## Failure modes
- Coordinator answers instead of delegating.
- State key mismatch between agents.
- Endless hand-offs.

## Minimal example
```python
r1 = agent("Research X", output_key="r1")      # specialists, one job each
r2 = agent("Research Y", output_key="r2")
state = run_parallel([r1, r2])                 # independent, so concurrent
final = agent("Combine {r1} and {r2}").run(state)   # coordinator merges
```

## Next skills
- If agents live in other processes: load `a2a`
- If one specialist per request: load `routing`
