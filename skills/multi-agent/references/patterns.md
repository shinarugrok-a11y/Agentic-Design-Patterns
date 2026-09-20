# Multi-Agent patterns (Ch 7)

Six notebook variants, all ADK/CrewAI: Sequential, Parallel, Loop, Coordinator, AgentTool, CrewAI crew.

Topologies: `SequentialAgent([Step1_Fetch(output_key='data'), Step2_Process])` for pipelines; `ParallelAgent([weather_fetcher, news_fetcher])` for fan-out; `LoopAgent([worker, ConditionChecker])` with `EventActions` exit for iterate-until-done; custom `BaseAgent._run_async_impl` coordinator delegating to `TaskExecutor`; `agent_tool` wrapping a specialist (e.g. image generator) as a callable tool; CrewAI `Crew(Process.sequential)` content team.

State rule: pass data via `output_key`/`session.state`, never by hoping the next agent "remembers". Keep roles broad (3-5 agents max).

## Notebook extracts (on-demand detail)

### Chapter_07_Multi_Agent_(ADK_Gemini_AgentTool).ipynb

```python
def generate_image(prompt: str) -> dict:
image_generator_agent = LlmAgent(
instruction=(
image_tool = agent_tool.AgentTool(
artist_agent = LlmAgent(
instruction=(
from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.genai import types
# 1. A simple function tool for the core capability.
```

### Chapter_07_Multi_Agent_(ADK_Gemini_Coordinator).ipynb

```python
class TaskExecutor(BaseAgent):
async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
greeter = LlmAgent(
instruction="You are a friendly greeter."
coordinator = LlmAgent(
instruction="When asked to greet, delegate to the Greeter. When asked to perform a task, delegate to the TaskExecutor.",
from google.adk.agents import LlmAgent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
# Correctly implement a custom agent by extending BaseAgent
```

### Chapter_07_Multi_Agent_(ADK_Gemini_Loop).ipynb

```python
class ConditionChecker(BaseAgent):
async def _run_async_impl(
process_step = LlmAgent(
instruction="You are a step in a longer process. Perform your task. If you are the final step, update session state by setting 'status' to 'completed'."
# The LoopAgent orchestrates the workflow.
poller = LoopAgent(
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
# Escalate to terminate the loop when the condition is met.
```

### Chapter_07_Multi_Agent_(ADK_Gemini_Parallel).ipynb

```python
weather_fetcher = Agent(
instruction="Fetch the weather for the given location and return only the weather report.",
output_key="weather_data"  # The result will be stored in session.state["weather_data"]
news_fetcher = Agent(
instruction="Fetch the top news story for the given topic and return only that story.",
output_key="news_data"      # The result will be stored in session.state["news_data"]
# Create the ParallelAgent to orchestrate the sub-agents
data_gatherer = ParallelAgent(
from google.adk.agents import Agent, ParallelAgent
```

### Chapter_07_Multi_Agent_(ADK_Gemini_Sequential).ipynb

```python
step1 = Agent(name="Step1_Fetch", output_key="data")
step2 = Agent(
instruction="Analyze the information found in state['data'] and provide a summary."
pipeline = SequentialAgent(
from google.adk.agents import SequentialAgent, Agent
# This agent's output will be saved to session.state["data"]
# This agent will use the data from the previous step.
# We instruct it on how to find and use this data.
# When the pipeline is run with an initial input, Step1 will execute,
# its response will be stored in session.state["data"], and then
```

### Chapter_07_Multi_Agent_(CrewAI_Gemini).ipynb

```python
def setup_environment():
def main():
researcher = Agent(
writer = Agent(
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
# Updated to a model from the Gemini 2.0 series for better performance and features.
# For cutting-edge (preview) capabilities, you could use "gemini-2.5-flash".
# Define Agents with specific roles and goals
backstory="You are an experienced research analyst with a knack for identifying key trends and synthesizing information.",
```
