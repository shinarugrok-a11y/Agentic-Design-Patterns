# Inter-Agent Communication (A2A) — Pattern reference

Load this file only when implementing `a2a`. Do not load by default.

## Book (Gulli) — rule of thumb
Use to orchestrate agents across frameworks (ADK, LangGraph, CrewAI) via HTTP + Agent Cards.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Comparison of A2A vs MCP. Fig. 2: A2A inter-agent communication pattern.

## Notebooks (extracted)

Inter-Agent Communication (A2A)

### Notebooks
- `Chapter_15_Inter_Agent_(A2A).ipynb`
- `Chapter_15_Inter_Agent_(A2A_AgentCard_WeatherBot).ipynb` *(JSON schema, not Python)*
- `Chapter_15_Inter_Agent_(Sync_Streaming_Requests).ipynb` *(JSON-RPC examples)*

### Patterns
- **Agent Card:** metadata describing name, URL, capabilities, skills with examples
- **A2A server:** `AgentSkill` + `AgentCard` + `ADKAgentExecutor` + `A2AStarletteApplication` + uvicorn
- **Calendar agent:** `CalendarToolset` with OAuth; RFC3339 timestamps; `primary` calendar default
- **JSON-RPC:** `sendTask` (sync) vs `sendTaskSubscribe` (streaming)

### Prompt templates
Calendar agent instruction:
```
You are an agent that can help manage a user's calendar.

Users will request information about the state of their calendar or to make changes to
their calendar. Use the provided tools for interacting with the calendar API.

If not specified, assume the calendar the user wants is the 'primary' calendar.

When using the Calendar API tools, use well-formed RFC3339 timestamps.

Today is {datetime.datetime.now()}.
```

### Minimal code
```python
# A2A server setup (fragment)
agent_card = AgentCard(
    name='Calendar Agent',
    url=f'http://{host}:{port}/',
    capabilities=AgentCapabilities(streaming=True),
    skills=[AgentSkill(id='check_availability', name='Check Availability', ...)],
)
runner = Runner(app_name=agent_card.name, agent=adk_agent, ...)
a2a_app = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)
uvicorn.run(Starlette(routes=a2a_app.routes()), host=host, port=port)
```

### Caveats
- Requires `GOOGLE_API_KEY` or `GOOGLE_GENAI_USE_VERTEXAI=TRUE`
- OAuth env vars: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- WeatherBot and Sync_Streaming notebooks are **JSON reference docs**, not executable Python
- A2A notebook code is fragmented across two cells — imports missing in snippet

---

## Failure modes (skill-level)
- Missing or stale Agent Card
- OAuth/calendar env vars unset
- Using MCP when you needed agent-to-agent tasks

## Chains with
`multi-agent`, `mcp`
