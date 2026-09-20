---
name: evaluation-monitoring
description: Score quality, latency, tokens, and goal drift in production. Use after you can run the agent. Do NOT use exact-match as the only metric.
role: [critic]
chapter: 19
token_cost_estimate: 252
chains_with: [reflection, goal-setting]
---

# Evaluation and Monitoring

## When to use
- Production or regression suites
- Mix exact-match, latency, tokens, LLM-as-judge JSON rubrics
- Detect anomalies vs a goal or contract between agents

## When NOT to use
- Still exploring a prompt (load `reflection` first)
- You only need an in-loop True/False (load `goal-setting`)
- No gold set and no rubric

## Inputs
- Agent output + expected or rubric
- Timing wrappers
- Judge model + mime JSON

## Outputs
- `overall_score` / pass-fail
- `latency_ms`, token estimates
- `prompt_feedback` on blocks

## Failure modes
- Exact-match false negatives
- `len(text.split())` ≠ tokens
- Empty `response.parts` (safety)

## Minimal example
```python
ok = agent_output.strip().lower() == expected.strip().lower()
t0 = time.perf_counter(); result = fn(); ms = (time.perf_counter()-t0)*1000
```

## Next skills
- If eval is an inner critique loop: load `reflection`
- If eval is a SMART stop condition: load `goal-setting`
