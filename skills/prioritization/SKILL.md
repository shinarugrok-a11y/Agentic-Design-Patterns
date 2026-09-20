---
name: prioritization
description: Rank tasks by urgency, importance, dependencies, cost. Use with competing tasks. Not for one task or fixed order.
role: [planner]
chapter: 20
token_cost_estimate: 200
chains_with: [planning, goal-setting]
---

# Prioritization

## When to use
- Many tasks compete for limited resources.
- Deadlines and dependencies differ.
- Priorities change as new tasks arrive.

## When NOT to use
- One task, or order fixed by dependencies.
- All tasks are equal and cheap.

## Inputs
- Task list with attributes
- Scoring criteria

## Outputs
- Ordered task list
- Rationale per task

## Failure modes
- Everything is P0.
- Priority set before the task exists.
- Stale ranking after new input.

## Minimal example
```python
def score(t): return 3*t.urgency + 2*t.importance - t.cost + t.blocks
ordered = sorted(tasks, key=score, reverse=True)
# LLM variant: create_new_task -> assign_priority -> list_tasks
```

## Next skills
- If ranked tasks become a plan: load `planning`
- If goals define importance: load `goal-setting`
