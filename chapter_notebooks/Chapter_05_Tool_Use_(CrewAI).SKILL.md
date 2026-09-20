---
name: tool-use
description: Function calling to the outside world. Use for live data, private stores, code, or side effects. Do NOT use for pure generation from weights.
role: [executor]
chapter: 5
token_cost_estimate: 252
chains_with: [mcp, exception-handling]
---

# Tool Use

## When to use
- Need live or private data the weights do not have
- Need precise calc, code execution, or search
- Need side effects (email, tickets, devices)

## When NOT to use
- Pure drafting from model knowledge
- Tools are many, evolving, and should be discovered (load `mcp`)
- Call must be blocked by policy first (load `guardrails-safety`)

## Inputs
- Tool name, description, typed parameters
- User request
- Orchestrator that executes calls

## Outputs
- Structured function call + raw tool result
- Answer that cites the result

## Failure modes
- Weak descriptions → missed or bogus calls
- Swallowing exceptions as strings hides failures
- No arg validation (wrong user_id, path, etc.)

## Minimal example
```python
@tool
def search_information(query: str) -> str: ...
agent = create_tool_calling_agent(llm, [search_information], prompt)
AgentExecutor(agent=agent).invoke({"input": question})
```

## Next skills
- If tools are remote/discoverable: load `mcp`
- If tools fail often: load `exception-handling`
