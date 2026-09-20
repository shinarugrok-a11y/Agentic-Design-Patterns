# Prioritization

Ch 20.

## Frameworks
- LangChain (ChatOpenAI, ChatPromptTemplate, Tool wrappers); pydantic task models.

## Key APIs from the notebooks
- `Task(BaseModel): description/priority/owner/status; CreateTaskArgs / PriorityArgs / AssignWorkerArgs`
- `SuperSimpleTaskManager: create_task / update_task / list_all_tasks`
- `create_new_task_tool / priority + assign tools wrapping the manager`

## Code patterns
- Pattern: create (typed) -> score priority -> order -> assign to worker -> track status.
- Typed tool args (PriorityArgs, AssignWorkerArgs) keep agent updates valid.
- Re-score on new arrivals; age old tasks.

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_20_Prioritization_(SuperSimplePM).ipynb`

