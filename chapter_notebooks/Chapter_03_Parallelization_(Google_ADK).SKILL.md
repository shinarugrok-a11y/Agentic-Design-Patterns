---
name: parallelization
description: Concurrent independent sub-tasks. Use for fan-out then one merge. Not when steps depend on each other.
role: [executor]
chapter: 3
token_cost_estimate: 210
chains_with: [multi-agent, prompt-chaining]
---

# Parallelization

## When to use
- Branches share the input, not each other's output.
- Fan-out research or many chunks, one synthesis.
- Latency is dominated by I/O waits.

## When NOT to use
- Step B needs step A: use `prompt-chaining`.
- Only one branch should run: use `routing`.

## Inputs
- Shared input
- Independent branches + merge prompt

## Outputs
- Per-branch results keyed by name
- Synthesised result

## Failure modes
- One slow or failed branch blocks the join.
- Merge hallucinates beyond branch outputs.
- Rate limits when N branches hit one API.

## Minimal example
```python
branches = RunnableParallel(summary=sum_chain, questions=q_chain,
                            topic=RunnablePassthrough())
result = (branches | synth_prompt | llm).invoke(topic)
```

## Next skills
- If branches are specialist agents: load `multi-agent`
- If a branch is itself sequential: load `prompt-chaining`
