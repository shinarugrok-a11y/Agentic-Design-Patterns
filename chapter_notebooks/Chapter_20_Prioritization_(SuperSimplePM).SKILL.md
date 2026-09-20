---
name: prioritization
description: Use when many candidate tasks compete for limited agent capacity. Do not use when tasks arrive strictly in FIFO order.
role: [planner]
chapter: 20
token_cost_estimate: 176
chains_with: [goal-setting, planning]
---

# Prioritization

## When to use
- Backlog exceeds capacity
- Tasks differ in value/urgency
- Need top-N focus per cycle

## When NOT to use
- Strict FIFO order required
- Only 1-2 tasks exist
- Ranking cost exceeds execution cost

## Inputs
- Backlog items with metadata
- Weights (value, urgency, effort)

## Outputs
- Ranked list with scores
- Top-N committed set

## Failure modes
- Easy-win bias — weight value over ease
- Stale ranks — re-score on new arrivals
- No WIP limit — cap active tasks, queue the rest

## Minimal example
```python
ranked = score(backlog, value=0.5, urgency=0.3, effort=-0.2)
top = ranked[:3]  # commit, queue rest
act(top); rescore(backlog)
```

## Next skills
- If align rank to measurable goals: load `goal-setting`
- If plan the top-N execution: load `planning`
