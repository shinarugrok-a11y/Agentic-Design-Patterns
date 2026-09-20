---
name: mcp
description: Use when agents need standardized tool or file access via MCP servers. Do not use for one-off local function calls.
role: [memory, executor]
chapter: 10
token_cost_estimate: 187
chains_with: [tool-use, guardrails]
---

# Model Context Protocol (MCP)

## When to use
- Standard file/dev/data access (filesystem, sheets)
- Share one tool server across agents
- Need capability isolation per server

## When NOT to use
- Single local function call suffices
- No MCP server exists for the need
- Direct SDK call is simpler and audited

## Inputs
- Server URL or stdio command
- Target folder or credential scope

## Outputs
- Agent with MCPToolset attached
- Scoped file/tool result

## Failure modes
- Down server — health-check and fail closed
- Over-scope — restrict TARGET_FOLDER_PATH, least privilege
- Transport mix-up — match HttpServerParams vs StdioServerParams

## Minimal example
```python
tools = MCPToolset(HttpServerParams(url))
agent = LlmAgent(name="files", tools=[tools])
# stdio alt: StdioServerParams("python3", ["mcp_server.py"])
```

## Next skills
- If need general tool-calling discipline: load `tool-use`
- If need to lock down tool args: load `guardrails`
