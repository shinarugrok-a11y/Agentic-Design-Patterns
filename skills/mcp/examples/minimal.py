"""Model Context Protocol (MCP) — minimal runnable demo (stdlib only)."""
TOOLS = {}

def tool(fn):
    TOOLS[fn.__name__] = fn
    return fn

@tool
def greet(name: str) -> str:
    return f"Hi {name}!"

def call(tool_name, **args):  # MCP-style dispatch by name
    return TOOLS[tool_name](**args)

print(call("greet", name="Ada"))
print("TOOLS:", list(TOOLS))
