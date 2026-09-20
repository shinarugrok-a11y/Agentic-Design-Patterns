# Model Context Protocol (MCP)

Ch 10.

## Frameworks
- FastMCP (server + @tool); Google ADK MCPToolset (HttpServerParameters, StdioServerParameters).

## Key APIs from the notebooks
- `Server: from fastmcp import FastMCP, tool; @server.tool def greet(name: str) -> str`
- `ADK client: MCPToolset(HttpServerParameters(url=...)) for remote servers`
- `ADK client: MCPToolset(StdioServerParameters(...)) for Filesystem example agent`

## Code patterns
- Pattern: define typed server tools -> run server (stdio/HTTP) -> attach MCPToolset to LlmAgent.
- Keep server tools small, typed, side-effect-explicit.
- Prefer stdio for local tools, HTTP for shared/remote tools.

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_10_MCP_(ADK_FastMCP_Server).ipynb`
- `chapter_notebooks/Chapter_10_MCP_(FastMCP_Client_Agent_init).ipynb`
- `chapter_notebooks/Chapter_10_MCP_(FastMCP_Server_Example).ipynb`
- `chapter_notebooks/Chapter_10_MCP_(Filesystem_Example_agent).ipynb`
- `chapter_notebooks/Chapter_10_MCP_(Filesystem_Example_init).ipynb`

