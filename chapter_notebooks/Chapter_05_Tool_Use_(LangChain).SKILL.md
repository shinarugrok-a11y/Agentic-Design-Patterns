---
name: tool-use
description: Function calling. Use for live data, computation or actions. Not when model knowledge suffices.
role: [executor]
chapter: 5
token_cost_estimate: 225
chains_with: [mcp, exception-handling]
---

# Tool Use

## When to use
- Need real-time or private data.
- Need exact computation or code execution.
- Need to trigger an action.

## When NOT to use
- Answer is static general knowledge.
- Destructive and unconfirmed: gate with `human-in-the-loop`.

## Inputs
- Tool schema (name, description, typed args)
- User request

## Outputs
- Structured tool call
- Grounded final answer

## Failure modes
- Vague docstring: wrong tool or args.
- Error returned as string, treated as data.
- Unbounded tool loop.

## Minimal example
```python
@tool
def get_stock_price(ticker: str) -> float:
    """Latest price for ticker. Raises ValueError if unknown."""
agent = create_tool_calling_agent(llm, [get_stock_price], prompt)
AgentExecutor(agent=agent, tools=[get_stock_price]).invoke(q)
```

## Next skills
- If tools live on external servers: load `mcp`
- If tool may fail or time out: load `exception-handling`
