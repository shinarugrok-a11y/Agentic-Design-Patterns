---
name: learning-and-adaptation
description: Improve behavior from experience (evolution, traces, online updates). Use in changing environments. Do NOT use for frozen prompts.
role: [memory, critic]
chapter: 9
token_cost_estimate: 234
chains_with: [reflection, memory-management]
---

# Learning and Adaptation

## When to use
- Environment or user prefs change over time
- Code/prompt population should evolve against an evaluator (OpenEvolve, SICA)
- Personalization from stored outcomes

## When NOT to use
- Fixed task with a frozen prompt
- One-off critique of a draft (load `reflection`)
- Only need to store facts, not change policy (load `memory-management`)

## Inputs
- Seed program or policy
- Evaluation function + metrics
- Iteration / population config

## Outputs
- Best program + metric dict
- Adapted behavior

## Failure modes
- Optimizes the proxy, not the real goal
- Self-modifying code without a sandbox
- Missing evaluator files (notebook is a stub)

## Minimal example
```python
evolve = OpenEvolve(initial_program_path=..., evaluation_file=..., config_path=...)
best = await evolve.run(iterations=1000)
print(best.metrics)
```

## Next skills
- If adaptation is critique-in-the-loop only: load `reflection`
- If you only persist experience: load `memory-management`
