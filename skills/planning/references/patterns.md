# Planning

Ch 6.

## Frameworks
- CrewAI (planner Agent/Task/Crew, Process.sequential); OpenAI Deep Research API.

## Key APIs from the notebooks
- `CrewAI: planner Agent + Task with Process.sequential Crew`
- `Deep Research notebook: research task submission + polling for the plan/result`
- `Plan represented as ordered steps with owners before any execution call`

## Code patterns
- Pattern: goal -> explicit step plan (with deps + success criteria) -> execute -> replan on failure.
- Write success criteria per step, not just per goal.
- Replan from the failed step; do not restart blindly.

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_06_Planning_(Code_Example).ipynb`
- `chapter_notebooks/Chapter_06_Planning_(Deep_Research_API).ipynb`

