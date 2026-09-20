# Inter-Agent Communication (A2A) — Patterns

## Pattern variants
- **Synchronous request/response** — `sendTask` / `tasks/send`; client blocks for one complete answer. Quick lookups.
- **Asynchronous polling** — server returns `working` plus a task id at once, client polls to `completed` or `failed`; the safe default for long work.
- **Streaming (SSE)** — `sendTaskSubscribe` / `tasks/sendSubscribe` holds one server-to-client connection and pushes incremental artifacts; use when partial results are useful.
- **Push notification (webhook)** — client registers a callback URL, server pushes on state change; for long tasks where polling or an open socket is wasteful.
- **Discovery** — well-known URI (`/.well-known/agent.json`) for open ecosystems, curated registry for enterprise access control, direct configuration for tightly coupled private pairs.

## Prompt templates

Client agent, delegation policy:
```
Before delegating, fetch the peer's Agent Card and confirm a skill whose
description and examples cover this request. If none does, do not delegate.
Send one task; keep its id and contextId. On state `input-required`, reply in
the same task with the same contextId, never in a new task.
```

## Code patterns

JSON-RPC 2.0 over HTTP — sync and streaming differ only in `method`:
```python
sync = {"jsonrpc": "2.0", "id": "1", "method": "sendTask",
        "params": {"id": "task-001", "sessionId": "session-001",
                   "message": {"role": "user",
                               "parts": [{"type": "text", "text": "USD to EUR?"}]},
                   "acceptedOutputModes": ["text/plain"], "historyLength": 5}}
stream = {**sync, "id": "2", "method": "sendTaskSubscribe"}
```

Google ADK (serving an ADK agent as an A2A server):
```python
skill = AgentSkill(id='check_availability', name='Check Availability',
                   description="Checks a user's availability using Google Calendar",
                   tags=['calendar'], examples=['Am I free 10-11am tomorrow?'])
agent_card = AgentCard(name='Calendar Agent', url=f'http://{host}:{port}/',
                       version='1.0.0', skills=[skill],
                       defaultInputModes=['text'], defaultOutputModes=['text'],
                       capabilities=AgentCapabilities(streaming=True))
handler = DefaultRequestHandler(agent_executor=ADKAgentExecutor(runner, agent_card),
                                task_store=InMemoryTaskStore())  # survives polls
app = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
uvicorn.run(Starlette(routes=app.routes()), host=host, port=port)
```

## Framework notes
- **LangChain / LangGraph, CrewAI** — framework-neutral by design: any can sit behind an A2A endpoint, and the client never sees the peer's internals (the remote agent is "opaque").
- **Google ADK** — `AgentSkill` / `AgentCard` / `AgentCapabilities` describe the agent; `A2AStarletteApplication` + `DefaultRequestHandler` + `InMemoryTaskStore` serve it.
- **MCP contrast** — MCP standardizes an agent's access to tools and data; A2A standardizes task delegation between agents. They compose.

## Failure modes in depth
- **Card overstates capabilities** — skills advertised but unimplemented, or `streaming: true` on a server that never emits SSE; match the request against skill `examples` and treat a first delegation as a probe with a fallback.
- **Orphaned tasks on partition** — a polled task stays `submitted`/`working` forever; set a client-side deadline per task id, and prefer push notifications so completion survives a dropped client.
- **Context lost at `input-required`** — the reply opens a fresh task; carry the server-generated `contextId` and original task id on every follow-up, with `historyLength` set to replay the thread.
- **Unauthenticated endpoints** — the card is itself a discovery surface; declare `authentication` schemes, pass OAuth 2.0 tokens or API keys in headers (never URLs or bodies), and guard card and task endpoints with mTLS plus audit logs.

## Source
Chapter 15 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_15_Inter_Agent_(A2A).ipynb, Chapter_15_Inter_Agent_(A2A_AgentCard_WeatherBot).ipynb, Chapter_15_Inter_Agent_(Sync_Streaming_Requests).ipynb.
