"""Minimal example: Human-in-the-Loop (Ch 13). Dependency-free illustration."""

def run(prompt: str) -> str:
    return f"[model output for: {prompt[:60]}...]"


def main() -> None:
    ticket = propose(action, risk="high", preview=diff)
    if approve(ticket, approver, timeout="10m"):
        execute(ticket)
    else: escalate_or_block(ticket)


if __name__ == "__main__":
    print(main())
