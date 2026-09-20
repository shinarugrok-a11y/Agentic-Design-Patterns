---
name: reflection
description: Self-correction through critique and revision. Critique a draft against explicit criteria and regenerate it until the criteria are met. Skip it when latency or cost matters more than output quality.
role: [critic]
chapter: 4
token_cost_estimate: 360
chains_with: [evaluation-and-monitoring, reasoning-techniques, prompt-chaining]
---

# Reflection

## When to use
- Output quality outranks latency and cost
- Explicit criteria exist to judge against
- Task is long-form text, code, or a plan

## When NOT to use
- Response is time- or cost-critical
- No objective criteria to critique against
- The producer is also the only available critic on a high-stakes task

## Inputs
- draft output
- evaluation criteria or rubric
- max iteration count

## Outputs
- structured critique
- revised output
- stop reason

## Failure modes
- Loop never converges without a hard iteration cap
- Self-critique rubber-stamps its own errors; use a separate critic
- Accumulated drafts overflow the context window
- Cost and latency multiply by the number of iterations

## Minimal example
```python
draft = producer(task)
for _ in range(MAX_ITERS):
    critique = critic(draft, CRITERIA)     # separate agent, not self
    if critique["verdict"] == "pass":
        break
    draft = producer(task, feedback=critique["issues"])
```

## Next skills
- If you need repeatable scoring: load `evaluation-and-monitoring`
- If the critique needs explicit inference: load `reasoning-techniques`
- If revision spans stages: load `prompt-chaining`
