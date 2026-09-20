# Tool Use — patterns (Ch 5)

## Pattern
1. Describe tools: precise name, docstring with examples, typed args.
2. Model emits a structured call; orchestrator executes it.
3. Feed the result back; model answers or calls again.
4. Raise on failure; return typed data.

## Prompt template
```
Docstring: Provides factual information on a topic. Use it for questions like
'What is the capital of France?'.
Task: Price for AAPL? Use the 'Stock Price Lookup Tool'; if not found, say so.
```

## Key APIs
- LangChain: `@tool`, `create_tool_calling_agent(llm, tools, prompt)`, `AgentExecutor`; prompt needs `{agent_scratchpad}`.
- CrewAI: `@tool("Name") def f(ticker: str) -> float` raising `ValueError`; `Agent(tools=[f])`.
- ADK: `google_search`, `BuiltInCodeExecutor()`, `VSearchAgent(datastore_id=...)`.

## Pitfalls -> fixes
- Wrong tool chosen -> one verb per tool, sharper docstring.
- Error strings as data -> raise exceptions.
- Huge outputs -> summarise in the tool.

Full notebook code: `notebook-code.md`; source `chapter_notebooks/Chapter_05_*`.
