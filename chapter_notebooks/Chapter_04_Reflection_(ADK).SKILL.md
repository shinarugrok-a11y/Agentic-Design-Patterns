---
name: reflection
description: Generate, critique, refine loop. Improve an output by having a critic (self or separate agent) evaluate it and feed critique into a refinement pass. Do not use for cheap, low-stakes outputs or when no clear evaluation criteria exist.
role: [critic]
chapter: 4
token_cost_estimate: 350
chains_with: [evaluation-monitoring, goal-setting, reasoning-techniques]
---

# Reflection

## When to use
- Output must meet explicit criteria (correctness, style, requirements).
- Code generation where a review can catch bugs before use.
- Quality matters more than latency or cost.
- A stopping signal (e.g. `CODE_IS_PERFECT`) can be defined.

## When NOT to use
- Simple factual answers; critique adds cost, not quality.
- No objective criteria: critic and producer will loop.
- Hard latency budget.

## Inputs
- Task/requirements
- Draft output
- Critic criteria
- Max iterations

## Outputs
- Refined output
- Critique history
- Stop reason (approved | max_iter)

## Failure modes
- No stop condition: infinite refine loop, cost blow-up.
- Same model as producer and critic shares blind spots.
- Critique is vague ('improve clarity') so refinement drifts.
- History grows past the context window after few iterations.

## Minimal example
```python
draft = llm(task)
for i in range(max_iter):
    critique = llm(f"Review against task. Say CODE_IS_PERFECT if done.\n{task}\n{draft}")
    if "CODE_IS_PERFECT" in critique: break
    draft = llm(f"Refine using critique:\n{critique}\n{draft}")
# ADK: SequentialAgent([generator(output_key=draft), reviewer(reads draft)])
```

## Next skills
- If critic needs formal metrics or a judge rubric: load `evaluation-monitoring`
- If stop criteria are goals to track: load `goal-setting`
- If critique should drive multi-path search: load `reasoning-techniques`
