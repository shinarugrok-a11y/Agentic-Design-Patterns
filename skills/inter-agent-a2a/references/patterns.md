# Inter-Agent Communication (A2A)

Ch 15.

## Frameworks
- Google ADK A2A (LlmAgent + AgentCard, CalendarToolset); Starlette/FastAPI serving.

## Key APIs from the notebooks
- `create_agent(client_id, client_secret) -> LlmAgent remote agent factory`
- `WeatherBot AgentCard notebook: capability advertisement document`
- `Sync_Streaming notebook: sync vs streaming request handlers; handle_auth(request) -> PlainTextResponse`

## Code patterns
- Pattern: publish AgentCard -> discover -> authenticated A2A request (sync/streaming) -> consume.
- Support both sync and streaming; negotiate per call.
- Authenticate every cross-agent request (handle_auth).

## Prompt templates
- See the chapter notebooks for full prompt strings used with each framework.

## Notebooks (do not modify)
- `chapter_notebooks/Chapter_15_Inter_Agent_(A2A).ipynb`
- `chapter_notebooks/Chapter_15_Inter_Agent_(A2A_AgentCard_WeatherBot).ipynb`
- `chapter_notebooks/Chapter_15_Inter_Agent_(Sync_Streaming_Requests).ipynb`

