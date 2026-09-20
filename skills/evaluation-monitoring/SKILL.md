---
name: evaluation-monitoring
description: Use when agent quality must be scored, judged, or tracked over time. Do not use for one-off demos with no quality bar.
role: [critic]
chapter: 19
token_cost_estimate: 195
chains_with: [reflection, learning-adaptation]
---

# Evaluation and Monitoring

## When to use
- Need pass/fail on agent outputs
- Need LLM-judge for open-ended quality
- Need regression tracking over releases

## When NOT to use
- One-off demo, no bar to meet
- No ground truth or rubric exists
- Scores won't change any decision

## Inputs
- Outputs + expected/rubric
- Judge model + logging config

## Outputs
- Score per output + aggregate
- Regression alerts

## Failure modes
- Vanity metrics — pair exact-match with judge + human spot-checks
- Judge bias — blind judges, rotate models, calibrate
- No history — log every score with version + prompt hash

## Minimal example
```python
s = accuracy(agent_out, expected)  # exact match
v = judge(agent_out, rubric)  # LLM-as-judge
log(version, prompt_hash, s, v)
```

## Next skills
- If fix what scores flagged: load `reflection`
- If improve policy from scores: load `learning-adaptation`
