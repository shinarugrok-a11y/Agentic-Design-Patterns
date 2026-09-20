---
name: mcp
description: Standard client-server interface for tools, resources and prompts. Connect an agent to external tools or data through an MCP server so capabilities are discovered, not hard-coded. Do not use for a fixed handful of local functions; direct function calling is simpler.
role: [memory, executor]
chapter: 10
token_cost_estimate: 360
chains_with: [tool-use, a2a, memory-management]
---

# Model Context Protocol

## When to use
- Many tools across services must be reusable by different agents/LLMs.
- Capabilities should be discoverable at runtime.
- You want to expose your own tools to other clients.
- Filesystem, sheets, DB or media servers already exist as MCP servers.

## When NOT to use
- 2-3 local Python functions: use `tool-use`.
- Agent-to-agent task delegation: use `a2a`.
- No network/process isolation allowed.

## Inputs
- Server connection (stdio command or HTTP URL)
- Optional `tool_filter`
- Env/credentials for the server

## Outputs
- Discovered tool set on the agent
- Tool call results
- Resources/prompts exposed

## Failure modes
- Relative path to filesystem server; must be absolute.
- No `tool_filter`: agent sees dangerous write tools it does not need.
- Server not running when agent starts; opaque connection error.
- Secrets passed in args instead of `env`.

## Minimal example
```python
root_agent = LlmAgent(model=..., name="fs_agent", instruction=...,
    tools=[MCPToolset(connection_params=StdioServerParameters(
        command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", ABS_PATH]),
        tool_filter=["list_directory", "read_file"])])
# server side: @tool() def greet(name: str) -> str: ...; FastMCP().run()
```

## Next skills
- If tools are local functions: load `tool-use`
- If peer is a whole agent, not a tool: load `a2a`
- If server is a memory/RAG store: load `memory-management`
