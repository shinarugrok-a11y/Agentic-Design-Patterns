---
name: learning-adaptation
description: Improve behaviour from evaluated outcomes. Use when episodes repeat and an evaluator exists. Not when behaviour must stay fixed.
role: [memory, critic]
chapter: 9
token_cost_estimate: 204
chains_with: [evaluation-monitoring, reflection]
---

# Learning and Adaptation

## When to use
- Task repeats and outcomes are scored.
- Prompts, code or policies should improve over runs.
- An evaluator or reward is available.

## When NOT to use
- Behaviour must stay fixed (compliance).
- No evaluator: nothing to learn from.

## Inputs
- Episode log with scores
- Mutable artifact (prompt, code, policy)

## Outputs
- Improved artifact
- Score history

## Failure modes
- Reward hacking on a proxy metric.
- Self-edit breaks tooling.
- Forgetting earlier gains.

## Minimal example
```python
best = program
for gen in range(N):
    cand = llm(f"Improve for {metric}:\n{best}")
    if evaluate(cand) > evaluate(best): best = cand   # keep only if better
```

## Next skills
- If a scoring rubric is needed: load `evaluation-monitoring`
- If changes need review: load `reflection`
