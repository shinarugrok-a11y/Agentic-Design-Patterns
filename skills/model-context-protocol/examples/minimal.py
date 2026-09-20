"""In-process stand-in for MCP: a server registers tools, a client discovers, then calls.

Real framework: FastMCP `@mcp.tool` on the server side and ADK
`MCPToolset(connection_params=..., tool_filter=[...])` on the client, over JSON-RPC/stdio.
Run: python3 examples/minimal.py
"""
from pathlib import Path

NOTES = Path(__file__).resolve().parent  # the server's entire world is this one directory


class FastMCP:
    def __init__(self, name):
        self.name, self._tools = name, {}

    def tool(self, fn):
        self._tools[fn.__name__] = fn
        return fn

    def list_tools(self):
        return [{"name": n, "description": (f.__doc__ or "").strip()}
                for n, f in self._tools.items()]

    def call_tool(self, tool_name, **kwargs):
        if tool_name not in self._tools:
            raise LookupError(f"{tool_name} not exposed by server {self.name!r}")
        return self._tools[tool_name](**kwargs)


mcp = FastMCP(name="files")


@mcp.tool
def read_note(name: str) -> str:
    """Read one note from the notes directory."""
    target = (NOTES / name).resolve()
    if target.parent != NOTES:
        raise PermissionError(f"{name} is outside the server's scope")
    return f"{len(target.read_text())} chars from {target.name}"


@mcp.tool
def delete_note(name: str) -> str:
    """Delete one note."""
    return f"deleted {name}"


ALLOWED = ["read_note"]  # client-side tool_filter: write tools stay out of the context
discovered = mcp.list_tools()
print("discovered:", [t["name"] for t in discovered])

for spec in discovered:
    if spec["name"] not in ALLOWED:
        print(f"skip {spec['name']}: filtered out before the model ever sees it")
        continue
    print(f"call {spec['name']}:", mcp.call_tool(spec["name"], name="minimal.py"))
