---
name: prioritization
description: Rank competing tasks before acting. Rank competing tasks by urgency, importance, dependencies, and cost, then act on the top item. Skip it when there is one task or a fixed queue order already applies.
role: [planner]
chapter: 20
token_cost_estimate: 360
chains_with: [planning, resource-aware-optimization, goal-setting-and-monitoring]
---

# Prioritization

## When to use
- More candidate tasks than capacity
- Goals conflict or compete for resources
- Urgency and importance differ across items

## When NOT to use
- One task, or a fixed queue order applies
- All items carry equal cost and value
- Re-ranking churn would cause thrash

## Inputs
- candidate task list
- ranking criteria and weights
- resource constraints

## Outputs
- ordered task queue
- chosen next action with rationale
- deferred or dropped items

## Failure modes
- Criteria weights unstated, so rankings are unreproducible
- Re-ranking every tick causes thrash and starvation
- Dependencies ignored, so blocked work is scheduled first
- Low-priority items starve forever with no aging rule

## Minimal example
```python
W = {"urgency": 0.4, "importance": 0.4, "cost": -0.2}  # explicit weights
ready = [t for t in tasks if set(t.depends_on) <= done]
for t in ready:
    t.score = sum(W[k] * t.criteria[k] for k in W) + aging(t)
next_task = max(ready, key=lambda t: t.score)
```

## Next skills
- If the order implies a plan: load `planning`
- If ranking is budget-driven: load `resource-aware-optimization`
- If priorities derive from a goal: load `goal-setting-and-monitoring`
