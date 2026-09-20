---
name: evaluation-monitoring
description: Metrics, trajectories and LLM-as-judge for continuous assessment. Measure accuracy, latency, tokens and trajectory quality, and use a rubric-driven LLM judge for subjective outputs. Do not use exact-match scoring for open-ended outputs or ship a judge without checking it against human labels.
role: [critic]
chapter: 19
token_cost_estimate: 350
chains_with: [reflection, guardrails, learning-adaptation]
---

# Evaluation and Monitoring

## When to use
- Agent runs in production; drift is possible.
- Comparing agent/model versions (A/B).
- Compliance or safety audit needed.
- Subjective quality (helpfulness, neutrality) must be scored.

## When NOT to use
- Prototype with no baseline yet.
- Output is deterministic and unit-testable.
- Judge model shares the bias under test.

## Inputs
- Agent outputs + expected outputs
- Trajectory (actions taken)
- Rubric with 1-5 criteria
- Latency/token logs

## Outputs
- Scores (accuracy, per-criterion)
- Latency ms, token counts
- Judge JSON: score, rationale, action

## Failure modes
- Exact-match scores 0 for paraphrased correct answers.
- Judge prompt without rubric: inconsistent scores.
- Token counts by `split()`; misleading cost.
- Evaluating final answer only; ignoring a bad trajectory.

## Minimal example
```python
RUBRIC = "Score 1-5 on clarity, neutrality, relevance, completeness, audience. Return JSON: overall_score, rationale, detailed_feedback, concerns, recommended_action"
judgment = json.loads(model.generate(RUBRIC + question, response_mime_type="application/json").text)
def timed(fn, *a):
    t = perf_counter(); r = fn(*a); return r, (perf_counter() - t) * 1000
# ADK: evalset files + pytest for CI
```

## Next skills
- If scores should drive refinement: load `reflection`
- If failing scores should block outputs: load `guardrails`
- If scores should update the agent over time: load `learning-adaptation`
