---
name: exploration-discovery
description: Use when the agent must autonomously explore and surface novel findings. Do not use when the task has a fixed known answer.
role: [planner, critic]
chapter: 21
token_cost_estimate: 173
chains_with: [reasoning-techniques, evaluation-monitoring]
---

# Exploration and Discovery

## When to use
- Open question, unknown answer
- Need agents to propose + review ideas
- Budget for explore-then-synthesize

## When NOT to use
- Fixed known answer exists
- No budget for open-ended work
- Findings can't be validated

## Inputs
- Research question + scope
- Explore budget and review bar

## Outputs
- Experiment reports
- Reviewer-approved insights

## Failure modes
- No synthesis — force finalize step with deadline
- Fake novelty — require experiments, not opinions
- No review — harsh reviewer gate before publishing

## Minimal example
```python
plan = propose(question)
report = run_experiments(plan)
insights = review(report)  # harsh gate
return synthesize(insights)
```

## Next skills
- If deepen the reasoning loop: load `reasoning-techniques`
- If validate findings rigorously: load `evaluation-monitoring`
