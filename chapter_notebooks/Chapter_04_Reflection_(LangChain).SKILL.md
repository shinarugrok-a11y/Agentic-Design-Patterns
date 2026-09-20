---
name: reflection
description: Generate, critique, revise. Use when first-pass quality is unreliable. Do NOT use for cheap one-shot tasks.
role: [critic]
chapter: 4
token_cost_estimate: 255
chains_with: [prompt-chaining, evaluation-monitoring]
---

# Reflection

## When to use
- First draft is often wrong (facts, code, style)
- You have a rubric or critic role distinct from the writer
- Goal is generate → critique → revise until pass or max N

## When NOT to use
- One-shot output is acceptable
- No stop condition or evaluator exists
- Latency budget forbids extra LLM calls

## Inputs
- Task + current draft
- Critic instructions / structured review schema
- Max iterations and pass token (e.g. `CODE_IS_PERFECT`)

## Outputs
- Revised artifact
- Critique status + reasoning

## Failure modes
- No stop token → unbounded loops
- Writer and critic collapse into one voice
- Structured review dict fails to parse

## Minimal example
```python
draft = generator.run(task)
for _ in range(max_n):
    critique = critic.run(draft)
    if "CODE_IS_PERFECT" in critique:
        break
    draft = refiner.run(draft, critique)
```

## Next skills
- If critique is a scored rubric in prod: load `evaluation-monitoring`
- If generate/refine are explicit stages: load `prompt-chaining`
