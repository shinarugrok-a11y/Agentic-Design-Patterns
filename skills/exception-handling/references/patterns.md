# Exception Handling patterns (Ch 12)

One notebook: ADK primary + fallback agents in a `SequentialAgent`.

Pattern: `primary_handler = Agent(instruction='Use get_precise_location_info…', tools=[get_precise_location_info])`; fallback agent checks `session.state` for primary failure and runs the coarse path. Orchestrated by `SequentialAgent([primary_handler, fallback_handler])` on `gemini-2.0-flash-exp`.

Rules: narrow instructions per handler (one job each); fallback reads state to decide (act only if primary failed); always mark degraded results; log full trace, not just the message.

Extensions: add retry with backoff around transient errors and a circuit breaker after N consecutive failures.

## Notebook extracts (on-demand detail)

### Chapter_12_Exception_Handling_(Fallback).ipynb

```python
primary_handler = Agent(
instruction="""
fallback_handler = Agent(
instruction="""
response_agent = Agent(
instruction="""
# The SequentialAgent ensures the handlers run in a guaranteed order.
robust_location_agent = SequentialAgent(
from google.adk.agents import Agent, SequentialAgent
# Agent 1: Tries the primary tool. Its focus is narrow and clear.
```
