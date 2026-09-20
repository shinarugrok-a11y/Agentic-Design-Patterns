# Model Context Protocol — Pattern reference

Load this file only when implementing `mcp`. Do not load by default.

## Book (Gulli) — rule of thumb
Use for scalable/enterprise systems that must discover and call evolving external tools without redeploy. Skip for a few fixed functions.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Model Context Protocol (client-server; resources, prompts, tools).

## Notebooks (extracted)

Model Context Protocol (MCP)

### Notebooks
- `Chapter_10_MCP_(ADK_FastMCP_Server).ipynb` *(filename says Server; content is ADK client)*
- `Chapter_10_MCP_(FastMCP_Client_Agent_init).ipynb` ⚠️ thin
- `Chapter_10_MCP_(FastMCP_Server_Example).ipynb`
- `Chapter_10_MCP_(Filesystem_Example_agent).ipynb`
- `Chapter_10_MCP_(Filesystem_Example_init).ipynb` ⚠️ thin

### Patterns
- **FastMCP server:** `@tool()` decorator on functions; `FastMCP().run()` on localhost:8000
- **ADK client:** `MCPToolset(connection_params=HttpServerParameters(url=...), tool_filter=['greet'])`
- **Stdio MCP:** `StdioServerParameters(command='npx', args=["-y", "@modelcontextprotocol/server-filesystem", ABS_PATH])`
- **Package init:** `from . import agent` in `__init__.py`

### Prompt templates
FastMCP greeter agent instruction:
```
You are a friendly assistant that can greet people by their name. Use the "greet" tool.
```

Filesystem agent instruction:
```
Help the user manage their files. You can list files, read files, and write files.
You are operating in the following directory: {TARGET_FOLDER_PATH}
```

### Minimal code
```python
# FastMCP server
from fastmcp import FastMCP, tool

@tool()
def greet(name: str) -> str:
    """Generates a personalized greeting."""
    return f"Hello, {name}!"

FastMCP().run()  # http://localhost:8000
```

```python
# ADK MCP client
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, HttpServerParameters

agent = LlmAgent(
    model='gemini-2.0-flash',
    tools=[MCPToolset(connection_params=HttpServerParameters(url="http://localhost:8000"), tool_filter=['greet'])],
)
```

### Caveats
- Server must be running before client connects
- Filesystem MCP requires **absolute path** to allowed directory
- Init notebooks are one-line package stubs
- `Filesystem_Example_agent` second cell shows Google Sheets/Drive stdio configs (incomplete snippet)
- `pip install fastmcp` required for server

---

## Failure modes (skill-level)
- Client starts before server
- Relative filesystem paths rejected
- Over-broad tool_filter / directory access

## Chains with
`tool-use`, `a2a`
