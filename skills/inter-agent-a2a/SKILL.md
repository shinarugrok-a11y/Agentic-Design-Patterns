---
name: inter-agent-a2a
description: Communicate between agents via AgentCards and standard A2A messages.
role: [executor, planner]
chapter: 15
token_cost_estimate: 209
chains_with: [multi-agent, mcp]
---

# Inter-Agent Communication (A2A)

## When to use
- Agents live in different services, runtimes, or orgs.
- Discovery via AgentCard + sync/streaming requests.
- Contracts must be versioned and authenticated.

## When NOT to use
- Same-process agents; direct calls are simpler.
- No shared protocol support on both sides.

## Inputs
- AgentCard
- A2A request envelope

## Outputs
- Remote agent response stream or result

## Failure modes
- AgentCard lies about capabilities; validate on first use.
- Auth misconfiguration blocks cross-agent calls.
- Streaming vs sync mismatch hangs the caller.

## Minimal example
```python
card = fetch_agent_card(url)  # capabilities, endpoint, auth
reply = a2a_request(card.endpoint, task)  # sync or streaming
```

## Next skills
- If remote agents join a local team topology: load `multi-agent`
- If remote capability is better exposed as a tool: load `mcp`
