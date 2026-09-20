---
name: exploration-discovery
description: Autonomously explore, hypothesize, and verify with reviewer gates.
role: [planner, critic]
chapter: 21
token_cost_estimate: 203
chains_with: [reasoning-techniques, evaluation-monitoring]
---

# Exploration and Discovery

## When to use
- Problem is open-ended; hypotheses must be generated.
- Reviewer agents score plans before expensive steps.
- Phased roles fit: professor/postdoc/reviewer style.

## When NOT to use
- Task has a known answer; direct solving is faster.
- No budget for exploratory dead ends.

## Inputs
- Research question + exploration budget
- Reviewer rubric + phase roles

## Outputs
- Ranked findings + verified artifacts

## Failure modes
- Unbounded exploration burns budget; cap steps.
- Weak reviewers pass flawed plans.
- Findings never converge into a deliverable.

## Minimal example
```python
plan = professor.propose(question)
score = reviewers.get_score(plan, report)
if score > bar: postdoc.execute(plan, max_steps=100)
```

## Next skills
- If hypotheses need rigorous inference: load `reasoning-techniques`
- If findings need scoring: load `evaluation-monitoring`
