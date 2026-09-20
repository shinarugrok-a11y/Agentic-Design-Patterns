"""Minimal example: Model Context Protocol (MCP) (Ch 10). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    tools = MCPToolset(HttpServerParams(url))
    agent = LlmAgent(name="files", tools=[tools])
    # stdio alt: StdioServerParams("python3", ["mcp_server.py"])


if __name__ == "__main__":
    print(main())
