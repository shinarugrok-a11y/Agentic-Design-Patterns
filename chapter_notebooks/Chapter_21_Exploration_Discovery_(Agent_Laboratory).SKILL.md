---
name: exploration-discovery
description: Generate, review, rank, evolve hypotheses. Use in open-ended domains. Not for well-defined optimisation.
role: [planner, critic]
chapter: 21
token_cost_estimate: 211
chains_with: [reflection, planning]
---

# Exploration and Discovery

## When to use
- Open-ended research question.
- Many candidate hypotheses to compare.
- Multi-persona review adds signal.

## When NOT to use
- Well-defined optimisation: use `planning`.
- Answer exists in a corpus: use `rag`.

## Inputs
- Research goal
- Review personas + criteria

## Outputs
- Ranked hypotheses
- Review reports

## Failure modes
- Reviewer groupthink.
- Unbounded rounds.
- Novelty without feasibility.

## Minimal example
```python
hyps = [llm(f"Propose a novel hypothesis for {goal}") for _ in range(k)]
reviews = {h: [llm(f"As {p}, review: {h}") for p in personas] for h in hyps}
ranked = sorted(hyps, key=lambda h: score(reviews[h]), reverse=True)
```

## Next skills
- If reviews need structure: load `reflection`
- If top hypothesis needs a plan: load `planning`
