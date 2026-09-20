---
name: evaluation-monitoring
description: Measure accuracy, latency, cost, trajectory; judge with rubrics. Use before and after deploying. Not exact-match for open outputs.
role: [critic]
chapter: 19
token_cost_estimate: 211
chains_with: [learning-adaptation, reflection]
---

# Evaluation and Monitoring

## When to use
- Behaviour must be tracked across versions.
- Open-ended outputs need an LLM judge.
- Production drift must be detected.

## When NOT to use
- Exact-match scoring of paraphrases.
- No ground truth and no rubric.

## Inputs
- Test cases or traces
- Metrics + rubric

## Outputs
- Scores per case
- Trajectory report

## Failure modes
- Exact-match on paraphrase.
- Judge without rubric.
- Metrics without cost/latency.

## Minimal example
```python
verdict = llm(f"""Score 1-5 on accuracy and completeness. Return JSON
{{"accuracy": n, "completeness": n, "reason": "..."}}
Question: {q}\nReference: {ref}\nAnswer: {ans}""")
scores = json.loads(verdict)
```

## Next skills
- If scores drive improvement: load `learning-adaptation`
- If one output needs critique: load `reflection`
