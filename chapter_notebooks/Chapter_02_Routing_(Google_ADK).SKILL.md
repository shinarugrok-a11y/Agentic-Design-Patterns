---
name: routing
description: Use when incoming requests fall into distinct types needing different handlers. Do not use when one handler can cover all inputs uniformly.
role: [planner, executor]
chapter: 2
token_cost_estimate: 194
chains_with: [prompt-chaining, tool-use]
---

# Routing

## When to use
- Requests fall into distinct types (refund vs tech-support)
- Handlers need different models, tools, or prompts
- Cost/quality trade-off differs per request type

## When NOT to use
- One handler covers all inputs well
- Only 1-2 trivial branches (use if/else)
- Classification cost exceeds handling cost

## Inputs
- Request text plus handler registry
- Router prompt or confidence threshold

## Outputs
- Chosen route with confidence
- Handler output

## Failure modes
- Silent misclassification — log route + confidence always
- Route explosion — merge routes with similar handling
- Default-route gap — always define a fallback handler

## Minimal example
```python
route = classify(req, ["billing", "tech", "other"])
handler = {"billing": bill_agent, "tech": tech_agent,
           "other": general_agent}[route.label]
return handler(req)
```

## Next skills
- If route needs multi-step work: load `prompt-chaining`
- If route needs external data: load `tool-use`
