---
name: goal-setting
description: Define explicit goals and iterate until they are met.
role: [planner]
chapter: 11
token_cost_estimate: 210
chains_with: [evaluation-monitoring, reflection]
---

# Goal Setting and Monitoring

## When to use
- Output must satisfy checkable goals.
- Iterate generate -> check goals -> fix until pass.
- Goals are explicit strings the checker can evaluate.

## When NOT to use
- Success is subjective with no testable criteria.
- One shot is enough; iteration adds no value.

## Inputs
- Goal list
- Max iterations + checker function

## Outputs
- Artifact passing all goals + iteration log

## Failure modes
- Vague goals the checker cannot evaluate.
- goals_met() false-positives stop iteration early.
- Infinite polish loop; enforce max_iterations.

## Minimal example
```python
goals = ["has tests", "typed args"]
code = generate(use_case)
while not goals_met(check(code), goals) and iters < 5:
    code = revise(code, feedback(code, goals))
```

## Next skills
- If goal checks need independent scoring: load `evaluation-monitoring`
- If missed goals need targeted revision: load `reflection`
