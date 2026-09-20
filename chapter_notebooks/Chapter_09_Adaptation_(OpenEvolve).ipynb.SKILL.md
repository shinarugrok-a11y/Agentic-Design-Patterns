---
name: learning-adaptation
description: Improve behavior from feedback via evolutionary or iterative updates.
role: [memory, critic]
chapter: 9
token_cost_estimate: 205
chains_with: [evaluation-monitoring, reflection]
---

# Learning and Adaptation

## When to use
- Repeated tasks produce win/fail feedback.
- You have a scorer.
- Adaptation budget allows multiple evolve-and-test cycles.

## When NOT to use
- One-off task with no repeat or feedback.
- No reliable fitness signal; evolution drifts.

## Inputs
- Current policy/prompt + feedback or scores
- Fitness function + iteration budget

## Outputs
- Adapted policy/prompt + improvement log

## Failure modes
- Overfitting to the latest feedback; forgetting prior wins.
- Noisy fitness signal drives regressions.
- Unbounded evolution burns budget without converging.

## Minimal example
```python
best = policy
for _ in range(budget):
    cand = mutate(best)
    if fitness(cand) > fitness(best): best = cand
```

## Next skills
- If adaptation needs reliable scoring first: load `evaluation-monitoring`
- If each candidate needs a critique pass: load `reflection`
