---
name: tool-use
description: Let the agent call typed external functions.
role: [executor]
chapter: 5
token_cost_estimate: 212
chains_with: [mcp, exception-handling]
---

# Tool Use

## When to use
- Task needs live data or actions.
- You can declare tools with typed schemas and descriptions.
- Results must be cited or verified from a source.

## When NOT to use
- Answer is fully derivable from context.
- No trusted tool endpoint exists; do not fake calls.

## Inputs
- Tool schemas
- User query + execution policy

## Outputs
- Tool call trace + grounded final answer

## Failure modes
- Vague tool descriptions cause wrong-tool selection.
- Unbounded calls loop; always cap iterations.
- Untrusted tool output injected as fact without validation.

## Minimal example
```python
tools = [search_information, get_stock_price]
agent = create_tool_calling_agent(llm, tools, prompt)
print(AgentExecutor(agent, tools).invoke({"input": q}))
```

## Next skills
- If tools must be shared across agents via a standard: load `mcp`
- If tool calls can fail or time out: load `exception-handling`
