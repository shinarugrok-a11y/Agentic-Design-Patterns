---
name: prioritization
description: Order competing tasks by urgency, value, and dependencies. Use when the backlog exceeds capacity. Do NOT use for a single task.
role: [planner]
chapter: 20
token_cost_estimate: 238
chains_with: [planning, resource-aware-optimization]
---

# Prioritization

## When to use
- Many actions, scarce time/people/budget
- Map language like urgent/ASAP → P0
- Default missing priority/assignee explicitly

## When NOT to use
- Single task pipeline (load `planning`)
- The scarce resource is model cost (load `resource-aware-optimization`)
- No competing work

## Inputs
- Task text
- Priority enum (P0/P1/P2)
- Worker allowlist

## Outputs
- `task_id` + priority + assignee
- Ordered `list_all_tasks`

## Failure modes
- Alert fatigue (all P0)
- Process restart drops the dict
- Parsing errors masked (`handle_parsing_errors=True`)

## Minimal example
```python
create_new_task(description)
assign_priority_to_task(task_id, "P0")  # if urgent
assign_task_to_worker(task_id, "Worker B")
list_all_tasks()
```

## Next skills
- If you still need a step plan per task: load `planning`
- If spend/latency is the scarce resource: load `resource-aware-optimization`
