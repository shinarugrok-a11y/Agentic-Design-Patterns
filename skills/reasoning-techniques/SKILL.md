---
name: reasoning-techniques
description: Explicit multi-step inference before answering. Make intermediate reasoning explicit with chain-of-thought, tree search, ReAct, or self-correction before answering. Skip it for lookups and formatting where one pass is already correct.
role: [critic]
chapter: 17
token_cost_estimate: 380
chains_with: [reflection, planning, tool-use]
---

# Reasoning Techniques

## When to use
- Problem needs multi-step logical inference
- Several solution paths deserve comparison
- Showing the work matters as much as the answer

## When NOT to use
- Lookup, extraction, or formatting task
- Inference budget or latency is tight
- The trace would leak sensitive detail to users

## Inputs
- problem statement
- technique choice (CoT, ToT, ReAct, self-correction)
- inference budget

## Outputs
- reasoning trace
- candidate paths with scores
- final verified answer

## Failure modes
- Fluent but wrong reasoning traces that read as justification
- Tree search explodes combinatorially without pruning
- ReAct loops repeat the same failed action
- Traces leaked to users expose internal or sensitive detail

## Minimal example
```python
# ReAct: reason, act, observe, repeat under a step cap
for _ in range(MAX_STEPS):
    thought, action = llm_step(history)
    if action.name == "final": return action.answer
    observation = tools[action.name](**action.args)
    history += [thought, action, observation]
    if repeated(action, history): break     # break stuck loops
```

## Next skills
- If answers need revision: load `reflection`
- If reasoning yields a step list: load `planning`
- If steps need external data: load `tool-use`
