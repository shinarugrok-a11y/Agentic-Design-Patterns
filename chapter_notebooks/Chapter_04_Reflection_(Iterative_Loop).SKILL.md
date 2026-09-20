---
name: reflection
description: Generate, critique, refine. Use when output must meet explicit criteria. Not for cheap outputs.
role: [critic]
chapter: 4
token_cost_estimate: 229
chains_with: [evaluation-monitoring, goal-setting]
---

# Reflection

## When to use
- Output must meet explicit criteria.
- Code where review catches bugs before use.
- A stop signal can be defined.

## When NOT to use
- Simple factual answers.
- No objective criteria: loop never converges.

## Inputs
- Task + criteria
- Draft, max iterations

## Outputs
- Refined output
- Critique history + stop reason

## Failure modes
- No stop condition: cost blow-up.
- Same model as producer and critic: shared blind spots.
- Vague critique makes refinement drift.

## Minimal example
```python
draft = llm(task)
for _ in range(max_iter):
    crit = llm(f"Review vs task. Say CODE_IS_PERFECT if done.\n{draft}")
    if "CODE_IS_PERFECT" in crit: break
    draft = llm(f"Refine per critique:\n{crit}\n{draft}")
```

## Next skills
- If critic needs metrics or a rubric: load `evaluation-monitoring`
- If stop criteria are tracked goals: load `goal-setting`
