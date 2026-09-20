"""Minimal example: Guardrails and Safety (Ch 18). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    verdict = guardrail.check(input, policy)  # jailbreak/PII/scope
    if verdict.block: log_and_refuse(verdict.reason)
    validate_tool_params(tool, args)  # pre-call gate


if __name__ == "__main__":
    print(main())
