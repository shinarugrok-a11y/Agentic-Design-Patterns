# Planning — patterns (Ch 6)

## Pattern
1. State the goal and constraints.
2. Planner emits numbered steps with dependencies.
3. Executor follows the plan; report per step.
4. Re-plan when a step fails or new facts appear.

## Prompt template
```
Planner: Create a plan for {goal}. Output numbered steps, each with inputs, expected output
and the tool or agent responsible. Keep to 5-8 steps.
Writer: Follow the plan exactly. Mark each step done and note deviations.
```

## Key APIs
- CrewAI: `Agent(role='Planner')`, `Agent(role='Writer')`; `Task(context=[plan_task])`; `Process.sequential`.
- OpenAI Deep Research: plan -> search -> synthesise loop as a built-in planner.
- Keep plan as JSON list so executors can check it.

## Pitfalls -> fixes
- Missing steps -> ask the planner to list assumptions and risks.
- Stale plan -> re-plan trigger on failure.
- Over-planning -> skip for single-step tasks.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_06_*`.
