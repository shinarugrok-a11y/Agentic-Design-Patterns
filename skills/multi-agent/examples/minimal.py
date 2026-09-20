"""Minimal example: Multi-Agent Collaboration (Ch 7). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    pipe = SequentialAgent([fetch, summarize])
    team = ParallelAgent([weather, news])
    loop = LoopAgent([worker, checker], max_iter=3)


if __name__ == "__main__":
    print(main())
