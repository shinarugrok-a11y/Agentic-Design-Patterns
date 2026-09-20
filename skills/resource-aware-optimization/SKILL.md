---
name: resource-aware-optimization
description: Route by complexity to the cheapest adequate model. Use under cost or latency budgets. Not when one model fits.
role: [planner]
chapter: 16
token_cost_estimate: 192
chains_with: [routing, evaluation-monitoring]
---

# Resource-Aware Optimization

## When to use
- Cost or latency budget is binding.
- Query difficulty varies widely.
- Cheap model handles most traffic.

## When NOT to use
- One model meets budget and quality.
- Quality cannot be verified per tier.

## Inputs
- Query
- Model tiers with cost/quality

## Outputs
- Chosen tier + answer
- Cost log

## Failure modes
- Hard query labelled simple.
- No critique loop on cheap answers.
- Classifier itself too expensive.

## Minimal example
```python
tier = llm_flash(f"Label simple|reasoning|internet: {q}").strip()
model = {"simple": flash, "reasoning": pro, "internet": flash_search}[tier]
answer = model(q)
```

## Next skills
- If the classifier needs design: load `routing`
- If cost and quality must be tracked: load `evaluation-monitoring`
