---
name: prioritization
description: Rank tasks by urgency, importance, dependencies and cost. Order or triage competing tasks with explicit criteria and re-rank as conditions change. Do not use when there is one task or when order is fixed by dependencies alone.
role: [planner]
chapter: 20
token_cost_estimate: 340
chains_with: [planning, goal-setting, resource-aware-optimization]
---

# Prioritization

## When to use
- Many tasks, limited resources.
- Urgency cues in natural language ('ASAP' -> P0).
- Dynamic re-prioritisation on new events.
- Assigning work to workers/queues.

## When NOT to use
- Single task.
- Strict DAG already defines order: use `planning`.
- Model/cost selection is the real problem: use `resource-aware-optimization`.

## Inputs
- Task list
- Criteria (urgency, importance, deps, cost)
- Priority scale (P0-P2)
- Available workers

## Outputs
- Ranked/assigned tasks
- Defaults for missing fields
- Updated task board

## Failure modes
- Everything becomes P0.
- Priority set before task exists (tool ordering).
- Invalid priority value accepted.
- No re-prioritisation when context changes.

## Minimal example
```python
tools = [create_new_task, assign_priority_to_task, assign_task_to_worker, list_all_tasks]
SYSTEM = """1. create_new_task first to get an id.
2. Map 'urgent/ASAP/critical' -> P0 via assign_priority_to_task.
3. Assign worker if named; else default P1 + 'Worker A'.
4. list_all_tasks to show final state."""
agent = AgentExecutor(agent=create_react_agent(llm, tools, prompt), tools=tools)
```

## Next skills
- If ranked tasks need step decomposition: load `planning`
- If priorities derive from goals: load `goal-setting`
- If ranking is about cost tiers: load `resource-aware-optimization`
