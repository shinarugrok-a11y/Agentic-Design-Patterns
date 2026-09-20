# Exploration patterns (Ch 21)

One primary notebook (+ blank second cell): AgentLaboratory multi-role research team.

Pattern (`agents.py`): `ReviewersAgent(model='gpt-4o-mini', notes=[])` with `inference(plan, report)` — "harsh but fair reviewer, expect good experiments that lead to insights"; paired with planner + worker roles running propose -> experiment -> review -> synthesize.

Rules: exploration budget up front (time/iterations); every claim needs an experiment behind it; reviewer gate is mandatory before any finding ships; final synthesis step is scheduled, not optional.

## Notebook extracts (on-demand detail)

### Chapter_21_Exploration_Discovery_(Agent_Laboratory).ipynb

```python
class ReviewersAgent:
def __init__(self, model="gpt-4o-mini", notes=None, openai_api_key=None):
def inference(self, plan, report):
def get_score(outlined_plan, latex, reward_model_llm, reviewer_type=None, attempts=3, openai_api_key=None):
class ProfessorAgent(BaseAgent):
def __init__(self, model="gpt4omini", notes=None, max_steps=100, openai_api_key=None):
def generate_readme(self):
class PostdocAgent(BaseAgent):
def __init__(self, model="gpt4omini", notes=None, max_steps=100, openai_api_key=None):
def context(self, phase):
```
