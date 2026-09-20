---
name: learning-and-adaptation
description: Strategy improvement from measured outcomes. Update the agent's strategy, prompts, or code from measured outcomes of past runs. Skip it when the environment is static or changes cannot be evaluated objectively.
role: [memory, critic]
chapter: 9
token_cost_estimate: 370
chains_with: [evaluation-and-monitoring, memory-management, reflection]
---

# Learning and Adaptation

## When to use
- Environment or user behavior shifts over time
- Outcomes can be scored objectively
- Repeated runs justify optimizing the strategy

## When NOT to use
- No measurable outcome signal exists
- Behavior must stay fixed and auditable
- A single run cannot be compared to a baseline

## Inputs
- outcome or reward signal
- candidate variants
- evaluator with a fitness metric

## Outputs
- selected variant
- performance delta
- updated strategy or prompt store

## Failure modes
- Optimizing a proxy metric that diverges from the real goal
- Self-modification with no overseer or rollback path
- Overfitting to a small benchmark set
- Unbounded evolution loops burning budget

## Minimal example
```python
best = baseline
for _ in range(BUDGET):
    variant = mutate(best)                 # prompt, tool choice, or code
    if evaluate(variant) > evaluate(best): # same held-out fitness set
        best, log = variant, log + [delta(best, variant)]
overseer.review(log)  # required before any self-modification is kept
```

## Next skills
- If you lack a fitness metric: load `evaluation-and-monitoring`
- If learned facts must persist: load `memory-management`
- If improvement is per-run: load `reflection`
