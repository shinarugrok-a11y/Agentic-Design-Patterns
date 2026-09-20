"""Minimal example: Prompt Chaining (Ch 1). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    extract = run("Extract entities: {text}")
    check = run(f"Validate JSON: {extract}")
    answer = run(f"Summarize for execs: {check}")
    return answer  # 3 stages, validated


if __name__ == "__main__":
    print(main())
