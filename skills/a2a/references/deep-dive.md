# Inter-Agent Communication (A2A) — deep dive

Source: Chapter 15 + `Chapter_15_Inter_Agent_(A2A_AgentCard_WeatherBot)`,
`Chapter_15_Inter_Agent_(A2A)`, `Chapter_15_Inter_Agent_(Sync_Streaming_Requests)`.

## Protocol essentials (book)
- Open, HTTP/JSON-RPC based; agents on different frameworks interoperate.
- **Agent Card**: JSON identity file (capabilities, skills, endpoint, auth).
- Interaction modes: synchronous request/response (`tasks/send` /
  `sendTask`), streaming (`tasks/sendSubscribe` / `sendTaskSubscribe`,
  SSE), asynchronous polling, push notifications.
- Task states include `input-required` for multi-turn clarification.
- Security: mTLS, explicit authentication schemes in the card.
- A2A (agent <-> agent tasks) complements MCP (LLM <-> tools/resources).
- Tooling: Trickle AI for visualising A2A traffic.

Rule of thumb: orchestrate two or more agents built with different
frameworks (ADK, LangGraph, CrewAI), or when an agent must discover and
consume other agents' capabilities dynamically.

## Agent Card (WeatherBot)
```json
{
  "name": "WeatherBot",
  "description": "Provides accurate weather forecasts and historical data.",
  "url": "http://weather-service.example.com/a2a",
  "version": "1.0.0",
  "capabilities": {"streaming": true, "pushNotifications": false, "stateTransitionHistory": true},
  "authentication": {"schemes": ["apiKey"]},
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "skills": [
    {"id": "get_current_weather", "name": "Get Current Weather",
     "description": "Retrieve real-time weather for any location.",
     "inputModes": ["text"], "outputModes": ["text"],
     "examples": ["What's the weather in Paris?", "Current conditions in Tokyo"],
     "tags": ["weather", "current", "real-time"]},
    {"id": "get_forecast", "name": "Get Forecast", "description": "Get 5-day weather predictions.",
     "inputModes": ["text"], "outputModes": ["text"],
     "examples": ["5-day forecast for New York", "Will it rain in London this weekend?"],
     "tags": ["weather", "forecast", "prediction"]}
  ]
}
```
`skills[].examples` double as routing hints for client agents.

## Server: ADK agent exposed over A2A
```python
async def create_agent(client_id, client_secret) -> LlmAgent:
    toolset = CalendarToolset(client_id=client_id, client_secret=client_secret)
    return LlmAgent(model="gemini-2.0-flash-001", name="calendar_agent",
        description="An agent that can help manage a user's calendar",
        instruction=f"""
You are an agent that can help manage a user's calendar.
Users will request information about the state of their calendar or to make changes to
their calendar. Use the provided tools for interacting with the calendar API.
If not specified, assume the calendar the user wants is the 'primary' calendar.
When using the Calendar API tools, use well-formed RFC3339 timestamps.
Today is {datetime.datetime.now()}.
""",
        tools=await toolset.get_tools())

def main(host, port):
    skill = AgentSkill(id="check_availability", name="Check Availability",
        description="Checks a user's availability for a time using their Google Calendar",
        tags=["calendar"], examples=["Am I free from 10am to 11am tomorrow?"])
    agent_card = AgentCard(name="Calendar Agent", description="An agent that can manage a user's calendar",
        url=f"http://{host}:{port}/", version="1.0.0",
        defaultInputModes=["text"], defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True), skills=[skill])

    runner = Runner(app_name=agent_card.name, agent=asyncio.run(create_agent(...)),
                    artifact_service=InMemoryArtifactService(),
                    session_service=InMemorySessionService(), memory_service=InMemoryMemoryService())
    agent_executor = ADKAgentExecutor(runner, agent_card)
    request_handler = DefaultRequestHandler(agent_executor=agent_executor, task_store=InMemoryTaskStore())
    a2a_app = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)
    routes = a2a_app.routes()
    routes.append(Route(path="/authenticate", methods=["GET"], endpoint=handle_auth))  # OAuth callback
    uvicorn.run(Starlette(routes=routes), host=host, port=port)
```

## Client requests (JSON-RPC)
Synchronous:
```json
{"jsonrpc": "2.0", "id": "1", "method": "sendTask",
 "params": {"id": "task-001", "sessionId": "session-001",
   "message": {"role": "user", "parts": [{"type": "text", "text": "What is the exchange rate from USD to EUR?"}]},
   "acceptedOutputModes": ["text/plain"], "historyLength": 5}}
```
Streaming:
```json
{"jsonrpc": "2.0", "id": "2", "method": "sendTaskSubscribe",
 "params": {"id": "task-002", "sessionId": "session-001",
   "message": {"role": "user", "parts": [{"type": "text", "text": "What's the exchange rate for JPY to GBP today?"}]},
   "acceptedOutputModes": ["text/plain"], "historyLength": 5}}
```
Reuse `sessionId` across turns; `historyLength` bounds the context the
server replays.

## Client-side discovery loop
```
GET {agent_url}/.well-known/agent.json  -> AgentCard
match user intent to card.skills (id/description/examples)
POST sendTask (or sendTaskSubscribe if capabilities.streaming)
handle task.state: completed | input-required (ask user, resend) | failed
```

## Checklist
- Advertise only skills the executor implements.
- Streaming for anything longer than a few seconds.
- Auth scheme declared in card and enforced by the server.
- Separate ports/hosts per agent for independent scaling.

## Pattern variants
- **Synchronous request/response** — `sendTask` / `tasks/send`; client blocks for one complete answer. Quick lookups.
- **Asynchronous polling** — server returns `working` plus a task id at once, client polls to `completed` or `failed`; the safe default for long work.
- **Streaming (SSE)** — `sendTaskSubscribe` / `tasks/sendSubscribe` holds one server-to-client connection and pushes incremental artifacts; use when partial results are useful.
- **Push notification (webhook)** — client registers a callback URL, server pushes on state change; for long tasks where polling or an open socket is wasteful.
- **Discovery** — well-known URI (`/.well-known/agent.json`) for open ecosystems, curated registry for enterprise access control, direct configuration for tightly coupled private pairs.

## More prompt templates
Client agent, delegation policy:
```
Before delegating, fetch the peer's Agent Card and confirm a skill whose
description and examples cover this request. If none does, do not delegate.
Send one task; keep its id and contextId. On state `input-required`, reply in
the same task with the same contextId, never in a new task.
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
