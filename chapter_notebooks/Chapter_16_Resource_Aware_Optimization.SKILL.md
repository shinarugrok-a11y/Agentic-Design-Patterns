---
name: resource-aware-optimization
description: Spend the cheapest resource that meets the bar. Classify request complexity, then spend the cheapest model, tool, and context that meets the quality bar. Skip it when every request needs maximum quality or budget is not a constraint.
role: [planner]
chapter: 16
token_cost_estimate: 370
chains_with: [routing, prioritization, evaluation-and-monitoring]
---

# Resource-Aware Optimization

## When to use
- API spend or latency is capped
- Request complexity varies widely
- Hardware, bandwidth, or battery is constrained

## When NOT to use
- Every request demands maximum quality
- Router overhead exceeds the savings
- Silent quality loss would be unacceptable

## Inputs
- request with complexity signal
- model and tool tiers with costs
- budget and latency limits

## Outputs
- chosen tier and rationale
- consumption record
- degraded-mode response when over budget

## Failure modes
- Router misjudges complexity and downgrades a hard task
- Router overhead costs more than it saves on cheap requests
- Budget tracked per call but never in aggregate
- Silent quality degradation with no signal to the caller

## Minimal example
```python
tier = classify(query)                     # "simple" | "complex"
model = FLASH if tier == "simple" else PRO
answer = model.invoke(query)
budget.charge(model.cost(answer))          # track aggregate, not per call
if budget.exhausted: return degrade(answer, notify=True)
```

## Next skills
- If tiering is intent-based: load `routing`
- If work must be ordered by value: load `prioritization`
- If quality drift needs tracking: load `evaluation-and-monitoring`
