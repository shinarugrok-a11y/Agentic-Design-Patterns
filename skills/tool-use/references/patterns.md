# Tool Use — Patterns

## Pattern variants
- **Function tool** — a plain typed function exposed with `@tool`; wins for one deterministic action with a clear schema.
- **Pre-built tool** — framework-supplied `google_search`, `BuiltInCodeExecutor`, Vertex AI Search; wins when the integration is standard and not worth owning.
- **Code execution as tool** — the model writes Python, a sandbox runs it; wins for exact arithmetic and ad-hoc data work no fixed schema covers.
- **Grounded datastore tool** — `VSearchAgent` over a datastore returning `grounding_metadata`; wins when answers must cite private documents.

## Prompt templates
The docstring *is* the selection prompt — say what it returns and when to pick it:

```
Provides factual information on a given topic. Use this tool to find answers
to questions like 'What is the capital of France?' or 'What is the weather
in London?'. Returns the price as a float; raises ValueError if not found.
```

Tool-calling agents need a scratchpad slot for the call/result loop:

```
system: You are a helpful assistant.
human:  {input}
placeholder: {agent_scratchpad}
```

## Code patterns
LangChain (tool-calling agent):

```python
@tool
def search_information(query: str) -> str:
    """Provides factual information on a given topic."""
    return simulated_results.get(query.lower(), simulated_results["default"])

agent = create_tool_calling_agent(llm, [search_information], agent_prompt)
executor = AgentExecutor(agent=agent, tools=[search_information], verbose=True)
response = await executor.ainvoke({"input": query})
```

Google ADK (built-in code executor; results arrive as typed event parts):

```python
code_agent = LlmAgent(name="calculator_agent", model="gemini-2.0-flash",
                      code_executor=BuiltInCodeExecutor(),
                      instruction="Write and execute Python; return only the result.")
async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID,
                                    new_message=content):
    for part in event.content.parts:
        if part.executable_code:
            print(part.executable_code.code)
        elif part.code_execution_result:
            print(part.code_execution_result.outcome, part.code_execution_result.output)
```

CrewAI (tool raises instead of returning an error string):

```python
@tool("Stock Price Lookup Tool")
def get_stock_price(ticker: str) -> float:
    """Fetches the latest simulated stock price. Raises ValueError if unknown."""
    price = simulated_prices.get(ticker.upper())
    if price is None:
        raise ValueError(f"Simulated price for '{ticker}' not found.")
    return price
```

## Framework notes
- **LangChain / LangGraph** — `@tool` declares; `create_tool_calling_agent` binds llm+tools+prompt; `AgentExecutor` is the runtime that actually executes calls and feeds results back.
- **Google ADK** — ships `google_search`, `BuiltInCodeExecutor`, and `VSearchAgent`; the `Runner` streams `executable_code` / `code_execution_result` / `grounding_metadata` parts.
- **CrewAI** — `@tool("Name")` attaches per `Agent`; `Task.description` and `expected_output` tell it how to behave when the tool fails.

## Failure modes in depth
- **Vague tool descriptions cause wrong-tool selection** — the docstring is the model's only signal. Name the return type and include example queries the tool covers.
- **Hallucinated or malformed arguments** — use few, flat, annotated parameters (`ticker: str -> float`) so schema validation rejects bad calls before the API is hit.
- **Unvalidated side effects** — split read tools from write tools; gate irreversible calls behind explicit confirmation rather than tool-choice.
- **Tool errors returned raw trigger retry loops** — raise a typed `ValueError` and instruct the task what to report on failure, so the model does not re-read an error string as data and retry forever.

## Source
Chapter 5 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_05_Tool_Use_(LangChain).ipynb, Chapter_05_Tool_Use_(CrewAI).ipynb, Chapter_05_Tool_Use_(Executing_Code).ipynb, Chapter_05_Tool_Use_(Google_Search).ipynb, Chapter_05_Tool_Use_(Vertex_AI_Search).ipynb.
