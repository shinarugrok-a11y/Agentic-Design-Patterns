---
name: parallelization
description: Concurrent execution of independent sub-tasks. Run independent LLM calls or tool calls at the same time, then merge results in one synthesis step. Do not use when steps depend on each other's output or when the merge step cannot reconcile results.
role: [executor]
chapter: 3
token_cost_estimate: 320
chains_with: [multi-agent, prompt-chaining, routing]
---

# Parallelization

## When to use
- Several sub-tasks share the same input but not each other's output.
- Fan-out research (3 topics, 3 APIs) then one merge.
- Latency is dominated by external I/O waits.
- Same prompt must run over many chunks.

## When NOT to use
- Step B needs step A's output: use `prompt-chaining`.
- Only one branch should run: use `routing`.
- Debug/logging budget is tight; concurrency adds complexity.

## Inputs
- Shared input
- List of independent branches
- Merge/synthesis prompt

## Outputs
- Per-branch results keyed by name
- Single synthesised result

## Failure modes
- One slow or failing branch blocks the whole join.
- Merge step hallucinates beyond branch outputs unless told to ground strictly.
- Rate limits hit when N branches call the same API at once.
- Shared mutable state raced between branches.

## Minimal example
```python
branches = RunnableParallel(summary=sum_chain, questions=q_chain,
                            terms=terms_chain, topic=passthrough)
result = (branches | synth_prompt | llm).invoke(topic)
# ADK: SequentialAgent([ParallelAgent([r1, r2, r3]), merger_agent])
# each r_i writes output_key; merger reads {r1_result}...
```

## Next skills
- If branches are specialist agents: load `multi-agent`
- If a branch is itself sequential: load `prompt-chaining`
- If only some branches should run: load `routing`
