---
name: mcp
description: Tool discovery via MCP servers. Use for many or shared tools. Not for a few local functions.
role: [memory, executor]
chapter: 10
token_cost_estimate: 226
chains_with: [a2a, exception-handling]
---

# Model Context Protocol

## When to use
- Tools live on external or shared servers.
- Tool set changes without redeploying.
- Resources must be discoverable.

## When NOT to use
- Two or three local functions: use `tool-use`.
- Agent-to-agent delegation: use `a2a`.

## Inputs
- Server URL or stdio command
- Optional tool_filter

## Outputs
- Discovered tool list
- Tool call results

## Failure modes
- Relative server path fails outside notebooks.
- No tool_filter: dangerous tools exposed.
- Secrets in prompts, not env.

## Minimal example
```python
fs = MCPToolset(connection_params=StdioServerParameters(
    command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", ABS_DIR]),
    tool_filter=["list_directory", "read_file"])
agent = LlmAgent(name="fs_agent", tools=[fs])
```

## Next skills
- If callees are agents, not tools: load `a2a`
- If tool errors need handling: load `exception-handling`
