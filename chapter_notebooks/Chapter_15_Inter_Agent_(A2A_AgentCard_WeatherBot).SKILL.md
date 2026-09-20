---
name: a2a
description: Use when independent agents must discover and call each other over a network. Do not use for agents inside one process that can share memory.
role: [executor, planner]
chapter: 15
token_cost_estimate: 174
chains_with: [multi-agent, mcp]
---

# Inter-Agent Communication (A2A)

## When to use
- Agents live in different services/orgs
- Need discovery via Agent Cards
- Sync + streaming calls required

## When NOT to use
- Same-process agents (use shared state)
- Single agent suffices
- No network trust exists

## Inputs
- AgentCard (name, url, skills, auth)
- JSON-RPC task envelope

## Outputs
- Task result with session id
- Capability-matched handler output

## Failure modes
- Schema drift — pin AgentCard version, validate envelopes
- Open endpoints — require auth schemes (apiKey)
- Dropped streams — support resume + historyLength

## Minimal example
```python
card = fetch_card("http://weather/a2a")  # skills, auth
task = sendTask(card.url, {"text": "Forecast Paris?"})
return stream_or_poll(task.id)
```

## Next skills
- If coordinate local specialists: load `multi-agent`
- If standardize tool access: load `mcp`
