# Memory Management — Patterns

## Pattern variants
- **Session state** — a per-thread dict (`session.state`) holding task flags and scratch values; wins for progress within one conversation.
- **Conversation buffer** — replay the turn history into the prompt via a `{history}` slot; wins for short chats where recency is all that matters.
- **Long-term semantic recall** — sessions written to a vector-backed service and searched by query; wins when facts must outlive the thread.
- **Namespaced store** — records under `(user_id, context)`, retrieved by filter plus similarity; wins when recall must be scoped per user.
- **Procedural memory** — stored instructions the agent rewrites by reflecting on the conversation; wins when behavior itself should adapt.
- **Managed service** — Vertex AI Memory Bank or `VertexAiRagMemoryService`; wins in production.

## Prompt templates
Short-term recall by prompt slot (`memory_key` must match the template variable):

```
You are a helpful travel agent.

Previous conversation:
{history}

New question: {question}
Response:
```

Procedural-memory update — reflect, then return replacement rules:

```
Current instructions: {instructions}
Conversation: {conversation}
Return only improved instructions: keep what worked, fix what did not.
```

## Code patterns
Google ADK (short-term writes: prefixed keys through the tool context, or `output_key`):

```python
def log_user_login(tool_context: ToolContext) -> dict:
    state = tool_context.state
    state["user:login_count"] = state.get("user:login_count", 0) + 1
    state["task_status"] = "active"      # session-scoped
    state["temp:validation_needed"] = True   # discarded, never persisted
    return {"status": "success"}

greeter = LlmAgent(name="Greeter", model="gemini-2.0-flash",
                   output_key="last_greeting")  # response -> session.state
```

Google ADK (long-term: ingest the session, then search it on later turns):

```python
memory_service = VertexAiRagMemoryService(
    rag_corpus=RAG_CORPUS_RESOURCE_NAME,
    similarity_top_k=5, vector_distance_threshold=0.7)
memory_service.add_session_to_memory(session)
# agents reach this through the `load_memory` tool / search_memory
```

LangChain buffer and LangGraph namespaced store:

```python
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(llm=llm, prompt=prompt, memory=memory)  # MessagesPlaceholder

store = InMemoryStore(index={"embed": embed, "dims": 2})
namespace = (user_id, "chitchat")
store.put(namespace, "a-memory", {"rules": ["User likes short, direct language"]})
items = store.search(namespace, filter={"my-key": "my-value"}, query="language preferences")
```

## Framework notes
- **LangChain / LangGraph** — `ChatMessageHistory` / `ConversationBufferMemory` inject one conversation; LangGraph's `BaseStore` keeps semantic, episodic, and procedural memory across sessions under namespaces.
- **Google ADK** — `Session` is the thread, `State` its temporary data, `SessionService` (`InMemory`, `Database`, `VertexAi`) its lifecycle, and `MemoryService` the searchable long-term store.
- **Other** — Vertex AI Memory Bank is the managed equivalent of a self-hosted long-term store.

## Failure modes in depth
- **Unbounded history growth** — a buffer replays every turn and eventually exceeds the context window. Window or summarize it, and keep durable facts in long-term memory, fetched on demand.
- **Mutating state in place** — assigning to the state dict outside an event is not tracked or persisted. Write via `output_key` or `EventActions(state_delta=...)` with `append_event`.
- **Stale or contradictory long-term facts** — overwrite a record at its existing key (`store.put(namespace, key, ...)`) instead of appending another version, so retrieval cannot return both.
- **Sensitive data persisted without scoping** — use the prefixes deliberately: `temp:` for values that must not survive the turn, `user:` and `app:` for deliberate scope, and namespace long-term writes by `user_id`.

## Source
Chapter 8 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_08_Memory_(X).ipynb for X in ADK_Explicit_State_Update, ADK_LlmAgent_output_key, ADK_SessionService, ADK_MemoryService_InMemory, LangChain_LangGraph.
