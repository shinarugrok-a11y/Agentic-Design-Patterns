"""Goal loop: act, re-check every success criterion each step, then stop or escalate.

Real framework: LangChain generate -> critique -> a judge prompt answering only
"True"/"False", wrapped in `for i in range(max_iterations)`.
Run: python3 examples/minimal.py
"""

GOAL = {"objective": "resolve billing dispute",
        "done_when": ["refund posted", "customer confirms"],
        "max_steps": 5}

TRANSCRIPT = []


def act(step: int) -> str:
    """Fake agent turn: each step adds one observable fact to the transcript."""
    return ["ticket opened", "refund posted", "policy cited", "customer confirms"][step % 4]


def judge(criterion: str) -> bool:
    """Fake LLM judge: one criterion in, a hard boolean out."""
    return criterion in TRANSCRIPT


def check(done_when: list, step: int) -> dict:
    missing = [c for c in done_when if not judge(c)]
    return {"met": not missing,
            "missing": missing,
            "at_risk": bool(missing) and step >= GOAL["max_steps"] // 2}


status = {"missing": GOAL["done_when"]}
for step in range(GOAL["max_steps"]):
    TRANSCRIPT.append(act(step))
    status = check(GOAL["done_when"], step)
    print(f"step {step}: did {TRANSCRIPT[-1]!r} | still missing {status['missing']}")
    if status["met"]:
        print(f"goal met: {GOAL['objective']}")
        break
    if status["at_risk"]:
        print(f"  at risk with {GOAL['max_steps'] - step - 1} steps left, escalating")
else:
    print(f"budget exhausted, unmet criteria: {status['missing']}")
