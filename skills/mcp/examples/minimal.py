"""Chapter 10 — FastMCP server + ADK client filter."""
from fastmcp import FastMCP, tool

@tool()
def greet(name: str) -> str:
    """Generates a personalized greeting."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    FastMCP().run()  # http://localhost:8000
# Client: MCPToolset(HttpServerParameters(url=...), tool_filter=["greet"])
