---
name: parallelization
description: Concurrent execution of independent subtasks. Run independent subtasks concurrently and join their results before the next step. Skip it when a subtask needs another's output or shared state is mutated.
role: [executor]
chapter: 3
token_cost_estimate: 350
chains_with: [multi-agent-collaboration, prompt-chaining, resource-aware-optimization]
---

# Parallelization

## When to use
- Subtasks share no data dependency
- Work is I/O bound (APIs, search, databases)
- Latency, not quality, is the bottleneck

## When NOT to use
- Any subtask consumes another's output
- Rate limits or budget cannot absorb the fan-out
- Debuggability matters more than speed

## Inputs
- list of independent subtasks
- concurrency limit
- aggregation prompt or function

## Outputs
- per-branch results
- merged synthesis
- partial-failure report

## Failure modes
- Hidden dependency between branches yields inconsistent results
- Rate limits or quota exhaustion from burst fan-out
- One branch fails and the aggregator receives nothing
- Interleaved logs make debugging and tracing hard

## Minimal example
```python
async def run(topic):
    results = await asyncio.gather(*(agent(topic) for agent in BRANCHES),
                                   return_exceptions=True)
    ok = [r for r in results if not isinstance(r, Exception)]
    return synthesize(ok)  # handle partial failure explicitly
```

## Next skills
- If branches need distinct expertise: load `multi-agent-collaboration`
- If the merged result feeds more stages: load `prompt-chaining`
- If fan-out risks budget: load `resource-aware-optimization`
