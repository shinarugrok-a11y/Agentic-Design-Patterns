---
name: prioritization
description: Score and order tasks by priority before assigning work.
role: [planner]
chapter: 20
token_cost_estimate: 188
chains_with: [planning, multi-agent]
---

# Prioritization

## When to use
- Backlog exceeds worker capacity.
- Tasks carry priority, owner, and status fields.
- Agents claim highest-value ready task first.

## When NOT to use
- Single task or strict FIFO order required.
- Priorities churn faster than work completes.

## Inputs
- Task list with priority/owner/status
- Scoring rule + capacity limit

## Outputs
- Ordered queue + assignments

## Failure modes
- Stale priorities starve important new tasks.
- Priority inflation: everything becomes P0.
- No aging; low-priority tasks never run.

## Minimal example
```python
tasks.sort(key=lambda t: t.priority)
assign(task_manager.list_all_tasks(), workers)
claim_highest_ready(worker)
```

## Next skills
- If ordered tasks need step plans: load `planning`
- If tasks fan out to workers: load `multi-agent`
