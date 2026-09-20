---
name: exploration-discovery
description: Multi-agent hypothesis generation, review, ranking and evolution. Search an open-ended problem space by generating hypotheses, critiquing them with independent reviewers, and evolving the best. Do not use for well-defined optimisation with a known solution path.
role: [planner, critic]
chapter: 21
token_cost_estimate: 340
chains_with: [multi-agent, reflection, planning]
---

# Exploration and Discovery

## When to use
- Solution space is undefined ('unknown unknowns').
- Research, market scanning, creative generation.
- Multiple reviewer personas reduce single-critic bias.
- Long-running autonomous investigation.

## When NOT to use
- Known procedure with a known answer.
- Budget cannot absorb many generate/review rounds.
- Safety review of novel actions is unavailable.

## Inputs
- Research question/domain
- Role prompts (generator, reviewers, ranker, evolver)
- Scoring schema
- Round budget

## Outputs
- Ranked hypotheses
- Structured reviews (JSON)
- Report/README artifact

## Failure modes
- Reviewers converge on the same critique; no diversity.
- Elo/ranking rewards persuasiveness over correctness.
- Unbounded rounds.
- Experiments run without safety gate.

## Minimal example
```python
reviewers = ["harsh but fair, wants insight", "harsh, wants impact", "open-minded, wants novelty"]
reviews = [llm(REVIEW_JSON_TEMPLATE, persona=p, plan=plan, report=report) for p in reviewers]
# JSON: Summary, Strengths, Weaknesses, Originality 1-4, ... Overall 1-10, Decision Accept|Reject
ranked = rank(hypotheses, reviews)          # Co-Scientist: Elo tournament
next_gen = evolve(ranked[:k])               # simplify, synthesise, recombine
```

## Next skills
- If roles need orchestration: load `multi-agent`
- If single-output critique suffices: load `reflection`
- If promising hypothesis needs an execution plan: load `planning`
