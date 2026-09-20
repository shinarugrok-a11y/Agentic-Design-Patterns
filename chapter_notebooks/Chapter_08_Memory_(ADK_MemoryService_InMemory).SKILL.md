---
name: memory-management
description: Session state plus searchable long-term memory. Use for multi-turn or cross-session context. Not for stateless requests.
role: [memory]
chapter: 8
token_cost_estimate: 215
chains_with: [rag, learning-adaptation]
---

# Memory Management

## When to use
- Multi-turn tasks need earlier facts.
- Cross-session personalisation.
- Agents share state via keys.

## When NOT to use
- Stateless one-shot requests.
- Corpus retrieval, not conversation: use `rag`.

## Inputs
- Session id
- State updates (output_key, tool_context.state)

## Outputs
- Session state dict
- Memory search results

## Failure modes
- State mutated directly instead of via events.
- Raw history overflows the context window.
- In-memory service loses data on restart.

## Minimal example
```python
agent = LlmAgent(name="greeter", output_key="last_greeting")
runner = Runner(agent=agent, session_service=InMemorySessionService(),
                memory_service=InMemoryMemoryService())
# later turn: tool_context.state["user:pref"] = "dark"; memory.search("pref")
```

## Next skills
- If recall comes from documents: load `rag`
- If memory feeds behaviour change: load `learning-adaptation`
