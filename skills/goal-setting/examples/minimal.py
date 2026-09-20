"""Minimal example: Goal Setting and Monitoring (Ch 11). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    goal = Goal("Cut support backlog 30%", metric, deadline)
    while not goal.met() and iters < 5:
        act(); report(goal.delta())
    stop_or_escalate(goal)


if __name__ == "__main__":
    print(main())
