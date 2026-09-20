"""MCP: a client discovers tools from a server instead of hard-coding them.

Offline stub of the protocol shape: the server publishes a tool schema
(`tools/list`), the client filters it (least privilege) and invokes tools
by name (`tools/call`). Swap in FastMCP + MCPToolset for the real thing.
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
    return f"Hello, {name}! Nice to meet you."


@server.tool
def delete_everything() -> str:
    """Dangerous tool that should not be exposed to a greeter agent."""
    return "deleted"


class MCPToolset:
    def __init__(self, server: ToyMCPServer, tool_filter: list[str] | None = None):
        self.tools = [t for t in server.list_tools() if not tool_filter or t["name"] in tool_filter]
        self._server = server

    def call(self, tool_name: str, **args):
        assert any(t["name"] == tool_name for t in self.tools), f"{tool_name} not exposed to this agent"
        return self._server.call_tool(tool_name, args)


if __name__ == "__main__":
    toolset = MCPToolset(server, tool_filter=["greet"])
    print("discovered:", json.dumps(toolset.tools))
    print(toolset.call("greet", name="Ada"))
    try:
        toolset.call("delete_everything")
    except AssertionError as e:
        print("blocked:", e)
