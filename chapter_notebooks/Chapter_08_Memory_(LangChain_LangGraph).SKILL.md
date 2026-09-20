---
name: memory-management
description: Short-term session state plus long-term searchable memory. Persist conversation context in session state and store durable facts in a searchable long-term store. Do not use for one-shot, stateless requests where nothing must survive the call.
role: [memory]
chapter: 8
token_cost_estimate: 370
chains_with: [rag, learning-adaptation, mcp]
---

# Memory Management

## When to use
- Multi-turn conversation must keep context.
- Track progress of a multi-step task across calls.
- Personalise from user preferences or history.
- Facts must survive across sessions (vector store, DB).

## When NOT to use
- Single question, single answer.
- Knowledge is external documents, not interaction history: use `rag`.
- Privacy rules forbid retaining user data.

## Inputs
- Session id / user id
- Events (messages, tool results)
- State deltas
- Memory queries

## Outputs
- Current session state dict
- Retrieved long-term memories
- Updated store

## Failure modes
- Mutating `session.state` directly instead of via `output_key`/`state_delta`; changes not persisted.
- Context window fills with raw history; no summarisation.
- No namespace/prefix (`user:`, `app:`, `temp:`); data leaks across scopes.
- In-memory service used in prod; memory lost on restart.

## Minimal example
```python
agent = LlmAgent(name="Greeter", instruction=..., output_key="last_greeting")
def log_login(tool_context: ToolContext) -> dict:
    s = tool_context.state
    s["user:login_count"] = s.get("user:login_count", 0) + 1
    s["temp:validation_needed"] = True
# long-term: store.put((user_id, ctx), key, {...}); store.search(ns, query=...)
# LangChain: ConversationBufferMemory(memory_key="chat_history", return_messages=True)
```

## Next skills
- If memory is a document corpus: load `rag`
- If stored experience should change behaviour: load `learning-adaptation`
- If memory service is remote: load `mcp`
