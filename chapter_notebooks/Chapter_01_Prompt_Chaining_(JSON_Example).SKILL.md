---
name: prompt-chaining
description: Sequential task decomposition. Use when a task has clear stages where the output of one feeds the next. Do NOT use for independent parallel tasks.
role: [executor]
chapter: 1
token_cost_estimate: 246
chains_with: [routing, tool-use]
---

# Prompt Chaining

## When to use
- Task splits into ordered stages (extract → transform → validate)
- One prompt drops constraints or mixes incompatible instructions
- Need parsers, schemas, or tools between LLM calls

## When NOT to use
- Stages are independent (load `parallelization`)
- Next step depends on classified intent (load `routing`)
- A single focused prompt already meets quality

## Inputs
- Source text or user goal
- Per-stage prompt templates
- Intermediate schema (JSON keys, parser)

## Outputs
- Final transformed artifact
- Named intermediates for debug/replay

## Failure modes
- Bad stage-1 output poisons the rest of the chain
- Passing raw prose instead of structured fields drops data
- Extra hops inflate latency and cost

## Minimal example
```python
extract = prompt_extract | llm | StrOutputParser()
chain = {"specifications": extract} | prompt_transform | llm | StrOutputParser()
result = chain.invoke({"text_input": source})
```

## Next skills
- If the next hop depends on intent: load `routing`
- If a stage must call APIs or code: load `tool-use`
