---
name: memory-management
description: Persist state across turns with sessions and memory services.
role: [memory]
chapter: 8
token_cost_estimate: 219
chains_with: [knowledge-retrieval, mcp]
---

# Memory Management

## When to use
- Agent must recall user facts or history across turns.
- Choose scope: session state vs long-term memory service.
- Multiple turns reference earlier outputs.

## When NOT to use
- Single-turn stateless task.
- Storing the data violates privacy/retention policy.

## Inputs
- Session/user id + what to store
- Scope: session state vs MemoryService

## Outputs
- Recalled context injected into the next turn

## Failure modes
- Unbounded history blows context; summarize or expire.
- Stale memory overrides fresher user input.
- No isolation between users/sessions leaks data.

## Minimal example
```python
runner = Runner(agent, session_service=InMemorySessionService())
session = session_service.create_session(user_id=u)
runner.run(user_id=u, session_id=session.id, query=q)
```

## Next skills
- If memory must be searched semantically, not just keyed: load `knowledge-retrieval`
- If memory backend must be a shared service: load `mcp`
