# Prioritization — deep dive

Source: Chapter 20 + `Chapter_20_Prioritization_(SuperSimplePM).ipynb`.

## Criteria (book)
Urgency, importance, dependencies, resource cost, expected value/benefit,
user preferences, alignment with strategic goals. Prioritisation happens at
several levels: strategic objectives, tactical steps, immediate actions.
Dynamic re-prioritisation adjusts focus as conditions change.

Rule of thumb: an agent must autonomously manage multiple, possibly
conflicting tasks or goals under resource constraints in a dynamic setting.
Examples: support triage (outage > password reset; high-value customers),
cloud scheduling (critical apps at peak, batch off-peak), driving safety
(brake > lane discipline), trading, project boards, cyber alerts by
severity, personal assistants.

## Notebook: Project Manager agent (LangChain ReAct)
### Data + manager
```python
class Task(BaseModel):
    id: str
    description: str
    priority: Optional[str] = None      # P0, P1, P2
    assigned_to: Optional[str] = None

class SuperSimpleTaskManager:
    def __init__(self): self.tasks: Dict[str, Task] = {}; self.next_task_id = 1
    def create_task(self, description):
        task_id = f"TASK-{self.next_task_id:03d}"; self.tasks[task_id] = Task(id=task_id, description=description)
        self.next_task_id += 1; return self.tasks[task_id]
    def update_task(self, task_id, **kwargs):
        task = self.tasks.get(task_id)
        if task:
            self.tasks[task_id] = task.model_copy(update={k: v for k, v in kwargs.items() if v is not None})
            return self.tasks[task_id]
    def list_all_tasks(self) -> str: ...
```
### Tools with Pydantic arg schemas
```python
class PriorityArgs(BaseModel):
    task_id: str = Field(description="The ID of the task to update, e.g., 'TASK-001'.")
    priority: str = Field(description="The priority to set. Must be one of: 'P0', 'P1', 'P2'.")

def assign_priority_to_task_tool(task_id: str, priority: str) -> str:
    if priority not in ["P0", "P1", "P2"]:
        return "Invalid priority. Must be P0, P1, or P2."
    task = task_manager.update_task(task_id, priority=priority)
    return f"Assigned priority {priority} to task {task.id}." if task else f"Task {task_id} not found."

pm_tools = [
    Tool(name="create_new_task", func=create_new_task_tool, description="Use this first to create a new task and get its ID.", args_schema=CreateTaskArgs),
    Tool(name="assign_priority_to_task", func=assign_priority_to_task_tool, description="Use this to assign a priority to a task after it has been created.", args_schema=PriorityArgs),
    Tool(name="assign_task_to_worker", func=assign_task_to_worker_tool, description="Use this to assign a task to a specific worker after it has been created.", args_schema=AssignWorkerArgs),
    Tool(name="list_all_tasks", func=task_manager.list_all_tasks, description="Use this to list all current tasks and their status."),
]
```
### System prompt (the prioritisation policy)
```
You are a focused Project Manager LLM agent. Your goal is to manage project tasks efficiently.

When you receive a new task request, follow these steps:
1.  First, create the task with the given description using the `create_new_task` tool. You must do this first to get a `task_id`.
2.  Next, analyze the user's request to see if a priority or an assignee is mentioned.
    - If a priority is mentioned (e.g., "urgent", "ASAP", "critical"), map it to P0. Use `assign_priority_to_task`.
    - If a worker is mentioned, use `assign_task_to_worker`.
3.  If any information (priority, assignee) is missing, you must make a reasonable default assignment (e.g., assign P1 priority and assign to 'Worker A').
4.  Once the task is fully processed, use `list_all_tasks` to show the final state.

Available workers: 'Worker A', 'Worker B', 'Review Team'
Priority levels: P0 (highest), P1 (medium), P2 (lowest)
```
### Executor
```python
pm_agent = create_react_agent(llm, pm_tools, pm_prompt_template)   # prompt has {chat_history}, {input}, {agent_scratchpad}
pm_agent_executor = AgentExecutor(agent=pm_agent, tools=pm_tools, verbose=True, handle_parsing_errors=True,
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True))
await pm_agent_executor.ainvoke({"input": "Create a task to implement a new login system. It's urgent and should be assigned to Worker B."})
await pm_agent_executor.ainvoke({"input": "Manage a new task: Review marketing website content."})   # defaults apply
```

