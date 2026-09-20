# A2A patterns (Ch 15)

Three notebooks: ADK calendar agent over A2A, WeatherBot AgentCard JSON, sync/streaming envelopes.

AgentCard (`WeatherBot`): `{name, description, url, version, capabilities: {streaming, pushNotifications, stateTransitionHistory}, authentication: {schemes: [apiKey]}, defaultInputModes: [text], skills: [...]}`.

Sync envelope: JSON-RPC `sendTask` with `{id: task-001, sessionId, message: {role: user, parts: [{type: text}]}, acceptedOutputModes, historyLength: 5}`. Streaming variant reuses the envelope over SSE.

ADK service agent: `LlmAgent(name='calendar_agent', model='gemini-2.0-flash-001')` + `CalendarToolset(client_id, client_secret)` exposed via `AgentSkill(id='check_availability', …)` with `GOOGLE_API_KEY`/Vertex check in `main(host, port)`.

## Notebook extracts (on-demand detail)

### Chapter_15_Inter_Agent_(A2A).ipynb

```python
async def create_agent(client_id, client_secret) -> LlmAgent:
toolset = CalendarToolset(client_id=client_id, client_secret=client_secret)
return LlmAgent(
instruction=f"""
def main(host: str, port: int):
agent_card = AgentCard(
async def handle_auth(request: Request) -> PlainTextResponse:
from google.adk.agents import LlmAgent # type: ignore[import-untyped]
from google.adk.tools.google_api_tool import CalendarToolset # type: ignore[import-untyped]
You are an agent that can help manage a user's calendar.
```

### Chapter_15_Inter_Agent_(A2A_AgentCard_WeatherBot).ipynb

```python
(boilerplate-only notebook; see .ipynb)
```

### Chapter_15_Inter_Agent_(Sync_Streaming_Requests).ipynb

```python
"method": "sendTask",
"method": "sendTaskSubscribe",
```
