"""Reasoning techniques: ReAct loop (Thought -> Action -> Observation) with a
bounded number of steps, plus a labelled CoT trace separated from the answer.

Offline stub: `think` is a scripted stand-in for the model.
"""
import ast
import operator

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.USub: operator.neg}


def calc(expr: str) -> str:
    """Arithmetic only (+ - * / and unary minus on numbers). Never eval model output."""
    if not isinstance(expr, str) or len(expr) > 100:
        return "calc error: expression must be text of at most 100 characters"

    def ev(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
            return OPS[type(node.op)](ev(node.operand))
        raise ValueError
    try:
        return str(ev(ast.parse(expr, mode="eval").body))
    except (SyntaxError, ValueError, ZeroDivisionError):
        return "calc error: unsupported expression"


TOOLS = {
    "search": lambda q: {"population of earth": "about 8 billion"}.get(q.lower(), "no result"),
    "calc": calc,
}
MAX_STEPS = 5


def think(question: str, scratchpad: list[str]) -> dict:
    """Stand-in for the model. Returns an action or a final answer."""
    if not scratchpad:
        return {"thought": "I need the population first.", "action": "search", "input": "population of earth"}
    if len(scratchpad) == 1:
        return {"thought": "Half of 8 billion is needed.", "action": "calc", "input": "8_000_000_000 / 2"}
    return {"thought": "I have everything.", "final": "Roughly 4 billion people."}


def react(question: str) -> tuple[list[str], str]:
    scratchpad: list[str] = []
    for step in range(MAX_STEPS):
        out = think(question, scratchpad)
        if "final" in out:
            return scratchpad + [f"Thought {step + 1}: {out['thought']}"], out["final"]
        observation = TOOLS[out["action"]](out["input"])
        scratchpad.append(f"Thought {step + 1}: {out['thought']} | Action: {out['action']}({out['input']!r}) "
                          f"| Observation: {observation}")
    return scratchpad, "Stopped: step budget exhausted."


if __name__ == "__main__":
    trace, answer = react("How many people is half the world's population?")
    print("=== reasoning trace (not user-facing) ===")
    print("\n".join(trace))
    print("=== final answer ===")
    print(answer)
    for bad in ("__import__('os').system('true')", "(1).__class__", "2**10**10"):
        if not calc(bad).startswith("calc error"):
            raise SystemExit(f"calc accepted {bad!r}")
