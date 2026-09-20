# Exception Handling and Recovery — patterns (Ch 12)

## Pattern
1. Classify errors: transient, deterministic, needs-human.
2. Retry transient with backoff; never retry deterministic.
3. Fallback path with a degraded but useful result.
4. Return structured error reports.

## Prompt template
```
Primary: Use get_precise_location. If it fails, return the error verbatim.
Fallback: Read {location}. Only if it is an error, call get_general_area.
Responder: Report the result and whether a fallback was used.
```

## Key APIs
- ADK: `SequentialAgent([primary, fallback, responder])` sharing `output_key='location'`.
- Tools return `{'status': 'error', 'error_message': ...}` for expected failures; raise for bugs.
- Retry: exponential backoff, jitter, max attempts.

## Pitfalls -> fixes
- Fallback fires on success -> condition on the error field.
- Retrying bad args -> classify first.
- Errors as data -> structured status.

Full notebook code: `notebook-code.md`; source `chapter_notebooks/Chapter_12_*`.
