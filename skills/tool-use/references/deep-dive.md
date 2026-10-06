# Tool Use (Function Calling) — deep dive

Source: Chapter 5 + `Chapter_05_Tool_Use_(LangChain).ipynb`, `(CrewAI)`,
`(Executing_Code)`, `(Google_Search)`, `(Vertex_AI_Search)`.
Labels: SOURCE = book text or its notebook (cited); DERIVED = ours;
ILLUSTRATIVE = our code, not from the book. GT:L = line in
`ground-truth/agentic_design_patterns.txt`.

## Mechanics (SOURCE, paraphrase of Ch 5 overview, GT:L2907–L2960)
1. Tools are described to the model (name, description, typed parameters).
2. The model decides a tool is needed and emits a structured call (JSON).
3. An orchestration layer executes the call and returns the result.
4. The model incorporates the result into its answer (or calls again).

Rule of thumb: use whenever the agent must leave the model's internal
knowledge: real-time data, private data, exact computation, code execution,
or triggering actions.

## Pattern A: LangChain `@tool` + `create_tool_calling_agent`
Provenance: SOURCE (abridged) — condensed from GT:L3059–L3126, `Chapter_05_Tool_Use_(LangChain).ipynb`; not verbatim.
```python
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

@tool
def search_information(query: str) -> str:
    """
    Provides factual information on a given topic. Use this tool to find answers to questions
    like 'What is the capital of France?' or 'What is the weather in London?'.
    """
    simulated_results = {"weather in london": "Cloudy, 15°C.", "capital of france": "Paris.",
                         "default": f"No specific information found for '{query}'."}
    return simulated_results.get(query.lower(), simulated_results["default"])

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),      # required for intermediate tool steps
])
agent = create_tool_calling_agent(llm, [search_information], agent_prompt)
agent_executor = AgentExecutor(agent=agent, tools=[search_information], verbose=True)
response = await agent_executor.ainvoke({"input": "What's the weather like in London?"})
```
The docstring *is* the tool description the model reads; include example
queries so the model knows when the tool applies.

## Pattern B: CrewAI tool that raises instead of returning error strings
Provenance: SOURCE (abridged) — condensed from GT:L3198–L3284; not verbatim.
```python
from crewai import Agent, Task, Crew
from crewai.tools import tool

@tool("Stock Price Lookup Tool")
def get_stock_price(ticker: str) -> float:
    """
    Fetches the latest simulated stock price for a given stock ticker symbol.
    Returns the price as a float. Raises a ValueError if the ticker is not found.
    """
    prices = {"AAPL": 178.15, "GOOGL": 1750.30, "MSFT": 425.50}
    price = prices.get(ticker.upper())
    if price is None:
        raise ValueError(f"Simulated price for ticker '{ticker.upper()}' not found.")
    return price

financial_analyst_agent = Agent(role="Senior Financial Analyst",
    goal="Analyze stock data using provided tools and report key prices.",
    backstory="You are an experienced financial analyst ... You provide clear, direct answers.",
    tools=[get_stock_price], allow_delegation=False, verbose=True)

analyze_aapl_task = Task(
    description=("What is the current simulated stock price for Apple (ticker: AAPL)? "
                 "Use the 'Stock Price Lookup Tool' to find it. "
                 "If the ticker is not found, you must report that you were unable to retrieve the price."),
    expected_output=("A single, clear sentence stating the simulated stock price for AAPL. "
                     "If the price cannot be found, state that clearly."),
    agent=financial_analyst_agent)
Crew(agents=[financial_analyst_agent], tasks=[analyze_aapl_task]).kickoff()
```
From the book/notebook comments (GT:L3198–L3240, `Chapter_05_Tool_Use_(CrewAI).ipynb`): the tool
"returns raw data (a float) or raises a standard Python error", and the task
description says how to react to both success and failure.

