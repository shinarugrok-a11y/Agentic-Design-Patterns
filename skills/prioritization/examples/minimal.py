"""Chapter 20 — In-memory prioritized tasks (P0/P1/P2)."""
from pydantic import BaseModel

class Task(BaseModel):
    id: str
    description: str
    priority: str = "P1"
    assignee: str = "Worker A"

class SuperSimpleTaskManager:
    def __init__(self):
        self.tasks, self.next_id = {}, 1
    def create_task(self, description: str) -> Task:
        tid = f"TASK-{self.next_id:03d}"; self.next_id += 1
        self.tasks[tid] = Task(id=tid, description=description)
        return self.tasks[tid]
    def assign_priority(self, task_id: str, priority: str) -> Task:
        self.tasks[task_id] = self.tasks[task_id].model_copy(update={"priority": priority})
        return self.tasks[task_id]
