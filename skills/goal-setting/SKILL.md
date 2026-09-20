---
name: goal-setting
description: Use when work must track measurable goals with iteration toward targets. Do not use for open-ended exploration without targets.
role: [planner]
chapter: 11
token_cost_estimate: 188
chains_with: [planning, evaluation-monitoring]
---

# Goal Setting and Monitoring

## When to use
- Outcome needs measurable targets
- Progress needs periodic check-ins
- Iteration must stop at a threshold

## When NOT to use
- Pure exploration with no target
- Goal cannot be quantified at all
- Single-shot task needs no tracking

## Inputs
- Goal statement + done criteria
- Baseline metrics

## Outputs
- Milestones with owners
- Stop/continue decision per check

## Failure modes
- Vague goals — force numeric targets + deadlines
- Vanity metrics — tie each metric to the outcome
- Endless loops — set max iterations + success threshold

## Minimal example
```python
goal = Goal("Cut support backlog 30%", metric, deadline)
while not goal.met() and iters < 5:
    act(); report(goal.delta())
stop_or_escalate(goal)
```

## Next skills
- If decompose goal into steps: load `planning`
- If score progress rigorously: load `evaluation-monitoring`
