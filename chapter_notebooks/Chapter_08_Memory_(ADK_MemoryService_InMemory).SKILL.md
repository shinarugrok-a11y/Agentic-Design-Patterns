---
name: memory-management
description: Session state plus searchable long-term memory. Use for multi-turn or cross-session context. Not for stateless requests.
role: [memory]
chapter: 8
token_cost_estimate: 210
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
state["temp:draft"] = draft          # this turn only
state["user:theme"] = "dark"         # this user, every session
memory.add(session)                  # long-term store
hits = memory.search("theme preference")   # recall later by meaning
```

## Next skills
- If recall comes from documents: load `rag`
- If memory feeds behaviour change: load `learning-adaptation`
