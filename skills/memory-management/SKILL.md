---
name: memory-management
description: Short-term session state plus long-term recall. Separate short-term session state from long-term persistent recall and write to each explicitly. Skip it for single-turn, stateless requests with no personalization.
role: [memory]
chapter: 8
token_cost_estimate: 380
chains_with: [knowledge-retrieval-rag, learning-and-adaptation, model-context-protocol]
---

# Memory Management

## When to use
- Conversation spans multiple turns
- Progress must survive across sessions
- Personalization needs recall of past preferences

## When NOT to use
- Single-turn, stateless request
- Data must not be retained for privacy reasons
- Recall cannot be scoped to the current user

## Inputs
- session id and history
- state keys to persist
- retrieval query

## Outputs
- updated session state
- long-term memory writes
- recalled facts injected into context

## Failure modes
- Unbounded history growth overflows the context window
- Mutating state in place instead of via a state delta loses events
- Stale or contradictory long-term facts poison later turns
- Sensitive data persisted without scoping or expiry

## Minimal example
```python
# short term: write via a state delta, never mutate state in place
actions = EventActions(state_delta={"user:tier": "gold", "temp:draft": text})
session_service.append_event(session, Event(actions=actions))

# long term: persist, then search on later turns
memory_service.add_session_to_memory(session)
hits = memory_service.search_memory(query="preferred airline", user_id=uid)
```

## Next skills
- If recall needs a document corpus: load `knowledge-retrieval-rag`
- If memory should change behavior: load `learning-and-adaptation`
- If memory lives in an external server: load `model-context-protocol`
