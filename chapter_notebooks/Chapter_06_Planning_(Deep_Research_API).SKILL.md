---
name: planning
description: Decompose a goal into ordered steps before acting. Turn a high-level objective into an explicit, ordered list of sub-steps, then execute or delegate them. Do not use for single-action requests or when the steps are already fixed by a pipeline.
role: [planner]
chapter: 6
token_cost_estimate: 320
chains_with: [goal-setting, prompt-chaining, prioritization]
---

# Planning

## When to use
- Request needs several interdependent operations.
- Steps are not known in advance and depend on the goal.
- Plan must be visible for review before execution.
- Long-horizon research or report generation.

## When NOT to use
- One tool call answers it.
- Pipeline is static: use `prompt-chaining`.
- Budget is tiny; planning tokens exceed task tokens.

## Inputs
- Goal statement
- Available tools/skills
- Constraints (time, budget)

## Outputs
- Ordered plan (steps, dependencies)
- Executed results per step
- Revised plan on deviation

## Failure modes
- Plan is plausible but skips a required step; execution 'succeeds' incompletely.
- Plan never revised when a step fails.
- Over-planning: 20 steps for a 2-step task.
- Steps reference tools the executor does not have.

## Minimal example
```python
plan = llm("Goal: {goal}. Produce a numbered plan of <=7 steps with deps.")
for step in parse(plan):
    result = execute(step)          # tool-use / delegate to sub-agent
    if failed(result): plan = llm(f"Revise plan given failure: {result}")
# CrewAI: Task(description="1. plan  2. write from plan", expected_output=...)
```

## Next skills
- If plan needs measurable success criteria: load `goal-setting`
- If steps are fixed after planning: load `prompt-chaining`
- If many candidate steps compete for resources: load `prioritization`
