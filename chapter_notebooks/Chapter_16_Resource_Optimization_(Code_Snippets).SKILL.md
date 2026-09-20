---
name: resource-optimization
description: Use when cost, latency, or model tier must be optimized per request. Do not use when quality demands the best model for every call.
role: [planner]
chapter: 16
token_cost_estimate: 183
chains_with: [routing, evaluation-monitoring]
---

# Resource-Aware Optimization

## When to use
- Mixed workload (easy + hard queries)
- Budget or latency SLOs exist
- Cheap pre-filter can triage

## When NOT to use
- All tasks need frontier quality
- Workload is tiny (savings negligible)
- No SLOs to optimize against

## Inputs
- Query complexity signal
- Tier table (pro vs flash, cache policy)

## Outputs
- Selected tier + justification
- Spend/latency delta

## Failure modes
- Silent downgrade — verify hard tasks on strong tier
- Stale cache — TTL + invalidation rules
- Over-engineering — measure savings before adding tiers

## Minimal example
```python
tier = "flash" if simple(query) else "pro"
answer = run_tier(tier, query)  # cached when repeat
log(cost(tier), latency)
```

## Next skills
- If route by request type: load `routing`
- If prove quality held: load `evaluation-monitoring`
