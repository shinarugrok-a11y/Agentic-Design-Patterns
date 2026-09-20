---
name: goal-setting
description: SMART objectives plus a loop that checks progress. Use for autonomous multi-step work. Do NOT use when success is undefined.
role: [planner]
chapter: 11
token_cost_estimate: 249
chains_with: [planning, evaluation-monitoring]
---

# Goal Setting and Monitoring

## When to use
- Agent must hit a specific, measurable objective without a human each step
- Generate → feedback → `True`/`False` goals-met loop
- SMART goals (specific, measurable, time-bound)

## When NOT to use
- No success criteria
- You only need a static plan document (load `planning`)
- Production scoring/telemetry (load `evaluation-monitoring`)

## Inputs
- Explicit goal bullets
- Generator + reviewer prompts
- `max_iterations`

## Outputs
- Artifact (e.g. `.py`) when goals pass
- Feedback history

## Failure modes
- Fuzzy goals → judge always True
- Max N hit silently
- LLM-generated filenames collide or are nonsense

## Minimal example
```python
for i in range(max_iterations):
    code = generate(use_case, goals, previous, feedback)
    feedback = review(code, goals)
    if goals_met(feedback):  # True/False
        break
```

## Next skills
- If you need the step list first: load `planning`
- If you need prod metrics/judges: load `evaluation-monitoring`
