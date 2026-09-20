---
name: planning
description: Decompose a goal into an explicit step plan before acting.
role: [planner]
chapter: 6
token_cost_estimate: 203
chains_with: [multi-agent, reflection]
---

# Planning

## When to use
- Goal needs 3+ ordered steps with dependencies.
- You must show or validate the plan before executing.
- Subgoals can be delegated to different executors.

## When NOT to use
- Single-step task; planning overhead exceeds benefit.
- Environment changes faster than a plan survives.

## Inputs
- Goal statement + constraints
- Available actions/agents

## Outputs
- Step plan with dependencies + success criteria

## Failure modes
- Plan looks plausible but skips a hard dependency.
- No replanning trigger when a step fails.
- Over-detailed plans go stale before execution.

## Minimal example
```python
plan = llm(f"Plan steps with deps for: {goal}\nActions: {actions}")
for step in parse(plan): execute(step) or replan(step)
```

## Next skills
- If steps fan out to different agents: load `multi-agent`
- If plan needs a critic pass first: load `reflection`
