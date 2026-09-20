# Memory Management — Pattern reference

Load this file only when implementing `memory-management`. Do not load by default.

## Book (Gulli) — rule of thumb
Use when the agent must keep conversational context, track multi-step progress, or recall preferences across turns/sessions.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Memory management design pattern (short-term Session/State vs long-term MemoryService).

## Notebooks (extracted)

Memory Management

### Notebooks
- `Chapter_08_Memory_(ADK_Explicit_State_Update).ipynb`
- `Chapter_08_Memory_(ADK_LlmAgent_output_key).ipynb`
- `Chapter_08_Memory_(ADK_MemoryService_InMemory).ipynb`
- `Chapter_08_Memory_(ADK_SessionService).ipynb`
- `Chapter_08_Memory_(LangChain_LangGraph).ipynb`

### Patterns
- **ADK state via tools:** `ToolContext.state` for namespaced keys (`user:`, `temp:`)
- **output_key:** agent response auto-persisted to session state
- **Session services:** `InMemorySessionService`, `DatabaseSessionService`, `VertexAiSessionService`
- **Memory services:** `InMemoryMemoryService`, `VertexAiRagMemoryService`
- **LangChain:** `ConversationBufferMemory`, `ChatMessageHistory`, `LLMChain` with `{history}` / `MessagesPlaceholder`
- **LangGraph store:** `InMemoryStore` with embed/search/filter namespaces

### Prompt templates
LangChain travel agent template:
```
You are a helpful travel agent.

Previous conversation:
{history}

New question: {question}
Response:
```

### Minimal code
```python
# ADK output_key persistence
greeting_agent = LlmAgent(name="Greeter", instruction="Generate a short greeting.", output_key="last_greeting")
# After runner.run(...): session.state["last_greeting"] is populated
```

```python
# Tool-based state update
def log_user_login(tool_context: ToolContext) -> dict:
    state = tool_context.state
    state["user:login_count"] = state.get("user:login_count", 0) + 1
    return {"status": "success"}
```

```python
# LangGraph memory store
store = InMemoryStore(index={"embed": embed, "dims": 2})
store.put(("user_id", "app"), "a-memory", {"rules": ["User likes short language"]})
items = store.search(("user_id", "app"), query="language preferences")
```

### Caveats
- `InMemory*` services lose data on restart
- Vertex services need GCP project, corpus/engine IDs, `google-adk[vertexai]`
- Database session needs SQLAlchemy driver (e.g. `psycopg2`)
- LangChain `return_messages=True` required for chat models with `MessagesPlaceholder`
- Check state *after* runner finishes all events

---

## Failure modes (skill-level)
- In-memory stores vanish on restart
- Context window overflow from unbounded history
- Reading state before the runner finishes

## Chains with
`rag`, `learning-and-adaptation`
