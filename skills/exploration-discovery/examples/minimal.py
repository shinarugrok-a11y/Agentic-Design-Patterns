"""Minimal example: Exploration and Discovery (Ch 21). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    plan = propose(question)
    report = run_experiments(plan)
    insights = review(report)  # harsh gate
    return synthesize(insights)


if __name__ == "__main__":
    print(main())
