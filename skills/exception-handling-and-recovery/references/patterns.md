# Exception Handling and Recovery — Patterns

## Pattern variants
- **Detect before handle** — validate output shape, check API codes (404, 500, 503), apply timeouts, watch for incoherent replies; everything downstream depends on classifying the fault.
- **Retry with backoff** — transient faults only (timeouts, 5xx, device not responding), capped attempts, optionally with adjusted parameters.
- **Fallback handler** — a coarser second path runs when the primary failed: precise geocode → city-level lookup. Wins when a degraded answer still has value.
- **Graceful degradation** — skip the corrupted file, log it, finish the batch, report skips at the end.
- **State rollback** — reverse the partial transaction before retrying; wins when the failed step already had side effects.
- **Escalation / notification** — alert a human or supervising agent for non-transient or repeated failures.

## Prompt templates

Fallback handler instruction — branches on a state flag, never on the exception text:
```
Check if the primary location lookup failed by looking at state["primary_location_failed"].
- If it is True, extract the city from the user's original query and use the
  get_general_area_info tool.
- If it is False, do nothing.
```

Responder that must admit failure instead of inventing a result:
```
Review the location information stored in state["location_result"].
Present this information clearly and concisely to the user.
If state["location_result"] does not exist or is empty, apologize that you could not
retrieve the location.
```

## Code patterns

Google ADK (`SequentialAgent` guarantees primary → fallback → responder ordering):
```python
from google.adk.agents import Agent, SequentialAgent

MODEL = "gemini-2.0-flash-exp"

primary = Agent(name="primary_handler", model=MODEL,
                tools=[get_precise_location_info],  # tool sets the state flag, never raises
                instruction="Use get_precise_location_info with the user's address.")
fallback = Agent(name="fallback_handler", model=MODEL, tools=[get_general_area_info],
                 instruction='If state["primary_location_failed"], use get_general_area_info.')
responder = Agent(name="response_agent", model=MODEL, tools=[],  # reasons over state only
                  instruction='Present state["location_result"]; apologize if empty.')

robust_location_agent = SequentialAgent(name="robust_location_agent",
                                        sub_agents=[primary, fallback, responder])
```

Plain Python (the detect/classify layer the chapter describes, under the agent):
```python
for attempt in range(MAX_ATTEMPTS):
    try:
        return tool(args, timeout=10)
    except (TimeoutError, ServiceUnavailable) as e:  # 5xx, transient
        log.warning("retry %s after %s", attempt, e)
        time.sleep(2 ** attempt)                     # capped exponential backoff
    except (InvalidInput, InsufficientFunds) as e:   # 4xx, never retryable
        log.error(e)
        return fallback(args)
escalate("tool unavailable after retries")
```

## Framework notes
- **LangChain / LangGraph** — not used in this chapter.
- **Google ADK** — recovery is agent topology: `SequentialAgent(sub_agents=[...])` for ordering, `state` keys as the failure signal, a tool-less final agent that only renders state.
- **Other** — combines with reflection (chapter 4): analyze the failure, retry with a refined prompt rather than re-issuing it verbatim.

## Failure modes in depth
- **Retrying non-transient errors** — "insufficient funds", "market closed", and malformed input never succeed on a repeat. Classify first: 4xx and validation errors go to fallback or escalation, 5xx and timeouts go to retry.
- **Swallowing errors** — a caught exception that leaves no trace looks like success. Set an explicit flag (`state["primary_location_failed"] = True`), log it, and make the responder apologize when `state["location_result"]` is empty.
- **Retry storms** — cap attempts and back off exponentially so a struggling dependency is not hammered; the same cap stops a trading bot from resubmitting an invalid order in a loop.
- **Untested fallback** — exercise it by forcing the primary to fail in tests, and keep it strictly simpler than the primary (city-level area, not precise geocode) so it has fewer ways to break.

## Source
Chapter 12 of "Agentic Design Patterns" (Gulli). Notebooks: Chapter_12_Exception_Handling_(Fallback).ipynb.
