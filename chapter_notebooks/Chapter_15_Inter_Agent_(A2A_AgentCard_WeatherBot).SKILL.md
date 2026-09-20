---
name: a2a
description: HTTP protocol so heterogeneous agents collaborate. Use across frameworks. Do NOT use for in-process sub-agents.
role: [executor, planner]
chapter: 15
token_cost_estimate: 270
chains_with: [multi-agent, mcp]
---

# Inter-Agent Communication (A2A)

## When to use
- Agents are built on different stacks (ADK, LangGraph, CrewAI)
- Need discovery via Agent Card (name, URL, skills, examples)
- Sync `sendTask` or streaming `sendTaskSubscribe`

## When NOT to use
- All roles share one process (load `multi-agent`)
- You only need tools/resources, not peer agents (load `mcp`)
- Single user-facing bot

## Inputs
- AgentCard + AgentSkill
- JSON-RPC task
- Auth (API keys, OAuth for calendar, etc.)

## Outputs
- Task artifacts / stream
- `input-required` for multi-turn

## Failure modes
- Undiscoverable card
- Missing `GOOGLE_CLIENT_ID` / secrets
- Confusing A2A (agents) with MCP (tools)

## Minimal example
```python
card = AgentCard(name="Calendar Agent", url=f"http://{host}:{port}/",
                 capabilities=AgentCapabilities(streaming=True), skills=[...])
A2AStarletteApplication(agent_card=card, http_handler=handler)
```

## Next skills
- If collaborators are local sub-agents: load `multi-agent`
- If the peer is a tool server: load `mcp`
