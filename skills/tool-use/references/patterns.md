# Tool Use patterns (Ch 5)

Five notebook variants: CrewAI `@tool` agents, ADK code executor, ADK `google_search`, LangChain tool-calling agent, Vertex AI Search datastore.

Pattern A — LangChain: `@tool`-decorated functions + `create_tool_calling_agent(llm, tools, prompt)` + `AgentExecutor`; requires a function-calling model (`gemini-*`, `gpt-4o-mini`).

Pattern B — CrewAI: `Agent(role, goal, tools=[...])` + `Task` + `Crew`; configure logging (`basicConfig INFO`) for the tool trace.

Pattern C — ADK search/code: `ADKAgent(tools=[google_search])` or `BuiltInCodeExecutor`; run via `Runner` + `InMemorySessionService` with `APP_NAME/USER_ID/SESSION_ID`.

Pattern D — Vertex AI Search: datastore-backed agent with `DATASTORE_ID` env; grounds answers in a private corpus.

Rules: one-line sharp tool descriptions, cap calls per task, always validate tool output before final answer.

## Notebook extracts (on-demand detail)

### Chapter_05_Tool_Use_(CrewAI).ipynb

```python
def get_stock_price(ticker: str) -> float:
financial_analyst_agent = Agent(
def main():
from crewai import Agent, Task, Crew
from crewai.tools import tool
# --- Best Practice: Configure Logging ---
# A basic logging setup helps in debugging and tracking the crew's execution.
# For production, it's recommended to use a more secure method for key management
# like environment variables loaded at runtime or a secret manager.
# Set the environment variable for your chosen LLM provider (e.g., OPENAI_API_KEY)
```

### Chapter_05_Tool_Use_(Executing_Code).ipynb

```python
code_agent = LlmAgent(
instruction="""You are a calculator agent.
async def call_agent_async(query):
async def main():
from google.adk.agents import Agent as ADKAgent, LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai import types
```

### Chapter_05_Tool_Use_(Google_Search).ipynb

```python
root_agent = ADKAgent(
instruction="I can answer your questions by searching the internet. Just ask me anything!",
async def call_agent(query):
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
# Define variables required for Session setup and Agent execution
# Define Agent with access to search tool
```

### Chapter_05_Tool_Use_(LangChain).ipynb

```python
def search_information(query: str) -> str:
agent_prompt = ChatPromptTemplate.from_messages([
async def run_agent_with_tool(query: str):
async def main():
# Prompt the user securely and set API keys as an environment variables
def search_information(query: str) -> str:
agent_prompt = ChatPromptTemplate.from_messages([
async def run_agent_with_tool(query: str):
async def main():
from langchain_google_genai import ChatGoogleGenerativeAI
```

### Chapter_05_Tool_Use_(Vertex_AI_Search).ipynb

```python
vsearch_agent = agents.VSearchAgent(
async def call_vsearch_agent_async(query: str):
async def run_vsearch_example():
from google.genai import types
from google.adk import agents
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
# Ensure you have set your GOOGLE_API_KEY and DATASTORE_ID environment variables
# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
# os.environ["DATASTORE_ID"] = "YOUR_DATASTORE_ID"
```
