# Exception Handling and Recovery — patterns (Ch 12)

## Pattern
1. Classify errors: transient, deterministic, needs-human.
2. Retry transient errors (capped); never repeat an invalid action.
3. Fallback path with a degraded but useful result.
4. Return structured error reports.

## Prompt template
```
Primary: Use get_precise_location_info with the user's address.
Fallback: Check state["primary_location_failed"]. If True, call get_general_area_info.
Responder: Present state["location_result"]; if empty, apologize.
```

## Key APIs
- ADK (book): `SequentialAgent(sub_agents=[primary_handler, fallback_handler, response_agent])`.
- The book never defines the tools or what sets `primary_location_failed`; write that yourself.
- Tools return `{'status': 'error', ...}` for expected failures; raise for bugs.

## Pitfalls -> fixes
- Fallback fires on success -> condition on the failure flag.
- Retrying bad args -> classify first.
- Errors as data -> structured status.

More: `deep-dive.md` (code, variants, failure modes); `chapter_notebooks/Chapter_12_*`.
