---
name: memory-management
description: Use when the agent must persist state across turns or sessions. Do not use for stateless single-turn tasks.
role: [memory]
chapter: 8
token_cost_estimate: 173
chains_with: [rag, learning-adaptation]
---

# Memory Management

## When to use
- Multi-turn conversations need context
- User facts must persist across sessions
- Agents share state via explicit keys

## When NOT to use
- Single-turn stateless task
- Context fits in the prompt already
- Privacy forbids storing the data

## Inputs
- Session/user namespace
- Facts with write policy

## Outputs
- Scoped readable state
- Memory hit/miss trace

## Failure modes
- Staleness — timestamp facts, expire aggressively
- Bloat — summarize, don't append forever
- Leakage — namespace by (app, user, session)

## Minimal example
```python
state['user_city'] = 'Paris'  # output_key or tool write
greeting = run('Greet for Paris')
recall = store.search(('prefs', user_id))
```

## Next skills
- If need doc-grounded recall: load `rag`
- If need memory that improves: load `learning-adaptation`
