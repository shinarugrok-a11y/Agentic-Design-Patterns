# Memory Management — deep dive

Source: Chapter 8 + `Chapter_08_Memory_(ADK_SessionService)`, `(ADK_LlmAgent_output_key)`,
`(ADK_Explicit_State_Update)`, `(ADK_MemoryService_InMemory)`, `(LangChain_LangGraph)`.

## Model (book)
- Short-term / contextual: recent interaction data inside the context window
  (session history + state).
- Long-term: external stores (vector DBs, key-value) searched semantically.
- ADK concepts: `Session` (thread of events), `State` (temporary dict for the
  session), `MemoryService` (searchable long-term store).
- Memory types: semantic (facts), episodic (experiences), procedural (rules/instructions).

## ADK session services
```python
from google.adk.sessions import InMemorySessionService, DatabaseSessionService, VertexAiSessionService
session_service = InMemorySessionService()                                   # dev/test, lost on restart
session_service = DatabaseSessionService(db_url="sqlite:///./my_agent_data.db")  # persistent
session_service = VertexAiSessionService(project=PROJECT_ID, location=LOCATION)  # managed; app_name = reasoning engine resource
```

## State update patterns (ADK)
Rule: never mutate `session.state` directly; changes must flow through events.

1. `output_key` on an agent:
```python
greeting_agent = LlmAgent(name="Greeter", model="gemini-2.0-flash",
    instruction="Generate a short, friendly greeting.", output_key="last_greeting")
# after runner.run(...): session_service.get_session(app, user, sid).state["last_greeting"]
```
2. Inside a tool via `ToolContext` (recommended for multi-key updates):
```python
def log_user_login(tool_context: ToolContext) -> dict:
    state = tool_context.state
    login_count = state.get("user:login_count", 0) + 1
    state["user:login_count"] = login_count
    state["task_status"] = "active"
    state["user:last_login_ts"] = time.time()
    state["temp:validation_needed"] = True
    return {"status": "success", "message": f"User login tracked. Total logins: {login_count}."}
```
3. Explicit `EventActions.state_delta` when appending events manually.

State key prefixes: `user:` persists per user across sessions, `app:` shared
app-wide, `temp:` discarded after the invocation, no prefix = session scope.

## ADK long-term memory
```python
from google.adk.memory import InMemoryMemoryService, VertexAiRagMemoryService
memory_service = InMemoryMemoryService()
memory_service = VertexAiRagMemoryService(
    rag_corpus="projects/<proj>/locations/us-central1/ragCorpora/<corpus>",
    similarity_top_k=5, vector_distance_threshold=0.7)
# memory_service.add_session_to_memory(session); memory_service.search_memory(...)
```
Memory Bank (managed) extracts and recalls user facts automatically across
ADK, LangGraph and CrewAI.

## LangChain short-term memory
```python
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
history = ChatMessageHistory(); history.add_user_message("I'm heading to New York next week.")

memory = ConversationBufferMemory(memory_key="history")          # string history for completion LLMs
template = """You are a helpful travel agent.
Previous conversation:
{history}
New question: {question}
Response:"""
conversation = LLMChain(llm=OpenAI(temperature=0), prompt=PromptTemplate.from_template(template), memory=memory)

# chat models: return_messages=True + MessagesPlaceholder
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
prompt = ChatPromptTemplate(messages=[
    SystemMessagePromptTemplate.from_template("You are a friendly assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{question}")])
```

## LangGraph long-term store
```python
from langgraph.store.memory import InMemoryStore
store = InMemoryStore(index={"embed": embed, "dims": 2})       # production: DB-backed store
namespace = (user_id, "chitchat")
store.put(namespace, "a-memory", {"rules": ["User likes short, direct language",
                                            "User only speaks English & python"], "my-key": "my-value"})
item = store.get(namespace, "a-memory")
items = store.search(namespace, filter={"my-key": "my-value"}, query="language preferences")
```
Procedural memory (self-updating instructions):
```python
def update_instructions(state, store):
    current = store.search(("instructions",))[0]
    new = llm.invoke(prompt_template.format(instructions=current.value["instructions"],
                                            conversation=state["messages"]))["new_instructions"]
    store.put(("agent_instructions",), "agent_a", {"instructions": new})

def call_model(state, store):
    instructions = store.get(("agent_instructions",), key="agent_a")[0]
    prompt = prompt_template.format(instructions=instructions.value["instructions"])
```

## Checklist
- Decide scope per key (`user:`/`app:`/`temp:`) before writing.
- Summarise or window history before the context fills.
- Use a persistent session service outside notebooks.
- Search long-term memory with a query, then inject only the hits.

## Pattern variants
- **Session state** — a per-thread dict (`session.state`) holding task flags and scratch values; wins for progress within one conversation.
- **Conversation buffer** — replay the turn history into the prompt via a `{history}` slot; wins for short chats where recency is all that matters.
- **Long-term semantic recall** — sessions written to a vector-backed service and searched by query; wins when facts must outlive the thread.
- **Namespaced store** — records under `(user_id, context)`, retrieved by filter plus similarity; wins when recall must be scoped per user.
- **Procedural memory** — stored instructions the agent rewrites by reflecting on the conversation; wins when behavior itself should adapt.
- **Managed service** — Vertex AI Memory Bank or `VertexAiRagMemoryService`; wins in production.

## More prompt templates
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

## Framework notes
- **LangChain / LangGraph** — `ChatMessageHistory` / `ConversationBufferMemory` inject one conversation; LangGraph's `BaseStore` keeps semantic, episodic, and procedural memory across sessions under namespaces.
- **Google ADK** — `Session` is the thread, `State` its temporary data, `SessionService` (`InMemory`, `Database`, `VertexAi`) its lifecycle, and `MemoryService` the searchable long-term store.
- **Other** — Vertex AI Memory Bank is the managed equivalent of a self-hosted long-term store.

## Failure modes in depth
- **Unbounded history growth** — a buffer replays every turn and eventually exceeds the context window. Window or summarize it, and keep durable facts in long-term memory, fetched on demand.
- **Mutating state in place** — assigning to the state dict outside an event is not tracked or persisted. Write via `output_key` or `EventActions(state_delta=...)` with `append_event`.
- **Stale or contradictory long-term facts** — overwrite a record at its existing key (`store.put(namespace, key, ...)`) instead of appending another version, so retrieval cannot return both.
- **Sensitive data persisted without scoping** — use the prefixes deliberately: `temp:` for values that must not survive the turn, `user:` and `app:` for deliberate scope, and namespace long-term writes by `user_id`.
