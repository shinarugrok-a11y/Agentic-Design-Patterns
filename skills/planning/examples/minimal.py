"""Planning: decompose a goal into ordered steps, execute, re-plan on failure.

Offline stub. `make_plan` and `replan` stand in for LLM calls that return a
JSON plan; `execute` stands in for tool-use or sub-agent delegation.
"""
from dataclasses import dataclass, field


@dataclass
class Step:
    id: int
    action: str
    depends_on: list[int] = field(default_factory=list)


def make_plan(goal: str) -> list[Step]:
    return [Step(1, "search sources"), Step(2, "extract key facts", [1]),
            Step(3, "draft report", [2]), Step(4, "add citations", [1, 3])]


def execute(step: Step, state: dict) -> tuple[bool, str]:
    if step.action == "search sources" and not state.get("retried"):
        return False, "search API timeout"          # first attempt fails
    return True, f"done: {step.action}"


def replan(plan: list[Step], failed: Step, state: dict) -> list[Step]:
    state["retried"] = True
    return plan                                      # simple retry policy


def run(goal: str) -> dict:
    plan, state, i = make_plan(goal), {}, 0
    while i < len(plan):
        step = plan[i]
        assert all(d in state for d in step.depends_on), "dependency not satisfied"
        ok, result = execute(step, state)
        if not ok:
            print(f"step {step.id} failed ({result}); re-planning")
            plan = replan(plan, step, state)
            continue
        state[step.id] = result
        i += 1
    return state


if __name__ == "__main__":
    for k, v in run("Write a cited report on topic X").items():
        print(k, v)
