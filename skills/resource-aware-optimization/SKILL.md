---
name: resource-aware-optimization
description: Spend cheaper/faster models unless the task needs more. Use under cost or latency caps. Do NOT default every call to the largest model.
role: [planner]
chapter: 16
token_cost_estimate: 243
chains_with: [routing, prioritization]
---

# Resource-Aware Optimization

## When to use
- Strict $ / token / latency / device limits
- Simple vs reasoning vs search should hit different models
- Graceful degradation beats hard failure

## When NOT to use
- One model meets SLA and budget
- You are choosing *what* to do, not *how expensive* (load `prioritization`)
- Classification itself costs more than it saves

## Inputs
- User prompt
- Tiers (flash/mini vs pro/o-series)
- Optional search path

## Outputs
- `{classification, model, response}`
- Spend/latency telemetry

## Failure modes
- Word-count routing is a toy
- High-temperature classifier jitter
- Cheap model fails with no escalate

## Minimal example
```python
cls = classify_prompt(prompt)["classification"]  # simple|reasoning|internet_search
ctx = google_search(prompt) if cls == "internet_search" else None
answer, model = generate_response(prompt, cls, ctx)
```

## Next skills
- If routing is by intent not cost: load `routing`
- If many tasks compete for budget: load `prioritization`
