"""Prioritization: create -> rank by explicit criteria -> assign -> re-rank.

Offline stub of the SuperSimplePM flow with a scoring formula instead of an
LLM. Tool ordering (create first) and value validation are enforced.
"""
from dataclasses import dataclass

WORKERS = ["Worker A", "Worker B", "Review Team"]
URGENT = ("urgent", "asap", "critical", "outage")


@dataclass
class Task:
    id: str
    description: str
    priority: str | None = None
    assigned_to: str | None = None
    deadline_days: int = 30
    blocks: int = 0                 # number of tasks depending on this one


class TaskManager:
    def __init__(self):
        self.tasks: dict[str, Task] = {}

    def create_task(self, description: str, **kw) -> Task:
        tid = f"TASK-{len(self.tasks) + 1:03d}"
        self.tasks[tid] = Task(tid, description, **kw)
        return self.tasks[tid]

    def assign_priority(self, tid: str, priority: str) -> str:
        if priority not in ("P0", "P1", "P2"):
            return "Invalid priority. Must be P0, P1, or P2."
        self.tasks[tid].priority = priority
        return f"{tid} -> {priority}"

    def assign_worker(self, tid: str, worker: str) -> str:
        self.tasks[tid].assigned_to = worker if worker in WORKERS else "Worker A"
        return f"{tid} -> {self.tasks[tid].assigned_to}"


def score(t: Task) -> float:
    urgency = 3 if any(w in t.description.lower() for w in URGENT) else 0
    return urgency + t.blocks * 1.5 + max(0, 10 - t.deadline_days) / 2


def rerank(tm: TaskManager, max_p0: int = 1):
    ranked = sorted(tm.tasks.values(), key=score, reverse=True)
    for i, t in enumerate(ranked):
        tm.assign_priority(t.id, "P0" if i < max_p0 and score(t) >= 3 else "P1" if score(t) >= 1 else "P2")
    return ranked


if __name__ == "__main__":
    tm = TaskManager()
    t1 = tm.create_task("Implement new login system ASAP", deadline_days=5)
    tm.assign_worker(t1.id, "Worker B")
    t2 = tm.create_task("Review marketing website content")
    t3 = tm.create_task("Fix outage in payment API", deadline_days=1, blocks=2)
    for t in rerank(tm):
        print(f"{t.id} {t.priority} {t.assigned_to or 'Worker A':12} score={score(t):.1f} {t.description}")
