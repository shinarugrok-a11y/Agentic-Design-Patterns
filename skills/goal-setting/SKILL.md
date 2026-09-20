---
name: goal-setting
description: Explicit measurable goals plus a progress check loop. Define SMART goals up front and iterate generate -> evaluate -> judge-goals-met until satisfied or budget spent. Do not use when success is not definable or when a single pass is acceptable.
role: [planner]
chapter: 11
token_cost_estimate: 330
chains_with: [planning, evaluation-monitoring, reflection]
---

# Goal Setting and Monitoring

## When to use
- Task has a checklist of success criteria.
- Agent must run unattended and know when it is done.
- Progress must be observable (state, tool outputs).
- Course correction is expected mid-task.

## When NOT to use
- Success is subjective and unmeasurable.
- One-shot response is fine.
- Criteria are enforced externally: use `evaluation-monitoring`.

## Inputs
- Goal list (specific, measurable)
- Max iterations
- Evaluator/judge prompt

## Outputs
- Artifact meeting goals
- Per-iteration feedback
- Boolean goals_met

## Failure modes
- Judge returns prose instead of `True`/`False`; loop never terminates.
- Goals conflict (simple vs. exhaustive edge cases).
- Iteration cap hit silently; unmet goals not reported.
- Goals not restated each iteration; drift.

## Minimal example
```python
goals = ["simple", "handles edge cases", "positive int only"]
for i in range(5):
    code = llm(prompt(use_case, goals, prev_code, feedback))
    feedback = llm(f"Critique vs goals {goals}:\n{code}")
    if llm(f"Goals met? Answer True/False.\n{feedback}").strip().lower() == "true": break
    prev_code = code
```

## Next skills
- If goals need decomposition into steps: load `planning`
- If judging needs a rubric or metrics: load `evaluation-monitoring`
- If critique/refine is the core loop: load `reflection`
