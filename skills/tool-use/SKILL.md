---
name: tool-use
description: Use when the model must act on the world via search, code, or APIs. Do not use when the answer is fully contained in model knowledge.
role: [executor]
chapter: 5
token_cost_estimate: 194
chains_with: [routing, exception-handling]
---

# Tool Use

## When to use
- Need live data (search, docs, DBs)
- Need actions (code exec, tickets, APIs)
- Answers must cite external sources

## When NOT to use
- Answer is in model knowledge
- No vetted tool exists for the need
- Tool cost/latency exceeds value

## Inputs
- Tool schemas with descriptions
- Task plus tool-call budget

## Outputs
- Grounded answer with tool trace
- Citations or action receipts

## Failure modes
- Bad tool choice — keep registry small with sharp descriptions
- Untrusted output — validate before reasoning over it
- Tool loops — cap calls per task (e.g. 5)

## Minimal example
```python
agent = tool_agent(llm, tools=[search, code_exec])
result = agent.invoke("Compare EV prices (cite sources)")
return cited(result)
```

## Next skills
- If pick tools per request type: load `routing`
- If tools fail or time out: load `exception-handling`
