# Tool Use

Ch 5.

## Frameworks
- CrewAI (@tool Agent/Task/Crew); LangChain (create_tool_calling_agent + AgentExecutor); ADK (google_search, BuiltInCodeExecutor, Vertex AI Search).

## Key APIs from the notebooks
- `CrewAI: @tool def get_stock_price(ticker: str) -> float; Crew with Agent/Task`
- `LangChain: @tool def search_information(query: str); create_tool_calling_agent(llm, tools, prompt)`
- `ADK: google_search tool, BuiltInCodeExecutor, call_agent_async(query) / call_vsearch_agent_async(query)`

## Code patterns
- Pattern: declare typed tools -> agent selects tool -> execute -> feed observation back -> final answer.
- One-line precise tool descriptions; typed args (pydantic-style).
- Cap tool iterations; log every call + observation.

## Prompt templates
- Tool description (one line, precise): `Returns the live price for a stock ticker.`
- Agent instruction: `Use tools when you lack live data. Cite the tool and observation.`

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_05_Tool_Use_(CrewAI).ipynb`
- `chapter_notebooks/Chapter_05_Tool_Use_(Executing_Code).ipynb`
- `chapter_notebooks/Chapter_05_Tool_Use_(Google_Search).ipynb`
- `chapter_notebooks/Chapter_05_Tool_Use_(LangChain).ipynb`
- `chapter_notebooks/Chapter_05_Tool_Use_(Vertex_AI_Search).ipynb`

