"""Minimal example: Learning and Adaptation (Ch 9). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    evolve = OpenEvolve(program, evaluator, config)
    best = await evolve.run(iterations=1000)
    print(best.metrics)  # promote only if held-out gains


if __name__ == "__main__":
    print(main())
