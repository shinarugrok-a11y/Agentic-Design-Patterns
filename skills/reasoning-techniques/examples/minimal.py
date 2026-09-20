"""ReAct loop: think, act, observe, repeat under a step cap, breaking on repeats.

Real framework: LangGraph cycle where a reflection node routes back to the
research node via add_conditional_edges until it routes to finalize_answer.
Run: python3 examples/minimal.py
"""

MAX_STEPS = 6
TOOLS = {
    "search": lambda q: "Ada Lovelace was born in 1815." if "born" in q else "no hits",
    "calc": lambda q: str(2026 - 1815),
}


def llm_step(history):
    """Fake reasoner: picks the next action from what has been observed so far."""
    seen = " ".join(history)
    if "1815" not in seen:
        return "I need her birth year.", ("search", "when was Ada Lovelace born")
    if "211" not in seen:
        return "Now subtract from this year.", ("calc", "2026 - 1815")
    return "I have everything.", ("final", "Ada Lovelace would be 211 years old.")


history, tried = [], set()
for step in range(MAX_STEPS):
    thought, (name, args) = llm_step(history)
    print(f"step {step}\n  thought: {thought}\n  action: {name}({args!r})")
    if name == "final":
        print(f"  answer: {args}")
        break
    if (name, args) in tried:
        print("  loop detected, stopping")
        break
    tried.add((name, args))
    observation = TOOLS[name](args)
    print(f"  observation: {observation}")
    history += [thought, f"{name}({args})", observation]
else:
    print(f"step cap {MAX_STEPS} reached without an answer")
