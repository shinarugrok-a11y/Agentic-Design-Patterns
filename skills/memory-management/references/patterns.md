# Memory Management

Ch 8.

## Frameworks
- Google ADK (SessionService, MemoryService, ToolContext state, output_key); LangChain/LangGraph (ChatMessageHistory, ConversationBufferMemory, BaseStore).

## Key APIs from the notebooks
- `ADK: InMemorySessionService / DatabaseSessionService / VertexAiSessionService`
- `ADK: InMemoryMemoryService / VertexAiRagMemoryService; LlmAgent(output_key=...) to persist outputs`
- `ADK: log_user_login(tool_context: ToolContext) explicit state update`

## Code patterns
- Pattern: session per user -> store key facts/output_key -> recall on next turn.
- Explicit state updates via ToolContext for structured facts (e.g. login).
- Prefer Database/VertexAi session services in production; InMemory is demo-only.

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_08_Memory_(ADK_Explicit_State_Update).ipynb`
- `chapter_notebooks/Chapter_08_Memory_(ADK_LlmAgent_output_key).ipynb`
- `chapter_notebooks/Chapter_08_Memory_(ADK_MemoryService_InMemory).ipynb`
- `chapter_notebooks/Chapter_08_Memory_(ADK_SessionService).ipynb`
- `chapter_notebooks/Chapter_08_Memory_(LangChain_LangGraph).ipynb`

