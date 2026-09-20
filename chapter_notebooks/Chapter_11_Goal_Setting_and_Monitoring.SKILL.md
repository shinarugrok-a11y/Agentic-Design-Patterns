---
name: goal-setting-and-monitoring
description: Measurable objectives with progress checks. State a measurable objective with success checks and re-evaluate progress after every step. Skip it when success is trivially observable in a single response.
role: [planner]
chapter: 11
token_cost_estimate: 360
chains_with: [planning, evaluation-and-monitoring, exception-handling-and-recovery]
---

# Goal Setting and Monitoring

## When to use
- Agent runs autonomously over many steps
- Success must be verified, not assumed
- Conditions can change mid-run

## When NOT to use
- Success is obvious from a single reply
- No measurable criteria can be defined
- The run is too short for monitoring to pay off

## Inputs
- goal statement
- measurable success criteria
- progress signals or metrics

## Outputs
- goal status verdict
- progress log
- course-correction or escalation decision

## Failure modes
- Unmeasurable goals make the monitor unable to stop
- Monitoring only at the end, so drift is caught too late
- Agent declares success without verifying criteria
- No iteration or time budget, so the loop runs forever

## Minimal example
```python
goal = {"objective": "resolve billing dispute",
        "done_when": ["refund posted", "customer confirms"],
        "max_steps": 12}
for step in range(goal["max_steps"]):
    act()
    status = check(goal["done_when"])       # evaluate every step, not only at the end
    if status.met: break
    if status.at_risk: escalate(status)
```

## Next skills
- If no step list exists: load `planning`
- If criteria need scoring: load `evaluation-and-monitoring`
- If a check fails hard: load `exception-handling-and-recovery`
