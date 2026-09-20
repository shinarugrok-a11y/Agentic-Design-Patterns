---
name: mcp
description: Expose tools and data through standard MCP servers.
role: [memory, executor]
chapter: 10
token_cost_estimate: 225
chains_with: [tool-use, memory-management]
---

# Model Context Protocol (MCP)

## When to use
- Tools or data must be shared across agents or sessions.
- Use a typed server + toolset client.
- Filesystem or domain tools need sandboxing.

## When NOT to use
- Single local function call; direct import is simpler.
- No MCP-compatible client in the stack.

## Inputs
- Server definition
- Client agent + toolset config

## Outputs
- Agent able to call MCP tools as native tools

## Failure modes
- Schema mismatch between server tool and client expectation.
- Stderr/stdout mixing breaks stdio transport.
- Over-permissive server exposes destructive filesystem ops.

## Minimal example
```python
server = FastMCP("demo")
@server.tool
def greet(name: str) -> str: return f"Hi {name}"
agent = LlmAgent(tools=[MCPToolset(HttpServerParameters(url))])
```

## Next skills
- If agent must select among MCP tools at runtime: load `tool-use`
- If MCP-backed data needs session memory: load `memory-management`
