# Tool Use — Pattern reference

Load this file only when implementing `tool-use`. Do not load by default.

## Book (Gulli) — rule of thumb
Use whenever the agent must leave the LLM's weights: live data, private stores, code, or side effects.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Examples of an agent using tools. Fig. 2: Tool use design pattern.

## Notebooks (extracted)

Tool Use

### Notebooks
- `Chapter_05_Tool_Use_(CrewAI).ipynb`
- `Chapter_05_Tool_Use_(Executing_Code).ipynb`
- `Chapter_05_Tool_Use_(Google_Search).ipynb`
- `Chapter_05_Tool_Use_(LangChain).ipynb`
- `Chapter_05_Tool_Use_(Vertex_AI_Search).ipynb`

### Patterns
- **CrewAI:** `@tool` decorator; tools return typed data or raise `ValueError` (not error strings)
- **ADK Google Search:** `Agent` + `google_search` tool + `Runner`/`InMemorySessionService`
- **ADK code execution:** `BuiltInCodeExecutor()` on `LlmAgent`; inspect `part.executable_code` and `part.code_execution_result`
- **LangChain:** `create_tool_calling_agent` + `AgentExecutor`; requires `{agent_scratchpad}` placeholder
- **Vertex AI:** `VSearchAgent` with `datastore_id`; streams via `run_async`

### Prompt templates
Calculator agent (ADK):
```
You are a calculator agent.
When given a mathematical expression, write and execute Python code to calculate the result.
Return only the final numerical result as plain text, without markdown or code blocks.
```

LangChain agent system:
```
You are a helpful assistant.
```

### Minimal code
```python
# LangChain tool-calling agent
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool

@tool
def search_information(query: str) -> str:
    """Provides factual information on a given topic."""
    return simulated_results.get(query.lower(), "No info found.")

agent = create_tool_calling_agent(llm, [search_information], agent_prompt)
executor = AgentExecutor(agent=agent, verbose=True)
await executor.ainvoke({"input": "What is the capital of France?"})
```

```python
# ADK with Google Search
root_agent = Agent(
    name="basic_search_agent",
    model="gemini-2.0-flash-exp",
    tools=[google_search],
    instruction="I can answer your questions by searching the internet.",
)
```

### Caveats
- CrewAI: raise exceptions from tools; let agent handle failures
- Vertex AI Search requires `DATASTORE_ID` env var and GCP permissions
- LangChain notebook has duplicate cells (pip install + getpass variants)
- Code executor: use `run_async` and check `event.is_final_response()` for final text
- `nest_asyncio.apply()` needed for async in Jupyter

---

## Failure modes (skill-level)
- Vague tool docs → wrong or skipped calls
- Tool returns error strings instead of raising
- Unvalidated args cause unsafe side effects

## Chains with
`mcp`, `exception-handling`
