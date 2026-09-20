"""Minimal example: Prioritization (Ch 20). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    ranked = score(backlog, value=0.5, urgency=0.3, effort=-0.2)
    top = ranked[:3]  # commit, queue rest
    act(top); rescore(backlog)


if __name__ == "__main__":
    print(main())
