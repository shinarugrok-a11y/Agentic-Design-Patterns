"""Minimal example: Evaluation and Monitoring (Ch 19). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    s = accuracy(agent_out, expected)  # exact match
    v = judge(agent_out, rubric)  # LLM-as-judge
    log(version, prompt_hash, s, v)


if __name__ == "__main__":
    print(main())
