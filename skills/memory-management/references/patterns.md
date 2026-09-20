# Memory Management — patterns (Ch 8)

## Pattern
1. Short-term: session state and history per session id.
2. Write state via `output_key` or `tool_context.state`, never by mutation.
3. Long-term: add finished sessions to a memory service; search on demand.
4. Summarise or window history before it overflows.

## Prompt template
```
Use the user's stored preferences: {user:pref}. Last result: {last_result}.
Before answering, search memory for prior facts about this user and cite them.
```

## Key APIs
- ADK: `InMemorySessionService`, `DatabaseSessionService`, `VertexAiSessionService`; `Runner(memory_service=...)`.
- ADK: `LlmAgent(output_key='k')`, `tool_context.state['user:pref']`, `memory.search_memory(query)`.
- LangChain: `ConversationBufferMemory`; LangGraph `InMemoryStore` for procedural memory.

## Pitfalls -> fixes
- Direct state mutation -> use `EventActions(state_delta=...)`.
- Context overflow -> summary memory or windowing.
- Lost on restart -> database or Vertex services.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_08_*`.
