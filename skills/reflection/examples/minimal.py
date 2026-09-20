"""Producer drafts, a separate critic judges against criteria, loop until pass or cap.

Real framework: Google ADK SequentialAgent(sub_agents=[generator, reviewer])
  with output_key="draft_text" / "review_output" passed through session.state
Run: python3 examples/minimal.py
"""

MAX_ITERS = 3
CRITERIA = ["has a docstring", "raises ValueError on negative input"]
TASK = "write calculate_factorial(n)"

DRAFTS = [
    "def calculate_factorial(n): ...",
    'def calculate_factorial(n):\n    """Return n!."""\n    ...',
    'def calculate_factorial(n):\n    """Return n!."""\n    if n < 0: raise ValueError(n)',
]


def producer(task: str, feedback=None) -> str:
    """Canned generator: each call returns the next, slightly better draft."""
    producer.calls += 1
    print(f"producer (feedback={feedback}) -> draft v{producer.calls}")
    return DRAFTS[min(producer.calls - 1, len(DRAFTS) - 1)]


producer.calls = 0


def critic(draft: str, criteria: list) -> dict:
    """Separate critic, not the producer: checks the draft against the rubric."""
    issues = [c for c in criteria if not _satisfies(draft, c)]
    return {"verdict": "pass" if not issues else "revise", "issues": issues}


def _satisfies(draft: str, criterion: str) -> bool:
    return '"""' in draft if "docstring" in criterion else "ValueError" in draft


draft = producer(TASK)
stop_reason = "iteration cap reached"
for _ in range(MAX_ITERS):
    critique = critic(draft, CRITERIA)
    print("  critique:", critique)
    if critique["verdict"] == "pass":
        stop_reason = "criteria met"
        break
    draft = producer(TASK, feedback=critique["issues"])

print(f"\nstop reason: {stop_reason}\nfinal draft:\n{draft}")
