"""Ranks ready tasks by explicit weights plus aging, then acts on the top one.

Real framework: LangChain create_react_agent + AgentExecutor driving typed
tools (assign_priority_to_task with a Pydantic PriorityArgs schema).
Run: python3 examples/minimal.py
"""

W = {"urgency": 0.4, "importance": 0.4, "cost": -0.2}   # explicit weights
AGING = 0.05                                            # per tick in queue

TASKS = [
    {"id": "T1", "desc": "restore checkout outage", "depends_on": [],
     "urgency": 0.9, "importance": 1.0, "cost": 0.6, "waited": 0},
    {"id": "T2", "desc": "ship billing report", "depends_on": ["T1"],
     "urgency": 0.8, "importance": 0.7, "cost": 0.3, "waited": 2},
    {"id": "T3", "desc": "tidy onboarding docs", "depends_on": [],
     "urgency": 0.1, "importance": 0.2, "cost": 0.1, "waited": 9},
]


def llm(task: dict) -> str:
    """Canned worker: the action taken once a task is selected."""
    return f"handled '{task['desc']}'"


def rank(tasks, done):
    ready = [t for t in tasks if set(t["depends_on"]) <= done]
    for t in ready:
        t["score"] = round(sum(W[k] * t[k] for k in W) + AGING * t["waited"], 3)
    return sorted(ready, key=lambda t: t["score"], reverse=True)


done, queue = set(), list(TASKS)
print(f"weights={W} aging={AGING}/tick\n")
while queue:
    ready = rank(queue, done)
    blocked = [t["id"] for t in queue if t not in ready]
    top = ready[0]
    print(f"ready={[(t['id'], t['score']) for t in ready]} blocked={blocked}")
    print(f"  -> picked {top['id']}: {llm(top)}\n")
    done.add(top["id"])
    queue.remove(top)
    for t in queue:
        t["waited"] += 1          # aging keeps low-priority work from starving
