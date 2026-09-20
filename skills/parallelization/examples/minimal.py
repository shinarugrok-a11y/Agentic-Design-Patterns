"""Minimal example: Parallelization (Ch 3). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    results = gather(run("Research solar"),
                   run("Research wind"),
                   run("Research hydro"))
    return run(f"Synthesize comparison: {results}")


if __name__ == "__main__":
    print(main())
