---
name: goal-setting
description: Measurable goals with a judge loop. Use when success must be checked. Not when success is undefinable.
role: [planner]
chapter: 11
token_cost_estimate: 217
chains_with: [reflection, prioritization]
---

# Goal Setting and Monitoring

## When to use
- Success has checkable criteria.
- Work should stop when goals are met.
- Progress must be reported per goal.

## When NOT to use
- Success cannot be defined.
- Single-shot task; no monitoring needed.

## Inputs
- Goals list
- Judge function or rubric

## Outputs
- Artifact meeting goals
- Per-goal status

## Failure modes
- Judge not boolean: loop never ends.
- Conflicting goals.
- Max iterations undefined.

## Minimal example
```python
for i in range(max_iter):
    code = llm(f"Goals: {goals}\nFeedback: {fb}\nWrite code")
    fb = llm(f"Critique vs goals:\n{code}")
    if llm(f"All goals met? True/False\n{code}\n{goals}").strip() == "True": break
```

## Next skills
- If the critique loop needs detail: load `reflection`
- If goals need ranking: load `prioritization`
