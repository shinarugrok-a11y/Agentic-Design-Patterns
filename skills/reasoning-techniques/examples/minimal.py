"""Reasoning techniques: ReAct loop (Thought -> Action -> Observation) with a
bounded number of steps, plus a labelled CoT trace separated from the answer.

Offline stub: `think` is a scripted stand-in for the model.
"""
TOOLS = {
    "search": lambda q: {"population of earth": "about 8 billion"}.get(q.lower(), "no result"),
    "calc": lambda expr: str(eval(expr, {"__builtins__": {}})),
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
