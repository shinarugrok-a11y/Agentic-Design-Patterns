"""Minimal example: Resource-Aware Optimization (Ch 16). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    tier = "flash" if simple(query) else "pro"
    answer = run_tier(tier, query)  # cached when repeat
    log(cost(tier), latency)


if __name__ == "__main__":
    print(main())
