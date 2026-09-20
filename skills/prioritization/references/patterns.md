# Prioritization — patterns (Ch 20)

## Pattern
1. Collect tasks with urgency, importance, dependencies, cost.
2. Score with an explicit formula or rubric.
3. Order; expose the rationale.
4. Re-rank when new tasks arrive.

## Prompt template
```
You are a project manager. Use tools in order: create_new_task first to get an id,
then assign_priority(task_id, P0|P1|P2), then list_tasks.
Priority: P0 blocks others or is due today; P1 due this week; P2 otherwise.
```

## Key APIs
- LangChain ReAct agent with `create_new_task`, `assign_priority`, `list_tasks` tools.
- Formula: `3*urgency + 2*importance - cost + blocked_count`.
- Keep the task store as a dict keyed by id.

## Pitfalls -> fixes
- Everything P0 -> cap P0 count.
- Priority before id -> enforce tool order in prompt.
- Stale ranking -> re-score on each new task.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_20_*`.
