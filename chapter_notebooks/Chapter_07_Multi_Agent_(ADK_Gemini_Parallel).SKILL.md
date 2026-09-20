---
name: multi-agent
description: Specialist agents plus a coordination model. Use when roles differ. Not when one agent suffices.
role: [planner, executor]
chapter: 7
token_cost_estimate: 234
chains_with: [a2a, routing]
---

# Multi-Agent Collaboration

## When to use
- Distinct roles (researcher, writer, reviewer).
- Work is sequential, parallel or loop-shaped.
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
r1 = LlmAgent(name="r1", output_key="r1", instruction="Research X")
r2 = LlmAgent(name="r2", output_key="r2", instruction="Research Y")
merge = LlmAgent(name="merge", instruction="Combine {r1} {r2}")
root = SequentialAgent(sub_agents=[ParallelAgent(sub_agents=[r1, r2]), merge])
```

## Next skills
- If agents live in other processes: load `a2a`
- If one specialist per request: load `routing`
