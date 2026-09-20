"""Minimal example: Reasoning Techniques (Ch 17). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    steps = cot(query)  # analyze -> queries -> evidence
    draft = answer(steps)
    final = self_correct(draft, requirements)
    return final


if __name__ == "__main__":
    print(main())
