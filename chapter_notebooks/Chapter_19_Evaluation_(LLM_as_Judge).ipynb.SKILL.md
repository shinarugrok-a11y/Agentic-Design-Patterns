---
name: evaluation-monitoring
description: Score outputs with metrics and LLM judges; monitor live.
role: [critic]
chapter: 19
token_cost_estimate: 203
chains_with: [reflection, goal-setting]
---

# Evaluation and Monitoring

## When to use
- Quality must be tracked across versions or time.
- Combine deterministic metrics + LLM-as-judge.
- Monitor live: latency, tokens, errors, drift.

## When NOT to use
- No ground truth or rubric exists yet.
- One-off prototype with no users.

## Inputs
- Agent outputs + expectations
- Live stream: latency, tokens, errors

## Outputs
- Scores + judge verdicts + drift alerts

## Failure modes
- LLM judge favors verbosity over correctness.
- Metric gaming: optimizing the score, not quality.
- No baseline; cannot tell if a change helped.

## Minimal example
```python
acc = evaluate_response_accuracy(out, expected)
verdict = LLMJudgeForLegalSurvey().judge_survey_question(q)
monitor.record_interaction(prompt, response)
```

## Next skills
- If low scores need revision loops: load `reflection`
- If scores become release goals: load `goal-setting`
