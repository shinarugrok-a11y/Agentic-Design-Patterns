"""Planning: decompose a goal into a dependency-ordered plan, execute it, and replan when a step's success test fails.

Real framework: CrewAI Task(description="1. Create a plan... 2. Execute it") run by Crew(process=Process.sequential)
Run: python3 examples/minimal.py
"""

TOOLS = {"search": "3 sources found", "draft": "600-word draft"}


def llm(goal: str, failure: dict = None) -> list:
    """Fake planner: first plan invents a tool that does not exist; the replan drops it."""
    plan = [
        {"id": 1, "action": "search", "depends_on": [], "done_when": "3 sources found"},
        {"id": 2, "action": "translate", "depends_on": [1], "done_when": "text in French"},
        {"id": 3, "action": "draft", "depends_on": [1], "done_when": "600-word draft"},
    ]
    if failure:
        plan = [s for s in plan if s["action"] in TOOLS]
    return plan


def topological_order(plan: list) -> list:
    ordered, done = [], set()
    for _ in range(len(plan)):
        for step in plan:
            if step["id"] not in done and set(step["depends_on"]) <= done:
                ordered.append(step)
                done.add(step["id"])
    return ordered


def execute(step):
    return TOOLS.get(step["action"], f"no tool named {step['action']!r}")


def meets(done_when, result):
    return done_when == result


goal = "Write a short research note"
plan, satisfied = llm(goal), set()
for attempt in range(2):
    replanned = False
    for step in topological_order(plan):
        if step["action"] in satisfied:
            continue
        result = execute(step)
        if meets(step["done_when"], result):
            print(f"step {step['id']} {step['action']}: {result}")
            satisfied.add(step["action"])
        else:
            print(f"step {step['id']} {step['action']}: {result} -- done_when unmet, replanning")
            plan = llm(goal, failure=step)
            replanned = True
            break
    if not replanned:
        break

print("goal reached via:", sorted(satisfied))
