---
name: evaluation-and-monitoring
description: Continuous scoring of outputs and trajectories. Score outputs and trajectories against defined metrics continuously, in development and in production. Skip formal evaluation for throwaway one-off runs nobody will depend on.
role: [critic]
chapter: 19
token_cost_estimate: 380
chains_with: [reflection, goal-setting-and-monitoring, learning-and-adaptation]
---

# Evaluation and Monitoring

## When to use
- Agent is deployed or about to be
- Versions, prompts, or models must be compared
- Drift, regressions, or anomalies must be caught

## When NOT to use
- One-off throwaway run nobody depends on
- No ground truth or rubric can be defined
- Judge cost exceeds the value of the signal

## Inputs
- test cases or evalset with ground truth
- metric definitions
- production traces

## Outputs
- metric scores and pass/fail
- trajectory diff against the ideal path
- drift and anomaly alerts

## Failure modes
- Only final answers scored, so bad trajectories pass
- LLM-as-judge inherits the generator's bias
- Metrics that no longer track user value
- Drift undetected because no baseline was stored

## Minimal example
```python
for case in evalset:
    out, traj = agent.run(case.input, trace=True)
    scores = {"match": score(out, case.expected),
              "trajectory": traj_diff(traj, case.ideal_steps),
              "tokens": traj.token_usage, "latency_ms": traj.ms}
    report(case.id, scores); alert_if_drift(scores, baseline[case.id])
```

## Next skills
- If a run needs fixing in place: load `reflection`
- If metrics track an objective: load `goal-setting-and-monitoring`
- If scores should drive updates: load `learning-and-adaptation`
