# Model Context Protocol — Patterns

## Pattern variants
- **Local stdio server** — JSON-RPC over STDIO via `StdioServerParameters(command='npx', ...)`; wins for filesystem or sensitive local data where latency and isolation matter.
- **Remote HTTP/SSE server** — Streamable HTTP or Server-Sent Events via `HttpServerParameters(url=...)`; wins when one team's tools must serve many agents and models.
- **Expose-your-own with FastMCP** — `@tool()` on a plain Python function; the signature, type hints, and docstring become the schema. Wins for proprietary internal functions.
- **Tool vs resource vs prompt** — a tool executes, a resource is static data, a prompt is a template. MCP does not make data agent-readable: serve Markdown, not PDFs.
- **Filtered toolset** — `tool_filter=['list_directory', 'read_file']` narrows a broad server to the subset this task needs, so unusable tools never reach the model.

## Prompt templates

Agent instruction naming the tool explicitly:
```
You are a friendly assistant that can greet people by their name.
Use the "greet" tool.
```

Agent instruction that pins the scope into the instruction, not just the server args:
```
Help the user manage their files. You can list files, read files, and write files.
You are operating in the following directory: {TARGET_FOLDER_PATH}
```

## Code patterns

FastMCP (server; docstring becomes the tool description):
```python
from fastmcp import FastMCP, tool

@tool()
def greet(name: str) -> str:
    """Generates a personalized greeting.

    Args:
        name: The name of the person to greet.
    """
    return f"Hello, {name}! Nice to meet you."

mcp_server = FastMCP()
mcp_server.run(transport="http", host="127.0.0.1", port=8000)
```

Google ADK (client over stdio, scoped to one absolute path):
```python
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='filesystem_assistant_agent',
    instruction=f'Help the user manage files under {TARGET_FOLDER_PATH}',
    tools=[MCPToolset(
        connection_params=StdioServerParameters(
            command='npx',
            args=["-y", "@modelcontextprotocol/server-filesystem", TARGET_FOLDER_PATH],
        ),
        tool_filter=['list_directory', 'read_file'],   # read-only
    )],
)
```

## Framework notes
- **LangChain / LangGraph** — not used in this chapter.
- **Google ADK** — `MCPToolset` accepts `StdioServerParameters`, `StdioConnectionParams` (pass credentials in its `env`, never in the prompt), or `HttpServerParameters`; an `__init__.py` with `from . import agent` makes the agent discoverable, then `adk web` drives it.
- **FastMCP / npx / uvx** — FastMCP generates schemas automatically and supports server composition and proxying; `npx` runs Node-packaged community servers and `uvx` runs Python ones in a throwaway environment.

## Failure modes in depth
- **Discovery returns tools the agent may not call** — the server must authenticate and authorize each client; on the client, set `tool_filter` so unauthorized tools never enter the model's context and cannot be attempted.
- **Protocol or schema version drift** — `@latest` in server args silently changes the contract, and FastMCP regenerates schemas from signatures. Pin versions and re-run `list_tools` discovery after any server upgrade.
- **Scope wider than the task** — pass one absolute directory to the filesystem server rather than a home directory, prefer a local server for sensitive data, and drop write tools from `tool_filter` for read-only work.
- **Chatty round trips** — use stdio locally, and a persistent Streamable HTTP/SSE session remotely; batch work into one coarse tool rather than many fine-grained calls, and cache the discovery manifest per session.

## Source
Chapter 10 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_10_MCP_(FastMCP_Server_Example).ipynb, Chapter_10_MCP_(ADK_FastMCP_Server).ipynb, Chapter_10_MCP_(Filesystem_Example_agent).ipynb.
