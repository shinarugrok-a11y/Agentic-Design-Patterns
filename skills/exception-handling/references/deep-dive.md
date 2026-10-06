# Exception Handling and Recovery — deep dive

Source: Chapter 12 (GT:L7539–L7807) + `Chapter_12_Exception_Handling_(Fallback).ipynb`.
Labels: SOURCE = book text or its notebook (cited); DERIVED = ours;
ILLUSTRATIVE = our code, not from the book. GT:L = line in
`ground-truth/agentic_design_patterns.txt`.

## Three layers (SOURCE, paraphrase of GT:L7591–L7620)
1. **Error detection**: malformed tool outputs, API errors such as 404/500,
   unusually long response times, incoherent replies; optionally monitoring
   by other agents.
2. **Error handling**: logging, retries for transient errors ("sometimes with
   slightly adjusted parameters"), fallbacks, graceful degradation,
   notification of humans or other agents.
3. **Recovery**: state rollback, root-cause investigation, self-correction or
   replanning, escalation to a human or higher-level system.

Rule of thumb (SOURCE, GT:L7753): any agent in a dynamic, real-world
environment where system failures, tool errors, network issues or
unpredictable inputs are possible and reliability matters.

## Use cases named in the chapter (SOURCE, GT:L7628–L7657)
Customer-service bot when the DB is down (inform, suggest later, escalate);
trading bot on "insufficient funds"/"market closed" (log, do not repeat the
invalid trade, notify); smart-home device failure (retry, then notify);
batch document processing (skip corrupted file, log, continue, report);
web scraping (CAPTCHA/404/503 -> pause, proxy, report URL); robotics
(pick failure -> readjust, retry, alert operator).

## Book example: primary -> fallback -> response (ADK)
Provenance: SOURCE — verbatim, notebook cell 0 of `Chapter_12_Exception_Handling_(Fallback).ipynb`; same code in the book at GT:L7666–L7714.
```python
from google.adk.agents import Agent, SequentialAgent

# Agent 1: Tries the primary tool. Its focus is narrow and clear.
primary_handler = Agent(
    name="primary_handler",
    model="gemini-2.0-flash-exp",
    instruction="""
Your job is to get precise location information.
Use the get_precise_location_info tool with the user's provided address.
    """,
    tools=[get_precise_location_info]
)

# Agent 2: Acts as the fallback handler, checking state to decide its action.
fallback_handler = Agent(
    name="fallback_handler",
    model="gemini-2.0-flash-exp",
    instruction="""
Check if the primary location lookup failed by looking at state["primary_location_failed"].
- If it is True, extract the city from the user's original query and use the get_general_area_info tool.
- If it is False, do nothing.
    """,
    tools=[get_general_area_info]
)

# Agent 3: Presents the final result from the state.
response_agent = Agent(
    name="response_agent",
    model="gemini-2.0-flash-exp",
    instruction="""
Review the location information stored in state["location_result"].
Present this information clearly and concisely to the user.
If state["location_result"] does not exist or is empty, apologize that you could not retrieve the location.
    """,
    tools=[] # This agent only reasons over the final state.
)


# The SequentialAgent ensures the handlers run in a guaranteed order.
robust_location_agent = SequentialAgent(
    name="robust_location_agent",
    sub_agents=[primary_handler, fallback_handler, response_agent]
)
```

### What the book example leaves out (verified against GT:L7666–L7730 and the notebook)
- `get_precise_location_info` and `get_general_area_info` are used but never
  defined, so the snippet does not run as printed.
- Nothing in the book sets `state["primary_location_failed"]` or
  `state["location_result"]`; the explanation (GT:L7718–L7728) says the
  fallback checks "by inspecting a state variable" but not who writes it.
- The fallback decision is an LLM following an instruction, not a code branch.
- `gemini-2.0-flash-exp` is a time-specific model id (UNCERTAIN today).

The block below is one way to fill that gap. It is not in the book.

Provenance: DERIVED — ILLUSTRATIVE, not from the book. `ToolContext` and `tool_context.state` are the ADK convention shown in Ch 8 (GT:L5312–L5328); `lookup_address` is a placeholder you supply.
```python
from google.adk.tools.tool_context import ToolContext

def get_precise_location_info(address: str, tool_context: ToolContext) -> dict:
    try:
        result = lookup_address(address)            # your geocoder; may time out
    except TimeoutError:
        tool_context.state["primary_location_failed"] = True
        return {"status": "error", "error_message": "precise lookup unavailable"}
    tool_context.state["primary_location_failed"] = False
    tool_context.state["location_result"] = result
    return {"status": "success"}
```
Keep the user-facing error short; log the exception detail separately.

## Retry policy
The book names retries for transient errors and "slightly adjusted
parameters" (GT:L7601–L7602) and "not repeatedly trying the same invalid
trade" (GT:L7637–L7638). It gives no retry code, backoff formula or attempt cap.

Provenance: DERIVED — ILLUSTRATIVE, not from the book.
```python
for attempt in range(max_retries):
    try:
        return call()
    except TransientError:
        time.sleep(base_delay * 2 ** attempt)
return {"status": "error", "action": "escalate", "reason": "retries exhausted"}
```
DERIVED rule: do not retry authentication failures, validation errors or
business-rule refusals such as "insufficient funds"; only the last one is a
book example.

## Degradation ladder (DERIVED)
precise tool -> approximate tool -> cached/last-known value -> honest
"unavailable" message -> human escalation (`human-in-the-loop`).

## Observability (DERIVED; the book names logging, GT:L7600)
Log: tool name, args (redacted), error class, attempt number, chosen
fallback, final status. Feed these into `evaluation-monitoring`.

## Pattern variants (SOURCE terms, GT:L7591–L7620; one-line glosses DERIVED)
- **Detect before handle** — validate output shape, check API codes, watch response times and incoherent replies.
- **Retry** — transient faults only, capped, optionally with adjusted parameters.
- **Fallback handler** — a coarser second path when the primary failed (precise -> city-level in the book example).
- **Graceful degradation** — partial functionality instead of failure; the batch example skips the corrupted file and reports it.
- **State rollback** — reverse recent changes or transactions.
- **Escalation / notification** — hand to a human operator or higher-level system.
- **With reflection** (SOURCE, GT:L7564–L7567) — analyse the failure and retry with a refined approach, such as an improved prompt.

## Prompt templates
Provenance: SOURCE — verbatim instruction strings from the book example (GT:L7686–L7690).
```
Check if the primary location lookup failed by looking at state["primary_location_failed"].
- If it is True, extract the city from the user's original query and use the
  get_general_area_info tool.
- If it is False, do nothing.
```

Provenance: SOURCE — verbatim instruction strings from the book example (GT:L7702–L7705).
```
Review the location information stored in state["location_result"].
Present this information clearly and concisely to the user.
If state["location_result"] does not exist or is empty, apologize that you could not
retrieve the location.
```

## Framework notes
- **Google ADK** (SOURCE) — the only code in the chapter: `SequentialAgent(sub_agents=[...])` for ordering, `state` keys as the failure signal, a tool-less final agent that renders state.
- **LangChain / LangGraph** — not used in this chapter.

## Failure modes in depth (DERIVED)
- **Retrying non-transient errors** — "insufficient funds", "market closed" and malformed input never succeed on a repeat. Classify first.
- **Swallowing errors** — a caught exception that leaves no trace looks like success. Set an explicit flag, log it, and make the responder apologise when the result is empty.
- **Retry storms** — cap attempts and back off so a struggling dependency is not hammered.
- **Untested fallback** — force the primary to fail in tests; keep the fallback simpler than the primary.
- **Leaking internals** — return a short user-facing message; keep stack traces in logs.
