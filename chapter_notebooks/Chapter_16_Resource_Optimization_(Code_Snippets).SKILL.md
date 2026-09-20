---
name: resource-aware-optimization
description: Pick model, tool and depth based on cost, latency and complexity. Classify request complexity first, then route to the cheapest model or path that meets quality. Do not use when a single model already meets budget and latency, or when quality must be maximal regardless of cost.
role: [planner]
chapter: 16
token_cost_estimate: 350
chains_with: [routing, prioritization, evaluation-monitoring]
---

# Resource-Aware Optimization

## When to use
- Strict API/compute budget.
- Latency-sensitive or edge deployment.
- Mixed workload: trivial and hard queries.
- Need fallback/degradation under load.

## When NOT to use
- Cost is irrelevant; always use the best model.
- Classifier cost exceeds savings.
- Task ordering, not model choice, is the issue: use `prioritization`.

## Inputs
- Request
- Complexity classifier (LLM or heuristic)
- Model tiers with cost
- Budget/latency constraints

## Outputs
- Chosen model/path
- Response
- Cost/latency record
- Critique feedback for the router

## Failure modes
- Classifier mislabels hard queries as simple; quality silently drops.
- Word-count heuristics proxy poorly for difficulty.
- No critique loop; routing never improves.
- Cheap model lacks tool support the path needs.

## Minimal example
```python
cls = llm_json("Classify: simple|reasoning|internet_search", prompt)["classification"]
model = {"simple": "gpt-4o-mini", "reasoning": "o4-mini", "internet_search": "gpt-4o"}[cls]
ctx = web_search(prompt) if cls == "internet_search" else ""
answer = call(model, f"{ctx}\n{prompt}")
# ADK: QueryRouterAgent -> gemini_flash_agent | gemini_pro_agent; CriticAgent reviews
```

## Next skills
- If routing logic itself: load `routing`
- If many tasks compete for the budget: load `prioritization`
- If need cost/latency metrics: load `evaluation-monitoring`
