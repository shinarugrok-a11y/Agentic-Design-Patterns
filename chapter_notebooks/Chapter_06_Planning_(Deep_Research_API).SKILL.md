---
name: planning
description: Decompose a goal into ordered steps before acting. Use for multi-step goals with unclear path. Not for single actions.
role: [planner]
chapter: 6
token_cost_estimate: 217
chains_with: [goal-setting, multi-agent]
---

# Planning

## When to use
- Goal needs several dependent steps.
- Path is not known up front; expect re-planning.
- Steps must be visible and checkable.

## When NOT to use
- Task is one action or a fixed pipeline.
- Plan quality cannot be judged: add `reflection`.

## Inputs
- Goal + constraints
- Available tools/agents

## Outputs
- Ordered plan with dependencies
- Execution log

## Failure modes
- Missing step discovered late.
- Plan never revised after failure.
- Over-planning trivial tasks.

## Minimal example
```python
steps = json.loads(llm(f"JSON list of steps for: {goal}"))   # plan first
for step in steps:
    out = executor(step, context=steps)                       # then execute in order
    if not ok(out): break                                     # re-plan; don't plough on
```

## Next skills
- If plan needs measurable success criteria: load `goal-setting`
- If steps are executed by agents: load `multi-agent`
