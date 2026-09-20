# Exploration and Discovery — patterns (Ch 21)

## Pattern
1. Generate many hypotheses for a goal.
2. Review each with several personas.
3. Rank; evolve the top candidates.
4. Stop after N rounds or no improvement.

## Prompt template
```
Proposer: Propose a novel, testable hypothesis for {goal}. State mechanism and a test.
Reviewer ({persona}): Score novelty, feasibility, impact 1-5 with one sentence each.
```

## Key APIs
- Google Co-Scientist: generate -> reflect -> rank -> evolve loop.
- Agent Laboratory: PhD/Postdoc/Professor roles across literature, experiments, writing.
- Structured review: JSON scores per persona; aggregate for ranking.

## Pitfalls -> fixes
- Groupthink -> diverse personas, blind reviews.
- Unbounded rounds -> round cap.
- Novel but infeasible -> weight feasibility.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_21_*`.
