# Routing patterns (Ch 2)

Three notebook variants: Google ADK router agent, LangGraph `RunnableBranch`, OpenRouter model routing.

Pattern A — ADK router: one classifier `Agent` with `FunctionTool`s per lane; router instruction lists lanes and calls the matching tool. Variants: `InMemoryRunner` + typed `Event` results.

Pattern B — LangGraph `RunnableBranch`: `ChatPromptTemplate` classifier piped into `RunnableBranch((condition, runnable), default)`; each branch is its own chain. Good for 2-5 lanes with prompt-level conditions.

Pattern C — OpenRouter: route by model (`openai/gpt-4o` vs cheaper models) via `POST /api/v1/chat/completions` with per-route model + headers. Use for cost-tier routing.

Prompt templates: classifier prompt enumerates lanes with 1-line criteria each and demands a single label + confidence. Always include an `other/fallback` lane.

## Notebook extracts (on-demand detail)

### Chapter_02_Routing_(Google_ADK).ipynb

```python
def booking_handler(request: str) -> str:
def info_handler(request: str) -> str:
def unclear_handler(request: str) -> str:
booking_tool = FunctionTool(booking_handler)
info_tool = FunctionTool(info_handler)
booking_agent = Agent(
info_agent = Agent(
coordinator = Agent(
instruction=(
def run_coordinator(runner: InMemoryRunner, request: str):
```

### Chapter_02_Routing_(LangGraph).ipynb

```python
def booking_handler(request: str) -> str:
def info_handler(request: str) -> str:
def unclear_handler(request: str) -> str:
coordinator_router_prompt = ChatPromptTemplate.from_messages([
# Use RunnableBranch to route based on the router chain's output.
# Define the branches for the RunnableBranch
"booker": RunnablePassthrough.assign(output=lambda x: booking_handler(x['request']['request'])),
"info": RunnablePassthrough.assign(output=lambda x: info_handler(x['request']['request'])),
delegation_branch = RunnableBranch(
def main():
```

### Chapter_02_Routing_(Openrouter).ipynb

```python
import requests
import json
```
