---
name: resource-optimization
description: Route each prompt to the cheapest sufficient model or path.
role: [planner]
chapter: 16
token_cost_estimate: 203
chains_with: [routing, evaluation-monitoring]
---

# Resource-Aware Optimization

## When to use
- Request difficulty varies; cheap models handle easy ones.
- Classify prompt -> pick model/path -> respond.
- Track cost, latency, and quality per route.

## When NOT to use
- Every request needs frontier quality.
- Classification costs more than it saves.

## Inputs
- Prompt + difficulty classifier
- Model/path tiers with cost profiles

## Outputs
- Response + route/cost accounting record

## Failure modes
- Classifier under-routes hard prompts to weak models.
- No quality fallback when cheap path fails.
- Savings measured without quality regression checks.

## Minimal example
```python
tier = classify_prompt(p)  # simple|search|reason
if tier == "search": ctx = google_search(p)
print(generate_response(p, tier, ctx))
```

## Next skills
- If tier selection is a dispatch problem: load `routing`
- If quality per tier needs measurement: load `evaluation-monitoring`
