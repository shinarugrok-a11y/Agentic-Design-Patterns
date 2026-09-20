# Model Context Protocol — patterns (Ch 10)

## Pattern
1. Run or point at an MCP server (HTTP or stdio).
2. Discover tools; filter to what the agent needs.
3. Agent calls tools through the toolset like local functions.
4. Pass secrets through env, absolute paths for stdio.

## Prompt template
```
You can list and read files under the allowed directory only.
Use the file tools; do not guess file contents.
```

## Key APIs
- Server: `FastMCP("name")`, `@mcp.tool()`, `mcp.run(transport='streamable-http')`.
- ADK client: `MCPToolset(connection_params=StreamableHTTPServerParams(url=...))`.
- Stdio: `StdioServerParameters(command='npx', args=[..., ABS_PATH])`, `tool_filter=[...]`.

## Pitfalls -> fixes
- Relative paths -> `os.path.abspath`.
- Too many tools exposed -> `tool_filter`.
- MCP vs A2A -> MCP for tools/resources, A2A for agents.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_10_*`.
