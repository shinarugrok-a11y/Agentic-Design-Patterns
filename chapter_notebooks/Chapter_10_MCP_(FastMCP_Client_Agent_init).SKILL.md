---
name: mcp
description: Standard client-server tool/resource discovery. Use when tools must be interchangeable across models. Do NOT use for a handful of hard-coded functions.
role: [memory, executor]
chapter: 10
token_cost_estimate: 247
chains_with: [tool-use, a2a]
---

# Model Context Protocol

## When to use
- Many evolving tools/data sources across models
- Need runtime discovery without redeploy
- Share one server among several agents

## When NOT to use
- Two local `@tool` functions (load `tool-use`)
- Cross-agent *task* protocol, not tools (load `a2a`)
- No network/process boundary

## Inputs
- HTTP (`HttpServerParameters`) or stdio (`npx` filesystem server)
- `tool_filter` allowlist
- Absolute directory for filesystem MCP

## Outputs
- Bound toolset on the LLM agent
- Tool call results

## Failure modes
- Connecting while the server is down
- Non-absolute paths
- Unfiltered tools → over-privilege

## Minimal example
```python
@tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"
# client: MCPToolset(HttpServerParameters(url="http://localhost:8000"), tool_filter=["greet"])
```

## Next skills
- If you only need in-process functions: load `tool-use`
- If agents must call *agents*: load `a2a`
