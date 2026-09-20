"""Minimal example: Planning (Ch 6). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    plan = planner(goal, tools, constraints)
    for step in plan.steps:
        obs = execute(step)
        if surprises(obs): plan = replan(plan, obs)


if __name__ == "__main__":
    print(main())
