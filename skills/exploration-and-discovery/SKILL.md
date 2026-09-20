---
name: exploration-and-discovery
description: Generate, critique, and evolve hypotheses. Generate, critique, and evolve hypotheses to surface unknown unknowns in an open-ended problem space. Skip it when the solution space is known and the task is to optimize within it.
role: [planner, critic]
chapter: 21
token_cost_estimate: 380
chains_with: [prioritization, reasoning-techniques, evaluation-and-monitoring]
---

# Exploration and Discovery

## When to use
- Solution space is open-ended
- The objective is novel hypotheses, not optimization
- Unknown unknowns must be surfaced

## When NOT to use
- The target is known - optimize instead
- Actions would touch irreversible real systems
- No budget or stopping rule can be set

## Inputs
- open-ended research question
- hypothesis generation and review roles
- experiment or search budget

## Outputs
- ranked hypotheses
- experiment results and evidence
- new knowledge write-up

## Failure modes
- Unbounded search burns budget with no stopping rule
- Plausible-sounding hypotheses never empirically tested
- Generator and reviewer collapse onto the same bias
- Exploration triggers irreversible actions on real systems

## Minimal example
```python
pool = generator(question, n=8)
for _ in range(ROUNDS):                      # bounded search
    reviewed = [reviewer(h) for h in pool]   # independent critic role
    top = rank(reviewed)[:3]
    pool = top + [evolve(h) for h in top]
return experiment(top[0], sandbox=True)      # never test on live systems
```

## Next skills
- If candidates exceed capacity: load `prioritization`
- If hypotheses need derivation: load `reasoning-techniques`
- If results need scoring: load `evaluation-and-monitoring`
