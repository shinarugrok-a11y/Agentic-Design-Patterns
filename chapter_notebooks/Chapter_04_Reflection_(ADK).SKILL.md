---
name: reflection
description: Use when output quality improves with draft-then-critique revision loops. Do not use for latency-critical single-shot answers.
role: [critic]
chapter: 4
token_cost_estimate: 196
chains_with: [reasoning-techniques, evaluation-monitoring]
---

# Reflection

## When to use
- Draft quality matters (writing, code, plans)
- Errors are detectable by a second pass
- Budget allows 2-4 revision rounds

## When NOT to use
- Latency-critical single-shot answers
- No clear quality criteria to critique against
- First draft is already verified correct

## Inputs
- Initial draft plus quality criteria
- Max iteration count

## Outputs
- Revised output
- Critique trace with stop reason

## Failure modes
- Oscillation — stop when critique repeats; cap iterations
- Shared blind spots — use different model/prompt for critic
- Over-polishing — freeze when score stops improving

## Minimal example
```python
draft = run(f"Write paragraph: {topic}")
for _ in range(3):
    notes = critique(draft, ["accuracy", "clarity"])
    if notes.clean: break
    draft = run(f"Revise: {draft} per {notes}")
```

## Next skills
- If need deeper self-correction prompts: load `reasoning-techniques`
- If need scored quality gates: load `evaluation-monitoring`
