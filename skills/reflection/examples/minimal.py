"""Reflection: generate -> critique -> refine with a sentinel stop condition.

Offline stub: the "critic" checks two concrete requirements. In production
both `produce` and `critique` are LLM calls; keep the sentinel and the cap.
"""
SENTINEL = "CODE_IS_PERFECT"
MAX_ITER = 3

TASK = "Write factorial(n): factorial(0)==1 and raise ValueError for n<0."


def produce(task: str, critique: str | None, prev: str | None) -> str:
    """Stand-in for llm(history). Improves the draft when given a critique."""
    if prev is None:
        return "def factorial(n):\n    return 1 if n == 0 else n * factorial(n - 1)\n"
    if "negative" in critique:
        return ("def factorial(n):\n    if n < 0:\n        raise ValueError('n must be >= 0')\n"
                "    return 1 if n == 0 else n * factorial(n - 1)\n")
    return prev


def critique(task: str, code: str) -> str:
    """Stand-in for the reviewer prompt. Returns SENTINEL when satisfied."""
    issues = []
    if "ValueError" not in code:
        issues.append("- does not raise ValueError for negative input")
    if "n == 0" not in code:
        issues.append("- factorial(0) case missing")
    return SENTINEL if not issues else "\n".join(issues)


def reflect(task: str) -> tuple[str, str]:
    draft, note = None, None
    for i in range(MAX_ITER):
        draft = produce(task, note, draft)
        note = critique(task, draft)
        if SENTINEL in note:
            return draft, f"approved after {i + 1} iteration(s)"
    return draft, "max iterations reached"


if __name__ == "__main__":
    code, status = reflect(TASK)
    print(status)
    print(code)
