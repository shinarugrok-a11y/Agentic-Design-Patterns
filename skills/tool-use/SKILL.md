---
name: tool-use
description: Function calling. Use for live data, computation or actions. Not when model knowledge suffices.
role: [executor]
chapter: 5
token_cost_estimate: 241
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
def get_stock_price(ticker: str) -> float:
    """Latest price for ticker. Raises ValueError if unknown."""
TOOLS = {"get_stock_price": get_stock_price}
call = llm_pick_tool(question, schemas(TOOLS))   # model picks name + args
result = TOOLS[call.name](**call.args)           # your code runs it
```

## Next skills
- If tools live on external servers: load `mcp`
- If tool may fail or time out: load `exception-handling`
