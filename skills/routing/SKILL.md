---
name: routing
description: Dynamic path selection. Use when input intent should pick a specialist workflow. Do NOT use for a single linear pipeline.
role: [planner, executor]
chapter: 2
token_cost_estimate: 256
chains_with: [prompt-chaining, tool-use]
---

# Routing

## When to use
- Incoming requests span distinct intents (book vs info vs other)
- Need to pick a tool, chain, or sub-agent from context
- Customer-support style triage before specialists run

## When NOT to use
- Every request follows the same stages (load `prompt-chaining`)
- Independent work should run together (load `parallelization`)
- Only one handler exists

## Inputs
- User query or current state
- Closed set of route labels
- Specialist agents/tools

## Outputs
- Selected route id
- Specialist response

## Failure modes
- Wrong label → wrong specialist
- No `unclear` fallback
- Router emits prose instead of a single label

## Minimal example
```python
router = classify_prompt | llm | StrOutputParser()  # booker|info|unclear
branch = RunnableBranch(
    (lambda x: x["decision"] == "booker", booking_handler),
    (lambda x: x["decision"] == "info", info_handler),
    unclear_handler,
)
```

## Next skills
- If the chosen path is a multi-stage pipeline: load `prompt-chaining`
- If the specialist must call APIs: load `tool-use`
