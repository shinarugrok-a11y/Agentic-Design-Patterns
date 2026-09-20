---
name: learning-adaptation
description: Agent changes behaviour from experience (RL, self-modification, evolution). Let the agent update its strategies, prompts or code based on evaluated outcomes over many episodes. Do not use when behaviour must be fixed and auditable or when there is no reliable evaluator.
role: [memory, critic]
chapter: 9
token_cost_estimate: 300
chains_with: [memory-management, reflection, evaluation-monitoring]
---

# Learning and Adaptation

## When to use
- Environment shifts and static rules degrade.
- A benchmark/evaluator can score each version.
- Personalisation over long horizons.
- Algorithm or prompt search (AlphaEvolve, OpenEvolve, SICA).

## When NOT to use
- Regulated behaviour that must not drift.
- No evaluator; 'learning' becomes random drift.
- Single session; use `memory-management` instead.

## Inputs
- Initial program/prompt
- Evaluator returning metrics
- Archive of past versions and scores
- Iteration budget

## Outputs
- Best-scoring version
- Metrics per iteration
- Archive

## Failure modes
- Reward hacking: metric improves, real quality does not.
- Self-modification breaks the agent's own tooling.
- Archive selects on noise; no held-out evaluation.
- Cost: 1000 iterations x full evaluation.

## Minimal example
```python
evolve = OpenEvolve(initial_program_path="prog.py",
                    evaluation_file="evaluator.py", config_path="config.yaml")
best = await evolve.run(iterations=1000)
print(best.metrics)
# SICA loop: pick best archived version -> self-edit code -> benchmark -> archive
```

## Next skills
- If learned facts need storage: load `memory-management`
- If single-output improvement is enough: load `reflection`
- If you need the evaluator itself: load `evaluation-monitoring`
