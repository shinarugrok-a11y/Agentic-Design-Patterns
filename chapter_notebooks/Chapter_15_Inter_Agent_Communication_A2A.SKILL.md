---
name: inter-agent-communication-a2a
description: Cross-framework agent delegation over HTTP. Delegate tasks across framework boundaries over A2A, discovering peers through their Agent Cards. Skip it when all agents live in one process; call them directly instead.
role: [executor, planner]
chapter: 15
token_cost_estimate: 370
chains_with: [multi-agent-collaboration, model-context-protocol, exception-handling-and-recovery]
---

# Inter-Agent Communication (A2A)

## When to use
- Agents run in separate processes or frameworks
- Peers must be discovered rather than hardcoded
- Long tasks need streaming or async updates

## When NOT to use
- All agents share one process
- No network or framework boundary exists
- Endpoints cannot be authenticated

## Inputs
- peer Agent Card or endpoint
- task payload
- sync or streaming mode

## Outputs
- task id and state
- streamed or final artifacts
- input-required follow-up prompts

## Failure modes
- Agent Card overstates capabilities, so delegation fails late
- Network partition leaves tasks orphaned in a pending state
- Multi-turn context lost across the input-required boundary
- No auth on endpoints, so any caller can drive the agent

## Minimal example
```python
card = httpx.get(f"{peer}/.well-known/agent.json").json()  # capabilities first
task = httpx.post(f"{peer}/tasks/send", json=payload).json()
while task["status"]["state"] in ("submitted", "working"):
    task = poll(peer, task["id"])   # input-required: reply in-thread
```

## Next skills
- If you own all the agents: load `multi-agent-collaboration`
- If the peer exposes tools: load `model-context-protocol`
- If peers can be unreachable: load `exception-handling-and-recovery`
