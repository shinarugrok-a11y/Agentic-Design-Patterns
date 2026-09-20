---
name: reasoning-techniques
description: Use when decisions need explicit step-by-step or self-correcting reasoning. Do not use for simple lookups with direct answers.
role: [critic]
chapter: 17
token_cost_estimate: 183
chains_with: [reflection, tool-use]
---

# Reasoning Techniques

## When to use
- Multi-hop questions need shown work
- Answers need verification passes
- Research needs generate->search->reflect loops

## When NOT to use
- Direct lookup with one answer
- Latency forbids multi-step thought
- Reasoning trace adds no trust

## Inputs
- Question plus strategy (CoT, self-correct, research)
- Tool access for grounding

## Outputs
- Step-by-step trace
- Final answer with checks

## Failure modes
- Rambling traces — demand numbered steps + verdict
- Harmful edits — diff self-corrections, revert on doubt
- Loop spin — cap research rounds, force finalize

## Minimal example
```python
steps = cot(query)  # analyze -> queries -> evidence
draft = answer(steps)
final = self_correct(draft, requirements)
return final
```

## Next skills
- If iterate the draft further: load `reflection`
- If ground steps in search/code: load `tool-use`
