---
name: mcp
description: Tool discovery via MCP servers. Use for many or shared tools. Not for a few local functions.
role: [memory, executor]
chapter: 10
token_cost_estimate: 240
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
tools = server.list_tools()                         # discover, don't hard-code
allowed = {t["name"] for t in tools} & {"list_directory", "read_file"}
if "read_file" in allowed:                          # empty allow-list = no tools
    text = server.call_tool("read_file", {"path": f"{ABS_DIR}/notes.md"})
```

## Next skills
- If callees are agents, not tools: load `a2a`
- If tool errors need handling: load `exception-handling`
