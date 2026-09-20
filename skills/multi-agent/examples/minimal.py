"""Multi-agent: coordinator delegates to specialists via shared state.

Offline stub of the ADK shapes: a coordinator that only delegates, a
sequential pipeline handing off through `state`, and a loop with an
escalating condition checker.
"""
from typing import Callable

State = dict


class Agent:
    def __init__(self, name: str, description: str, run: Callable[[str, State], str], output_key: str | None = None):
        self.name, self.description, self._run, self.output_key = name, description, run, output_key

    def __call__(self, msg: str, state: State) -> str:
        out = self._run(msg, state)
        if self.output_key:
            state[self.output_key] = out
        return out


def coordinator(msg: str, state: State, sub_agents: list[Agent]) -> str:
    """Delegate only. Picks the sub-agent whose description matches best."""
    scores = {a: sum(w in a.description.lower() for w in msg.lower().split()) for a in sub_agents}
    best = max(scores, key=scores.get)
    return f"[Coordinator -> {best.name}] " + best(msg, state)


def sequential(msg: str, state: State, steps: list[Agent]) -> str:
    out = msg
    for step in steps:
        out = step(out, state)
    return out


def loop(msg: str, state: State, body: Agent, done: Callable[[State], bool], max_iterations: int = 5) -> str:
    for i in range(max_iterations):
        body(msg, state)
        if done(state):                      # ConditionChecker -> escalate=True
            return f"loop finished after {i + 1} iteration(s)"
    return "max_iterations reached"


if __name__ == "__main__":
    state: State = {}
    greeter = Agent("Greeter", "greet users hello", lambda m, s: "Hello there!")
    booker = Agent("Booker", "book flights hotels travel", lambda m, s: f"booked: {m}")
    print(coordinator("please book a hotel", state, [greeter, booker]))

    fetch = Agent("Fetch", "", lambda m, s: "raw data about " + m, output_key="data")
    summarise = Agent("Summarise", "", lambda m, s: f"summary of {s['data']}")
    print(sequential("solar power", state, [fetch, summarise]))

    counter = Agent("Step", "", lambda m, s: s.__setitem__("n", s.get("n", 0) + 1) or "step")
    print(loop("go", state, counter, done=lambda s: s.get("n", 0) >= 3))