## Scoring formula (for many tasks)
```
score = w_u * urgency + w_i * importance + w_v * value - w_c * cost
subject to: dependencies satisfied; capacity per worker; hard deadlines first
```
Re-score on every new event (new task, failure, deadline change) and keep
a stable tie-break (creation order) to avoid thrashing.

## Ranking prompt template
```
Tasks: {json list with id, description, deadline, deps, est_cost}
Criteria (in order): safety/urgency, hard deadlines, blocking dependencies,
business value, cost. Return JSON: [{"id":..., "priority": "P0|P1|P2", "reason":...}] sorted by priority.
Never assign P0 to more than {n} tasks.
```

## Checklist
- Validate priority values inside the tool, not only in the prompt.
- Create before prioritise (ids first).
- Explicit defaults for missing info.
- Bound P0 count; re-rank on change; log rationale.

## Pattern variants
- **Criteria scoring** — weight urgency, importance, dependencies, resource availability, and cost/benefit into one number; reproducible and auditable.
- **Priority tiers** — map language ("urgent", "ASAP", "critical") onto a fixed ladder such as P0/P1/P2, with a stated default (P1) when the request says nothing.
- **LLM-as-ranker** — the model reads the request and applies the criteria in its instruction; use when criteria are fuzzy or user-stated, not when the ranking must be reproducible.
- **Dependency-aware selection** — filter to tasks whose prerequisites are done before scoring, so blocked work never reaches the top.
- **Dynamic re-prioritization** — recompute on a triggering event (new critical alert, approaching deadline), not on every tick.
- **Level of prioritization** — high-level goal selection, sub-task ordering inside a plan, or immediate action selection; pick one level per ranking pass.

## More prompt templates
Project-manager agent instruction (from the chapter's `pm_prompt_template` system message):

```
You are a focused Project Manager agent. When you receive a task request:
1. Create the task with `create_new_task` first - you need the task_id.
2. Inspect the request for a priority or an assignee.
   - Urgency words ("urgent", "ASAP", "critical") map to P0; use
     `assign_priority_to_task`.
   - A named worker goes to `assign_task_to_worker`.
3. If priority or assignee is missing, apply the default: P1, 'Worker A'.
4. Finish with `list_all_tasks` to show the resulting queue.
Workers: 'Worker A', 'Worker B', 'Review Team'.
Priorities: P0 (highest), P1 (medium), P2 (lowest).
```

State the tie-break and the default in the prompt; an unstated default is an invisible ranking rule.

## Framework notes
- **LangChain** — `create_react_agent` + `AgentExecutor`, Pydantic `args_schema` per tool, `ConversationBufferMemory` so re-prioritization sees earlier decisions.
- **Google ADK / CrewAI** — no prioritization example in this chapter; the same shape works as a ranking tool plus `session.state` for the queue.

## Failure modes in depth
- **Unstated weights** — an LLM ranking with no written criteria cannot be reproduced or reviewed; put the weights and the default tier in the instruction, and keep the scoring in a tool rather than in free text.
- **Re-ranking thrash** — recomputing every tick makes the agent switch tasks mid-flight; re-prioritize only on events that change the inputs, and keep the current task unless the new top item beats it by a margin.
- **Dependencies ignored** — a high-urgency item whose prerequisite is unfinished scores top and then stalls; build the ready set first (`depends_on` satisfied), then score only that set.
- **Starvation** — P2 items never surface under a pure score sort; add an aging term that raises a task's score with queue time, or reserve capacity per tier.