## Pattern C: ADK built-in tools
Provenance: SOURCE (abridged) — condensed from GT:L3362–L3595; not verbatim.
```python
from google.adk.agents import LlmAgent, Agent
from google.adk.tools import google_search
from google.adk.code_executors import BuiltInCodeExecutor

# Live web search
search_agent = Agent(name="basic_search_agent", model="gemini-2.0-flash-exp",
    instruction="I can answer your questions by searching the internet.", tools=[google_search])

# Code execution for exact computation
code_agent = LlmAgent(name="calculator_agent", model="gemini-2.0-flash",
    code_executor=BuiltInCodeExecutor(),
    instruction="""You are a calculator agent.
    When given a mathematical expression, write and execute Python code to calculate the result.
    Return only the final numerical result as plain text, without markdown or code blocks.""")

# Enterprise search over a Vertex AI datastore
from google.adk import agents
DATASTORE_ID = os.environ.get("DATASTORE_ID")          # book: GT:L3607, checked at GT:L3688
if not DATASTORE_ID:
    raise SystemExit("Error: DATASTORE_ID environment variable is not set.")
vsearch_agent = agents.VSearchAgent(name="q2_strategy_vsearch_agent", model="gemini-2.0-flash-exp",
    datastore_id=DATASTORE_ID, model_parameters={"temperature": 0.0})
```
Inspecting code-execution events:
Provenance: SOURCE (abridged) — condensed from GT:L3502–L3516 (prints and flags removed).
```python
for part in event.content.parts:
    if part.executable_code:        print(part.executable_code.code)
    elif part.code_execution_result: print(part.code_execution_result.outcome, part.code_execution_result.output)
    elif part.text:                  print(part.text)
```
`VSearchAgent` final events expose `event.grounding_metadata.grounding_attributions`
for source citations (GT:L3662–L3664).

## Runner boilerplate (ADK)
Provenance: SOURCE (abridged) — combined from GT:L3392–L3400 (session + `Runner`) and GT:L3495–L3497 (`async for ... runner.run_async`).
```python
session_service = InMemorySessionService()
await session_service.create_session(app_name=APP, user_id=UID, session_id=SID)
runner = Runner(agent=agent, app_name=APP, session_service=session_service)
async for event in runner.run_async(user_id=UID, session_id=SID,
        new_message=types.Content(role="user", parts=[types.Part(text=query)])):
    if event.is_final_response(): ...
```
In notebooks use `nest_asyncio.apply()` before `asyncio.run`.

## Tool design checklist (DERIVED)
- One verb per tool; precise name; docstring with when-to-use examples.
- Typed parameters; validate inside the tool.
- Raise for unexpected failures; return structured dicts (`{"status": ..., ...}`) for expected outcomes.
- Keep outputs small; summarise large payloads before returning.
- Restrict dangerous tools (`before_tool_callback`, see `guardrails`).

## Pattern variants (DERIVED summary; book terms cited where present)
- **Function tool** — a plain typed function exposed with `@tool`; wins for one deterministic action with a clear schema.
- **Pre-built tool** — framework-supplied `google_search`, `BuiltInCodeExecutor`, Vertex AI Search; wins when the integration is standard and not worth owning.
- **Code execution as tool** — the model writes Python, a sandbox runs it; wins for exact arithmetic and ad-hoc data work no fixed schema covers.
- **Grounded datastore tool** — `VSearchAgent` over a datastore returning `grounding_metadata`; wins when answers must cite private documents.

## More prompt templates
The docstring *is* the selection prompt — say what it returns and when to pick it:

Provenance: SOURCE — docstring of `search_information`, GT:L3086–L3091, reflowed.
```
Provides factual information on a given topic. Use this tool to find answers
to phrases like 'capital of France' or 'weather in London?'.
```

Provenance: SOURCE — docstring of the CrewAI `get_stock_price` tool, GT:L3227–L3230 / `Chapter_05_Tool_Use_(CrewAI).ipynb`.
```
Fetches the latest simulated stock price for a given stock ticker symbol.
Returns the price as a float. Raises a ValueError if the ticker is not found.
```

Tool-calling agents need a scratchpad slot for the call/result loop:

Provenance: SOURCE (abridged) — `agent_prompt` messages from GT:L3124–L3128.
```
system: You are a helpful assistant.
human:  {input}
placeholder: {agent_scratchpad}
```

## Framework notes (APIs SOURCE as cited above; role descriptions DERIVED)
- **LangChain / LangGraph** — `@tool` declares; `create_tool_calling_agent` binds llm+tools+prompt; `AgentExecutor` is the runtime that actually executes calls and feeds results back.
- **Google ADK** — ships `google_search`, `BuiltInCodeExecutor`, and `VSearchAgent`; the `Runner` streams `executable_code` / `code_execution_result` / `grounding_metadata` parts.
- **CrewAI** — `@tool("Name")` attaches per `Agent`; `Task.description` and `expected_output` tell it how to behave when the tool fails.

## Failure modes in depth (DERIVED)
- **Vague tool descriptions cause wrong-tool selection** — the docstring is the model's only signal. Name the return type and include example queries the tool covers.
- **Hallucinated or malformed arguments** — use few, flat, annotated parameters (`ticker: str -> float`) so schema validation rejects bad calls before the API is hit.
- **Unvalidated side effects** — split read tools from write tools; gate irreversible calls behind explicit confirmation rather than tool-choice.
- **Tool errors returned raw trigger retry loops** — raise a typed `ValueError` and instruct the task what to report on failure, so the model does not re-read an error string as data and retry forever.
