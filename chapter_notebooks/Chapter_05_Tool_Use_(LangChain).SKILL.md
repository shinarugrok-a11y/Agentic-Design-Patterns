---
name: tool-use
description: Function calling to reach outside the model. Let the model emit a structured call to a described function when it needs live data, computation, or an action. Do not use when the answer is in the model's knowledge or when the action is irreversible without a confirmation gate.
role: [executor]
chapter: 5
token_cost_estimate: 340
chains_with: [mcp, exception-handling, guardrails]
---

# Tool Use

## When to use
- Need real-time or private data (weather, DB, search).
- Need exact computation or code execution.
- Need to trigger an action (email, ticket, API write).
- Tool has a clear name, docstring and typed args.

## When NOT to use
- Answer is static general knowledge.
- Action is destructive and unconfirmed: gate with `human-in-the-loop`.
- Many heterogeneous tools across services: use `mcp`.

## Inputs
- Tool schema (name, description, typed params)
- User request
- Tool execution runtime

## Outputs
- Structured tool call (name + args)
- Tool result fed back to model
- Final grounded answer

## Failure modes
- Vague docstring: model picks wrong tool or wrong args.
- Tool returns a string error instead of raising; agent treats it as data.
- Unbounded tool loop when result never satisfies the model.
- Tool output too large for context.

## Minimal example
```python
@tool
def get_stock_price(ticker: str) -> float:
    """Return latest price for ticker. Raises ValueError if unknown."""
    ...
agent = create_tool_calling_agent(llm, [get_stock_price], prompt)
AgentExecutor(agent=agent, tools=[get_stock_price]).invoke({"input": q})
# ADK built-ins: google_search, BuiltInCodeExecutor, VSearchAgent
```

## Next skills
- If tools live on external servers or need discovery: load `mcp`
- If tool may fail or time out: load `exception-handling`
- If tool args must be validated before execution: load `guardrails`
