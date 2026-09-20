---
name: prompt-chaining
description: Sequential task decomposition. Split a task into ordered stages and feed each stage's output into the next prompt. Skip it when subtasks are independent or a single prompt already answers reliably.
role: [executor]
chapter: 1
token_cost_estimate: 350
chains_with: [routing, tool-use, reflection]
---

# Prompt Chaining

## When to use
- Task splits into 2+ ordered stages
- Each stage consumes the previous stage's output
- You must validate or reshape data between stages
- A single prompt keeps dropping instructions

## When NOT to use
- Subtasks are independent - parallelize instead
- One prompt already passes your quality bar
- Chain latency exceeds the request budget

## Inputs
- initial task text
- stage prompt templates
- per-stage output schema

## Outputs
- final stage output
- intermediate artifacts per stage

## Failure modes
- Error in an early stage propagates silently to the end
- Unparsed free text between stages breaks the next prompt
- Latency and cost grow linearly with chain length
- Context lost because only the last output is forwarded

## Minimal example
```python
extract = prompt_extract | llm | StrOutputParser()
chain = ({"specs": extract} | prompt_transform | llm | StrOutputParser())
result = chain.invoke({"text_input": raw_text})
```

## Next skills
- If stage 1 must choose a handler: load `routing`
- If a stage needs external data: load `tool-use`
- If stage output is unreliable: load `reflection`
