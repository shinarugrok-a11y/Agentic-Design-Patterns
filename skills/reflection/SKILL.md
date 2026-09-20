---
name: reflection
description: Generate, critique, then refine output in a loop.
role: [critic]
chapter: 4
token_cost_estimate: 239
chains_with: [evaluation-monitoring, planning]
---

# Reflection

## When to use
- First-draft output needs measurable improvement.
- You can state explicit critique criteria.
- 2-4 refinement passes fit the latency budget.

## When NOT to use
- Output is already good enough; extra passes waste budget.
- No reliable critic or rubric exists.

## Inputs
- Draft output + critique rubric
- Max iterations + stop condition

## Outputs
- Refined output + critique trail

## Failure modes
- Critic and generator agree too easily; no real improvement.
- Loop oscillates instead of converging; needs a stop rule.
- Over-refinement strips correct content.

## Minimal example
```python
draft = llm(f"Write ad copy: {brief}")
for _ in range(3):
    notes = llm(f"Critique against {rubric}: {draft}")
    if "PASS" in notes: break
    draft = llm(f"Revise using {notes}: {draft}")
```

## Next skills
- If refined output needs scoring before release: load `evaluation-monitoring`
- If critique reveals the plan itself is wrong: load `planning`
