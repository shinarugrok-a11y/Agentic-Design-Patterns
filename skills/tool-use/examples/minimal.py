"""Minimal example: Tool Use (Ch 5). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    agent = tool_agent(llm, tools=[search, code_exec])
    result = agent.invoke("Compare EV prices (cite sources)")
    return cited(result)


if __name__ == "__main__":
    print(main())
