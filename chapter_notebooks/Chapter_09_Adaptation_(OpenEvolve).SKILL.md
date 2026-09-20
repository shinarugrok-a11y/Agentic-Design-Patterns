---
name: learning-adaptation
description: Use when agent behavior must improve from feedback or evolution. Do not use for fixed, audited, deterministic behavior.
role: [memory, critic]
chapter: 9
token_cost_estimate: 182
chains_with: [evaluation-monitoring, reflection]
---

# Learning and Adaptation

## When to use
- Repeated tasks with measurable quality
- Evaluator or reward signal exists
- Budget for many iterations (100s+)

## When NOT to use
- One-off task with no repeats
- No trustworthy evaluator
- Behavior must stay audited and fixed

## Inputs
- Initial program path + evaluator file
- Evolution config (iterations, population)

## Outputs
- Best program with metrics
- Before/after comparison

## Failure modes
- Evaluator gaming — hold out a separate test set
- Regressions — keep elite archive, re-test top-K
- Unsafe drift — gate promotion on human/safety review

## Minimal example
```python
evolve = OpenEvolve(program, evaluator, config)
best = await evolve.run(iterations=1000)
print(best.metrics)  # promote only if held-out gains
```

## Next skills
- If need trustworthy scoring: load `evaluation-monitoring`
- If need per-output revision: load `reflection`
