# Prioritization — Patterns

## Pattern variants
- **Criteria scoring** — weight urgency, importance, dependencies, resource availability, and cost/benefit into one number; reproducible and auditable.
- **Priority tiers** — map language ("urgent", "ASAP", "critical") onto a fixed ladder such as P0/P1/P2, with a stated default (P1) when the request says nothing.
- **LLM-as-ranker** — the model reads the request and applies the criteria in its instruction; use when criteria are fuzzy or user-stated, not when the ranking must be reproducible.
- **Dependency-aware selection** — filter to tasks whose prerequisites are done before scoring, so blocked work never reaches the top.
- **Dynamic re-prioritization** — recompute on a triggering event (new critical alert, approaching deadline), not on every tick.
- **Level of prioritization** — high-level goal selection, sub-task ordering inside a plan, or immediate action selection; pick one level per ranking pass.

## Prompt templates

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

## Code patterns

LangChain (ReAct agent + typed tools) — ranking is exposed as tools over a task store, so every priority change is a logged, validated call:

```python
class Task(BaseModel):
    id: str
    description: str
    priority: Optional[str] = None      # P0, P1, P2
    assigned_to: Optional[str] = None

class PriorityArgs(BaseModel):
    task_id: str = Field(description="e.g. 'TASK-001'")
    priority: str = Field(description="One of: 'P0', 'P1', 'P2'.")

pm_tools = [Tool(name="assign_priority_to_task", func=assign_priority_to_task_tool,
                 description="Assign a priority to a task after it is created.",
                 args_schema=PriorityArgs), ...]

pm_agent = create_react_agent(llm, pm_tools, pm_prompt_template)
pm_agent_executor = AgentExecutor(agent=pm_agent, tools=pm_tools,
    handle_parsing_errors=True,
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True))
```

The tool validates before it mutates (`if priority not in ["P0","P1","P2"]`) and `update_task` uses `model_copy(update=...)` for a type-safe write.

## Framework notes
- **LangChain** — `create_react_agent` + `AgentExecutor`, Pydantic `args_schema` per tool, `ConversationBufferMemory` so re-prioritization sees earlier decisions.
- **Google ADK / CrewAI** — no prioritization example in this chapter; the same shape works as a ranking tool plus `session.state` for the queue.

## Failure modes in depth
- **Unstated weights** — an LLM ranking with no written criteria cannot be reproduced or reviewed; put the weights and the default tier in the instruction, and keep the scoring in a tool rather than in free text.
- **Re-ranking thrash** — recomputing every tick makes the agent switch tasks mid-flight; re-prioritize only on events that change the inputs, and keep the current task unless the new top item beats it by a margin.
- **Dependencies ignored** — a high-urgency item whose prerequisite is unfinished scores top and then stalls; build the ready set first (`depends_on` satisfied), then score only that set.
- **Starvation** — P2 items never surface under a pure score sort; add an aging term that raises a task's score with queue time, or reserve capacity per tier.

## Source
Chapter 20 of "Agentic Design Patterns" (Gulli). Notebook: Chapter_20_Prioritization_(SuperSimplePM).ipynb.
