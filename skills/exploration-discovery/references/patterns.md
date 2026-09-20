# Exploration and Discovery

Ch 21.

## Frameworks
- Agent Laboratory pattern (professor/postdoc/reviewer agents, OpenAI models).

## Key APIs from the notebooks
- `ReviewersAgent.inference(plan, report); get_score(outlined_plan, latex, reward_llm, attempts=3)`
- `ProfessorAgent(BaseAgent, max_steps=100): proposes plans; generate_readme()`
- `PostdocAgent(BaseAgent, max_steps=100): executes phases via context(phase)`

## Code patterns
- Pattern: propose -> reviewer score (attempts=3) -> execute capped steps -> compile README/report.
- Gate every expensive phase on a reviewer score.
- Cap executors with max_steps=100.

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb`

