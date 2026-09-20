# Prioritization patterns (Ch 20)

One notebook: SuperSimplePM ReAct agent.

Pattern: ReAct agent (`create_react_agent` + `AgentExecutor`) with `ChatOpenAI` + `ConversationBufferMemory`, `ChatPromptTemplate` scoring prompt, Pydantic `BaseModel/Field` task schemas (`List, Optional, Dict, Type`), `Tool` wrappers for backlog ops; `.env` + `load_dotenv()` for `OPENAI_API_KEY`; `asyncio` execution.

Scoring prompt: weights value/urgency/effort explicitly; outputs ranked list with one-line justification per item; commits top-N, queues rest.

Rule: re-score whenever backlog changes; enforce a WIP cap so ranking means something.

## Notebook extracts (on-demand detail)

### Chapter_20_Prioritization_(SuperSimplePM).ipynb

```python
class Task(BaseModel):
class SuperSimpleTaskManager:
def __init__(self):
def create_task(self, description: str) -> Task:
def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
def list_all_tasks(self) -> str:
class CreateTaskArgs(BaseModel):
class PriorityArgs(BaseModel):
class AssignWorkerArgs(BaseModel):
def create_new_task_tool(description: str) -> str:
```
