"""Goal setting and monitoring: iterate until a strict boolean judge says met.

Offline stub of the Chapter 11 loop: generate -> feedback -> goals_met.
Deterministic checks stand in for the LLM critic/judge.
"""
GOALS = ["handles n == 0", "rejects negative input", "has a docstring"]
MAX_ITERATIONS = 5


def generate(use_case: str, goals: list[str], previous: str, feedback: str) -> str:
    """Stand-in for llm(generate_prompt(...)). Applies one fix per iteration."""
    code = previous or "def binary_gap(n):\n    return max(map(len, bin(n)[2:].strip('0').split('1')), default=0)\n"
    if "docstring" in feedback:
        code = code.replace("def binary_gap(n):\n", 'def binary_gap(n):\n    """Longest run of zeros between ones."""\n')
    if "negative" in feedback:
        code = code.replace('"""\n', '"""\n    if n < 0:\n        raise ValueError("n must be positive")\n', 1)
    if "n == 0" in feedback:
        code = code.replace("    return max", "    if n == 0:\n        return 0\n    return max", 1)
    return code


def get_feedback(code: str, goals: list[str]) -> str:
    """Stand-in for the reviewer prompt: names the first unmet goal(s)."""
    unmet = []
    if '"""' not in code:
        unmet.append("missing docstring")
    if "ValueError" not in code:
        unmet.append("does not reject negative input")
    if "n == 0" not in code:
        unmet.append("does not handle n == 0")
    return "; ".join(unmet) if unmet else "all goals satisfied"


def goals_met(feedback: str) -> bool:
    """Stand-in for: llm('Respond with only one word: True or False').strip().lower() == 'true'"""
    return feedback == "all goals satisfied"


def run(use_case: str) -> tuple[str, str]:
    previous, feedback = "", ""
    for i in range(MAX_ITERATIONS):
        code = generate(use_case, GOALS, previous, feedback)
        feedback = get_feedback(code, GOALS)
        if goals_met(feedback):
            return code, f"goals met at iteration {i + 1}"
        previous = code
    return code, f"stopped at cap; unmet: {feedback}"


if __name__ == "__main__":
    code, status = run("Binary gap of a positive integer")
    print(status)
    print(code)
