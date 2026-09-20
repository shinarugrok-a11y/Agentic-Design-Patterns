---
name: a2a
description: HTTP protocol for agents to discover and delegate to each other. Coordinate agents built on different frameworks or hosts via Agent Cards and `tasks/send` / `tasks/sendSubscribe`. Do not use for agents in the same process and framework; in-process sub-agents are simpler.
role: [executor, planner]
chapter: 15
token_cost_estimate: 380
chains_with: [multi-agent, mcp, routing]
---

# Inter-Agent Communication (A2A)

## When to use
- Agents on different frameworks (ADK, LangGraph, CrewAI).
- Remote agent must be discovered by capability.
- Long-running tasks need streaming or `input-required` state.
- Modular deployment on separate ports/hosts.

## When NOT to use
- All agents in one process: use `multi-agent`.
- Peer is a tool/data source, not an agent: use `mcp`.
- No auth/mTLS possible for the transport.

## Inputs
- Agent Card (name, url, skills, auth, capabilities)
- Task message with parts
- Session id

## Outputs
- Task result / streamed updates
- Task state (completed | input-required | failed)
- Discovered remote skills

## Failure modes
- Agent Card advertises a skill the executor cannot fulfil.
- Sync `tasks/send` used for a long task; client times out.
- Missing auth scheme; open endpoint.
- Session id not reused; multi-turn context lost.

## Minimal example
```python
card = AgentCard(name="Calendar Agent", url=f"http://{host}:{port}/", version="1.0.0",
    capabilities=AgentCapabilities(streaming=True), skills=[AgentSkill(id="check_availability", ...)])
app = A2AStarletteApplication(agent_card=card,
    http_handler=DefaultRequestHandler(agent_executor=ADKAgentExecutor(runner, card),
                                       task_store=InMemoryTaskStore()))
# client: {"jsonrpc":"2.0","method":"sendTask","params":{"id":..,"message":{...}}}
```

## Next skills
- If agents are co-located: load `multi-agent`
- If peer exposes tools, not tasks: load `mcp`
- If which remote agent to call: load `routing`
