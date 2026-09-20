# Exception Handling and Recovery — reference patterns

Source: Chapter 12 + `Chapter_12_Exception_Handling_(Fallback).ipynb`.

## Three layers (book)
1. **Error detection**: validate tool outputs, check API error codes, apply
   timeouts, watch for unexpected formats.
2. **Error handling**: logging for diagnostics, retries for transient
   failures, fallbacks to alternative tools/methods, graceful degradation,
   notifications to users/operators.
3. **Recovery**: restore a stable state (rollback, state reset), diagnose
   root cause, self-correct the plan, escalate to a human when needed.

Rule of thumb: any agent in a dynamic real-world environment where tool
errors, network issues or unpredictable inputs are possible.

## Use cases named in the chapter
Customer-service bot when the DB is down (inform, retry later, escalate);
trading bot on "insufficient funds"/"market closed" (log, do not repeat the
invalid trade, notify); smart-home device failure (retry, then notify);
batch document processing (skip corrupted file, log, continue, report);
web scraping (CAPTCHA/404/503 -> pause, proxy, report URL); robotics
(sensor-detected pick failure -> readjust, retry, alert).

## Notebook pattern: primary -> fallback -> response (ADK)
```python
from google.adk.agents import Agent, SequentialAgent

primary_handler = Agent(name="primary_handler", model="gemini-2.0-flash-exp",
    instruction="""
Your job is to get precise location information.
Use the get_precise_location_info tool with the user's provided address.
    """,
    tools=[get_precise_location_info])          # tool sets state["primary_location_failed"] on error

fallback_handler = Agent(name="fallback_handler", model="gemini-2.0-flash-exp",
    instruction="""
Check if the primary location lookup failed by looking at state["primary_location_failed"].
- If it is True, extract the city from the user's original query and use the get_general_area_info tool.
- If it is False, do nothing.
    """,
    tools=[get_general_area_info])

response_agent = Agent(name="response_agent", model="gemini-2.0-flash-exp",
    instruction="""
Review the location information stored in state["location_result"].
Present this information clearly and concisely to the user.
If state["location_result"] does not exist or is empty, apologize that you could not retrieve the location.
    """,
    tools=[])

robust_location_agent = SequentialAgent(name="robust_location_agent",
    sub_agents=[primary_handler, fallback_handler, response_agent])
```
Why it works: the failure is recorded as *state*, the fallback is
conditional on that state, and the presenter has an explicit branch for
"nothing retrieved". Each agent has one narrow job.

## Tool-side conventions
```python
def get_precise_location_info(address: str, tool_context: ToolContext) -> dict:
    try:
        result = geocode(address, timeout=5)
        tool_context.state["location_result"] = result
        return {"status": "success", "result": result}
    except (TimeoutError, ServiceUnavailable) as e:       # transient -> flag for fallback
        tool_context.state["primary_location_failed"] = True
        return {"status": "error", "error_message": str(e)}
    # ValueError for malformed address: let it raise; do not retry
```
- Expected/recoverable outcomes -> structured error dict.
- Programming or input errors -> raise (surface, do not loop).

## Retry policy sketch
```python
for attempt in range(max_retries):
    try:
        return call()
    except TransientError:
        sleep(base * 2 ** attempt + jitter)
raise EscalateToHuman("retries exhausted")
```
Never retry: authentication failures, validation errors, "insufficient
funds", 4xx client errors.

## Degradation ladder
precise tool -> approximate tool -> cached/last-known value -> honest
"unavailable" message -> human escalation (`human-in-the-loop`).

## Observability
Log: tool name, args (redacted), error class, attempt number, chosen
fallback, final status. Feed these into `evaluation-monitoring`.
