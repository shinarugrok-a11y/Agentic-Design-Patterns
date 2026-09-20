# Exception Handling and Recovery — Pattern reference

Load this file only when implementing `exception-handling`. Do not load by default.

## Book (Gulli) — rule of thumb
Use for any real-world agent where tool errors, timeouts, or bad inputs are expected and uptime matters.

## Book — visual (figure captions; images stay in the PDF)
Fig. 1: Key components of exception handling and recovery. Fig. 2: Exception handling pattern.

## Notebooks (extracted)

Exception Handling and Recovery

### Notebooks
- `Chapter_12_Exception_Handling_(Fallback).ipynb`

### Patterns
- **Sequential fallback chain:** primary handler → fallback (reads `state["primary_location_failed"]`) → response agent
- **State-driven recovery:** fallback agent inspects state flags set by failed primary tool
- **Separation of concerns:** response agent has no tools — only formats final state

### Prompt templates
Primary handler:
```
Your job is to get precise location information.
Use the get_precise_location_info tool with the user's provided address.
```

Fallback handler:
```
Check if the primary location lookup failed by looking at state["primary_location_failed"].
- If it is True, extract the city from the user's original query and use the get_general_area_info tool.
- If it is False, do nothing.
```

### Minimal code
```python
robust_location_agent = SequentialAgent(
    name="robust_location_agent",
    sub_agents=[primary_handler, fallback_handler, response_agent],
)
```

### Caveats
- **Incomplete snippet** — `get_precise_location_info` and `get_general_area_info` referenced but not defined in notebook
- Relies on primary tool setting `state["primary_location_failed"]` correctly
- ADK `gemini-2.0-flash-exp` model specified

---

## Failure modes (skill-level)
- Fallback never sees the failure flag
- Retries without backoff hammer a dead API
- Silent swallow → wrong user-facing answer

## Chains with
`tool-use`, `guardrails-safety`
