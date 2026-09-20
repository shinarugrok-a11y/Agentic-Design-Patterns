---
name: reasoning-techniques
description: Explicit multi-step inference (CoT, ToT, ReAct, self-correction). Use for hard problems. Do NOT use for simple lookups.
role: [critic]
chapter: 17
token_cost_estimate: 230
chains_with: [reflection, planning]
---

# Reasoning Techniques

## When to use
- Multi-step logic, math, or research synthesis
- Protocols: CoT, Tree-of-Thoughts, ReAct, self-correction, DeepSearch
- Root agent delegates to search and code specialists

## When NOT to use
- Factual lookup or short rewrite
- You only need a writer/critic pair (load `reflection`)
- You need an action plan more than a thought trace (load `planning`)

## Inputs
- Question + process prompt
- Optional search/code tools
- Stop when ready to finalize

## Outputs
- Intermediate thoughts / tree / tool traces
- Final answer

## Failure modes
- Decorative step lists, wrong answer
- Graph compiled without node bodies
- Reflection never terminates

## Minimal example
```python
root = Agent(name="RootAgent", tools=[
    AgentTool(agent=search_agent),
    AgentTool(agent=code_agent),
])
```

## Next skills
- If the loop is draft/critique: load `reflection`
- If you need an executable plan: load `planning`
