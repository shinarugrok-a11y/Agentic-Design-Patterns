---
name: planning
description: Use when a goal needs decomposing into an ordered plan before acting. Do not use for single-step or fully reactive tasks.
role: [planner]
chapter: 6
token_cost_estimate: 185
chains_with: [goal-setting, multi-agent]
---

# Planning

## When to use
- Goal needs 3+ ordered steps
- Steps need different tools or agents
- Must show/validate the plan first

## When NOT to use
- Single-step or purely reactive task
- Environment changes faster than plans
- Plan cost exceeds execution cost

## Inputs
- Goal plus constraints
- Available actions and tools

## Outputs
- Ordered plan with owners
- Replan trigger conditions

## Failure modes
- Unexecutable plans — ground each step in a real action
- Over-planning — timebox planning, then act
- Stale plans — replan on unexpected observations

## Minimal example
```python
plan = planner(goal, tools, constraints)
for step in plan.steps:
    obs = execute(step)
    if surprises(obs): plan = replan(plan, obs)
```

## Next skills
- If track plan against measurable goals: load `goal-setting`
- If assign steps to specialists: load `multi-agent`
