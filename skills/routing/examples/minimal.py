"""Minimal example: Routing (Ch 2). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    route = classify(req, ["billing", "tech", "other"])
    handler = {"billing": bill_agent, "tech": tech_agent,
               "other": general_agent}[route.label]
    return handler(req)


if __name__ == "__main__":
    print(main())
