"""Minimal example: Exception Handling and Recovery (Ch 12). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    try:
        loc = precise_lookup(addr)
    except ToolError:
        loc = coarse_lookup(addr)  # flagged degraded
        log("fallback used", trace)


if __name__ == "__main__":
    print(main())
