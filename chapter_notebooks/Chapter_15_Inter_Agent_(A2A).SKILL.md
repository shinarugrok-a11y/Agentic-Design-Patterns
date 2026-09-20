---
name: a2a
description: Delegate to remote agents via Agent Cards. Use across processes or vendors. Not for in-process agents.
role: [executor, planner]
chapter: 15
token_cost_estimate: 221
chains_with: [multi-agent, exception-handling]
---

# Inter-Agent Communication

## When to use
- Agents run in different processes or vendors.
- Capabilities must be discoverable (Agent Card).
- Long tasks need streaming or push updates.

## When NOT to use
- Agents share one process: use `multi-agent`.
- Calling tools, not agents: use `mcp`.

## Inputs
- Agent Card URL
- Task message (JSON-RPC)

## Outputs
- Task id + status
- Artifacts from the remote agent

## Failure modes
- Card overstates skills.
- Sync call times out on long tasks.
- No auth on the endpoint.

## Minimal example
```python
card = requests.get(f"{url}/.well-known/agent.json").json()
resp = requests.post(url, json={"jsonrpc": "2.0", "id": 1,
    "method": "message/send", "params": {"message": msg}})
```

## Next skills
- If remote agents need a coordinator: load `multi-agent`
- If remote call can fail: load `exception-handling`
