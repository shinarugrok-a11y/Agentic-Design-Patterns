# Prioritization — Pattern reference

Load this file only when implementing `prioritization`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when many actions compete under limited time/budget; rank by urgency, value, and dependencies.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Prioritization design pattern.

## Notebooks (extracted)

Prioritization

### Notebooks
- `Chapter_20_Prioritization_(SuperSimplePM).ipynb`

### Patterns
- **In-memory task manager:** Pydantic `Task` model; dict for O(1) lookup; `model_copy(update=...)`
- **Priority levels:** P0 (urgent/ASAP/critical), P1 (default), P2
- **ReAct PM agent:** `create_react_agent` + tools with `args_schema` (Pydantic)
- **Workflow:** create task first → assign priority/worker → list_all_tasks
- **Default assignment:** agent fills missing priority/assignee with P1 / Worker A

### Prompt templates
PM system prompt:
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

### Minimal code
```python
class SuperSimpleTaskManager:
    def create_task(self, description: str) -> Task:
        task_id = f"TASK-{self.next_task_id:03d}"
        self.tasks[task_id] = Task(id=task_id, description=description)
        return self.tasks[task_id]

pm_agent_executor = AgentExecutor(
    agent=create_react_agent(llm, pm_tools, pm_prompt_template),
    tools=pm_tools,
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
    handle_parsing_errors=True,
)
await pm_agent_executor.ainvoke({"input": "Create urgent login task for Worker B"})
```

### Caveats
- In-memory only — no persistence across restarts
- Requires `OPENAI_API_KEY` via `.env`
- Urgency→P0 mapping is agent-interpreted, not rule-based
- `handle_parsing_errors=True` masks ReAct format failures

---

## Failure modes (skill-level)
- Everything tagged P0
- In-memory queue lost on restart
- Agent invents owners not in the allowlist

## Chains with
`planning`, `resource-aware-optimization`
