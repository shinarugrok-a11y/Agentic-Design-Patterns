"""MCP: a client discovers tools from a server instead of hard-coding them.

Offline stub of the protocol shape: the server publishes a tool schema
(`tools/list`), the client filters it (least privilege) and invokes tools
by name (`tools/call`). Those two method names come from the MCP spec, not
the book (EXTERNAL-UNVERIFIED). Swap in FastMCP + MCPToolset for the real thing.
"""
import inspect
import json


class ToyMCPServer:
    def __init__(self):
        self._tools = {}

    def tool(self, fn):
        self._tools[fn.__name__] = fn
        return fn

    def list_tools(self) -> list[dict]:
        return [{"name": n, "description": inspect.getdoc(f),
                 "params": list(inspect.signature(f).parameters)} for n, f in self._tools.items()]

    def call_tool(self, name: str, args: dict):
        if name not in self._tools:
            raise KeyError(f"unknown tool {name}")
        return self._tools[name](**args)


server = ToyMCPServer()


@server.tool
def greet(name: str) -> str:
    """Generates a personalized greeting."""
    if not isinstance(name, str) or not name.strip() or len(name) > 100:
        raise ValueError("name must be a non-empty string of at most 100 characters")
    return f"Hello, {name}! Nice to meet you."


@server.tool
def delete_everything() -> str:
    """Dangerous tool that should not be exposed to a greeter agent."""
    return "deleted"


class MCPToolset:
    def __init__(self, server: ToyMCPServer, tool_filter: list[str] | None = None):
        # None = expose every tool; [] = expose none. Never treat an empty filter as "all".
        self.tools = [t for t in server.list_tools() if tool_filter is None or t["name"] in tool_filter]
        self._server = server

    def call(self, tool_name: str, **args):
        if not any(t["name"] == tool_name for t in self.tools):     # not assert: survives python -O
            raise PermissionError(f"{tool_name} not exposed to this agent")
        return self._server.call_tool(tool_name, args)


if __name__ == "__main__":
    toolset = MCPToolset(server, tool_filter=["greet"])
    print("discovered:", json.dumps(toolset.tools))
    print(toolset.call("greet", name="Ada"))
    try:
        toolset.call("delete_everything")
    except PermissionError as e:
        print("blocked:", e)
    else:
        raise SystemExit("tool_filter failed: delete_everything ran")
    if MCPToolset(server, tool_filter=[]).tools:
        raise SystemExit("tool_filter=[] exposed tools")
    print("tool_filter=[] exposes: []")
