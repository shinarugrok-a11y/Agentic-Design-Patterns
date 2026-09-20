---
name: model-context-protocol
description: Standard client-server interface for tools and resources. Expose or consume tools, resources, and prompts over MCP so capabilities are discoverable at runtime. Skip it when a fixed, small set of local functions is enough; call them directly.
role: [memory, executor]
chapter: 10
token_cost_estimate: 370
chains_with: [tool-use, guardrails-safety, knowledge-retrieval-rag]
---

# Model Context Protocol

## When to use
- Tools live outside your process or language
- Capabilities must be discovered at runtime
- The same tools serve multiple models or clients

## When NOT to use
- A few local functions cover the need
- Extra transport latency is unacceptable
- You cannot scope server permissions safely

## Inputs
- server endpoint and transport
- declared tools and resources
- auth credentials

## Outputs
- discovered capability list
- tool invocation results
- resource contents

## Failure modes
- Server discovery returns tools the agent has no permission to call
- Protocol or schema version drift between client and server
- Filesystem or network scope wider than the task needs
- Latency from chatty round trips per tool call

## Minimal example
```python
mcp = FastMCP(name="files")

@mcp.tool
def read_note(name: str) -> str:
    """Read one note from the notes directory."""
    return (NOTES / name).read_text()      # keep scope narrow

# client side: discover, then call only what the task needs
tools = await client.list_tools()
```

## Next skills
- If calls are local functions: load `tool-use`
- If servers expose write access: load `guardrails-safety`
- If resources are documents: load `knowledge-retrieval-rag`
