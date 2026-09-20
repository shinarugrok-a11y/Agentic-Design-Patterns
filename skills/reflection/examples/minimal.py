"""Minimal example: Reflection (Ch 4). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    draft = run(f"Write paragraph: {topic}")
    for _ in range(3):
        notes = critique(draft, ["accuracy", "clarity"])
        if notes.clean: break
        draft = run(f"Revise: {draft} per {notes}")


if __name__ == "__main__":
    print(main())
