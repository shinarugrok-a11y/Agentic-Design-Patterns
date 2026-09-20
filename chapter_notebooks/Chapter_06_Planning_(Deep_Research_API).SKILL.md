---
name: planning
description: Decompose a goal into ordered steps before acting. Use for multi-step goals with unclear path. Not for single actions.
role: [planner]
chapter: 6
token_cost_estimate: 218
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
plan  = Task(description=f"Numbered step plan for: {goal}", agent=planner)
write = Task(description="Execute the plan", agent=writer, context=[plan])
Crew(agents=[planner, writer], tasks=[plan, write],
     process=Process.sequential).kickoff()
```

## Next skills
- If plan needs measurable success criteria: load `goal-setting`
- If steps are executed by agents: load `multi-agent`
