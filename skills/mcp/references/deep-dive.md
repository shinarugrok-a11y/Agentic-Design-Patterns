# Model Context Protocol (MCP) — deep dive

Source: Chapter 10 + `Chapter_10_MCP_(FastMCP_Server_Example)`, `(ADK_FastMCP_Server)`,
`(FastMCP_Client_Agent_init)`, `(Filesystem_Example_agent)`, `(Filesystem_Example_init)`.

## What MCP standardises (book)
Client-server protocol. Servers expose **tools** (callable functions),
**resources** (data) and **prompts** (templates). Any compliant client (an
LLM app/agent) discovers and uses them. Compared with plain function
calling, MCP is for many/evolving/shared tools; direct function calling is
enough for a fixed small set.

Rule of thumb: use for complex, scalable or enterprise systems that need
a diverse and evolving set of external tools, or when interoperability
between different LLMs and tools matters.

## Server: FastMCP
```python
# fastmcp_server.py
from fastmcp import FastMCP, tool

@tool()
def greet(name: str) -> str:
    """
    Generates a personalized greeting.
    Args:
        name: The name of the person to greet.
    Returns:
        A greeting string.
    """
    return f"Hello, {name}! Nice to meet you."

mcp_server = FastMCP()          # default http://localhost:8000, discovers @tool() functions
if __name__ == "__main__":
    mcp_server.run()            # schema at /tools.json
```
The docstring becomes the tool description the client LLM reads.

## Client: ADK agent consuming an HTTP MCP server
```python
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, HttpServerParameters

root_agent = LlmAgent(model="gemini-2.0-flash", name="fastmcp_greeter_agent",
    instruction='You are a friendly assistant that can greet people by their name. Use the "greet" tool.',
    tools=[MCPToolset(connection_params=HttpServerParameters(url="http://localhost:8000"),
                      tool_filter=["greet"])])
```
Package layout expected by `adk web`/`adk run`:
```
adk_agent_samples/fastmcp_client_agent/__init__.py   # from . import agent
adk_agent_samples/fastmcp_client_agent/agent.py      # defines root_agent
```

## Client: stdio MCP server (filesystem)
```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

TARGET_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_managed_files")
os.makedirs(TARGET_FOLDER_PATH, exist_ok=True)

root_agent = LlmAgent(model="gemini-2.0-flash", name="filesystem_assistant_agent",
    instruction=("Help the user manage their files. You can list files, read files, and write files. "
                 f"You are operating in the following directory: {TARGET_FOLDER_PATH}"),
    tools=[MCPToolset(
        connection_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", TARGET_FOLDER_PATH]),  # MUST be absolute
        # tool_filter=['list_directory', 'read_file']   # read-only exposure
    )])
```

## Passing secrets to a stdio server
```python
connection_params = StdioConnectionParams(server_params={
    "command": "uvx", "args": ["mcp-google-sheets@latest"],
    "env": {"SERVICE_ACCOUNT_PATH": SERVICE_ACCOUNT_PATH, "DRIVE_FOLDER_ID": DRIVE_FOLDER_ID}})
# or a local python server:
connection_params = StdioConnectionParams(server_params={
    "command": "python3", "args": ["./agent/mcp_server.py"], "env": {...}})
```
Credentials go in `env`, never in `args` or the instruction.

## Ecosystem notes (book)
- ADK can both consume MCP servers and expose ADK tools through an MCP server.
- MCP Tools for Genmedia: Imagen, Veo, Chirp 3 HD, Lyria via MCP.
- MCP vs A2A: MCP connects an LLM to resources/tools; A2A coordinates tasks
  between agents. They compose.

## Checklist
- Absolute paths for filesystem servers.
- `tool_filter` to expose only what the task needs (least privilege).
- Start the server before the agent; surface connection errors clearly.
- Version-pin server packages (`@latest` is convenient, not reproducible).

## Pattern variants
- **Local stdio server** — JSON-RPC over STDIO via `StdioServerParameters(command='npx', ...)`; wins for filesystem or sensitive local data where latency and isolation matter.
- **Remote HTTP/SSE server** — Streamable HTTP or Server-Sent Events via `HttpServerParameters(url=...)`; wins when one team's tools must serve many agents and models.
- **Expose-your-own with FastMCP** — `@tool()` on a plain Python function; the signature, type hints, and docstring become the schema. Wins for proprietary internal functions.
- **Tool vs resource vs prompt** — a tool executes, a resource is static data, a prompt is a template. MCP does not make data agent-readable: serve Markdown, not PDFs.
- **Filtered toolset** — `tool_filter=['list_directory', 'read_file']` narrows a broad server to the subset this task needs, so unusable tools never reach the model.

## More prompt templates
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

## Framework notes
- **LangChain / LangGraph** — not used in this chapter.
- **Google ADK** — `MCPToolset` accepts `StdioServerParameters`, `StdioConnectionParams` (pass credentials in its `env`, never in the prompt), or `HttpServerParameters`; an `__init__.py` with `from . import agent` makes the agent discoverable, then `adk web` drives it.
- **FastMCP / npx / uvx** — FastMCP generates schemas automatically and supports server composition and proxying; `npx` runs Node-packaged community servers and `uvx` runs Python ones in a throwaway environment.

## Failure modes in depth
- **Discovery returns tools the agent may not call** — the server must authenticate and authorize each client; on the client, set `tool_filter` so unauthorized tools never enter the model's context and cannot be attempted.
- **Protocol or schema version drift** — `@latest` in server args silently changes the contract, and FastMCP regenerates schemas from signatures. Pin versions and re-run `list_tools` discovery after any server upgrade.
- **Scope wider than the task** — pass one absolute directory to the filesystem server rather than a home directory, prefer a local server for sensitive data, and drop write tools from `tool_filter` for read-only work.
- **Chatty round trips** — use stdio locally, and a persistent Streamable HTTP/SSE session remotely; batch work into one coarse tool rather than many fine-grained calls, and cache the discovery manifest per session.
